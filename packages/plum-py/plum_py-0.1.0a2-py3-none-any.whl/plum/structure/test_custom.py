# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test custom Structure subclass."""

import pytest
from baseline import Baseline

from plum import (
    ExcessMemoryError,
    calcsize,
    getdump,
    pack,
    unpack,
)

from plum.int.little import UInt16, UInt8
from plum.structure import Structure, StructureType

from ..tests.utils import wrap_message


class CustomStructureClass(StructureType):

    value_cls = {1: UInt8, 2: UInt16}

    def __call__(cls, *args, **kwargs):
        members = dict(*args, **kwargs)
        size = members.pop('size', 1)
        value = members.pop('value')
        assert not members, "only 'size' and 'value' members supported"
        value_cls = cls.value_cls[size]

        self = dict.__new__(cls)
        self.size = UInt8(size)
        self.value = value_cls(value)

        return self


class Custom(Structure, metaclass=CustomStructureClass):

    @classmethod
    def __unpack__(cls, memory, dump):
        self = dict.__new__(cls)

        if dump:
            dump.cls = cls

        self.size = UInt8.__unpack__(
            memory, None if dump is None else dump.add_level(access='size'))

        value_cls = cls.value_cls[self.size]

        self.value = value_cls.__unpack__(
            memory, None if dump is None else dump.add_level(access='value'))

        return self


class TestCustom(object):

    """Test initialization variants."""

    sample1 = Custom(size=1, value=8)
    sample1_bytes = b'\x01\x08'
    sample1_dump = Baseline("""
        +--------+----------+-------+--------+--------+
        | Offset | Access   | Value | Memory | Type   |
        +--------+----------+-------+--------+--------+
        |        | x        |       |        | Custom |
        | 0      |   .size  | 1     | 01     | UInt8  |
        | 1      |   .value | 8     | 08     | UInt8  |
        +--------+----------+-------+--------+--------+
        """)

    sample2 = Custom(size=2, value=16)
    sample2_bytes = b'\x02\x10\x00'
    sample2_dump = Baseline("""
        +--------+----------+-------+--------+--------+
        | Offset | Access   | Value | Memory | Type   |
        +--------+----------+-------+--------+--------+
        |        | x        |       |        | Custom |
        | 0      |   .size  | 2     | 02     | UInt8  |
        | 1      |   .value | 16    | 10 00  | UInt16 |
        +--------+----------+-------+--------+--------+
        """)

    def test_init(self):

        assert getdump(self.sample1) == self.sample1_dump
        assert getdump(self.sample2) == self.sample2_dump

    def test_calcsize(self):
        assert calcsize(self.sample1) == 2
        assert calcsize(self.sample2) == 3

    def test_pack_builtins(self):
        assert pack(Custom, {'size': 1, 'value': 8}) == self.sample1_bytes
        assert pack(Custom, {'size': 2, 'value': 16}) == self.sample2_bytes

    def test_pack_instance(self):
        assert pack(self.sample1) == self.sample1_bytes

    def test_unpack(self):
        sample1 = unpack(Custom, self.sample1_bytes)
        assert getdump(sample1) == self.sample1_dump

        sample2 = unpack(Custom, self.sample2_bytes)
        assert getdump(sample2) == self.sample2_dump

    def test_unpack_excess(self):
        with pytest.raises(ExcessMemoryError) as trap:
            unpack(Custom, self.sample1_bytes + b'\x99')

        expected = Baseline("""


            +--------+-----------------+-------+--------+--------+
            | Offset | Access          | Value | Memory | Type   |
            +--------+-----------------+-------+--------+--------+
            |        | x               |       |        | Custom |
            | 0      |   size          | 1     | 01     | UInt8  |
            | 1      |   value         | 8     | 08     | UInt8  |
            | 2      | <excess memory> |       | 99     |        |
            +--------+-----------------+-------+--------+--------+

            1 unconsumed memory bytes (3 available, 2 consumed)
            """)

        assert wrap_message(trap.value) == expected
