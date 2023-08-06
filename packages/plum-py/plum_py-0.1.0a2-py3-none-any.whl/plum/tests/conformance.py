# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import logging

import pytest

from .. import (
    ExcessMemoryError,
    InsufficientMemoryError,
    SizeError,
    calcsize,
    getdump,
    pack,
    unpack,
)

from .utils import wrap_message


class SampleClass(type):

    def __new__(mcs, name, bases, namespace, validate=True):
        return super().__new__(mcs, name, bases, namespace)

    def __init__(cls, name, bases, namespace, validate=True):
        super().__init__(name, bases, namespace)

        if validate:
            basecls = cls.__basecls__

            base_dir = {n for n in dir(basecls) if not n.startswith('_')}

            for name in {n for n in base_dir if not n.startswith('test')}:
                if (getattr(basecls, name) is ...) and (getattr(cls, name) is ...):
                    raise TypeError(f'subclass missing {name!r} attribute')

            cls_dir = {n for n in dir(cls) if not n.startswith('_')}

            extras = {n for n in cls_dir - base_dir if not n.startswith('test')}

            if extras:
                extras = list(sorted(extras))
                raise TypeError(f'illegal subclass attribute {extras}')
        else:
            # subclasses validate attributes against me
            cls.__basecls__ = cls


class Sample(metaclass=SampleClass, validate=False):

    __basecls__ = None

    cls = ...
    """Plum type to test."""

    value = ...
    """Sample value to use to construct plum type instance and to compare."""

    def iter_instances(self):
        yield self.cls(self.value), "instantiated from self.value"

    def iter_values(self):
        yield self.value, "self.value"
        yield self.cls(self.value), "instance"


class BasicConformance(Sample, validate=False):

    bindata = ...
    """Sample packed binary data."""

    cls_nbytes = None
    """Size of plum type being tested."""

    dump = ...
    """Expected dump of sample plum type instance."""

    greedy = False
    """If plum type being tested consumes remaining memory."""

    pack = staticmethod(pack)
    """pack() function to test with (allow plum_c to override to recycle test cases)."""

    retval_str = None
    """Expected return value of __str__ method (default to str of value)."""

    retval_repr = None
    """Expected return value of __repr__ method (default to standard based on value)."""

    unpack = staticmethod(unpack)
    """unpack() function to test with (allow plum_c to override to recycle test cases)."""

    unpack_excess = ...
    """Expected exception message of unpack() method when 1 byte extra."""

    unpack_shortage = ...
    """Expected exception message of unpack() method when short 1 byte."""

    def test_init_via_value(self):
        """Test instantiation with single value."""
        for instance, desc in self.iter_instances():
            logging.info(desc)
            assert getdump(instance) == self.dump

    def test_calcsize_with_cls(self):
        if self.cls_nbytes is None:
            with pytest.raises(SizeError):
                calcsize(self.cls)
        else:
            assert calcsize(self.cls) == self.cls_nbytes

    def test_calcsize_with_instance(self):
        for instance, desc in self.iter_instances():
            logging.info(desc)
            assert calcsize(instance) == len(self.bindata)

    def test_dump(self):
        for instance, desc in self.iter_instances():
            logging.info(desc)
            assert getdump(instance) == self.dump

    def test_pack_cls_value(self):
        for value, desc in self.iter_values():
            logging.info(desc)
            assert pack(self.cls, self.value) == self.bindata

    def test_pack_instance(self):
        for instance, desc in self.iter_instances():
            logging.info(desc)
            assert pack(instance) == self.bindata

    def test_unpack(self):
        instance = self.unpack(self.cls, self.bindata)
        assert getdump(instance) == self.dump

    def test_unpack_shortage(self):
        if self.bindata:
            with pytest.raises(InsufficientMemoryError) as trap:
                self.unpack(self.cls, self.bindata[:-1])

            assert wrap_message(trap.value) == self.unpack_shortage

    def test_unpack_excess(self):
        with pytest.raises(ExcessMemoryError) as trap:
            self.unpack(self.cls, self.bindata + b'\x99')

        assert wrap_message(trap.value) == self.unpack_excess

    def test_str(self):
        if self.retval_str is None:
            expected = str(self.value)
        else:
            expected = self.retval_str

        for instance, desc in self.iter_instances():
            logging.info(desc)
            assert str(instance) == expected

    def test_repr(self):
        if self.retval_repr is None:
            expected = f'{self.cls.__name__}({self.value!r})'
        else:
            expected = self.retval_repr

        for instance, desc in self.iter_instances():
            logging.info(desc)
            assert repr(instance) == expected
