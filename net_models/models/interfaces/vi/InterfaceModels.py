import ipaddress
from net_models.models.BaseModels import VendorIndependentBaseModel
from net_models.models.interfaces.vi import InterfaceSwitchportModel
from net_models.models.interfaces.vi import InterfaceRouteportModel
from net_models.models.Fields import BASE_INTERFACE_NAME
from pydantic.typing import (List, Optional, Dict, Literal)
from pydantic import root_validator, validator, conint, constr
from net_models.validators import *


class InterfaceLagMemberConfig(VendorIndependentBaseModel):

    _modelname = "interface_lag_member_config"

    group: conint(ge=1)
    protocol: Literal["lacp", "pagp"]
    mode: Literal["active", "pasive", "desirable", "auto", "on"]


class InterfaceLldpConfig(VendorIndependentBaseModel):

    transmit: Optional[bool]
    receive: Optional[bool]


class InterfaceCdpConfig(VendorIndependentBaseModel):

    enabled: bool


class InterfaceDiscoveryProtocols(VendorIndependentBaseModel):

    cdp: Optional[InterfaceCdpConfig]
    lldp: Optional[InterfaceLldpConfig]


class InterfaceModel(VendorIndependentBaseModel):

    _modelname = "interface_model"
    _identifiers = ["name"]
    _children = {InterfaceSwitchportModel: "l2_port", InterfaceRouteportModel: "l3_port"}

    tags: List[constr(strip_whitespace=True, to_lower=True)] = []

    name: BASE_INTERFACE_NAME
    description: Optional[str]
    l2_port: Optional[InterfaceSwitchportModel]
    l3_port: Optional[InterfaceRouteportModel]
    lag_member: Optional[InterfaceLagMemberConfig]
    discovery_protocols: Optional[InterfaceDiscoveryProtocols]

    @root_validator(allow_reuse=True)
    def generate_tags(cls, values):
        tags = set(values.get("tags"))
        if values.get("l2_port"):
            tags.add("l2")
        if values.get("l3_port"):
            tags.add("l3")
        if values.get("lag_member"):
            tags.add("lag-member")

        # Interface types
        lower_name = values.get("name").lower()
        if "ethernet" in lower_name:
            tags.add("physical")
        elif any([x in lower_name for x in ["loopback", "vlan", "bdi", "tunnel", "pseudowire"]]):
            tags.add("virtual")
        values["tags"] = sorted(list(tags))
        return values

    _normalize_tags = validator('tags', allow_reuse=True)(remove_duplicates_and_sort)
    _normalize_interface_name = validator('name', allow_reuse=True, pre=True)(normalize_interface_name)


class InterfaceContainerModel(VendorIndependentBaseModel):

    interfaces: Dict[BASE_INTERFACE_NAME, InterfaceModel] # Actually collections.OrderedDict, because Python 3.6

    _sort_interfaces = validator("interfaces", allow_reuse=True)(sort_interface_dict)
