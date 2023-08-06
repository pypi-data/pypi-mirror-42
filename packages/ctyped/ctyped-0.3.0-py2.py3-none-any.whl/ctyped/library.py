import ctypes
import inspect
import logging
import os
from collections import namedtuple
from contextlib import contextmanager
from ctypes.util import find_library
from functools import partial, partialmethod, reduce
from typing import Any, Optional, Callable

from .exceptions import FunctionRedeclared, UnsupportedTypeError, TypehintError, CtypedException
from .types import CChars, CastedTypeBase, CInt8, CInt16, CInt32, CInt64, CInt8U, CInt16U, CInt32U, CInt64U

LOGGER = logging.getLogger(__name__)


FuncInfo = namedtuple('FuncInfo', ['name_py', 'name_c', 'annotations', 'options'])


_MISSING = namedtuple('MissingType', [])


class Scopes:

    def __init__(self):
        self._scopes = []
        self._keys = ['prefix', 'str_type', 'int_bits', 'int_sign']

    def push(self, params):

        scope = {key: params.get(key) for key in self._keys}
        self._scopes.append(scope)

    def pop(self):
        self._scopes.pop()

    def flatten(self):

        scopes = self._scopes
        keys_bool = {'int_sign'}
        keys_concat = {'prefix'}
        result = {}

        def choose(current, prev):
            return current or prev

        def pick_bool(current, prev):
            return current if current is not None else prev

        def concat(current, prev):
            return (prev or '') + (current or '')

        for key in self._keys:

            if key in keys_concat:
                reducer = concat

            elif key in keys_bool:
                reducer = pick_bool

            else:
                reducer = choose

            result[key] = reduce(reducer, (scope[key] for scope in scopes[::-1]))

        return result

    @contextmanager
    def context(self, params):
        self.push(params)
        yield self
        self.pop()


class Library:
    """Main entry point to describe C library interface.

    Basic usage:

    .. code-block:: python

        lib = Library('mylib')

        with lib.scope(prefix='mylib_'):

            @lib.function()
            def my_func():
                ...

        lib.bind_types()

    """

    def __init__(
            self, name: str, *, autoload: bool=True,
            prefix: Optional[str] = None,
            str_type: CastedTypeBase=CChars,
            int_bits: Optional[int]=None,
            int_sign: Optional[bool]=None
    ):
        """

        :param name: Shared library name or filepath.

        :param autoload: Load library just on Library object initialization.

        :param prefix: Function name prefix to apply to functions under the manager.

            Useful when C functions have common prefixes.

        :param str_type: Type to represent strings.

            * ``CChars`` - strings as chars (ANSI) **default**
            * ``CCharsW`` - strings as wide chars (UTF)

            .. note:: This setting is global to library. Can be changed on function definition level.

        :param int_bits: int length to use by default.

            Possible values: 8, 16, 32, 64

            .. note:: This setting is global to library. Can be changed on function definition level.

        :param int_sign: Flag. Whether to use signed (True) or unsigned (False) ints.

            .. note:: This setting is global to library. Can be changed on function definition level.

        """
        scopes = Scopes()
        scopes.push(locals())

        self.name = name
        self.lib = None
        self.funcs = {}
        self._scopes = scopes

        autoload and self.load()

    @contextmanager
    def scope(
        self,
        prefix: Optional[str]=None, *,
        str_type: Optional[CastedTypeBase] = None,
        int_bits: Optional[int]=None,
        int_sign: Optional[bool]=None,
    ):
        """Nestable context manager. Used for namespacing and common parameters application..

        .. code-block:: python

            with lib.scope(prefix='MyLib_'):

                @lib.f('my_func', int_bits=64)  # Will be expanded into `MyLib_my_func`
                def some_func(val: int) -> int:
                    ...

        :param prefix: Function name prefix to apply to functions under the manager. See ``__init__`` docstrings.

        :param str_type: Type to represent strings. See ``__init__`` docstrings.

        :param int_bits: int length to use by default. See ``__init__`` docstrings.

        :param int_sign: Flag. Whether to use signed (True) or unsigned (False) ints.  See ``__init__`` docstrings.

        """
        with self._scopes.context(locals()):
            yield

    def load(self):
        """Loads shared library."""
        name = self.name

        if not os.path.exists(name):
            name = find_library(name)

        lib = ctypes.CDLL(name, use_errno=True)

        if lib._name is None:
            lib = None

        if lib is None:
            raise CtypedException('Unable to find library: %s' % name)

        self.lib = lib

    def function(
            self, name_c: Optional[str]=None, *, wrap: bool=False,
            str_type: Optional[CastedTypeBase]=None,
            int_bits: Optional[int]=None,
            int_sign: Optional[bool]=None
    ):
        """Decorator to mark functions which exported from the library.

        :param name_c: C function name with or without prefix (see ``.scope(prefix=)``).
            If not set, Python function name is used.

        :param wrap: Do not replace decorated function with ctypes function,
            but with wrapper, allowing pre- or post-process ctypes function call.

            Useful to organize functions to classes (to automatically pass ``self``)
            to ctypes function to C function.

            .. code-block:: python

                class Thing(CObject):

                    @lib.function(wrap=True)
                    def one(self, some: int) -> int:
                        # Implicitly pass Thing instance alongside
                        # with explicitly passed `some` arg.
                        ...

                    @lib.function(wrap=True)
                    def two(self, some:int, cfunc: Callable) -> int:
                        # `cfunc` is a wrapper, calling an actual ctypes function.
                        # If no arguments provided the wrapper will try detect them
                        # automatically.
                        result = cfunc()
                        return result + 1

        :param str_type: Type to represent strings.

            .. note:: Overrides the same named param from library level (see ``__init__`` description).

        :param int_bits: int length to be used in function.

            .. note:: Overrides the same named param from library level (see ``__init__`` description).

        :param int_sign: Flag. Whether to use signed (True) or unsigned (False) ints.

            .. note:: Overrides the same named param from library level (see ``__init__`` description).

        """
        locals_ = locals()

        def cfunc_wrapped(*args, f: Callable, **kwargs):

            if not args:
                argvals = inspect.getargvalues(inspect.currentframe().f_back)
                loc = argvals.locals
                args = [loc[argname] for argname in argvals.args if argname != 'cfunc']

            return f(*args)

        def cfunc_direct(*args, f: Callable, **kwargs):
            return f(*args)

        def function_(func_py: Callable):

            with self._scopes.context(locals_) as scopes:
                scope = scopes.flatten()

            info = self._extract_func_info(func_py, name_c=name_c, scope=scope)
            name = info.name_c

            func_c = getattr(self.lib, name)

            # Prepare for late binding in .bind_types().
            func_c.ctyped = info

            if wrap:
                func_args = inspect.getfullargspec(func_py).args

                if 'cfunc' in func_args:
                    # Use existing function, pass `cfunc`.

                    LOGGER.debug('Func [ %s -> %s ] uses wrapped manual call.', name, info.name_py)

                    func_swapped = partialmethod(func_py, cfunc=partial(cfunc_wrapped, f=func_c))

                else:
                    # Use automatic function.

                    LOGGER.debug('Func [ %s -> %s ] uses wrapped auto call.', name, info.name_py)

                    func_swapped = partialmethod(cfunc_direct, f=func_c)

                func_swapped.cfunc = func_c
                func_out = func_swapped

            else:

                LOGGER.debug('Func [ %s -> %s ] uses direct call.' % (name, info.name_py))

                func_out = func_c

            self.funcs[name] = func_out

            return func_out

        return function_

    def method(self, name_c: Optional[str]=None, **kwargs):
        """Decorator. The same as ``.function()`` with ``wrap=True``."""
        return self.function(name_c=name_c, wrap=True, **kwargs)

    def bind_types(self):
        """Deduces ctypes argument and result types from Python type hints,
        binding those types to ctypes functions.


        """
        LOGGER.debug('Binding signature types to ctypes functions ...')

        def thint_str_to_obj(thint: str):
            fback = inspect.currentframe().f_back

            while fback:
                target = fback.f_globals.get(thint)

                if target:
                    return target

                fback = fback.f_back

        def cast_type(name: str, thint: Any):

            if thint is None:
                return None

            if isinstance(thint, str):
                thint_orig = thint
                thint = thint_str_to_obj(thint)

                if thint is None:
                    raise TypehintError(
                        'Unable to resolve type hint. Function: %s. Arg: %s. Type: %s. ' %
                        (name_py, name, thint_orig))

            if thint is str:
                thint = func_info.options['str_type']

            if thint is int:
                int_bits = func_info.options['int_bits']
                int_sign = func_info.options['int_sign']

                if int_bits:
                    assert int_bits in {8, 16, 32, 64}, 'Wrong value passed for int_bits.'

                type_idx = 1 if int_sign is False else 0

                thint = {

                    8: (CInt8, CInt8U),
                    16: (CInt16, CInt16U),
                    32: (CInt32, CInt32U),
                    64: (CInt64, CInt64U),

                }.get(int_bits)[type_idx] or thint

            return thint

        for name_c, func_out in self.funcs.items():

            func_c = getattr(func_out, 'cfunc', func_out)
            func_info: FuncInfo = func_c.ctyped

            name_py = func_info.name_py
            annotations = func_info.annotations
            errcheck = None

            try:
                restype = cast_type('return', annotations.pop('return', None))

                if restype and issubclass(restype, CastedTypeBase):
                    errcheck = restype._ct_res
                    restype = restype._ct_typ

                argtypes = [cast_type(argname, argtype) for argname, argtype in annotations.items()]

            except TypehintError:
                # Reset annotations to allow subsequent .bind_types() calls w/o exceptions.
                func_info.annotations.clear()
                raise

            try:
                if argtypes:
                    func_c.argtypes = argtypes

                if restype:
                    func_c.restype = restype

                if errcheck:
                    func_c.errcheck = errcheck

            except TypeError as e:

                raise UnsupportedTypeError(
                    'Unsupported types declared for %s (%s). Args: %s. Result: %s. Errcheck: %s.' %
                    (name_py, name_c, argtypes, restype, errcheck)) from e

    #####################################################################################
    # Shortcuts

    f = function
    m = method
    s = scope

    #####################################################################################
    # Private

    def _extract_func_info(self, func: Callable, *, name_c: Optional[str]=None, scope: dict=None) -> FuncInfo:

        name_py = func.__name__
        name = scope['prefix'] + (name_c or name_py)

        if name in self.funcs:
            raise FunctionRedeclared('Unable to redeclare: %s (%s)' % (name, name_py))

        annotated_args = {}
        annotations = func.__annotations__

        # Gather all args and annotations for them.
        for argname in inspect.getfullargspec(func).args:

            if argname == 'cfunc':
                continue

            annotation = annotations.get(argname, _MISSING)

            if argname == 'self' and annotation is _MISSING:
                # Pick class name from qualname.
                annotation = func.__qualname__.split('.')[-2]

            annotated_args[argname] = annotation

        annotated_args['return'] = annotations.get('return')

        return FuncInfo(name_py=name_py, name_c=name, annotations=annotated_args, options=scope)
