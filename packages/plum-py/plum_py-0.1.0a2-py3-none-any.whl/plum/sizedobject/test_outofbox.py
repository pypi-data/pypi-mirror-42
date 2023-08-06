# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test SizedObject as is."""

from baseline import Baseline

from ..tests.conformance import BasicConformance
from . import SizedObject


class TestDefault(BasicConformance):

    bindata = b'\x03\x00\x01\x02'

    cls = SizedObject

    cls_nbytes = None

    dump = Baseline("""
            +--------+---------+-------+--------+-------------+
            | Offset | Access  | Value | Memory | Type        |
            +--------+---------+-------+--------+-------------+
            |        | x       |       |        | SizedObject |
            | 0      |   .size | 3     | 03     | UInt8       |
            |        |   .item |       |        | Array       |
            | 1      |     [0] | 0     | 00     | UInt8       |
            | 2      |     [1] | 1     | 01     | UInt8       |
            | 3      |     [2] | 2     | 02     | UInt8       |
            +--------+---------+-------+--------+-------------+
            """)

    value = dict(size=3, item=[0, 1, 2])

    unpack_excess = Baseline("""


        +--------+-----------------+-------+--------+-------------+
        | Offset | Access          | Value | Memory | Type        |
        +--------+-----------------+-------+--------+-------------+
        |        | x               |       |        | SizedObject |
        | 0      |   size          | 3     | 03     | UInt8       |
        |        |   item          |       |        | Array       |
        | 1      |     [0]         | 0     | 00     | UInt8       |
        | 2      |     [1]         | 1     | 01     | UInt8       |
        | 3      |     [2]         | 2     | 02     | UInt8       |
        | 4      | <excess memory> |       | 99     |             |
        +--------+-----------------+-------+--------+-------------+

        1 unconsumed memory bytes (5 available, 4 consumed)
        """)

    unpack_shortage = Baseline("""


        +--------+--------+----------------------+--------+-------------+
        | Offset | Access | Value                | Memory | Type        |
        +--------+--------+----------------------+--------+-------------+
        |        | x      |                      |        | SizedObject |
        | 0      |   size | 3                    | 03     | UInt8       |
        | 1      |   item | <insufficient bytes> | 00 01  | Array       |
        +--------+--------+----------------------+--------+-------------+

        InsufficientMemoryError: 1 too few memory bytes to unpack Array (3
        needed, only 2 available), dump above shows interrupted progress
        """)

    retval_str = Baseline("""
        SizedObject(size=UInt8(3), item=Array([UInt8(0), UInt8(1), UInt8(2)]))
        """)

    retval_repr = Baseline("""
        SizedObject(size=UInt8(3), item=Array([UInt8(0), UInt8(1), UInt8(2)]))
        """)
