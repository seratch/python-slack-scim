# The default is v1
from .v1.client import SCIMClient
from .v1.errors import SCIMApiError
from .v1.group import Group, Member as GroupMember
from .v1.groups import Groups
from .v1.service_provider_configs import ServiceProviderConfigs
from .v1.user import User
from .v1.users import Users
