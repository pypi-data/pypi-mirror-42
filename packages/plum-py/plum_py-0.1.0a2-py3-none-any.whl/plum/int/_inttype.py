# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Integer type metaclass."""

from enum import Enum, IntEnum

from .._plumtype import PlumType

try:
    import plum_c._fastint as fastint
except ImportError:
    fastint = None


class IntType(PlumType):

    """Int type metaclass.

    Create custom |Int| subclass. For example:

        >>> from plum.int import Int
        >>> class SInt24(Int, nbytes=3, signed=True, byteorder='big'):
        ...     pass
        ...
        >>>

    :param int nbytes: number of memory bytes
    :param bool signed: signed integer
    :param str byteorder: ``'big'`` or ``'little'``
    :param IntEnum enum: associated enum (or ``True`` members in namespace)

    """

    def __new__(mcs, name, bases, namespace, nbytes=None, signed=None, byteorder=None, enum=None):
        return super().__new__(mcs, name, bases, namespace)

    def __init__(cls, name, bases, namespace, nbytes=None, signed=None, byteorder=None, enum=None):
        super().__init__(name, bases, namespace)

        if nbytes is None:
            nbytes = cls._nbytes

        nbytes = int(nbytes)

        assert nbytes > 0

        if signed is None:
            signed = cls._signed

        signed = bool(signed)

        if byteorder is None:
            byteorder = cls._byteorder

        assert byteorder in {'big', 'little'}

        if signed:
            minvalue = -(1 << (nbytes * 8 - 1))
            maxvalue = (1 << (nbytes * 8 - 1)) - 1
        else:
            minvalue = 0
            maxvalue = (1 << (nbytes * 8)) - 1

        if enum is None:
            enum = cls._enum_cls
        elif enum is True:
            enum = IntEnum(name, namespace)

        if enum is not None:
            try:
                valid = issubclass(enum, IntEnum)
            except TypeError:
                valid = False

            if valid:
                for member in enum:
                    setattr(cls, member.name, member)
            else:
                raise TypeError('invalid enum, expected IntEnum subclass or True')

        cls._byteorder = byteorder
        cls._enum_cls = enum
        cls._max = maxvalue
        cls._min = minvalue
        cls._nbytes = nbytes
        cls._signed = signed

        if fastint:
            cls.__unpack_fast__ = fastint.c_api_unpack(nbytes, byteorder == 'little', signed)
