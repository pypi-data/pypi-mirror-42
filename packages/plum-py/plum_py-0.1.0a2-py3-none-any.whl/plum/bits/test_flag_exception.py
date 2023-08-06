# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test flag bitfield construction exceptions."""

from enum import IntEnum, IntFlag

import pytest

from plum.bits import Bits


class MyEnum(IntEnum):

    """Enumneation definition."""

    A = 1
    B = 2


class MyFlag(IntFlag):

    """Flag definition."""

    A = 1
    B = 2


class TestInit:

    """Test constructor."""

    @staticmethod
    def test_invalid_flag_class():
        """Test invalid flag class."""
        # pylint: disable=unused-variable
        with pytest.raises(TypeError) as trap:
            class MyBits(Bits, nbytes=2, flag=MyEnum):
                # pylint: disable=missing-docstring
                # pylint: disable=too-few-public-methods
                pass

        assert str(
            trap.value) == 'invalid enum, expected IntFlag subclass or True'

    @staticmethod
    def test_invalid_flag_anotation():
        """Test invalid flag flag parameter together with anotations."""
        # pylint: disable=unused-variable
        with pytest.raises(TypeError) as trap:
            class MyBits(Bits, nbytes=2, flag=MyFlag):
                # pylint: disable=missing-docstring
                # pylint: disable=too-few-public-methods
                invalid: int

        assert str(trap.value) == (
            "subclass may not contain bitfield definitions (or any annotation)"
            " when 'flag' argument specifies an integer flag enumeration")
