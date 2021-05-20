from netcm.models.BaseModels import VendorIndependentBaseModel
from netcm.models.VendorIndependent.SharedModels import AuthBase
from netcm.models.Fields import GENERIC_OBJECT_NAME
from pydantic.typing import Optional, List, Union, Literal
from pydantic import root_validator
import ipaddress

def validate_asn_is_defined(values):
    return values

class BfdTemplate(VendorIndependentBaseModel):

    # TODO: Unfinished
    name: GENERIC_OBJECT_NAME
    type: Literal["single-hop", "multi-hop"]
    min_rx: int
    min_tx: int
    multiplier: int


class RoutingProtocolBase(VendorIndependentBaseModel):

    pass

class RoutingProtocolIgpBase(RoutingProtocolBase):

    passive_interfaces: List[str]

class RoutingOspfProcess(RoutingProtocolBase):

    process_id: GENERIC_OBJECT_NAME

class RoutingIsisNetwork(VendorIndependentBaseModel):

    area_id: str
    system_id: str
    nsel: str

class AuthenticationIsisMode(VendorIndependentBaseModel):

    level: str
    auth_mode: str

class AuthenticationIsisKeychain(VendorIndependentBaseModel):

    level: str
    keychain: GENERIC_OBJECT_NAME

class AuthenticationIsis(VendorIndependentBaseModel):

    mode: List[AuthenticationIsisMode]
    keychain: List[AuthenticationIsisKeychain]

class RoutingIsisProcess(RoutingProtocolBase):

    process_id: GENERIC_OBJECT_NAME
    it_type: str
    metric_style: str
    fast_flood: Optional[int]
    max_lsp_lifetime: Optional[int]
    network: RoutingIsisNetwork
    authentication: AuthenticationIsis


class BgpNeighborBase(VendorIndependentBaseModel):
    """
    Base Class for BGP Nighbor, used for neighbors and peer-groups
    """
    # TODO: Unfinished
    asn: Optional[int]
    description: Optional[str]

class BgpPeerGroup(BgpNeighborBase):
    # TODO: Unfinished
    pass

class BgpNeighbor(BgpNeighborBase):
    # TODO: Unfinished

    asn: Optional[int]
    address: Union[ipaddress.IPv4Address, ipaddress.IPv6Address]
    peer_group: Optional[BgpPeerGroup]



class BgpRedistributeEntry(VendorIndependentBaseModel):
    # TODO: Unfinished
    type: str
    route_map: Optional[GENERIC_OBJECT_NAME]
    metric: Optional[str]


class BgpAddressFamily(VendorIndependentBaseModel):
    # TODO: Unfinished
    neighbors: List[BgpNeighbor]
    peer_groups: List[BgpPeerGroup]
    redistribute: List[BgpRedistributeEntry]


class RoutingBgpProcess(RoutingProtocolBase):
    # TODO: Unfinished
    asn: int
    neighbors: List[BgpNeighbor]
    peer_groups: List[BgpPeerGroup]
    address_families: Optional[List[BgpAddressFamily]]