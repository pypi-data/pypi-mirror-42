# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Sized array structure type metaclass."""

from ..array import Array as _Array
from ..structure import StructureType


class SizedArrayType(StructureType):

    """SizedArray type metaclass.

    Create custom |SizedArray| subclass. For example:

        >>> from plum.sizedarray import SizedArray
        >>> from plum.int.little import UInt16
        >>> class MySizedArray(SizedArray, dims_cls=UInt16, dims_name='size', item_cls=UInt16, array_name='array'):
        ...     pass
        ...
        >>>

    :param dims_cls: structure size member type
    :type dims_cls: ArrayType (1 dimensional) or IntType
    :param str dims_name: structure size member name
    :param ArrayType item_cls: item type for structure array member
    :param str array_name: structure array member name

    """

    def __new__(mcs, name, bases, namespace, dims_cls=None, dims_name=None, item_cls=None, array_name=None):
        return type.__new__(mcs, name, bases, namespace)

    def __init__(cls, name, bases, namespace, dims_cls=None, dims_name=None, item_cls=None, array_name=None):
        type.__init__(cls, name, bases, namespace)

        if dims_cls is None:
            dims_cls = cls._dims_cls

        if dims_name is None:
            dims_name = cls._dims_name

        if item_cls is None:
            item_cls = cls._item_cls

        if array_name is None:
            array_name = cls._array_name

        try:
            ndims = dims_cls._dims[0]
        except AttributeError:
            ndims = 1
            dims_is_scalar = True
        else:
            dims_is_scalar = False

        class Array(_Array, item_cls=item_cls, dims=tuple([None] * ndims)):
            pass

        Array.__name__ = 'Array'

        cls._array_cls = Array
        cls._array_name = array_name
        cls._item_cls = item_cls
        cls._nbytes = None
        cls._ndims = ndims
        cls._dims_cls = dims_cls
        cls._dims_is_scalar = dims_is_scalar
        cls._dims_name = dims_name

    def __call__(cls, *args, **kwargs):
        if len(args) == 1:
            arg = args[0]
            if not isinstance(arg, dict):
                args = ({cls._array_name: arg},)

        members = dict(*args, **kwargs)

        if not members:
            items = []
            dims = [0] * cls._ndims
            count = None
        else:
            count = members.pop(cls._dims_name, None)
            items = members.pop(cls._array_name, None)

            if members:
                if len(members) == 1:
                    member = list(members.keys())[0]
                    raise TypeError(f'got an unexpected member {member!r}')
                else:
                    members = "', '".join(members)
                    raise TypeError(f"got unexpected members '{members}'")

            dims = []
            _items = items
            for i in range(cls._ndims):
                try:
                    dims.append(len(_items))
                    _items = _items[0]
                except (TypeError, IndexError):
                    raise TypeError('{ndims} dimensions expected, only {i} found')

        if count is None:
            if cls._dims_is_scalar:
                count = dims[0]
            else:
                count = dims

        self = dict.__new__(cls)
        self[cls._dims_name] = cls._dims_cls(count)
        self[cls._array_name] = cls._array_cls._make_instance(items, dims)

        return self
