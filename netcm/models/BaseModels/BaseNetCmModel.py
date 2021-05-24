# from diffsync import DiffSyncModel
import yaml
from pydantic import BaseModel, validate_model
from netcm.utils.CustomYamlDumper import CustomYamlDumper


class BaseNetCmModel(BaseModel):
    """Base Network Config Model Class"""

    def check(self):
        *_, validation_error = validate_model(self.__class__, self.__dict__)
        if validation_error:
            raise validation_error

    def yaml(self, indent: int = 2, **kwargs):
        data_dict = self.dict(**kwargs)
        return yaml.dump(data=data_dict, Dumper=CustomYamlDumper, indent=indent)


class VendorIndependentBaseModel(BaseNetCmModel):
    """Vendor Independent Base Model Class"""

    pass