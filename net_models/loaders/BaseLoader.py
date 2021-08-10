# Standard Libraries
# Third party packages
from pydantic.typing import Union
# Local package
from net_models.fields import InterfaceName
from net_models.models import InterfaceModel
from net_models.inventory import (Inventory, Group, Host, GlobalConfig, HostConfig, GroupConfig)
from net_models.utils import get_logger
# Local module


class BaseLoader(object):

    def __init__(self):
        self.logger = get_logger(name="BaseLoader", verbosity=5)
        self.inventory = Inventory(hosts={}, groups={})

    def find_host(self, host_name) -> Union[Host, None]:

        host = None
        try:
            host = self.inventory.hosts.get(host_name)
        except KeyError:
            self.logger.debug(msg=f"Host {host_name} not found in inventory.")
        except Exception as e:
            msg = f"Unhandled Exception occured while searching host {host_name}. Exception: {repr(e)}"
            self.logger.error(msg=msg)
            raise

        return host

    def get_group(self, group_name: str, create_if_missing: bool = True) -> Union[Group, None]:
        group = self.inventory.groups.get(group_name, None)
        if group is None:
            if create_if_missing:
                self.logger.debug(f"Creating group '{group_name}'")
                group = Group(name=group_name, config=GroupConfig())
                self.inventory.groups[group.name] = group
            else:
                self.logger.debug(f"Group '{group_name}' not present in inventory")
        return group

    def get_host(self, host_name: str, create_if_missing: bool = True) -> Union[Host, None]:
        host = self.inventory.hosts.get(host_name, None)
        if host is None:
            if create_if_missing:
                self.logger.debug(f"Creating host '{host_name}'")
                host = Host(name=host_name)
                self.inventory.hosts[host.name] = host
            else:
                self.logger.debug(f"Host '{host_name}' not present in inventory")
        return host


    def get_interface(self, host_name: str, interface_name: InterfaceName, create_if_missing: bool = True) -> Union[InterfaceModel, None]:
        if not isinstance(interface_name, InterfaceName):
            interface_name = InterfaceName.validate_name(interface_name)
        # Host must already exist
        host = self.get_host(host_name=host_name, create_if_missing=False)
        interface = None
        if host is None:
            self.logger.error(f"Specified host {host_name} not present in inventory, cannot retreive interface {interface_name}")
            return None
        if host.config is None:
            if create_if_missing:
                self.logger.debug(f"Creating GlobalConfig for host {host.name}")
                host.config = HostConfig(interfaces={})
            else:
                self.logger.error(f"Host {host_name} does not have config, cannot retreive interface.")
                return None
        interface = host.config.interfaces.get(interface_name, None)
        if interface is None:
            if create_if_missing:
                self.logger.debug(f"Creating interface {interface_name} on host {host.name}")
                interface = InterfaceModel(name=interface_name)
                host.config.interfaces[interface.name] = interface
            else:
                self.logger.debug(f"Interface {interface_name} not present on host {host.name}")
        return interface





    def update_host(self, host_name: str, params: dict = None):
        host = self.find_host(host_name=host_name)
        if params is None:
            params = {}
        if host is None:
            self.logger.debug(msg=f"Creating host {host_name}")
            host = Host(name=host_name, **params)
            self.inventory.hosts.update({host_name: host})
        elif isinstance(host, Host):
            for k, v in params.items():
                if v is not None:
                    setattr(host, k, v)


    def update_host_interface(self, host_name: str, interface_name: InterfaceName, params: dict = None):
        host = None
        if params is None:
            params = {}
        if not isinstance(interface_name, InterfaceName):
            interface_name = InterfaceName.validate_name(interface_name)
        try:
            host = self.inventory.hosts.get(host_name)
            if host.config is None:
                self.logger.debug(f"Creating HostConfig for host '{host_name}'")
                host.config = HostConfig(interfaces={})
            if host.config.interfaces is None:
                self.logger.debug(f"Constructing Interfaces for host '{host_name}'")
                host.config.interfaces = {}
            if interface_name not in host.config.interfaces.keys():
                self.logger.debug(f"Creating interface {interface_name} on host {host_name}")
                interface = InterfaceModel(name=interface_name, **params)
                host.config.interfaces[interface_name] = interface
            else:
                self.logger.debug(f"Found existing interface {interface_name} on host {host_name}")
                for k, v in params.items():
                    if v is not None:
                        setattr(host.config.interfaces[interface_name], k, v)
        except Exception as e:
            msg = f"Unhandled Exception occured while getting host {host_name}. Exception: {repr(e)}"
            self.logger.error(msg=msg)
            raise




    def finish(self):
        self.inventory = self.inventory.clone()
        # model.inventory.check()
        print(self.inventory.yaml(exclude_none=True, indent=2))


