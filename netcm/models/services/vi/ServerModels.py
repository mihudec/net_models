import ipaddress
from pydantic.typing import Optional, Union, List, Literal
from pydantic import conint, root_validator
from netcm.models.BaseModels import VendorIndependentBaseModel
from netcm.models.BaseModels.SharedModels import KeyBase, AuthBase
from netcm.models.Fields import GENERIC_OBJECT_NAME, VRF_NAME, BASE_INTERFACE_NAME


class ServerPropertiesBase(VendorIndependentBaseModel):

    server: Union[ipaddress.IPv4Address, ipaddress.IPv6Address]
    address_version: Optional[Literal["ipv4", "ipv6"]]

    @root_validator(allow_reuse=True)
    def generate_address_version(cls, values):
        if not values.get("address_version"):
            if isinstance(values.get("server"), ipaddress.IPv4Address):
                values["address_version"] = "ipv4"
            elif isinstance(values.get("server"), ipaddress.IPv6Address):
                values["address_version"] = "ipv6"
        return values


class NtpServer(ServerPropertiesBase):

    src_interface: Optional[str]
    key: Optional[str]
    prefer: Optional[bool]


class LoggingServer(ServerPropertiesBase):

    protocol: Optional[Literal["tcp", "udp"]]
    port: Optional[int]


class AaaServer(ServerPropertiesBase):

    name: GENERIC_OBJECT_NAME
    timeout: Optional[conint(ge=1)]
    key: Optional[KeyBase]
    single_connection: Optional[bool]


class RadiusServer(AaaServer):

    retransmit: Optional[conint(ge=1)]


class TacacsServer(AaaServer):

    pass


class AaaServerGroup(VendorIndependentBaseModel):

    name: GENERIC_OBJECT_NAME
    src_interface: Optional[BASE_INTERFACE_NAME]
    vrf: Optional[VRF_NAME]


class RadiusServerGroup(AaaServerGroup):

    servers: List[RadiusServer]


class TacacsServerGroup(AaaServerGroup):

    servers: List[TacacsServer]
