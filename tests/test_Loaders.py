import unittest
import pathlib
from net_models.models.interfaces import *


from net_models.inventory import Host, GlobalConfig
from net_models.loaders import BaseLoader, ExcelLoader



class TestBaseLoader(unittest.TestCase):

    TEST_CLASS = BaseLoader

    def test_init(self):

        loader = self.TEST_CLASS()
        loader.get_host(host_name="TestHost-A")
        for i in range(1, 49):
            interface = loader.get_interface(host_name="TestHost-A", interface_name=f"Te1/0/{i}")
            interface.lag_member = InterfaceLagMemberConfig(group=10, protocol='lacp', mode='active')
        loader.get_interface(host_name="TestHost-A", interface_name="vlan1")

        loader.finish()

class TestExcelLoader(unittest.TestCase):

    RESOURCE_PATH = pathlib.Path(__file__).resolve().parent.joinpath("resources")

    def test_01(self):
        path = self.RESOURCE_PATH.joinpath("ExcelLoaderResource-01.xlsx")
        el = ExcelLoader(input_file=path)
        # el.load_vlan_definitions()
        el.load_physical_links()
        el.load_ospf_templates()
        el.load_l3_links()
        el.load_l3_ports()
        el.load_bgp_routers()
        el.load_bgp_neighbors()

        el.finish()

if __name__ == '__main__':
    unittest.main()