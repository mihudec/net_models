from pydantic import validator, root_validator, Field
from net_models.models.BaseModels import VendorIndependentBaseModel
from net_models.models.Fields import *
from net_models.validators import *
from pydantic.typing import Literal, List, Union, Optional



class InterfaceSpanningTreeConfig(VendorIndependentBaseModel):
    
    _modelname = "spanning_tree_port_config"
    _identifiers = []

    link_type: Optional[Literal["point-to-point", "shared"]]
    portfast: Optional[Literal["edge", "network", "disable", "trunk"]]
    bpduguard: Optional[bool]
    root_guard: Optional[bool]
    loop_guard: Optional[bool]


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
    """
    List of allowed VLANs on this interface.
    Preferably `List[int]`, however validators will take care of things like `"1-10,20"` or `[1, 2, 3, "5-10"]`
    """
    encapsulation: Optional[Literal["dot1q", "isl", "negotiate"]]

    negotiation: Optional[bool]
    """
    Wether or not negotiate trunking, for example via DTP. 
    Setting this field to `False` will result in :code:`switchport nonegotiate`
    """
    stp: Optional[InterfaceSpanningTreeConfig]

    @root_validator(allow_reuse=True)
    def validate_allowed_vlans_present(cls, values):
        if values.get("allowed_vlans"):
            assert values.get("mode") in ["trunk"], "Field 'allowed_vlans' is only allowed when 'mode' in ['trunk']."
        return values

    _vlan_range_validator = validator('allowed_vlans', allow_reuse=True)(expand_vlan_range)

