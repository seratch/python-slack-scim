# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = service_provider_configs_from_dict(json.loads(json_string))

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


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class AuthenticationScheme:
    description: Optional[str]
    name: Optional[str]
    primary: Optional[bool]
    spec_url: Optional[str]
    type: Optional[str]

    def __init__(self, description: Optional[str], name: Optional[str], primary: Optional[bool], spec_url: Optional[str], type: Optional[str]) -> None:
        self.description = description
        self.name = name
        self.primary = primary
        self.spec_url = spec_url
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'AuthenticationScheme':
        assert isinstance(obj, dict)
        description = from_union([from_str, from_none], obj.get("description"))
        name = from_union([from_str, from_none], obj.get("name"))
        primary = from_union([from_bool, from_none], obj.get("primary"))
        spec_url = from_union([from_str, from_none], obj.get("specUrl"))
        type = from_union([from_str, from_none], obj.get("type"))
        return AuthenticationScheme(description, name, primary, spec_url, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["description"] = from_union([from_str, from_none], self.description)
        result["name"] = from_union([from_str, from_none], self.name)
        result["primary"] = from_union([from_bool, from_none], self.primary)
        result["specUrl"] = from_union([from_str, from_none], self.spec_url)
        result["type"] = from_union([from_str, from_none], self.type)
        return result


class Bulk:
    max_operations: Optional[int]
    max_payload_size: Optional[int]
    supported: Optional[bool]

    def __init__(self, max_operations: Optional[int], max_payload_size: Optional[int], supported: Optional[bool]) -> None:
        self.max_operations = max_operations
        self.max_payload_size = max_payload_size
        self.supported = supported

    @staticmethod
    def from_dict(obj: Any) -> 'Bulk':
        assert isinstance(obj, dict)
        max_operations = from_union([from_int, from_none], obj.get("maxOperations"))
        max_payload_size = from_union([from_int, from_none], obj.get("maxPayloadSize"))
        supported = from_union([from_bool, from_none], obj.get("supported"))
        return Bulk(max_operations, max_payload_size, supported)

    def to_dict(self) -> dict:
        result: dict = {}
        result["maxOperations"] = from_union([from_int, from_none], self.max_operations)
        result["maxPayloadSize"] = from_union([from_int, from_none], self.max_payload_size)
        result["supported"] = from_union([from_bool, from_none], self.supported)
        return result


class ChangePassword:
    supported: Optional[bool]

    def __init__(self, supported: Optional[bool]) -> None:
        self.supported = supported

    @staticmethod
    def from_dict(obj: Any) -> 'ChangePassword':
        assert isinstance(obj, dict)
        supported = from_union([from_bool, from_none], obj.get("supported"))
        return ChangePassword(supported)

    def to_dict(self) -> dict:
        result: dict = {}
        result["supported"] = from_union([from_bool, from_none], self.supported)
        return result


class Filter:
    max_results: Optional[int]
    supported: Optional[bool]

    def __init__(self, max_results: Optional[int], supported: Optional[bool]) -> None:
        self.max_results = max_results
        self.supported = supported

    @staticmethod
    def from_dict(obj: Any) -> 'Filter':
        assert isinstance(obj, dict)
        max_results = from_union([from_int, from_none], obj.get("maxResults"))
        supported = from_union([from_bool, from_none], obj.get("supported"))
        return Filter(max_results, supported)

    def to_dict(self) -> dict:
        result: dict = {}
        result["maxResults"] = from_union([from_int, from_none], self.max_results)
        result["supported"] = from_union([from_bool, from_none], self.supported)
        return result


class ServiceProviderConfigs:
    authentication_schemes: Optional[List[AuthenticationScheme]]
    bulk: Optional[Bulk]
    change_password: Optional[ChangePassword]
    etag: Optional[ChangePassword]
    filter: Optional[Filter]
    patch: Optional[ChangePassword]
    sort: Optional[ChangePassword]
    xml_data_format: Optional[ChangePassword]

    def __init__(self, authentication_schemes: Optional[List[AuthenticationScheme]], bulk: Optional[Bulk], change_password: Optional[ChangePassword], etag: Optional[ChangePassword], filter: Optional[Filter], patch: Optional[ChangePassword], sort: Optional[ChangePassword], xml_data_format: Optional[ChangePassword]) -> None:
        self.authentication_schemes = authentication_schemes
        self.bulk = bulk
        self.change_password = change_password
        self.etag = etag
        self.filter = filter
        self.patch = patch
        self.sort = sort
        self.xml_data_format = xml_data_format

    @staticmethod
    def from_dict(obj: Any) -> 'ServiceProviderConfigs':
        assert isinstance(obj, dict)
        authentication_schemes = from_union([lambda x: from_list(AuthenticationScheme.from_dict, x), from_none], obj.get("authenticationSchemes"))
        bulk = from_union([Bulk.from_dict, from_none], obj.get("bulk"))
        change_password = from_union([ChangePassword.from_dict, from_none], obj.get("changePassword"))
        etag = from_union([ChangePassword.from_dict, from_none], obj.get("etag"))
        filter = from_union([Filter.from_dict, from_none], obj.get("filter"))
        patch = from_union([ChangePassword.from_dict, from_none], obj.get("patch"))
        sort = from_union([ChangePassword.from_dict, from_none], obj.get("sort"))
        xml_data_format = from_union([ChangePassword.from_dict, from_none], obj.get("xmlDataFormat"))
        return ServiceProviderConfigs(authentication_schemes, bulk, change_password, etag, filter, patch, sort, xml_data_format)

    def to_dict(self) -> dict:
        result: dict = {}
        result["authenticationSchemes"] = from_union([lambda x: from_list(lambda x: to_class(AuthenticationScheme, x), x), from_none], self.authentication_schemes)
        result["bulk"] = from_union([lambda x: to_class(Bulk, x), from_none], self.bulk)
        result["changePassword"] = from_union([lambda x: to_class(ChangePassword, x), from_none], self.change_password)
        result["etag"] = from_union([lambda x: to_class(ChangePassword, x), from_none], self.etag)
        result["filter"] = from_union([lambda x: to_class(Filter, x), from_none], self.filter)
        result["patch"] = from_union([lambda x: to_class(ChangePassword, x), from_none], self.patch)
        result["sort"] = from_union([lambda x: to_class(ChangePassword, x), from_none], self.sort)
        result["xmlDataFormat"] = from_union([lambda x: to_class(ChangePassword, x), from_none], self.xml_data_format)
        return result


def service_provider_configs_from_dict(s: Any) -> ServiceProviderConfigs:
    return ServiceProviderConfigs.from_dict(s)


def service_provider_configs_to_dict(x: ServiceProviderConfigs) -> Any:
    return to_class(ServiceProviderConfigs, x)
