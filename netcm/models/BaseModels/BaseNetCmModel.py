# from diffsync import DiffSyncModel
import yaml
import json
from pydantic import BaseModel, validate_model, Extra
from netcm.utils.CustomYamlDumper import CustomYamlDumper


class BaseNetCmModel(BaseModel):
    """Base Network Config Model Class"""

    class Config:
        extra = Extra.forbid

    def check(self):
        *_, validation_error = validate_model(self.__class__, self.__dict__)
        if validation_error:
            raise validation_error

    def yaml(self, indent: int = 2, **kwargs):
        data_dict = self.dict(**kwargs)
        return yaml.dump(data=data_dict, Dumper=CustomYamlDumper, indent=indent)

    def serial_dict(self, **kwargs):
        return json.loads(self.json(**kwargs))


class VendorIndependentBaseModel(BaseNetCmModel):
    """Vendor Independent Base Model Class"""

    pass