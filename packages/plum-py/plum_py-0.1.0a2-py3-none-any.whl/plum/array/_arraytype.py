# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from .._utils import calcsize, SizeError
from .._plum import Plum
from .._plumtype import PlumType

GREEDY_DIMS = (None,)


class ArrayInitError(Exception):
    pass


class ArrayType(PlumType):

    """Array type metaclass.

    Create custom |Array| subclass. For example:

        >>> from plum.array import Array
        >>> from plum.int.little import UInt16
        >>> class MyArray(Array, item_cls=UInt16, dims=(10,)):
        ...     pass
        ...
        >>>

    :param PlumType item_cls: array item type
    :param dims: array dimension
    :type dims: tuple of int

    """

    def __new__(mcs, name, bases, namespace, item_cls=None, dims=None):
        return super().__new__(mcs, name, bases, namespace)

    def __init__(cls, name, bases, namespace, item_cls=None, dims=None):
        super().__init__(name, bases, namespace)

        if item_cls is None:
            item_cls = cls._item_cls

        assert issubclass(item_cls, Plum)

        if dims is None:
            dims = cls._dims

        if len(dims) > 1:
            item_cls = ArrayType('Array', bases, {}, item_cls, dims[1:])
            item_cls.__name__ = 'Array'

        if None in dims:
            nbytes = None
            assert all(d is None for d in dims)
        else:
            dims = tuple(int(d) for d in dims)
            assert all(d > 0 for d in dims)

            try:
                nbytes = calcsize(item_cls)
            except SizeError:
                nbytes = None
            else:
                nbytes *= dims[0]

        cls._dims = dims
        cls._item_cls = item_cls
        cls._nbytes = nbytes

    def _make_instance(cls, iterable, dims=None, index=''):
        item_cls = cls._item_cls
        item_cls_is_this_type = isinstance(item_cls, ArrayType)

        if dims is None:
            dims = cls._dims

        if iterable is None:
            if dims == GREEDY_DIMS:
                iterable = []
            elif item_cls_is_this_type:
                iterable = [None] * dims[0]
            else:
                iterable = [0] * dims[0]

        self = list.__new__(cls, iterable)
        list.__init__(self, iterable)

        if (dims[0] is not None) and (len(self) != dims[0]):
            invalid_dimension = (
                f'expected length of item{index} to be {dims[0]} '
                f'but instead found {len(self)}')
            raise ArrayInitError(invalid_dimension)

        for i, item in enumerate(self):
            if type(item) is not item_cls:
                try:
                    if item_cls_is_this_type:
                        self[i] = item_cls._make_instance(item, dims=dims[1:], index=index + f'[{i}]')
                    else:
                        self[i] = item_cls(item)
                except ArrayInitError:
                    # allow lowest level one to propagate
                    raise
                except Exception as exc:
                    raise ArrayInitError(
                        f"unexpected {type(exc).__name__!r} "
                        f"exception occurred during array initialization, "
                        f"item{index}[{i}] did not successfully convert to a "
                        f"{item_cls.__name__!r}, original exception "
                        f"traceback appears above this exception's traceback"
                    ).with_traceback(exc.__traceback__)

        return self

    def __call__(cls, iterable=None):
        return cls._make_instance(iterable)
