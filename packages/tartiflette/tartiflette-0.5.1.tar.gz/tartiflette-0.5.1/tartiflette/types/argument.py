from typing import Any, Optional, Union

from tartiflette.types.type import GraphQLType


class GraphQLArgument:
    """
    Argument Definition

    Arguments are used for:
      - GraphQLField resolvers
      - GraphQLInputObject fields
    """

    def __init__(
        self,
        name: str,
        gql_type: Union[str, GraphQLType],
        default_value: Optional[Any] = None,
        description: Optional[str] = None,
        schema=None,
    ) -> None:
        # TODO: Narrow the default_value type ?
        self.name = name
        self.gql_type = gql_type
        self.default_value = default_value
        self.description = description
        self._type = {}
        self._schema = schema

    def __repr__(self) -> str:
        return (
            "{}(name={!r}, gql_type={!r}, "
            "default_value={!r}, description={!r})".format(
                self.__class__.__name__,
                self.name,
                self.gql_type,
                self.default_value,
                self.description,
            )
        )

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: Any) -> bool:
        return self is other or (
            type(self) is type(other)
            and self.name == other.name
            and self.gql_type == other.gql_type
            and self.default_value == other.default_value
        )

    # Introspection Attribute
    @property
    def type(self) -> dict:
        return self._type

    @property
    def is_required(self) -> bool:
        if not isinstance(self.gql_type, GraphQLType):
            return False
        return self.gql_type.is_not_null and self.default_value is None

    # Introspection Attribute
    @property
    def defaultValue(self) -> Any:  # pylint: disable=invalid-name
        return self.default_value

    def bake(self, schema: "GraphQLSchema") -> None:
        self._schema = schema
        if isinstance(self.gql_type, GraphQLType):
            self._type = self.gql_type
        else:
            self._type["name"] = self.gql_type
            self._type["kind"] = self._schema.find_type(self.gql_type).kind
