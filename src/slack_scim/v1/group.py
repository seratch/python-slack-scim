# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = group_from_dict(json.loads(json_string))

from typing import Optional, Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Member:
    display: Optional[str]
    value: Optional[str]

    def __init__(self, display: Optional[str], value: Optional[str]) -> None:
        self.display = display
        self.value = value

    @staticmethod
    def from_dict(obj: Any) -> 'Member':
        assert isinstance(obj, dict)
        display = from_union([from_str, from_none], obj.get("display"))
        value = from_union([from_str, from_none], obj.get("value"))
        return Member(display, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["display"] = from_union([from_str, from_none], self.display)
        result["value"] = from_union([from_str, from_none], self.value)
        return result


class Meta:
    created: Optional[str]
    location: Optional[str]

    def __init__(self, created: Optional[str], location: Optional[str]) -> None:
        self.created = created
        self.location = location

    @staticmethod
    def from_dict(obj: Any) -> 'Meta':
        assert isinstance(obj, dict)
        created = from_union([from_str, from_none], obj.get("created"))
        location = from_union([from_str, from_none], obj.get("location"))
        return Meta(created, location)

    def to_dict(self) -> dict:
        result: dict = {}
        result["created"] = from_union([from_str, from_none], self.created)
        result["location"] = from_union([from_str, from_none], self.location)
        return result


class Group:
    display_name: Optional[str]
    id: Optional[str]
    members: Optional[List[Member]]
    meta: Optional[Meta]
    schemas: Optional[List[str]]

    def __init__(self, display_name: Optional[str], id: Optional[str], members: Optional[List[Member]], meta: Optional[Meta], schemas: Optional[List[str]]) -> None:
        self.display_name = display_name
        self.id = id
        self.members = members
        self.meta = meta
        self.schemas = schemas

    @staticmethod
    def from_dict(obj: Any) -> 'Group':
        assert isinstance(obj, dict)
        display_name = from_union([from_str, from_none], obj.get("displayName"))
        id = from_union([from_str, from_none], obj.get("id"))
        members = from_union([lambda x: from_list(Member.from_dict, x), from_none], obj.get("members"))
        meta = from_union([Meta.from_dict, from_none], obj.get("meta"))
        schemas = from_union([lambda x: from_list(from_str, x), from_none], obj.get("schemas"))
        return Group(display_name, id, members, meta, schemas)

    def to_dict(self) -> dict:
        result: dict = {}
        result["displayName"] = from_union([from_str, from_none], self.display_name)
        result["id"] = from_union([from_str, from_none], self.id)
        result["members"] = from_union([lambda x: from_list(lambda x: to_class(Member, x), x), from_none], self.members)
        result["meta"] = from_union([lambda x: to_class(Meta, x), from_none], self.meta)
        result["schemas"] = from_union([lambda x: from_list(from_str, x), from_none], self.schemas)
        return result


def group_from_dict(s: Any) -> Group:
    return Group.from_dict(s)


def group_to_dict(x: Group) -> Any:
    return to_class(Group, x)
