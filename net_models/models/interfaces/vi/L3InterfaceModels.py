from pydantic import validator, root_validator
from net_models.models.BaseModels import VendorIndependentBaseModel
from net_models.models.BaseModels.SharedModels import AuthBase
from net_models.models.Fields import *
from net_models.validators import *
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


class InterfaceDhcpClientConfig(VendorIndependentBaseModel):

    _model_name = "interface_dhcp_client"

    enabled: Optional[bool]


class InterfaceIPv4Container(VendorIndependentBaseModel):

    _modelname = "interface_ipv4_container"

    addresses: Optional[List[InterfaceIPv4Address]]
    unnumbered: Optional[INTERFACE_NAME]
    dhcp_client: Optional[InterfaceDhcpClientConfig]

    @root_validator(allow_reuse=True)
    def validate_non_overlapping(cls, values):
        addresses = values.get("addresses")
        if addresses is None:
            return values
        for address in addresses:
            other_addresses = list(addresses)
            other_addresses.remove(address)
            for other_address in other_addresses:
                if address.address in other_address.address.network:
                    raise AssertionError(f"Address {str(other_address.address)} overlaps with {str(address.address)}")
        return values

    @root_validator(allow_reuse=True)
    def validate_single_primary(cls, values):
        addresses = values.get("addresses")
        if addresses is None:
            return values
        if len(addresses) == 1:
            return values
        # Get addresses with secondary==False or secondary==None
        primary_addresses = [x for x in addresses if x.secondary in [False, None]]
        if len(primary_addresses) > 1:
            raise AssertionError(f"Multiple 'primary addresses' found, only one allowed. {[x.dict() for x in addresses]}")
        return values


class InterfaceIPv6Container(VendorIndependentBaseModel):

    _modelname = "interface_ipv6_container"

    addresses: Optional[List[InterfaceIPv6Address]]


class InterfaceOspfConfig(VendorIndependentBaseModel):

    _modelname = "interface_ospf_config"

    network_type: Optional[str]
    cost: Optional[int]
    priority: Optional[int]
    process_id: Optional[int]
    area: Optional[int]

    @root_validator(allow_reuse=True)
    def validate_process_and_area(cls, values):
        if values.get("process_id") and not values.get("area"):
            raise AssertionError("When 'process_id' is set, 'area' is required.")
        elif not values.get("process_id") and values.get("area"):
            raise AssertionError("When 'area' is set, 'process_id' is required.")
        return values


class InterfaceBfdConfig(VendorIndependentBaseModel):

    template: GENERIC_OBJECT_NAME


class IsisMetricField(VendorIndependentBaseModel):

    _modelname = "isis_metric_field"

    level: Literal["level-1", "level-2"]
    metric: int


class IsisInterfaceAuthentication(AuthBase):

    mode: Optional[str]
    keychain: Optional[str]

class InterfaceIsisConfig(VendorIndependentBaseModel):

    _modelname = "interface_isis_config"

    network_type: Optional[str]
    circuit_type: Optional[str]
    process_id: Optional[int]
    authentication: Optional[IsisInterfaceAuthentication]
    metric: Optional[List[IsisMetricField]]


class InterfaceRouteportModel(VendorIndependentBaseModel):

    _modelname = "routeport_model"
    _identifiers = []

    ipv4: Optional[InterfaceIPv4Container]
    ipv6: Optional[InterfaceIPv6Container]
    vrf: Optional[str]
    ospf: Optional[InterfaceOspfConfig]
    isis: Optional[InterfaceIsisConfig]
    bfd: Optional[InterfaceBfdConfig]
