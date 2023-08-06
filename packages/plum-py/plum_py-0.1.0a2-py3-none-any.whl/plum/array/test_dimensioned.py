# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import pytest
from baseline import Baseline

from plum import (
    ExcessMemoryError,
    InsufficientMemoryError,
    calcsize,
    getdump,
    pack,
    unpack,
)

from ..int.little import UInt16, UInt8
from ..tests.utils import wrap_message
from . import Array


class Array2x2(Array, dims=(2,2), item_cls=UInt16):
    pass


sample_list = [[0x0000, 0x0001], [0x0100, 0x0101]]

sample_bytes = b'\x00\x00\x01\x00\x00\x01\x01\x01'

sample = Array2x2(sample_list)

sample_dump = Baseline("""
    +--------+---------+-------+--------+----------+
    | Offset | Access  | Value | Memory | Type     |
    +--------+---------+-------+--------+----------+
    |        | x       |       |        | Array2x2 |
    |        |   [0]   |       |        |          |
    | 0      |     [0] | 0     | 00 00  | UInt16   |
    | 2      |     [1] | 1     | 01 00  | UInt16   |
    |        |   [1]   |       |        |          |
    | 4      |     [0] | 256   | 00 01  | UInt16   |
    | 6      |     [1] | 257   | 01 01  | UInt16   |
    +--------+---------+-------+--------+----------+
    """)



class TestInit:

    def test_init_dict(self):
        """Test initialization via lists."""
        assert getdump(sample) == sample_dump

    def test_init_default(self):
        expected_dump = Baseline("""
            +--------+---------+-------+--------+----------+
            | Offset | Access  | Value | Memory | Type     |
            +--------+---------+-------+--------+----------+
            |        | x       |       |        | Array2x2 |
            |        |   [0]   |       |        |          |
            | 0      |     [0] | 0     | 00 00  | UInt16   |
            | 2      |     [1] | 0     | 00 00  | UInt16   |
            |        |   [1]   |       |        |          |
            | 4      |     [0] | 0     | 00 00  | UInt16   |
            | 6      |     [1] | 0     | 00 00  | UInt16   |
            +--------+---------+-------+--------+----------+
            """)

        assert getdump(Array2x2()) == expected_dump


class TestUtilities:

    @staticmethod
    def test_calcsize():
        assert calcsize(Array2x2) == 8
        assert calcsize(sample) == 8

    @staticmethod
    def test_dump():
        assert getdump(sample) == sample_dump

    @staticmethod
    def test_pack_builtins():
        assert pack(Array2x2, sample_list) == sample_bytes

    @staticmethod
    def test_pack_instance():
        assert pack(sample) == sample_bytes

    @staticmethod
    def test_unpack():
        a = unpack(Array2x2, sample_bytes)

        assert getdump(a) == sample_dump

    @staticmethod
    def test_unpack_shortage():
        with pytest.raises(InsufficientMemoryError) as trap:
            unpack(Array2x2, sample_bytes[:-1])

        expected = Baseline("""


            +--------+---------+----------------------+--------+----------+
            | Offset | Access  | Value                | Memory | Type     |
            +--------+---------+----------------------+--------+----------+
            |        | x       |                      |        | Array2x2 |
            |        |   [0]   |                      |        |          |
            | 0      |     [0] | 0                    | 00 00  | UInt16   |
            | 2      |     [1] | 1                    | 01 00  | UInt16   |
            |        |   [1]   |                      |        |          |
            | 4      |     [0] | 256                  | 00 01  | UInt16   |
            | 6      |     [1] | <insufficient bytes> | 01     | UInt16   |
            +--------+---------+----------------------+--------+----------+

            InsufficientMemoryError: 1 too few memory bytes to unpack UInt16 (2
            needed, only 1 available), dump above shows interrupted progress
            """)

        assert wrap_message(trap.value) == expected

    @staticmethod
    def test_unpack_excess():
        with pytest.raises(ExcessMemoryError) as trap:
            unpack(Array2x2, sample_bytes + b'\x99')

        expected = Baseline("""


            +--------+-----------------+-------+--------+----------+
            | Offset | Access          | Value | Memory | Type     |
            +--------+-----------------+-------+--------+----------+
            |        | x               |       |        | Array2x2 |
            |        |   [0]           |       |        |          |
            | 0      |     [0]         | 0     | 00 00  | UInt16   |
            | 2      |     [1]         | 1     | 01 00  | UInt16   |
            |        |   [1]           |       |        |          |
            | 4      |     [0]         | 256   | 00 01  | UInt16   |
            | 6      |     [1]         | 257   | 01 01  | UInt16   |
            | 8      | <excess memory> |       | 99     |          |
            +--------+-----------------+-------+--------+----------+

            1 unconsumed memory bytes (9 available, 8 consumed)
            """)

        assert wrap_message(trap.value) == expected


class TestIndexAccess:

    def test_valid_lookup(self):
        assert sample[0] == [0x0000, 0x0001]
        assert sample[1] == [0x0100, 0x0101]
        assert isinstance(sample[0], Array)

    def test_valid_set(self):
        a = Array2x2([[0x0000, 0x0001], [0x0100, 0x9999]])
        a[1][1] = UInt16(0x0101)
        assert getdump(a) == sample_dump

    def test_invalid_lookup(self):
        with pytest.raises(IndexError) as trap:
            sample[3]
        assert str(trap.value) == 'list index out of range'

        with pytest.raises(IndexError) as trap:
            sample[0][3]
        assert str(trap.value) == 'list index out of range'

    def test_invalid_set_index(self):
        a = Array2x2([[0, 0], [0, 0]])
        with pytest.raises(IndexError) as trap:
            a[1][3] = 0
        assert str(trap.value) == 'list assignment index out of range'

    def test_untyped_set(self):
        a = Array2x2([[0x0000, 0x0001], [0x0100, 0x9999]])
        a[1][1] = 0x0101
        assert getdump(a) == sample_dump


class TestCompare:

    def test_versus_list(self):
        assert sample == sample_list
        assert not (sample != sample_list)

    def test_versus_same(self):
        assert sample == sample
        assert not (sample != sample)

    def test_versus_dissimiliar(self):
        assert sample != [0, 1]
        assert sample != [[0, 1, 2], [3, 4, 5]]


