# from diffsync import DiffSyncModel
import yaml
import json
from pydantic import BaseModel, validate_model, Extra
from net_models.utils.CustomYamlDumper import CustomYamlDumper


class BaseNetCmModel(BaseModel):
    """Base Network Config Model Class"""

    class Config:
        extra = Extra.forbid

    def check(self):
        *_, validation_error = validate_model(self.__class__, self.__dict__)
        if validation_error:
            raise validation_error

    def yaml(self, indent: int = 2, exclude_none: bool = False, **kwargs):
        data_dict = self.dict(exclude_none=exclude_none, **kwargs)
        return yaml.dump(data=data_dict, Dumper=CustomYamlDumper, indent=indent)

    def serial_dict(self, exclude_none: bool = False, **kwargs):
        return json.loads(self.json(exclude_none=exclude_none, **kwargs))


class VendorIndependentBaseModel(BaseNetCmModel):
    """Vendor Independent Base Model Class"""

    pass