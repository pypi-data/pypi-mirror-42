# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Structure type metaclass."""

from .._plum import Plum
from .._plumtype import PlumType
from ._member import Member


class StructureType(PlumType):

    """Structure type metaclass.

    Create custom |Structure| subclass. For example:

        >>> from plum.structure import Structure
        >>> from plum.int.little import UInt16, UInt8
        >>>
        >>> class MyStructure(Structure):
        ...     byte: UInt8
        ...     word: UInt16
        ...
        >>>

    """

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)

        nbytes = 0

        members = dict()
        ignore = set()

        for name, member_cls in getattr(cls, '__annotations__', {}).items():
            try:
                nbytes += member_cls._nbytes
            except TypeError:
                # one or the other is None, set overall size as "varies"
                nbytes = None
            except AttributeError:
                raise TypeError(f'Structure member {name!r} must be a Plum subclass (or Varies)')

            try:
                # retrieve default or member definition after the type annotation
                member = getattr(cls, name)
            except AttributeError:
                # no default or member definition present, create a member definition
                # and place it within the new class namespace to facilitate attribute
                # get/set capability
                member = Member()
                setattr(cls, name, member)
            else:
                # if it's a default value, create a member definition with it and
                # overwrite the default in the new class namespace with the
                # member definition to facilitate attribute get/set capability
                if not isinstance(member, Member):
                    member = Member(default=member)
                    setattr(cls, name, member)

            member._cls = member_cls
            member.name = name

            members[name] = member

            if member.ignore:
                ignore.add(name)

        cls._ignore = ignore
        cls._members = members
        cls._nbytes = nbytes if members else None

    def __call__(cls, *args, **kwargs):
        if not cls._members:
            # "anonymous" structure, accept members so long as they are a plum type
            self = dict.__new__(cls, *args, **kwargs)
            dict.__init__(self, *args, **kwargs)

            for key, value in self.items():
                if not isinstance(value, Plum):
                    raise TypeError(f'{key!r} member must be a plum type')

            return self

        if args:
            if len(args) > 1:
                excess_args = (
                    f'{cls.__name__} expected at most 1 positional arguments, '
                    f'got {len(args)}')
                raise TypeError(excess_args)

            arg = args[0]

            if kwargs:
                # support iterable of (name, value) pairs (and make a fresh copy)
                arg = dict(arg)

                arg.update(kwargs)
                kwargs = arg

            elif isinstance(arg, dict):
                kwargs = arg

            else:
                # support iterable of (name, value) pairs
                kwargs = dict(arg)

        members = cls._members

        extras = set(kwargs) - set(members)

        if extras:
            s = 's' if len(extras) > 1 else ''
            invalid_members = (
                f'{cls.__name__}() '
                f'got {len(extras)} unexpected members{s} ')
            invalid_members += ', '.join(repr(m) for m in members if m in extras)
            raise TypeError(invalid_members)

        values = [kwargs.get(n, m.default) for n, m in members.items()]

        missing = [n for n, v in zip(members, values) if v is None]

        if missing:
            s = 's' if len(missing) > 1 else ''
            missing_members = (
                f'{cls.__name__}() '
                f'missing {len(missing)} required keyword-only argument{s} ')
            missing_members += ', '.join(missing)
            raise TypeError(missing_members)

        self = dict.__new__(cls)

        for member, value in zip(members.values(), values):
            mbr_cls = member.get_cls(self)
            if type(value) is mbr_cls:
                dict.__setitem__(self, member.name, value)
            else:
                dict.__setitem__(self, member.name, mbr_cls(value))

        return self
