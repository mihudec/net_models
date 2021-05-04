from pydantic.class_validators import validator
from netcm.models.BaseModels import BaseNetCmModel
from netcm.fields import *
from netcm.validators import*

import ipaddress
from typing import (
    Literal,
    List,
    Optional
)

from pydantic import (
    root_validator,
    conint,
    constr
)





class InterfaceSpanningTreeConfig(BaseNetCmModel):
    
    _modelname = "spanning_tree_port_config"
    _identifiers = []

    portfast: Optional[bool]


class SwitchportAbstractModel(BaseNetCmModel):

    _modelname = "switchport_abstract_model"
    _identifiers = []
    _children = {InterfaceSpanningTreeConfig: "stp"}

    mode: Optional[Literal["access", "trunk", "negotiate"]]
    untagged_vlan: Optional[vlan_id]
    tagged_vlans: Optional[List[vlan_id]]
    encapsulation: Optional[Literal["dot1q", "isl"]]
    negotiation: Optional[bool]
    stp: Optional[InterfaceSpanningTreeConfig]

    @root_validator
    def validate_tagged_vlans_present(cls, values):
        if values.get("tagged_vlans"):
            assert values.get("mode") in ["trunk"], "Field 'tagged_vlans' is only allowed when 'mode' in ['trunk']."
        return values

    @root_validator
    def validate_vlans_disjoint(cls, values):
        if values.get("tagged_vlans") and values.get("untagged_vlan"):
            assert values.get("untagged_vlan") not in values.get("tagged_vlans"), f"Vlan {values.get('untagged_vlan')} cannot be both tagged and untagged."
        elif values.get("tagged_vlans") and not values.get("untagged_vlan"):
            assert 1 not in values.get("tagged_vlans"), "Vlan 1 cannot be tagged if untagged_vlan is None."
        return values


class InterfaceIPv4Address(BaseNetCmModel):

    _modelname = "interface_ipv4_address_model"

    address: ipaddress.IPv4Interface
    secondary: Optional[bool]

    _validate_address = validator("address", allow_reuse=True)(ipv4_is_assignable)


class InterfaceIPv6Address(BaseNetCmModel):

    _modelname = "interface_ipv6_address_model"

    address: ipaddress.IPv6Interface


class InterfaceIPv4Container(BaseNetCmModel):

    _modelname = "interface_ipv4_container"

    addresses: Optional[List[InterfaceIPv4Address]]

    @root_validator
    def validate_non_overlapping(cls, values):
        #TODO: Add
        return values


class InterfaceIPv6Container(BaseNetCmModel):

    _modelname = "interface_ipv6_container"

    addresses: Optional[List[InterfaceIPv6Address]]


class RouteportAbstractModel(BaseNetCmModel):

    _modelname = "routeport_abstract_model"
    _identifiers = []

    ipv4: Optional[InterfaceIPv4Container]
    ipv6: Optional[InterfaceIPv6Container]


class InterfaceAbstractModel(BaseNetCmModel):

    _modelname = "interface_abstract_model"
    _identifiers = ["name"]
    _children = {SwitchportAbstractModel, "l2_port"}

    name: interface_name
    description: Optional[str]
    l2_port: Optional[SwitchportAbstractModel]
    l3_port: Optional[RouteportAbstractModel]
