from pydantic import validator, root_validator
from netcm.models.BaseModels import VendorIndependentBaseModel
from netcm.fields import *
from netcm.validators import *
from typing import (List, Optional)
from typing_extensions import (Literal)

class InterfaceIPv4Address(VendorIndependentBaseModel):

    _modelname = "interface_ipv4_address_model"

    address: ipaddress.IPv4Interface
    secondary: Optional[bool]

    _validate_address = validator("address", allow_reuse=True)(ipv4_is_assignable)


class InterfaceIPv6Address(VendorIndependentBaseModel):

    _modelname = "interface_ipv6_address_model"

    address: ipaddress.IPv6Interface


class InterfaceIPv4Container(VendorIndependentBaseModel):

    _modelname = "interface_ipv4_container"

    addresses: Optional[List[InterfaceIPv4Address]]

    @root_validator
    def validate_non_overlapping(cls, values):
        #TODO: Add
        return values


class InterfaceIPv6Container(VendorIndependentBaseModel):

    _modelname = "interface_ipv6_container"

    addresses: Optional[List[InterfaceIPv6Address]]


class InterfaceRouteportModel(VendorIndependentBaseModel):

    _modelname = "routeport_abstract_model"
    _identifiers = []

    ipv4: Optional[InterfaceIPv4Container]
    ipv6: Optional[InterfaceIPv6Container]
