from net_models.models.BaseModels import VendorIndependentBaseModel
from net_models.models.Fields import VRF_NAME, INTERFACE_NAME
from pydantic.typing import Optional
from pydantic import conint
import ipaddress

class StaticRoute(VendorIndependentBaseModel):

    vrf: Optional[VRF_NAME]
    interface: Optional[INTERFACE_NAME]
    metric: Optional[conint(ge=1, le=255)]

class StaticRouteV4(StaticRoute):

    network: ipaddress.IPv4Network
    next_hop: Optional[ipaddress.IPv4Address]


class StaticRouteV6(StaticRoute):

    network: ipaddress.IPv6Network
    next_hop: Optional[ipaddress.IPv6Address]
