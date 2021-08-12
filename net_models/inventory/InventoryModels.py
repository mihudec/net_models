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

    vlan_definitions: Optional[List[VLANHostMapping]]
    vrf_definitions: Optional[List[VRFModel]]

    @validator('vlan_definitions', allow_reuse=True)
    def sort_vlan_definitions(cls, value):
        if value is not None:
            return sorted(value, key=lambda x: x.vlan_id)
        else:
            return value

    @validator('vrf_definitions', allow_reuse=True)
    def sort_vrf_definitions(cls, value):
        if value is not None:
            return sorted(value, key=lambda x: x.name)
        else:
            return value


class Host(InventoryModel):

    name: GENERIC_OBJECT_NAME
    config: Optional[HostConfig]


class Group(InventoryModel):

    name: Optional[GENERIC_OBJECT_NAME]
    config: Optional[GroupConfig]
    children: Optional[Dict[GENERIC_OBJECT_NAME, 'Group']]
    hosts: Optional[Dict[GENERIC_OBJECT_NAME, Union[dict, None]]]

    def add_child(self, group_name: GENERIC_OBJECT_NAME, group: 'Group' = None):
        result = None
        if self.children is None:
            self.children = {}
        if group_name in self.children.keys():
            result = False
        else:
            self.children[group_name] = group if group is not None else Group()
            result = True
        return result

    def add_host(self, host_name: GENERIC_OBJECT_NAME):
        result = None
        if self.hosts is None:
            self.hosts = {}
        if host_name in self.hosts.keys():
            result = False
        else:
            self.hosts[host_name] = None
            result = True
        return result

    def get_flat_children(self) -> Dict[GENERIC_OBJECT_NAME, 'Group']:
        group_dict = {}
        if self.children is not None:
            for name, group in self.children.items():
                group_dict.update(group.get_flat_children())
                group_clone = group.clone()
                group_clone.children = None
                if name not in group_dict.keys():
                    group_dict[name] = group_clone
        return group_dict


Group.update_forward_refs()

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

