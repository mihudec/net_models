from net_models.models.BaseModels import BaseNetCmModel, VendorIndependentBaseModel

from net_models.models.services.vi.ServerModels import (
    RadiusServer,
    RadiusServerGroup,
    TacacsServer,
    TacacsServerGroup
)


models_map = {
    "RadiusServer": RadiusServer,
    "RadiusServerGroup": RadiusServerGroup,
    "TacacsServer": TacacsServer,
    "TacacsServerGroup": TacacsServerGroup
}