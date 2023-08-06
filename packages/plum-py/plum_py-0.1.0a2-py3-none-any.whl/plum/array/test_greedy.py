# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import pytest
from baseline import Baseline

from plum import (
    ExcessMemoryError,
    InsufficientMemoryError,
    SizeError,
    calcsize,
    getdump,
    pack,
    unpack,
)

from ..int.little import UInt16, UInt8
from ..tests.utils import wrap_message
from . import Array as _Array


class Array(_Array, item_cls=UInt16):
    pass


sample_list = [0, 1, 2, 3]

sample_bytes = b'\x00\x00\x01\x00\x02\x00\x03\x00'

sample = Array(sample_list)

sample_dump = Baseline("""
    +--------+--------+-------+--------+--------+
    | Offset | Access | Value | Memory | Type   |
    +--------+--------+-------+--------+--------+
    |        | x      |       |        | Array  |
    | 0      |   [0]  | 0     | 00 00  | UInt16 |
    | 2      |   [1]  | 1     | 01 00  | UInt16 |
    | 4      |   [2]  | 2     | 02 00  | UInt16 |
    | 6      |   [3]  | 3     | 03 00  | UInt16 |
    +--------+--------+-------+--------+--------+
    """)



class TestInit:

    def test_init_dict(self):
        """Test initialization via lists."""
        assert getdump(sample) == sample_dump

    def test_init_default(self):
        expected_dump = Baseline("""
            +--------+--------+-------+--------+-------+
            | Offset | Access | Value | Memory | Type  |
            +--------+--------+-------+--------+-------+
            |        | x      |       |        | Array |
            +--------+--------+-------+--------+-------+
            """)

        assert getdump(Array()) == expected_dump


class TestUtilities:

    @staticmethod
    def test_calcsize():
        with pytest.raises(SizeError):
            calcsize(Array)
        assert calcsize(sample) == 8

    @staticmethod
    def test_dump():
        assert getdump(sample) == sample_dump

    @staticmethod
    def test_pack_builtins():
        assert pack(Array, sample_list) == sample_bytes

    @staticmethod
    def test_pack_instance():
        assert pack(sample) == sample_bytes

    @staticmethod
    def test_unpack():
        a = unpack(Array, sample_bytes)

        assert getdump(a) == sample_dump

    @staticmethod
    def test_unpack_insufficient():
        with pytest.raises(InsufficientMemoryError) as trap:
            unpack(Array, sample_bytes + b'\x99')

        expected = Baseline("""


            +--------+--------+----------------------+--------+--------+
            | Offset | Access | Value                | Memory | Type   |
            +--------+--------+----------------------+--------+--------+
            |        | x      |                      |        | Array  |
            | 0      |   [0]  | 0                    | 00 00  | UInt16 |
            | 2      |   [1]  | 1                    | 01 00  | UInt16 |
            | 4      |   [2]  | 2                    | 02 00  | UInt16 |
            | 6      |   [3]  | 3                    | 03 00  | UInt16 |
            | 8      |   [4]  | <insufficient bytes> | 99     | UInt16 |
            +--------+--------+----------------------+--------+--------+

            InsufficientMemoryError: 1 too few memory bytes to unpack UInt16 (2
            needed, only 1 available), dump above shows interrupted progress
            """)

        assert wrap_message(trap.value) == expected


class TestIndexAccess:

    def test_valid_lookup(self):
        assert sample[0] == 0
        assert sample[1] == 1
        assert isinstance(sample[0], UInt16)

    def test_valid_set(self):
        a = Array([0, 1, 2, 99])
        a[3] = UInt16(3)
        assert getdump(a) == sample_dump

    def test_invalid_lookup(self):
        with pytest.raises(IndexError) as trap:
            sample[4]
        assert str(trap.value) == 'list index out of range'

    def test_invalid_set_index(self):
        a = Array(sample_list)
        with pytest.raises(IndexError) as trap:
            a[4] = 0
        assert str(trap.value) == 'list assignment index out of range'

    def test_untyped_set(self):
        a = Array([0, 1, 2, 99])
        a[3] = 3
        assert getdump(a) == sample_dump


class TestCompare:

    def test_versus_list(self):
        assert sample == sample_list
        assert not (sample != sample_list)

    def test_versus_same(self):
        assert sample == sample
        assert not (sample != sample)

    def test_versus_dissimiliar(self):
        assert sample != [[0, 1, 2], [3, 4, 5]]


