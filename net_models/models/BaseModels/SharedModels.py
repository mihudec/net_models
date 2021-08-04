from pydantic import root_validator
from pydantic.typing import Union, Optional, List, Literal, List
from net_models.models import VendorIndependentBaseModel
from net_models.fields import GENERIC_OBJECT_NAME, VRF_NAME, VLAN_ID, ROUTE_TARGET, ROUTE_DISTINGUISHER, AFI, SAFI


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
    active: Optional[bool]




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

