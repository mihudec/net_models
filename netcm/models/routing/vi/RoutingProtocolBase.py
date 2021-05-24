from netcm.models.BaseModels import VendorIndependentBaseModel
from netcm.models.Fields import GENERIC_OBJECT_NAME
from pydantic.typing import Optional

class RoutingProtocolBase(VendorIndependentBaseModel):

    router_id: Optional[GENERIC_OBJECT_NAME]