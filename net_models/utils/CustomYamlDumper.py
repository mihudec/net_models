# Preparation for migration to ruamel.yaml
# from ruamel.yaml import YAML
# from ruamel.yaml.representer import Representer
# from ruamel.yaml.dumper import Dumper
# from ruamel.yaml.emitter import Emitter
# from ruamel.yaml.serializer import Serializer
# from ruamel.yaml.resolver import Resolver



import yaml
from yaml.representer import Representer
from yaml.dumper import Dumper
from yaml.emitter import Emitter
from yaml.serializer import Serializer
from yaml.resolver import Resolver
from collections import OrderedDict

# yaml = YAML()

def represent_ordereddict(dumper, data):
    value = []

    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)

        value.append((node_key, node_value))

    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)


class CustomYamlRepresenter(Representer):

    def represent_none(self, data):
        return self.represent_scalar(u'tag:yaml.org,2002:null', u'')

    def represent_dict(self, data):
        data_keys = list(data.keys())
        if "name" in data_keys:
            data_keys.insert(0, data_keys.pop(data_keys.index("name")))
        if "tags" in data_keys:
            data_keys.insert(1, data_keys.pop(data_keys.index("tags")))
        if "hosts" in data_keys:
            data_keys.append(data_keys.pop(data_keys.index("hosts")))
        values = [(self.represent_data(key), self.represent_data(data[key])) for key in data_keys]
        return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', values)


class CustomYamlDumper(Emitter, Serializer, CustomYamlRepresenter, Resolver):
    def __init__(self, stream,
                 default_style=None, default_flow_style=None,
                 canonical=None, indent=None, width=None,
                 allow_unicode=None, line_break=None,
                 encoding=None, explicit_start=None, explicit_end=None, sort_keys=False,
                 version=None, tags=None):
        Emitter.__init__(self, stream, canonical=canonical,
                         indent=indent, width=width,
                         allow_unicode=allow_unicode, line_break=line_break)
        Serializer.__init__(self, encoding=encoding,
                            explicit_start=explicit_start, explicit_end=explicit_end,
                            version=version, tags=tags)
        CustomYamlRepresenter.__init__(self, default_style=default_style,
                                       default_flow_style=default_flow_style)
        Resolver.__init__(self)

        CustomYamlRepresenter.add_representer(type(None), CustomYamlRepresenter.represent_none)
        CustomYamlRepresenter.add_representer(OrderedDict, represent_ordereddict)
        CustomYamlRepresenter.add_representer(dict, CustomYamlRepresenter.represent_dict)


    def increase_indent(self, flow=False, indentless=False):
        return super(CustomYamlDumper, self).increase_indent(flow=flow, indentless=False)