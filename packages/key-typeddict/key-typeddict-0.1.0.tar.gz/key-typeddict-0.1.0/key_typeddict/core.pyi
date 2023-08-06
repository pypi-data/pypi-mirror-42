from typing import Any, Dict, Type, Union

# mypy_extensions.TypedDict should be present in the dependency graph
# noinspection PyUnresolvedReferences
from mypy_extensions import TypedDict


class Key:
    def __init__(self, name: str, required: bool = False): ...


def KeyTypedDict(typename: str,
                      fields: Dict[Union[str, Key], Type[Any]],
                      *,
                      total: bool = ...,
                      allow_extra: bool = ...) -> Type[dict]: ...
