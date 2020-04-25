# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = group_from_dict(json.loads(json_string))

from typing import Optional, Any, List, TypeVar, Type, cast, Callable


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


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


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


class Name:
    family_name: Optional[str]
    given_name: Optional[str]
    honorific_prefix: Optional[str]

    def __init__(self, family_name: Optional[str], given_name: Optional[str], honorific_prefix: Optional[str]) -> None:
        self.family_name = family_name
        self.given_name = given_name
        self.honorific_prefix = honorific_prefix

    @staticmethod
    def from_dict(obj: Any) -> 'Name':
        assert isinstance(obj, dict)
        family_name = from_union([from_str, from_none], obj.get("familyName"))
        given_name = from_union([from_str, from_none], obj.get("givenName"))
        honorific_prefix = from_union([from_str, from_none], obj.get("honorificPrefix"))
        return Name(family_name, given_name, honorific_prefix)

    def to_dict(self) -> dict:
        result: dict = {}
        result["familyName"] = from_union([from_str, from_none], self.family_name)
        result["givenName"] = from_union([from_str, from_none], self.given_name)
        result["honorificPrefix"] = from_union([from_str, from_none], self.honorific_prefix)
        return result


class Manager:
    manager_id: Optional[str]

    def __init__(self, manager_id: Optional[str]) -> None:
        self.manager_id = manager_id

    @staticmethod
    def from_dict(obj: Any) -> 'Manager':
        assert isinstance(obj, dict)
        manager_id = from_union([from_str, from_none], obj.get("managerId"))
        return Manager(manager_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["managerId"] = from_union([from_str, from_none], self.manager_id)
        return result


class UrnScimSchemasExtensionEnterprise10:
    cost_center: Optional[str]
    department: Optional[str]
    division: Optional[str]
    employee_number: Optional[str]
    manager: Optional[Manager]
    organization: Optional[str]

    def __init__(self, cost_center: Optional[str], department: Optional[str], division: Optional[str], employee_number: Optional[str], manager: Optional[Manager], organization: Optional[str]) -> None:
        self.cost_center = cost_center
        self.department = department
        self.division = division
        self.employee_number = employee_number
        self.manager = manager
        self.organization = organization

    @staticmethod
    def from_dict(obj: Any) -> 'UrnScimSchemasExtensionEnterprise10':
        assert isinstance(obj, dict)
        cost_center = from_union([from_str, from_none], obj.get("costCenter"))
        department = from_union([from_str, from_none], obj.get("department"))
        division = from_union([from_str, from_none], obj.get("division"))
        employee_number = from_union([from_str, from_none], obj.get("employeeNumber"))
        manager = from_union([Manager.from_dict, from_none], obj.get("manager"))
        organization = from_union([from_str, from_none], obj.get("organization"))
        return UrnScimSchemasExtensionEnterprise10(cost_center, department, division, employee_number, manager, organization)

    def to_dict(self) -> dict:
        result: dict = {}
        result["costCenter"] = from_union([from_str, from_none], self.cost_center)
        result["department"] = from_union([from_str, from_none], self.department)
        result["division"] = from_union([from_str, from_none], self.division)
        result["employeeNumber"] = from_union([from_str, from_none], self.employee_number)
        result["manager"] = from_union([lambda x: to_class(Manager, x), from_none], self.manager)
        result["organization"] = from_union([from_str, from_none], self.organization)
        return result


class Member:
    active: Optional[bool]
    display_name: Optional[str]
    external_id: Optional[str]
    id: Optional[str]
    locale: Optional[str]
    meta: Optional[Meta]
    name: Optional[Name]
    nick_name: Optional[str]
    password: Optional[str]
    preferred_language: Optional[str]
    profile_url: Optional[str]
    schemas: Optional[List[str]]
    timezone: Optional[str]
    title: Optional[str]
    urn_scim_schemas_extension_enterprise_10: Optional[UrnScimSchemasExtensionEnterprise10]
    user_name: Optional[str]
    user_type: Optional[str]

    def __init__(self, active: Optional[bool], display_name: Optional[str], external_id: Optional[str], id: Optional[str], locale: Optional[str], meta: Optional[Meta], name: Optional[Name], nick_name: Optional[str], password: Optional[str], preferred_language: Optional[str], profile_url: Optional[str], schemas: Optional[List[str]], timezone: Optional[str], title: Optional[str], urn_scim_schemas_extension_enterprise_10: Optional[UrnScimSchemasExtensionEnterprise10], user_name: Optional[str], user_type: Optional[str]) -> None:
        self.active = active
        self.display_name = display_name
        self.external_id = external_id
        self.id = id
        self.locale = locale
        self.meta = meta
        self.name = name
        self.nick_name = nick_name
        self.password = password
        self.preferred_language = preferred_language
        self.profile_url = profile_url
        self.schemas = schemas
        self.timezone = timezone
        self.title = title
        self.urn_scim_schemas_extension_enterprise_10 = urn_scim_schemas_extension_enterprise_10
        self.user_name = user_name
        self.user_type = user_type

    @staticmethod
    def from_dict(obj: Any) -> 'Member':
        assert isinstance(obj, dict)
        active = from_union([from_bool, from_none], obj.get("active"))
        display_name = from_union([from_str, from_none], obj.get("displayName"))
        external_id = from_union([from_str, from_none], obj.get("externalId"))
        id = from_union([from_str, from_none], obj.get("id"))
        locale = from_union([from_str, from_none], obj.get("locale"))
        meta = from_union([Meta.from_dict, from_none], obj.get("meta"))
        name = from_union([Name.from_dict, from_none], obj.get("name"))
        nick_name = from_union([from_str, from_none], obj.get("nickName"))
        password = from_union([from_str, from_none], obj.get("password"))
        preferred_language = from_union([from_str, from_none], obj.get("preferredLanguage"))
        profile_url = from_union([from_str, from_none], obj.get("profileUrl"))
        schemas = from_union([lambda x: from_list(from_str, x), from_none], obj.get("schemas"))
        timezone = from_union([from_str, from_none], obj.get("timezone"))
        title = from_union([from_str, from_none], obj.get("title"))
        urn_scim_schemas_extension_enterprise_10 = from_union([UrnScimSchemasExtensionEnterprise10.from_dict, from_none], obj.get("urn:scim:schemas:extension:enterprise:1.0"))
        user_name = from_union([from_str, from_none], obj.get("userName"))
        user_type = from_union([from_str, from_none], obj.get("userType"))
        return Member(active, display_name, external_id, id, locale, meta, name, nick_name, password, preferred_language, profile_url, schemas, timezone, title, urn_scim_schemas_extension_enterprise_10, user_name, user_type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["active"] = from_union([from_bool, from_none], self.active)
        result["displayName"] = from_union([from_str, from_none], self.display_name)
        result["externalId"] = from_union([from_str, from_none], self.external_id)
        result["id"] = from_union([from_str, from_none], self.id)
        result["locale"] = from_union([from_str, from_none], self.locale)
        result["meta"] = from_union([lambda x: to_class(Meta, x), from_none], self.meta)
        result["name"] = from_union([lambda x: to_class(Name, x), from_none], self.name)
        result["nickName"] = from_union([from_str, from_none], self.nick_name)
        result["password"] = from_union([from_str, from_none], self.password)
        result["preferredLanguage"] = from_union([from_str, from_none], self.preferred_language)
        result["profileUrl"] = from_union([from_str, from_none], self.profile_url)
        result["schemas"] = from_union([lambda x: from_list(from_str, x), from_none], self.schemas)
        result["timezone"] = from_union([from_str, from_none], self.timezone)
        result["title"] = from_union([from_str, from_none], self.title)
        result["urn:scim:schemas:extension:enterprise:1.0"] = from_union([lambda x: to_class(UrnScimSchemasExtensionEnterprise10, x), from_none], self.urn_scim_schemas_extension_enterprise_10)
        result["userName"] = from_union([from_str, from_none], self.user_name)
        result["userType"] = from_union([from_str, from_none], self.user_type)
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
