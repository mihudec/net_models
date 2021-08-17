# Standard Libraries
import ipaddress
# Third party packages
from pydantic import Extra, root_validator, validator, conint
from pydantic.typing import Optional, List, Literal, Dict, Tuple
# Local package
from net_models.exceptions import *
from net_models.fields import InterfaceName, GENERIC_OBJECT_NAME, LAG_MODE, VRF_NAME
from net_models.validators import sort_interface_dict, required_together, ipv4s_in_same_subnet, ipv4_is_assignable, validate_unique, remove_duplicates_and_sort
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

    hostname: Optional[GENERIC_OBJECT_NAME]
    interfaces: Optional[Dict[InterfaceName, InterfaceModel]] # Actually collections.OrderedDict, because Python 3.6
    routing: Optional[RoutingConfig]
    vrf_names: Optional[List[VRF_NAME]]

    _sort_interfaces = validator("interfaces", allow_reuse=True)(sort_interface_dict)


    def get_interface(self, interface_name: str, interface_params: dict = None, create_if_missing: bool = False):
        interface = None
        if self.interfaces is None:
            if create_if_missing:
                self.interfaces = {}
            else:
                return None
        interface = self.interfaces.get(interface_name)
        if interface is None:
            if create_if_missing:
                if interface_params is not None:
                    if interface_params.get("name"):
                        interface_name = interface_params.pop("name")
                    interface = InterfaceModel(name=interface_name, **interface_params)
                else:
                    interface = InterfaceModel(name=interface_name)
                self.interfaces[interface.name] = interface

        return interface

    @validator('vrf_names')
    def sort_vrf_names(cls, value):
        if value is not None:
            remove_duplicates_and_sort(data=value)
        return value


    def add_vrf_name(self, vrf_name):
        if self.vrf_names is None:
            self.vrf_names = []
        if vrf_name not in self.vrf_names:
            self.vrf_names.append(vrf_name)


    def _get_interface(self, interface_name: str):
        interface_name = normalize_interface_name(interface_name=interface_name)
        if self.interfaces is None:
            return None
        if interface_name not in self.interfaces.keys():
            return None
        if interface_name in self.interfaces.keys():
            return self.interfaces[interface_name]


    def _create_interface(self, interface: InterfaceModel, force_create: bool = False) -> bool:
        if not isinstance(interface, InterfaceModel):
            interface = InterfaceModel.parse_obj(interface)
        current_interface = self.get_interface(interface_name=interface.name)
        if current_interface is None:
            if self.interfaces is None:
                self.interfaces = {}
            self.interfaces[interface.name] = interface
        else:
            if force_create:
                self.interfaces[interface.name] = interface
            else:
                raise InterfaceAlreadyExists(f"Interface {interface.name} already exist.")

    def _get_or_create_interface(self,
                                 interface_name: str = None,
                                 interface: Union[InterfaceModel, dict] = None) -> Tuple[InterfaceModel, bool]:
        """

        Args:
            interface_name: Name of the interface
            interface: Model or dict representation of the interface

        Returns: Tuple of InterfaceModel, bool - True if interface has been just created, False if it was fetched

        """
        if interface is None:
            if interface_name is not None:
                interface = InterfaceModel(name=interface_name)
            else:
                raise ValueError("Need either 'interface_name' or 'interface' (or both). Got none of those.")
        else:
            if isinstance(interface, dict):
                if 'name' in interface.keys():
                    interface = InterfaceModel.parse_obj(interface)
                else:
                    if interface_name is not None:
                        interface['name'] = interface_name
                        interface = InterfaceModel.parse_obj(interface)
                    else:
                        raise ValueError("Need either 'interface_name' or 'interface' (or both). Got none of those.")
            elif isinstance(interface, InterfaceModel):
                # All good here
                pass
            else:
                raise ValueError(f"Param interface has to be Union[InterfaceModel, dict]. Got {type(interface)}")

        if not isinstance(interface, InterfaceModel):
            raise AssertionError("Ath this point, interface should me a model. Something went wrong.")

        candidate = self._get_interface(interface_name=interface.name)
        if candidate is None:
            self._create_interface(interface=interface)
            return interface, True
        else:
            return candidate, False

    def _update_interface(self, interface_params: Union[InterfaceModel, dict]):
        raise NotImplementedError

    def _delete_interface(self, interface_name: str):
        raise NotImplementedError



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

    class Config:
        extra = Extra.allow
        anystr_strip_whitespace = True
        validate_assignment = True

    name: GENERIC_OBJECT_NAME
    config: Optional[HostConfig]

    def _get_or_create_config(self):
        if self.config is None:
            self.config = HostConfig()
        return self.config

    def get_or_create_interface(self, interface_name: str = None, interface: Union[InterfaceModel, dict] = None):
        config = self._get_or_create_config()
        return config._get_or_create_interface(interface_name=interface_name, interface=interface)




class Group(InventoryModel):

    class Config:
        extra = Extra.allow
        anystr_strip_whitespace = True
        validate_assignment = True

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

    def structure(self):
        structure = {}
        if self.hosts is not None:
            structure['hosts'] = {k: None for k in self.hosts.keys()}
        if self.children is not None:
            structure['children'] = {}
            for name, group in self.children.items():
                structure['children'].update({name: group.structure()})
        return structure

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

    def structure(self):
        structure = {}
        if self.groups is not None:
            for group_name, group in self.groups.items():
                structure.update({group_name: group.structure()})
        return structure



