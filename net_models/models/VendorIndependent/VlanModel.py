from pydantic import validator, root_validator
from net_models.models.BaseModels import VendorIndependentBaseModel
from net_models.models.Fields import *
from net_models.validators import *
from typing import (List, Optional)
from typing_extensions import (Literal)


class VlanModel(VendorIndependentBaseModel):

    _modelname = "vlan_model"

    vlan_id: VLAN_ID
    name: str