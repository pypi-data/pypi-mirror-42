import typing

from dataclasses import dataclass
from graphql import GraphQLField, GraphQLObjectType
from graphql.utilities.schema_printer import print_type

from .constants import IS_STRAWBERRY_FIELD
from .type_converter import get_graphql_type_for_annotation


def _get_resolver(cls, field_name):
    def _resolver(obj, info):
        # TODO: can we make this nicer?
        # does it work in all the cases?

        field_resolver = getattr(cls(**(obj.__dict__ if obj else {})), field_name)

        if getattr(field_resolver, IS_STRAWBERRY_FIELD, False):
            return field_resolver(obj, info)

        return field_resolver

    return _resolver


def _get_fields(cls):
    cls_annotations = typing.get_type_hints(cls)

    fields = {
        key: GraphQLField(
            get_graphql_type_for_annotation(value, field_name=key),
            resolve=_get_resolver(cls, key),
        )
        for key, value in cls_annotations.items()
    }

    fields.update(
        {
            key: value.field
            for key, value in cls.__dict__.items()
            if getattr(value, IS_STRAWBERRY_FIELD, False)
        }
    )

    return fields


def type(cls):
    def wrap():
        def repr_(self):
            return print_type(self.field)

        setattr(cls, "__repr__", repr_)

        cls._fields = _get_fields(cls)
        cls.field = GraphQLObjectType(name=cls.__name__, fields=cls._fields)

        return dataclass(cls, repr=False)

    return wrap()
