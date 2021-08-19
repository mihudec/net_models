
from pydantic import Extra
from pydantic.typing import Optional, Dict, List, Literal, Tuple
from net_models.exceptions import *
from net_models.fields import *
from net_models.models.BaseModels import BaseNetModel, VRFModel, VLANModel
from net_models.models.interfaces import *
from net_models.models.routing import *
from net_models.models.services import *



class RoutingConfig(BaseNetModel):

    bgp: Optional[RoutingBgpProcess]
    isis: Optional[List[RoutingIsisProcess]]
    ospf: Optional[List[RoutingOspfProcess]]
    static_ipv4: Optional[List[StaticRouteV4]]


class HostMapping(BaseNetModel):

    hosts: Optional[List[GENERIC_OBJECT_NAME]]


class VLANHostMapping(VLANModel, HostMapping):

    pass


class BaseConfig(BaseNetModel):

    class Config:
        extra = Extra.allow
        anystr_strip_whitespace = True
        validate_assignment = True

    vrfs: Optional[List[VRF_NAME]]
    vrf_definitions: Optional[List[VRFModel]]
    vlan_definitions: Optional[List[VLANModel]]
    routing: Optional[RoutingConfig]
    ntp: Optional[NtpConfig]
    snmp: Optional[SnmpConfig]
    logging: Optional[LoggingConfig]

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

    @validator('vrfs')
    def sort_vrfs(cls, value):
        if value is not None:
            remove_duplicates_and_sort(data=value)
        return value

class GroupConfig(BaseConfig):

    vlans: Optional[List[VLAN_ID]]
    vlan_definitions: Optional[List[VLANHostMapping]]
    @validator('vlans', allow_reuse=True)

    def sort_vlans(cls, value):
        if value is not None:
            return remove_duplicates_and_sort(data=value)
        else:
            return value

    @validator('vlan_definitions', allow_reuse=True)
    def sort_vlan_definitions(cls, value):
        if value is not None:
            return sorted(value, key=lambda x: x.vlan_id)
        else:
            return value

class HostConfig(BaseConfig):

    hostname: Optional[GENERIC_OBJECT_NAME]
    vlans: Optional[List[VLAN_ID]]
    interfaces: Optional[Dict[InterfaceName, InterfaceModel]] # Actually collections.OrderedDict, because Python 3.6

    _sort_interfaces = validator("interfaces", allow_reuse=True)(sort_interface_dict)

    @validator('vlans', allow_reuse=True)
    def sort_vlans(cls, value):
        if value is not None:
            return remove_duplicates_and_sort(data=value)
        else:
            return value



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
