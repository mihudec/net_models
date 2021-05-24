import ipaddress
from pydantic.typing import Optional, Union, List, Literal
from pydantic import conint
from netcm.models.BaseModels import VendorIndependentBaseModel
from netcm.models.VendorIndependent.SharedModels import KeyBase, AuthBase
from netcm.models.Fields import GENERIC_OBJECT_NAME, VRF_NAME, BASE_INTERFACE_NAME


class ServerPropertiesBase(VendorIndependentBaseModel):

    server: Union[ipaddress.IPv4Address, ipaddress.IPv6Address]
    vrf: Optional[VRF_NAME]



class NtpServer(ServerPropertiesBase):

    source_interface: Optional[str]
    key: Optional[str]
    prefer: Optional[bool]


class LoggingServer(ServerPropertiesBase):

    procol: Optional[Literal["tcp", "udp"]]
    port: Optional[int]


class AaaServer(ServerPropertiesBase):

    name: GENERIC_OBJECT_NAME
    timeout: Optional[conint(ge=1)]
    key: Optional[KeyBase]
    single_connection: Optional[bool]


class RadiusServer(AaaServer):

    pass


class TacacsServer(AaaServer):

    pass


class AaaServerGroup(VendorIndependentBaseModel):

    source_interface: Optional[BASE_INTERFACE_NAME]
    vrf: Optional[VRF_NAME]


class RadiusServerGroup(AaaServerGroup):

    servers: List[RadiusServer]


class TacacsServerGroup(AaaServerGroup):

    servers: List[TacacsServer]
