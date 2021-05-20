import ipaddress
from netcm.models.BaseModels import VendorIndependentBaseModel
from netcm.models.VendorIndependent.L2InterfaceModels import *
from netcm.models.VendorIndependent.L3InterfaceModels import *
from pydantic.typing import (List, Optional, Dict, Literal)
from pydantic import root_validator, validator, conint, constr
from netcm.validators import *


class InterfaceLagMemberConfig(VendorIndependentBaseModel):

    _modelname = "interface_lag_member_config"

    group: int
    protocol: str
    mode: str


class InterfaceModel(VendorIndependentBaseModel):

    _modelname = "interface_model"
    _identifiers = ["name"]
    _children = {InterfaceSwitchportModel: "l2_port", InterfaceRouteportModel: "l3_port"}

    tags: List[str] = []

    name: interface_name
    description: Optional[str]
    l2_port: Optional[InterfaceSwitchportModel]
    l3_port: Optional[InterfaceRouteportModel]
    lag_member: Optional[InterfaceLagMemberConfig]

    @root_validator(allow_reuse=True)
    def generate_tags(cls, values):
        if values.get("l2_port"):
            if "l2" not in values["tags"]:
                values["tags"].append("l2")
        if values.get("l3_port"):
            if "l3" not in values["tags"]:
                values["tags"].append("l3")
        if values.get("lag_member"):
            if "lag_member" not in values["tags"]:
                values["tags"].append("lag_member")
        return values


class InterfaceContainerModel(VendorIndependentBaseModel):

    interfaces: Dict[GENERIC_INTERFACE_NAME, InterfaceModel] # Actually collections.OrderedDict, because Python 3.6

    _sort_interfaces = validator("interfaces", allow_reuse=True)(sort_interface_dict)
