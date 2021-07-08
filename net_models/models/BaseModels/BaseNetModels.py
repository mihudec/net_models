# from diffsync import DiffSyncModel
import yaml
import json
from pydantic import BaseModel, validate_model, Extra
from net_models.utils.CustomYamlDumper import CustomYamlDumper
from net_models.fields import GENERIC_OBJECT_NAME

class BaseNetModel(BaseModel):
    """Base Network Config Model Class"""

    class Config:
        extra = Extra.forbid
        anystr_strip_whitespace = True

    def check(self):
        *_, validation_error = validate_model(self.__class__, self.__dict__)
        if validation_error:
            raise validation_error

    def yaml(self, indent: int = 2, exclude_none: bool = False, **kwargs):
        data_dict = self.dict(exclude_none=exclude_none, **kwargs)
        return yaml.dump(data=data_dict, Dumper=CustomYamlDumper, indent=indent)

    def serial_dict(self, exclude_none: bool = False, **kwargs):
        return json.loads(self.json(exclude_none=exclude_none, **kwargs))


class VendorIndependentBaseModel(BaseNetModel):
    """Vendor Independent Base Model Class"""

    pass

class NamedModel(BaseNetModel):

    name: GENERIC_OBJECT_NAME