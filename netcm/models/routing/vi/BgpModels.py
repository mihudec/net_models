from netcm.models.BaseModels import VendorIndependentBaseModel
from netcm.models.routing import RoutingProtocolBase
from netcm.models.Fields import *
from pydantic.typing import Optional, List, Union, Literal
from pydantic import root_validator, Field
import ipaddress

class BgpTimers(VendorIndependentBaseModel):

    hello: int = Field(title="Hello time", description="Hello timer in seconds")
    hold: int = Field(title="Hold time", description="Hold timer in seconds")

    @root_validator
    def hold_higher_than_hello(cls, values: dict) -> dict:
        """Validates that hold time is higher than hello time"""
        if values.get("hello") >= values.get("hold"):
            msg = "'hold' must be higher than 'hello'"
            raise AssertionError(msg)
        return values

class BgpFallOver(VendorIndependentBaseModel):

    enabled: bool
    type: Optional[Literal["route-map", "bfd"]]
    route_map: Optional[ROUTE_MAP_NAME]
    """Name of the route-map"""

    @root_validator
    def routemap_required(cls, values: dict) -> dict:
        """Asserts that ``route-map`` is provided if ``type`` == ``"route-map"``"""
        if values.get("type") == "route-map" and not values.get("route-map"):
            msg = "Field 'route-map' is required when 'type' == 'route-map'"
            raise AssertionError()


class BgpNeighborBase(VendorIndependentBaseModel):
    """
    Base Class for BGP Nighbor, used for neighbors and peer-groups
    """
    # TODO: Unfinished
    name: Optional[GENERIC_OBJECT_NAME]
    """Optional name, might be used for looking up neighbors from inventory"""
    asn: Optional[ASN]
    """Autonomous System Number"""
    description: Optional[str]
    """Neighbor description"""
    version: Optional[conint(le=4, ge=4)]
    src_interface: Optional[INTERFACE_NAME]
    """Update source"""
    next_hop_self: Optional[bool]
    """Set NextHop to self"""
    rr_client: Optional[bool]
    """Route Reflector Client"""

class BgpPeerGroup(BgpNeighborBase):
    """
    BGP Peer Group
    """

    is_peergroup: bool = True

class BgpNeighbor(BgpNeighborBase):
    """
    BGP Neighbor
    """
    # TODO: Unfinished

    address: Optional[Union[ipaddress.IPv4Address, ipaddress.IPv6Address]]
    peer_group: Optional[BgpPeerGroup]
    dest_interface: Optional[INTERFACE_NAME]
    """Might be used when referencing neighbor by name rather than address"""

    @root_validator
    def check_if_address_needed(cls, values: dict) -> dict:
        if not all([values.get(x) for x in ["name", "dst_interface"]]):
            if not values.get("address"):
                msg = "Neighbor needs address specified, unless there is both 'name' and 'dst_interface'"
                raise AssertionError(msg)

        return values



class BgpRedistributeEntry(VendorIndependentBaseModel):
    """
    BGP Redistribute Statement
    """
    type: str
    """What to redistribure"""
    route_map: Optional[GENERIC_OBJECT_NAME]
    """Name of the route-map"""
    metric: Optional[str]


class BgpAddressFamily(VendorIndependentBaseModel):
    # TODO: Unfinished
    afi: Literal["ipv4", "ipv6", "vpnv4", "vpnv6"]
    """Address family type"""
    safi: Optional[Literal["unicast", "multicast"]]
    """Address family sub-type"""
    vrf: Optional[VRF_NAME]
    """Name of the VRF"""
    neighbors: List[BgpNeighbor]
    """List of :py:class:`BgpNeighbor` in this Address Family"""
    peer_groups: List[BgpPeerGroup]
    """List of :py:class:`BgpPeerGroup` in this Address Family"""
    redistribute: List[BgpRedistributeEntry]


class RoutingBgpProcess(RoutingProtocolBase):
    # TODO: Unfinished
    asn: ASN
    """Autonomous System Number"""
    neighbors: List[BgpNeighbor]
    """List of :py:class:`BgpNeighbor` objects"""
    peer_groups: List[BgpPeerGroup]
    address_families: Optional[List[BgpAddressFamily]]