# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Sized object structure type metaclass."""

from .. import SizeError, calcsize
from ..structure import StructureType


class SizedObjectType(StructureType):

    """SizedObject type metaclass.

    Create custom |SizedObject| subclass. For example:

        >>> from plum.array import Array
        >>> from plum.sizedobject import SizedObject
        >>> from plum.int.little import UInt16
        >>>
        >>> class GreedyArray(Array, item_cls=UInt16):
        ...     pass
        ...
        >>> class MySizedObject(SizedObject, item_cls=GreedyArray, item_name='array', size_cls=UInt16, size_name='size', size_factor=2):
        ...     pass
        ...
        >>>

    :param PlumType item_cls: structure item member type
    :param str item_name: structure item member name
    :param IntType size_cls: structure size member type
    :param str size_name: structure size member name
    :param int size_factor: size multiplier to calculate number of bytes

    """

    def __new__(mcs, name, bases, namespace,
                item_cls=None, item_name=None,
                size_cls=None, size_name=None, size_factor=None):
        return type.__new__(mcs, name, bases, namespace)

    def __init__(cls, name, bases, namespace,
                 item_cls=None, item_name=None,
                 size_cls=None, size_name=None, size_factor=None):
        type.__init__(cls, name, bases, namespace)

        if item_cls is None:
            item_cls = cls._item_cls

        if item_name is None:
            item_name = cls._item_name

        if size_cls is None:
            size_cls = cls._size_cls

        if size_name is None:
            size_name = cls._size_name

        if size_factor is None:
            size_factor = cls._size_factor

        assert size_factor > 0

        try:
            nbytes = calcsize(item_cls)
        except SizeError:
            nbytes = None

        cls._item_cls = item_cls
        cls._item_name = str(item_name)
        cls._keys = {item_name, size_name}
        cls._nbytes = nbytes
        cls._size_cls = size_cls
        cls._size_factor = int(size_factor)
        cls._size_name = str(size_name)

    def __call__(cls, *args, **kwargs):
        if args:
            if len(args) > 1:
                raise TypeError(
                    f'{cls.__name__} expected at most 1 arguments, got {len(args)}')

            arg = args[0]

            if not isinstance(arg, dict) or (set(arg) - cls._keys):
                arg = {cls._item_name: arg}

            if kwargs:
                kwargs = dict(arg, **kwargs)
            else:
                kwargs = arg

        extras = set(kwargs) - cls._keys
        if extras:
            s = 's' if len(extras) > 1 else ''
            message = (
                f'{cls.__name__}() '
                f'got {len(extras)} unexpected member{s}: ')
            message += ', '.join(repr(e) for e in sorted(extras))
            raise TypeError(message)

        try:
            item = kwargs[cls._item_name]
        except KeyError:
            item = cls._item_cls()
        else:
            if not isinstance(item, cls._item_cls):
                item = cls._item_cls(item)

        try:
            size = kwargs[cls._size_name]
        except KeyError:
            nbytes = calcsize(item)
            size, remainder = divmod(nbytes, cls._size_factor)
            if remainder:
                raise TypeError(
                    f'item size is not an even multiple of {cls._size_factor}')
            size = cls._size_cls(size)
        else:
            if not isinstance(size, cls._size_cls):
                size = cls._size_cls(size)

        self = dict.__new__(cls)
        dict.__setitem__(self, cls._size_name, size)
        dict.__setitem__(self, cls._item_name, item)

        return self
