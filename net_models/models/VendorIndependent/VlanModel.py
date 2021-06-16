from net_models.fields.Fields import VLAN_ID
from net_models.models import VendorIndependentBaseModel


class VlanModel(VendorIndependentBaseModel):

    _modelname = "vlan_model"

    vlan_id: VLAN_ID
    name: str