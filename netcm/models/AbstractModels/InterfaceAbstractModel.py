from netcm.models.BaseModels import BaseNetCmModel

class InterfaceAbstractModel(BaseNetCmModel):

    _modelname = "interface_abstract_model"
    _identifiers = ["name"]

    name: str
    