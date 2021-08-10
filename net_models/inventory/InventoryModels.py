# Standard Libraries
import ipaddress
# Third party packages
from pydantic import root_validator, validator, conint
from pydantic.typing import Optional, List, Literal, Dict
# Local package
from net_models.fields import InterfaceName, GENERIC_OBJECT_NAME, LAG_MODE, VRF_NAME
from net_models.validators import sort_interface_dict, required_together, ipv4s_in_same_subnet, ipv4_is_assignable, validate_unique
from net_models.models import (
    BaseNetModel,
    InterfaceModel,
    VRFModel,
    VLANModel
)
from net_models.models.routing import *
# Local module




class InventoryModel(BaseNetModel):

    pass


class RoutingConfig(InventoryModel):

    bgp: Optional[RoutingBgpProcess]
    isis: Optional[List[RoutingIsisProcess]]
    ospf: Optional[List[RoutingOspfProcess]]
    static_ipv4: Optional[List[StaticRouteV4]]


class GlobalConfig(BaseNetModel):

    interfaces: Dict[InterfaceName, InterfaceModel] # Actually collections.OrderedDict, because Python 3.6

    _sort_interfaces = validator("interfaces", allow_reuse=True)(sort_interface_dict)


class HostConfig(BaseNetModel):

    interfaces: Dict[InterfaceName, InterfaceModel] # Actually collections.OrderedDict, because Python 3.6
    routing: Optional[RoutingConfig]


    _sort_interfaces = validator("interfaces", allow_reuse=True)(sort_interface_dict)


class HostMapping(BaseNetModel):

    hosts: Optional[List[GENERIC_OBJECT_NAME]] = []


class VLANHostMapping(VLANModel, HostMapping):

    pass


class GroupConfig(BaseNetModel):

    vlan_definitions: Optional[List[VLANHostMapping]] = []
    vrf_definitions: Optional[List[VRFModel]] = []

    @validator('vlan_definitions', allow_reuse=True)
    def sort_vlan_definitions(cls, value):
        return sorted(value, key=lambda x: x.vlan_id)


class Host(InventoryModel):

    name: GENERIC_OBJECT_NAME
    config: Optional[HostConfig]

class Group(InventoryModel):

    name: GENERIC_OBJECT_NAME
    config: Optional[GroupConfig]



class Link(InventoryModel):

    a_host: GENERIC_OBJECT_NAME
    z_host: GENERIC_OBJECT_NAME
    a_interface: InterfaceName
    z_interface: InterfaceName

class DescriptionLink(Link):

    a_description: Optional[str]
    z_description: Optional[str]

class PhysicalLink(Link):


    a_description: Optional[str]
    z_description: Optional[str]
    a_lag_group: Optional[conint(ge=1)]
    z_lag_group: Optional[conint(ge=1)]
    a_lag_mode: Optional[LAG_MODE]
    z_lag_mode: Optional[LAG_MODE]


class L3Link(Link):

    a_description: Optional[str]
    z_description: Optional[str]
    a_vrf: Optional[VRF_NAME]
    z_vrf: Optional[VRF_NAME]
    a_ipv4_address: Optional[ipaddress.IPv4Interface]
    z_ipv4_address: Optional[ipaddress.IPv4Interface]
    ipv4_network: Optional[ipaddress.IPv4Network]

    @root_validator(allow_reuse=True)
    def validate_both_ipv4_present(cls, values):
        required_together(values=values, required=['a_ipv4_address', 'z_ipv4_address'])

        return values

    @root_validator(allow_reuse=True)
    def validate_ipv4_addresses(cls, values):

        a_addr: ipaddress.IPv4Interface = values.get('a_ipv4_address')
        z_addr: ipaddress.IPv4Interface = values.get('z_ipv4_address')
        addr_list = [a_addr, z_addr]
        if all(addr_list):
            ipv4s_in_same_subnet(ips=addr_list)
            for addr in addr_list:
                ipv4_is_assignable(address=addr)
            validate_unique(values=addr_list)

        return values




class Inventory(InventoryModel):

    hosts: Dict[GENERIC_OBJECT_NAME, Host]
    groups: Dict[GENERIC_OBJECT_NAME, Group]

