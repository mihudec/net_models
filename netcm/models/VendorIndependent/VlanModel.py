from pydantic import validator, root_validator
from netcm.models.BaseModels import VendorIndependentBaseModel
from netcm.models.Fields import *
from netcm.validators import *
from typing import (List, Optional)
from typing_extensions import (Literal)


class VlanModel(VendorIndependentBaseModel):

    _modelname = "vlan_model"

    vlan_id: VLAN_ID
    name: str