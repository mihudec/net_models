from pydantic import validator, root_validator
from netcm.models.BaseModels import VendorIndependentBaseModel
from netcm.models.Fields import *
from netcm.validators import *
from pydantic.typing import Literal, List, Union, Optional



class InterfaceSpanningTreeConfig(VendorIndependentBaseModel):
    
    _modelname = "spanning_tree_port_config"
    _identifiers = []

    link_type: Optional[Literal["point-to-point", "shared"]]
    portfast: Optional[Literal["edge", "network", "disable", "trunk"]]
    bpduguard: Optional[Literal["enable", "disable"]]
    guard: Optional[Literal["loop", "root", "none"]]


class InterfaceSwitchportModel(VendorIndependentBaseModel):
    """
    Model for switched interfaces
    """

    _modelname = "switchport_model"
    _identifiers = []
    _children = {InterfaceSpanningTreeConfig: "stp"}

    mode: Optional[Literal["access", "trunk", "dynamic auto", "dynamic desirable", "dot1q-tunnel", "private-vlan host", "private-vlan promiscuous"]]
    """Operational mode"""

    untagged_vlan: Optional[VLAN_ID]
    """ID of untagged VLAN. Used for Access or Native VLAN"""

    allowed_vlans: Optional[Union[List[VLAN_ID], Literal["all", "none"]]]
    encapsulation: Optional[Literal["dot1q", "isl", "negotiate"]]
    negotiation: Optional[bool]
    stp: Optional[InterfaceSpanningTreeConfig]

    @root_validator(allow_reuse=True)
    def validate_allowed_vlans_present(cls, values):
        if values.get("allowed_vlans"):
            assert values.get("mode") in ["trunk"], "Field 'allowed_vlans' is only allowed when 'mode' in ['trunk']."
        return values

    _remove_duplicates_from_allowed_vlans = validator('allowed_vlans', allow_reuse=True)(expand_vlan_range)

