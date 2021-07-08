from pydantic.typing import Union, Optional, List
from net_models.models import VendorIndependentBaseModel
from net_models.fields import GENERIC_OBJECT_NAME


class KeyBase(VendorIndependentBaseModel):

    value: str
    encryption_type: Optional[int]


class KeyChain(VendorIndependentBaseModel):

    name: GENERIC_OBJECT_NAME
    description: Optional[str]
    keys_list: List[KeyBase]


class AuthBase(VendorIndependentBaseModel):

    pass


