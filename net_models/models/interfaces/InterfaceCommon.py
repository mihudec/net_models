
from pydantic.typing import Optional

from net_models.models import VendorIndependentBaseModel
from net_models.fields import GENERIC_OBJECT_NAME

class InterfaceServicePolicy(VendorIndependentBaseModel):

    input: Optional[GENERIC_OBJECT_NAME]
    output: Optional[GENERIC_OBJECT_NAME]