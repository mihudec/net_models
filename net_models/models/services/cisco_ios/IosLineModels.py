from net_models.models import BaseNetModel
from net_models.models.services.vi.AaaMethods import IosLineAaaConfig
from pydantic.types import conlist, conint
from pydantic.typing import Optional, Literal



class IosLineConfig(BaseNetModel):

    line_type: Literal['aux', 'console', 'vty']
    line_range: conlist(item_type=conint(ge=0), min_items=1, max_items=2)
    aaa_config: Optional[IosLineAaaConfig]
    """AAA Configuration Object"""
    exec_timeout: Optional[conint(ge=0)]
    """EXEC Timeout in seconds"""
