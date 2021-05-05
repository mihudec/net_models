from pydantic.class_validators import validator
from netcm.models.BaseModels import VendorIndependentBaseModel
from netcm.models.VendorIndependent.L2InterfaceModels import *
from netcm.models.VendorIndependent.L3InterfaceModels import *
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


class InterfaceModel(VendorIndependentBaseModel):

    _modelname = "interface_abstract_model"
    _identifiers = ["name"]
    _children = {InterfaceSwitchportModel: "l2_port", InterfaceRouteportModel: "l3_port"}

    name: interface_name
    description: Optional[str]
    l2_port: Optional[InterfaceSwitchportModel]
    l3_port: Optional[InterfaceRouteportModel]
