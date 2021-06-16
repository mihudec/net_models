import ipaddress
from pydantic.typing import Optional, Union, List, Literal
from pydantic import conint, root_validator
from net_models.fields import GENERIC_OBJECT_NAME, VRF_NAME, BASE_INTERFACE_NAME, InterfaceName
from net_models.models import VendorIndependentBaseModel
from net_models.models.BaseModels.SharedModels import KeyBase

def validate_servers_unique(cls, values):
    names = [x.name for x in values.get("servers")]
    servers = [x.server for x in values.get("servers")]

    if len(names) != len(set(names)):
        msg = f"Server names must be unique."
        raise AssertionError(msg)

    if len(servers) != len(set(servers)):
        msg = f"Server addresses must be unique."
        raise AssertionError(msg)

    return values


class ServerBase(VendorIndependentBaseModel):

    pass


class ServerPropertiesBase(ServerBase):

    server: Union[ipaddress.IPv4Address, ipaddress.IPv6Address]
    src_interface: Optional[InterfaceName]
    vrf: Optional[VRF_NAME]


class NtpKey(KeyBase):

    key_id: int
    method: Literal["md5"]
    trusted: Optional[bool]


class NtpServer(ServerPropertiesBase):

    key_id: Optional[int]
    prefer: Optional[bool]


class NtpAccessGroups(VendorIndependentBaseModel):

    serve_only: Optional[GENERIC_OBJECT_NAME]
    query_only: Optional[GENERIC_OBJECT_NAME]
    serve: Optional[GENERIC_OBJECT_NAME]
    peer: Optional[GENERIC_OBJECT_NAME]


class NtpConfig(VendorIndependentBaseModel):

    authenticate: Optional[bool]
    servers: Optional[List[NtpServer]]
    peers: Optional[List[NtpServer]]
    ntp_keys: Optional[List[NtpKey]]
    src_interface: Optional[InterfaceName]
    access_groups: Optional[NtpAccessGroups]


class LoggingServer(ServerPropertiesBase):

    protocol: Optional[Literal["tcp", "udp"]]
    port: Optional[int]


class AaaServer(ServerBase):

    name: GENERIC_OBJECT_NAME
    server: Union[ipaddress.IPv4Address, ipaddress.IPv6Address]
    address_version: Optional[Literal["ipv4", "ipv6"]]
    timeout: Optional[conint(ge=1)]
    key: KeyBase
    single_connection: Optional[bool]

    @root_validator(allow_reuse=True)
    def generate_address_version(cls, values):
        if not values.get("address_version"):
            if isinstance(values.get("server"), ipaddress.IPv4Address):
                values["address_version"] = "ipv4"
            elif isinstance(values.get("server"), ipaddress.IPv6Address):
                values["address_version"] = "ipv6"
        return values


class RadiusServer(AaaServer):

    retransmit: Optional[conint(ge=1)]


class TacacsServer(AaaServer):

    pass


class AaaServerGroup(ServerBase):

    name: GENERIC_OBJECT_NAME
    src_interface: Optional[InterfaceName]
    vrf: Optional[VRF_NAME]

    _validate_servers_unique = root_validator(allow_reuse=True)(validate_servers_unique)


class RadiusServerGroup(AaaServerGroup):

    servers: List[RadiusServer]


class TacacsServerGroup(AaaServerGroup):

    servers: List[TacacsServer]



