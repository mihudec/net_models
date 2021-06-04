from net_models.models.BaseModels import VendorIndependentBaseModel
from net_models.models.BaseModels.SharedModels import AuthBase
from net_models.models.Fields import GENERIC_OBJECT_NAME
from net_models.utils.get_logger import get_logger
from pydantic.typing import Optional, List, Union, Literal
from pydantic import root_validator
import ipaddress

LOGGER = get_logger(name="NetCm-RoutingProtocols")

def validate_asn_is_defined(values):
    return values

class BfdAuthentication(AuthBase):

    method: Literal["md5","meticulous-md5","meticulous-sha-1","sha-1"]
    keychain: GENERIC_OBJECT_NAME

class BfdTemplate(VendorIndependentBaseModel):

    # TODO: Unfinished
    name: GENERIC_OBJECT_NAME
    type: Literal["single-hop", "multi-hop"]
    min_rx: Optional[int]
    min_tx: Optional[int]
    both: Optional[int]
    microseconds: Optional[bool]
    multiplier: int
    authentication: Optional[BfdAuthentication]

    @root_validator
    def validate_timers(cls, values):
        if values.get("min_tx") is not None and values.get("min_rx") is not None:
            if values.get("both") is not None:
                msg = "If 'min-tx and 'min-rx' are specified, 'both' must be None"
                LOGGER.error(msg=msg)
                raise AssertionError(msg)
        return values

class RoutingProtocolBase(VendorIndependentBaseModel):

    pass

class RoutingProtocolIgpBase(RoutingProtocolBase):

    passive_interfaces: List[str]

class RoutingOspfProcess(RoutingProtocolBase):

    process_id: GENERIC_OBJECT_NAME

class RoutingIsisNetwork(VendorIndependentBaseModel):

    area_id: str
    system_id: str
    nsel: str

class AuthenticationIsisMode(VendorIndependentBaseModel):

    level: str
    auth_mode: str

class AuthenticationIsisKeychain(VendorIndependentBaseModel):

    level: str
    keychain: GENERIC_OBJECT_NAME

class AuthenticationIsis(VendorIndependentBaseModel):

    mode: List[AuthenticationIsisMode]
    keychain: List[AuthenticationIsisKeychain]

class RoutingIsisProcess(RoutingProtocolBase):

    process_id: GENERIC_OBJECT_NAME
    it_type: str
    metric_style: str
    fast_flood: Optional[int]
    max_lsp_lifetime: Optional[int]
    network: RoutingIsisNetwork
    authentication: AuthenticationIsis

