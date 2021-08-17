import datetime
import pathlib
import yaml
import shutil

from pydantic.typing import List

from net_models.utils import get_logger
from net_models.utils.CustomYamlDumper import CustomYamlDumper
from net_models.inventory import Inventory

class BaseInventoryDumper(object):

    def __init__(self, inventory: Inventory, verbosity: int = 4):
        self.logger = get_logger(name='InventoryDumper', verbosity=verbosity)
        self.inventory = inventory


class AnsibleInventoryDumper(BaseInventoryDumper):

    def __init__(self, inventory: Inventory, directory: pathlib.Path):
        super().__init__(inventory=inventory)
        self.directory = pathlib.Path(directory).resolve()
        self.indent = 2

    def backup_inventory(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print(timestamp)
        backup_directory = self.directory.parent.joinpath(f"backup_{timestamp}_{self.directory.name}")
        self.logger.info(msg="Creating backup of inventory.")
        shutil.copytree(self.directory, backup_directory)

    def remove_all_backups(self):
        backup_directories = [x for x in self.directory.parent.iterdir() if x.is_dir() and x.name.startswith('backup_')]
        for backup_directory in backup_directories:
            self.logger.info(f"Deleting backup of inventory: {backup_directory}")
            shutil.rmtree(backup_directory)

    def dump_inventory(self, path: pathlib.Path = None,
                       separate_host_sections: bool = False,
                       common_host_sections: List[str] = ['name']):
        if path is None:
            path = self.directory
        else:
            path = pathlib.Path(path).resolve()
            path.mkdir(exist_ok=True, parents=True)
        hosts_file = path.joinpath('hosts.yml')
        host_vars = path.joinpath('host_vars')
        group_vars = path.joinpath('group_vars')

        [x.mkdir(exist_ok=True) for x in [host_vars, group_vars]]

        inventory_dict = self.inventory.serial_dict(exclude_none=True)
        # Dump Structure
        with hosts_file.open(mode='w') as f:
            yaml.dump(data=self.inventory.structure(), stream=f, Dumper=CustomYamlDumper, indent=self.indent)
        # Dump host_vars
        for host_name, host in inventory_dict['hosts'].items():
            self.logger.debug(msg=f"Dumping host_vars for host {host_name}")
            del host['name']
            if 'config' in host.keys():
                host.update(host['config'])
                del host['config']
            if len(host.keys()):
                if separate_host_sections:
                    common_host_sections = ['name']
                    host_dir = host_vars.joinpath(host_name)
                    host_dir.mkdir(exist_ok=True)
                    self.dump_separate_sections(data=host, path=host_dir, common_sections=common_host_sections)
                else:
                    with host_vars.joinpath(f"{host_name}.yml").open(mode='w') as f:
                        yaml.dump(data=host, stream=f, Dumper=CustomYamlDumper, indent=self.indent)

        # Dump group_vars
        # Build flat dict of all groups
        group_dict = {}
        self.logger.debug("Dumping group_vars...")
        for group_name, group in self.inventory.groups.items():
            group_dict.update({k:v.serial_dict(exclude={'name', 'hosts', 'children'}, exclude_none=True) for k, v in group.get_flat_children().items()})
            # Include self
            group_dict.update({group_name: group.serial_dict(exclude={'name', 'hosts', 'children'}, exclude_none=True)})
        for group_name, group in group_dict.items():
            self.logger.debug(msg=f"Dumping group_vars for group {group_name}")
            if 'config' in group.keys():
                group.update(group['config'])
                del group['config']
            if len(group.keys()):
                if separate_host_sections:
                    common_group_sections = ['name']
                    group_dir = group_vars.joinpath(group_name)
                    group_dir.mkdir(exist_ok=True)
                    self.dump_separate_sections(data=group, path=group_dir, common_sections=common_group_sections)
                else:
                    with group_vars.joinpath(f"{group_name}.yml").open(mode='w') as f:
                        yaml.dump(data=group, stream=f, Dumper=CustomYamlDumper, indent=self.indent)
        

    def dump_separate_sections(self, data: dict, path: pathlib.Path, common_sections: List[str] = []):
        common_file = path.joinpath(f"{path.name}.yml")
        present_common_sections = [x for x in data.keys() if x in common_sections]
        present_separate_sections = [x for x in data.keys() if x not in common_sections]

        if len(present_common_sections):
            common_data = {section_key:data[section_key] for section_key in present_common_sections}
            with common_host_file.open(mode='w') as f:
                yaml.dump(data=common_data, stream=f, Dumper=CustomYamlDumper, indent=self.indent)

        if len(present_separate_sections):
            for section_key in present_separate_sections:
                with path.joinpath(f"{section_key}.yml").open(mode='w') as f:
                    yaml.dump(data={section_key: data[section_key]}, stream=f, Dumper=CustomYamlDumper, indent=self.indent)


    def dump_yaml(self):
        inventory_dict = self.inventory.serial_dict(exclude_none=True)
        for host in inventory_dict['hosts'].values():
            del host['name']
            if 'config' in host.keys():
                host.update(host['config'])
                del host['config']
        print(yaml.dump(data=inventory_dict, Dumper=CustomYamlDumper, indent=self.indent))

