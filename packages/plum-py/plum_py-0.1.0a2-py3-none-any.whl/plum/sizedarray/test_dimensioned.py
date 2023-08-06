# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test SizedArray subclass."""

import pytest
from baseline import Baseline

from .. import getdump
from ..array import Array
from ..int.little import UInt16, UInt8
from . import SizedArray
from .test_outofbox import TestCompare as _TestCompare
from .test_outofbox import TestInit as _TestInit
from .test_outofbox import TestUtilities as _TestUtilities


class Dims(Array, dims=(2,), item_cls=UInt16):
    pass


class SizedArray2D(SizedArray, dims_cls=Dims, dims_name='dims', item_cls=UInt16, array_name='matrix'):
    pass


sample_dict = dict(dims=[2, 2], matrix=[[0, 1], [2, 3]])
sample_bytes = b'\x02\x00\x02\x00\x00\x00\x01\x00\x02\x00\x03\x00'
sample = SizedArray2D(sample_dict)

sample_dump = Baseline("""
    +--------+-----------+-------+--------+--------------+
    | Offset | Access    | Value | Memory | Type         |
    +--------+-----------+-------+--------+--------------+
    |        | x         |       |        | SizedArray2D |
    |        |   .dims   |       |        | Dims         |
    |  0     |     [0]   | 2     | 02 00  | UInt16       |
    |  2     |     [1]   | 2     | 02 00  | UInt16       |
    |        |   .matrix |       |        | Array        |
    |        |     [0]   |       |        |              |
    |  4     |       [0] | 0     | 00 00  | UInt16       |
    |  6     |       [1] | 1     | 01 00  | UInt16       |
    |        |     [1]   |       |        |              |
    |  8     |       [0] | 2     | 02 00  | UInt16       |
    | 10     |       [1] | 3     | 03 00  | UInt16       |
    +--------+-----------+-------+--------+--------------+
    """)


class TestInit(_TestInit):

    """Test initialization variants."""

    sample_cls = SizedArray2D
    sample_dict = sample_dict

    sample = sample
    sample_dump = sample_dump

    missing_count = SizedArray2D(matrix=sample_dict['matrix'])

    items_as_arg = SizedArray2D(sample_dict['matrix'])

    mismatch = SizedArray2D(dims=[3, 3], matrix=sample_dict['matrix'])

    mismatch_dump = Baseline("""
        +--------+-----------+-------+--------+--------------+
        | Offset | Access    | Value | Memory | Type         |
        +--------+-----------+-------+--------+--------------+
        |        | x         |       |        | SizedArray2D |
        |        |   .dims   |       |        | Dims         |
        |  0     |     [0]   | 3     | 03 00  | UInt16       |
        |  2     |     [1]   | 3     | 03 00  | UInt16       |
        |        |   .matrix |       |        | Array        |
        |        |     [0]   |       |        |              |
        |  4     |       [0] | 0     | 00 00  | UInt16       |
        |  6     |       [1] | 1     | 01 00  | UInt16       |
        |        |     [1]   |       |        |              |
        |  8     |       [0] | 2     | 02 00  | UInt16       |
        | 10     |       [1] | 3     | 03 00  | UInt16       |
        +--------+-----------+-------+--------+--------------+
        """)

    no_defaults_dump = Baseline("""
        +--------+-----------+-------+--------+--------------+
        | Offset | Access    | Value | Memory | Type         |
        +--------+-----------+-------+--------+--------------+
        |        | x         |       |        | SizedArray2D |
        |        |   .dims   |       |        | Dims         |
        | 0      |     [0]   | 0     | 00 00  | UInt16       |
        | 2      |     [1]   | 0     | 00 00  | UInt16       |
        |        |   .matrix |       |        | Array        |
        +--------+-----------+-------+--------+--------------+
        """)

    # inherit test cases


class TestUtilities(_TestUtilities):

    sample = sample
    sample_bytes = sample_bytes
    sample_cls = SizedArray2D
    sample_dict = sample_dict
    sample_dump = sample_dump

    insufficient_message = Baseline("""


            +--------+-----------+----------------------+--------+--------------+
            | Offset | Access    | Value                | Memory | Type         |
            +--------+-----------+----------------------+--------+--------------+
            |        | x         |                      |        | SizedArray2D |
            |        |   dims    |                      |        | Dims         |
            |  0     |     [0]   | 2                    | 02 00  | UInt16       |
            |  2     |     [1]   | 2                    | 02 00  | UInt16       |
            |        |   matrix  |                      |        | Array        |
            |        |     [0]   |                      |        |              |
            |  4     |       [0] | 0                    | 00 00  | UInt16       |
            |  6     |       [1] | 1                    | 01 00  | UInt16       |
            |        |     [1]   |                      |        |              |
            |  8     |       [0] | 2                    | 02 00  | UInt16       |
            | 10     |       [1] | <insufficient bytes> | 03     | UInt16       |
            +--------+-----------+----------------------+--------+--------------+

            InsufficientMemoryError: 1 too few memory bytes to unpack UInt16 (2
            needed, only 1 available), dump above shows interrupted progress
            """)

    excess_message = Baseline("""


            +--------+-----------------+-------+--------+--------------+
            | Offset | Access          | Value | Memory | Type         |
            +--------+-----------------+-------+--------+--------------+
            |        | x               |       |        | SizedArray2D |
            |        |   dims          |       |        | Dims         |
            |  0     |     [0]         | 2     | 02 00  | UInt16       |
            |  2     |     [1]         | 2     | 02 00  | UInt16       |
            |        |   matrix        |       |        | Array        |
            |        |     [0]         |       |        |              |
            |  4     |       [0]       | 0     | 00 00  | UInt16       |
            |  6     |       [1]       | 1     | 01 00  | UInt16       |
            |        |     [1]         |       |        |              |
            |  8     |       [0]       | 2     | 02 00  | UInt16       |
            | 10     |       [1]       | 3     | 03 00  | UInt16       |
            | 12     | <excess memory> |       | 99     |              |
            +--------+-----------------+-------+--------+--------------+

            1 unconsumed memory bytes (13 available, 12 consumed)
            """)


class TestIndexAccess:

    def test_lookup_forwarded(self):
        assert sample[0] == [0, 1]
        assert sample[0:1] == [[0, 1]]

    def test_set_forwarded(self):
        instance = SizedArray2D([[99, 99], [99, 99], [99, 99]])
        instance[0] = [0, 1]
        instance[1:3] = [[2, 3], [4, 5]]

        expected_dump = Baseline("""
            +--------+-----------+-------+--------+--------------+
            | Offset | Access    | Value | Memory | Type         |
            +--------+-----------+-------+--------+--------------+
            |        | x         |       |        | SizedArray2D |
            |        |   .dims   |       |        | Dims         |
            |  0     |     [0]   | 3     | 03 00  | UInt16       |
            |  2     |     [1]   | 2     | 02 00  | UInt16       |
            |        |   .matrix |       |        | Array        |
            |        |     [0]   |       |        |              |
            |  4     |       [0] | 0     | 00 00  | UInt16       |
            |  6     |       [1] | 1     | 01 00  | UInt16       |
            |        |     [1]   |       |        |              |
            |  8     |       [0] | 2     | 02 00  | UInt16       |
            | 10     |       [1] | 3     | 03 00  | UInt16       |
            |        |     [2]   |       |        |              |
            | 12     |       [0] | 4     | 04 00  | UInt16       |
            | 14     |       [1] | 5     | 05 00  | UInt16       |
            +--------+-----------+-------+--------+--------------+
            """)

        assert getdump(instance) == expected_dump


class TestNameAccess:

    def test_valid_lookup(self):
        assert sample.dims == [2, 2]
        assert sample.matrix == sample_dict['matrix']

    def test_valid_set(self):
        instance = SizedArray2D(dims=[1, 1], matrix=[[1]])
        instance.dims = [2, 2]
        instance.matrix = sample_dict['matrix']
        assert getdump(instance) == sample_dump

    def test_invalid_lookup(self):
        with pytest.raises(AttributeError) as trap:
            sample.junk

        assert str(trap.value) == f"'SizedArray2D' object has no attribute 'junk'"


class TestCompare(_TestCompare):

    sample = sample
    sample_dict = sample_dict

    # inherit test cases
