# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Integer type."""

from ._inttype import IntType
from .._plum import Plum

class Int(int, Plum, metaclass=IntType):

    """Interpret memory bytes as an integer.

    :param x: value
    :type x: number or str
    :param int base: base of x when x is ``str``

    """

    _byteorder = 'little'
    _enum_cls = None
    _max = 0xffffffff
    _min = 0
    _nbytes = 4
    _signed = False

    def __new__(cls, *args, **kwargs):
        self = int.__new__(cls, *args, **kwargs)
        if (self < cls._min) or (self > cls._max):
            raise ValueError(
                f'{cls.__name__} requires {cls._min} <= number <= {cls._max}')
        return self

    @classmethod
    def __unpack__(cls, memory, dump):
        nbytes = cls._nbytes
        buffer = memory.consume_bytes(nbytes, dump, cls)
        self = cls.from_bytes(buffer, cls._byteorder, signed=cls._signed)

        if dump:
            dump.value = self

        return self

    @classmethod
    def __pack__(cls, value, dump):
        if not isinstance(value, int):
            raise TypeError(f'value must be int, dict, or {cls.__name__}')

        bytes_ = value.to_bytes(cls._nbytes, cls._byteorder, signed=cls._signed)

        if dump:
            dump.value = value
            dump.memory = bytes_
            dump.cls = cls

        yield bytes_

    def __str__(self):
        enum_cls = type(self)._enum_cls
        if enum_cls:
            try:
                # must convert to int first to avoid recursion on ValueError
                member = enum_cls(int(self))
            except ValueError:
                pass
            else:
                return str(member)
        return int.__str__(self)

    def __repr__(self):
        cls = type(self)
        enum_cls = cls._enum_cls
        if enum_cls:
            try:
                # must convert to int first to avoid recursion on ValueError
                member = enum_cls(int(self))
            except ValueError:
                pass
            else:
                return f'{cls.__name__}({repr(member)})'

        return f'{cls.__name__}({int.__str__(self)})'
