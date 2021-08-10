import inspect
from net_models.models.BaseModels import *
from net_models.models.services import *
from net_models.models.interfaces import *
from net_models.models.routing import *


models_map = {k:v for k, v in dict(globals()).items() if inspect.isclass(v) and issubclass(v, BaseNetModel)}

if __name__ == '__main__':
    for k,v in models_map.items():
        print(k, v)