from pydantic import validator, root_validator
from netcm.models.BaseModels import VendorIndependentBaseModel
from netcm.fields import *
from netcm.validators import *
from typing import (List, Optional)
from typing_extensions import (Literal)

class InterfaceSpanningTreeConfig(VendorIndependentBaseModel):
    
    _modelname = "spanning_tree_port_config"
    _identifiers = []

    portfast: Optional[bool]


class InterfaceSwitchportModel(VendorIndependentBaseModel):

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

