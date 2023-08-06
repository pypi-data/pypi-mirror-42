# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import pytest
from baseline import Baseline

from . import InsufficientMemoryError, ExcessMemoryError, unpack
from .int.little import UInt8, UInt16
from .tests.utils import wrap_message


class TestUnpack:

    unpack = staticmethod(unpack)

    def test_bytes(self):
        x = self.unpack(UInt16, b'\x02\x01')
        assert type(x) is UInt16
        assert x == 0x0102

    def test_bytearray(self):
        x = self.unpack(UInt16, bytearray([2, 1]))
        assert type(x) is UInt16
        assert x == 0x0102

    def test_insufficient(self):
        with pytest.raises(InsufficientMemoryError) as trap:
            self.unpack(UInt16, b'\x01')

        expected_message = Baseline("""


            +--------+--------+----------------------+--------+--------+
            | Offset | Access | Value                | Memory | Type   |
            +--------+--------+----------------------+--------+--------+
            | 0      | x      | <insufficient bytes> | 01     | UInt16 |
            +--------+--------+----------------------+--------+--------+

            InsufficientMemoryError: 1 too few memory bytes to unpack UInt16 (2
            needed, only 1 available), dump above shows interrupted progress
            """)

        assert wrap_message(trap.value) == expected_message

    def test_excess(self):
        with pytest.raises(ExcessMemoryError) as trap:
            self.unpack(UInt16, b'\x02\x01\x00')

        expected_message = Baseline("""


            +--------+-----------------+-------+--------+--------+
            | Offset | Access          | Value | Memory | Type   |
            +--------+-----------------+-------+--------+--------+
            | 0      | x               | 258   | 02 01  | UInt16 |
            | 2      | <excess memory> |       | 00     |        |
            +--------+-----------------+-------+--------+--------+

            1 unconsumed memory bytes (3 available, 2 consumed)
            """)

        assert wrap_message(trap.value) == expected_message
