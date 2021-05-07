# from diffsync import DiffSyncModel
from pydantic import BaseModel, validate_model


class BaseNetCmModel(BaseModel):
    """Base Network Config Model Class

    """
    def check(self):
        *_, validation_error = validate_model(self.__class__, self.__dict__)
        if validation_error:
            raise validation_error

class VendorIndependentBaseModel(BaseNetCmModel):
    """Vendor Independent Base Model Class

    """