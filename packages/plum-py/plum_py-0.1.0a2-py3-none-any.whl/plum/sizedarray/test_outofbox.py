# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test SizedArray as is."""

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

from . import SizedArray

from ..tests.utils import wrap_message


sample_dict = dict(count=5, array=[0, 1, 2, 3, 4])
sample_bytes = b'\x05\x00\x01\x02\x03\x04'
sample = SizedArray(sample_dict)

sample_dump = Baseline("""
    +--------+----------+-------+--------+------------+
    | Offset | Access   | Value | Memory | Type       |
    +--------+----------+-------+--------+------------+
    |        | x        |       |        | SizedArray |
    | 0      |   .count | 5     | 05     | UInt8      |
    |        |   .array |       |        | Array      |
    | 1      |     [0]  | 0     | 00     | UInt8      |
    | 2      |     [1]  | 1     | 01     | UInt8      |
    | 3      |     [2]  | 2     | 02     | UInt8      |
    | 4      |     [3]  | 3     | 03     | UInt8      |
    | 5      |     [4]  | 4     | 04     | UInt8      |
    +--------+----------+-------+--------+------------+
    """)


class TestInit:

    """Test initialization variants."""

    sample_cls = SizedArray
    sample_dict = sample_dict

    sample = sample
    sample_dump = sample_dump

    missing_count = SizedArray(array=[0, 1, 2, 3, 4])

    items_as_arg = SizedArray([0, 1, 2, 3, 4])

    mismatch = SizedArray(count=3, array=[0, 1])

    mismatch_dump = Baseline("""
        +--------+----------+-------+--------+------------+
        | Offset | Access   | Value | Memory | Type       |
        +--------+----------+-------+--------+------------+
        |        | x        |       |        | SizedArray |
        | 0      |   .count | 3     | 03     | UInt8      |
        |        |   .array |       |        | Array      |
        | 1      |     [0]  | 0     | 00     | UInt8      |
        | 2      |     [1]  | 1     | 01     | UInt8      |
        +--------+----------+-------+--------+------------+
        """)

    def test_dict(self):
        """Test dict argument where len(array) matches count."""
        sample = self.sample_cls(self.sample_dict)
        assert getdump(sample) == self.sample_dump

    def test_kwargs(self):
        """Test keyword arguments where len(array) matches count."""
        sample = self.sample_cls(**self.sample_dict)
        assert getdump(sample) == self.sample_dump

    def test_outofsync(self):
        """Test that len(array) is allowed to not match specified count."""
        assert getdump(self.mismatch) == self.mismatch_dump

    def test_missing_count(self):
        """Test that count computed automatically when not specified."""
        assert getdump(self.missing_count) == self.sample_dump

    def test_accepts_items(self):
        """Test that array accepted as argument and count computed automatically."""
        assert getdump(self.items_as_arg) == self.sample_dump

    no_defaults_dump = Baseline("""
        +--------+----------+-------+--------+------------+
        | Offset | Access   | Value | Memory | Type       |
        +--------+----------+-------+--------+------------+
        |        | x        |       |        | SizedArray |
        | 0      |   .count | 0     | 00     | UInt8      |
        |        |   .array |       |        | Array      |
        +--------+----------+-------+--------+------------+
        """)

    def test_no_args(self):
        """Test no arguments passed to constructor."""
        assert getdump(self.sample_cls()) == self.no_defaults_dump


class TestUtilities:

    sample = sample
    sample_bytes = sample_bytes
    sample_cls = SizedArray
    sample_dict = sample_dict
    sample_dump = sample_dump

    def test_calcsize(self):
        with pytest.raises(SizeError):
            calcsize(self.sample_cls)

        assert calcsize(self.sample) == len(self.sample_bytes)

    def test_dump(self):
        assert getdump(self.sample) == self.sample_dump

    def test_pack_builtins(self):
        assert pack(self.sample_cls, self.sample_dict) == self.sample_bytes

    def test_pack_instance(self):
        assert pack(self.sample) == self.sample_bytes

    def test_unpack(self):
        instance = unpack(self.sample_cls, self.sample_bytes)
        assert getdump(instance) == self.sample_dump

    insufficient_message = Baseline("""


            +--------+---------+----------------------+--------+------------+
            | Offset | Access  | Value                | Memory | Type       |
            +--------+---------+----------------------+--------+------------+
            |        | x       |                      |        | SizedArray |
            | 0      |   count | 5                    | 05     | UInt8      |
            |        |   array |                      |        | Array      |
            | 1      |     [0] | 0                    | 00     | UInt8      |
            | 2      |     [1] | 1                    | 01     | UInt8      |
            | 3      |     [2] | 2                    | 02     | UInt8      |
            | 4      |     [3] | 3                    | 03     | UInt8      |
            |        |     [4] | <insufficient bytes> |        | UInt8      |
            +--------+---------+----------------------+--------+------------+

            InsufficientMemoryError: 1 too few memory bytes to unpack UInt8 (1
            needed, only 0 available), dump above shows interrupted progress
            """)

    def test_unpack_shortage(self):
        with pytest.raises(InsufficientMemoryError) as trap:
            unpack(self.sample_cls, self.sample_bytes[:-1])

        assert wrap_message(trap.value) == self.insufficient_message

    excess_message = Baseline("""


            +--------+-----------------+-------+--------+------------+
            | Offset | Access          | Value | Memory | Type       |
            +--------+-----------------+-------+--------+------------+
            |        | x               |       |        | SizedArray |
            | 0      |   count         | 5     | 05     | UInt8      |
            |        |   array         |       |        | Array      |
            | 1      |     [0]         | 0     | 00     | UInt8      |
            | 2      |     [1]         | 1     | 01     | UInt8      |
            | 3      |     [2]         | 2     | 02     | UInt8      |
            | 4      |     [3]         | 3     | 03     | UInt8      |
            | 5      |     [4]         | 4     | 04     | UInt8      |
            | 6      | <excess memory> |       | 99     |            |
            +--------+-----------------+-------+--------+------------+

            1 unconsumed memory bytes (7 available, 6 consumed)
            """)

    def test_unpack_excess(self):
        with pytest.raises(ExcessMemoryError) as trap:
            unpack(self.sample_cls, self.sample_bytes + b'\x99')

        assert wrap_message(trap.value) == self.excess_message


class TestIndexAccess:

    def test_lookup_forwarded(self):
        assert sample[0] == 0
        assert sample[1:3] == [1, 2]

    def test_set_forwarded(self):
        instance = SizedArray([0, 99, 2, 99, 99])
        instance[1] = 1
        instance[3:5] = [3, 4]
        assert getdump(instance) == sample_dump


class TestNameAccess:

    def test_valid_lookup(self):
        assert sample.count == 5
        assert sample.array == [0, 1, 2, 3, 4]

    def test_valid_set(self):
        instance = SizedArray(count=1, array=[1])
        instance.count = 5
        instance.array = [0, 1, 2, 3, 4]
        assert getdump(instance) == sample_dump

    def test_invalid_lookup(self):
        with pytest.raises(AttributeError) as trap:
            sample.junk

        assert str(trap.value) == f"'SizedArray' object has no attribute 'junk'"


class TestCompare:

    sample = sample
    sample_dict = sample_dict

    def test_versus_dict(self):
        assert self.sample == self.sample_dict
        assert not (self.sample != self.sample_dict)

    def test_extra_member(self):
        dict_copy = self.sample_dict.copy()
        dict_copy['junk'] = 3
        assert self.sample != dict_copy
        assert not (self.sample == dict_copy)

    def test_versus_same(self):
        assert self.sample == self.sample
        assert not (self.sample != self.sample)
