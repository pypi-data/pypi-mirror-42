# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Sized array structure type."""

from ..int.little import UInt8
from ..structure import Structure
from ._sizedarraytype import SizedArrayType


class SizedArray(Structure, metaclass=SizedArrayType):

    """Interpret memory bytes as a structure with a size and an array member.

    When unpacking members, size member determines dimensions of array
    member. When instantiating, size member determined from array member
    value when size member not provided.

    Arguments follow form and behavior of :class:`dict`.

    :param value: base member values
    :type value: mapping or iterable
    :param dict kwargs: member values

    """

    # filled in by metaclass
    _array_cls = None
    _array_name = 'array'
    _item_cls = UInt8
    _nbytes = None
    _ndims = 1
    _dims_cls = UInt8
    _dims_is_scalar = True
    _dims_name = 'count'

    @classmethod
    def __unpack__(cls, memory, dump):
        self = dict.__new__(cls)

        if dump:
            dump.cls = cls

            size_dump = dump.add_level(access=cls._dims_name)
            dims = cls._dims_cls.__unpack__(memory, size_dump)
            self[cls._dims_name] = dims

            if cls._dims_is_scalar:
                dims = (dims, )

            items_dump = dump.add_level(access=cls._array_name)
            items = cls._array_cls.__unpack__(memory, items_dump, dims)

        else:
            dims = cls._dims_cls.__unpack__(memory, None)
            self[cls._dims_name] = dims

            if cls._dims_is_scalar:
                dims = (dims, )

            items = cls._array_cls.__unpack__(memory, None, dims)

        self[cls._array_name] = items

        return self

    def __getitem__(self, key):
        if isinstance(key, (int, slice)):
            item = self[self._array_name].__getitem__(key)
        else:
            item = Structure.__getitem__(self, key)

        return item

    def __setitem__(self, key, value):
        if isinstance(key, (int, slice)):
            self[self._array_name].__setitem__(key, value)
        else:
            if key == self._dims_name:
                if not isinstance(value, self._dims_cls):
                    value = self._dims_cls(value)
            elif key == self._array_name:
                if not isinstance(value, self._array_cls):
                    value = self._array_cls(value)

            Structure.__setitem__(self, key, value)
