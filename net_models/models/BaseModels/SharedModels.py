# Standard Libraries
# Third party packages
from pydantic import root_validator
from pydantic.typing import Union, Optional, List, Literal, List
# Local package
from net_models.fields import (
    GENERIC_OBJECT_NAME, VRF_NAME, VLAN_ID, BRIDGE_DOMAIN_ID,
    ROUTE_TARGET, ROUTE_DISTINGUISHER, AFI, SAFI
)
# Local module
from .BaseNetModels import VendorIndependentBaseModel


__all__ = ['KeyBase', 'KeyChain', 'AuthBase', 'VLANModel', 'RouteTarget', 'VRFAddressFamily', 'VRFModel']


class KeyBase(VendorIndependentBaseModel):

    value: str
    encryption_type: Optional[int]


class KeyChain(VendorIndependentBaseModel):

    name: GENERIC_OBJECT_NAME
    description: Optional[str]
    keys_list: List[KeyBase]


class AuthBase(VendorIndependentBaseModel):

    pass


class VLANModel(VendorIndependentBaseModel):

    _modelname = "vlan_model"

    vlan_id: VLAN_ID
    name: Optional[GENERIC_OBJECT_NAME]
    enabled: Optional[bool]


class BridgeDomainModel(VendorIndependentBaseModel):
    bridge_domain_id: BRIDGE_DOMAIN_ID
    enabled: Optional[bool]


class RouteTarget(VendorIndependentBaseModel):

    rt: ROUTE_TARGET
    action: Literal['export', 'import', 'both']
    rt_type: Optional[Literal['stitching']]


class VRFAddressFamily(VendorIndependentBaseModel):

    afi: AFI
    """Address family type"""
    safi: Optional[SAFI]
    """Address family sub-type"""
    route_targets: Optional[List[RouteTarget]]


class VRFModel(VendorIndependentBaseModel):

    name: VRF_NAME
    rd: Optional[ROUTE_DISTINGUISHER]
    address_families: Optional[List[VRFAddressFamily]]
    description: Optional[str]

