from net_models.models.BaseModels import VendorIndependentBaseModel
from pydantic.typing import Union, Optional
import ipaddress


class KeyBase(VendorIndependentBaseModel):

    value: str
    encryption_type: Optional[int]


class AuthBase(VendorIndependentBaseModel):

    pass