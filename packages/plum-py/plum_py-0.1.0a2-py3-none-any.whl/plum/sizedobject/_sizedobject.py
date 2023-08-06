# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Sized object structure type."""

from .. import InsufficientMemoryError
from ..array import Array
from ..int.little import UInt8
from ..structure import Structure
from ._sizedobjecttype import SizedObjectType


class SizedObject(Structure, metaclass=SizedObjectType):

    """Interpret memory bytes as a structure with a size and an item member.

    When unpacking members, size member determines number of memory bytes
    of item member which follows. When instantiating, size member determined
    from item member value when size member not provided.

    Arguments follow form and behavior of :class:`dict`.

    :param value: base member values
    :type value: mapping or iterable
    :param dict kwargs: member values

    """

    # filled in by metaclass
    _item_cls = Array
    _item_name = 'item'
    _keys = {'item', 'size'}
    _nbytes = None
    _size_cls = UInt8
    _size_factor = 1
    _size_name = 'size'

    @classmethod
    def __unpack__(cls, memory, dump):
        self = dict.__new__(cls)

        try:
            dump.cls = cls
        except AttributeError:
            # dump must be None
            size_dump = None
        else:
            size_dump = dump.add_level(access=cls._size_name)

        size = cls._size_cls.__unpack__(memory, size_dump)
        self[cls._size_name] = size

        try:
            add_level = dump.add_level
        except AttributeError:
            # dump must be None
            item_dump = None
        else:
            item_dump = add_level(access=cls._item_name)

        nbytes = size * cls._size_factor

        if memory.available < nbytes:
            # cause InsufficientMemoryError to be raise
            memory.consume_bytes(nbytes, item_dump, cls._item_cls)

        with memory.limit(nbytes):
            self[cls._item_name] = cls._item_cls.__unpack__(memory, item_dump)

        return self
