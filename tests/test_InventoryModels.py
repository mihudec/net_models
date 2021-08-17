import unittest

from net_models.exceptions import *
from net_models.inventory import *

from tests import TestBaseNetModel


class TestGroup(TestBaseNetModel):

    def test_get_all_groups(self):
        group = Group(
            name="A",
            children={
                "B": Group(
                    name="B",
                    children={
                        "C": Group(name="C"),
                        "D": Group(name="D")
                    }
                )
            }
        )
        group_dict = group.get_flat_children()
        print({k:v.serial_dict(include={'config'}, exclude_none=True) for k, v in group_dict.items()})


class TestHostConfig(TestBaseNetModel):


    def test_get_interface_01(self):
        existing_interface = InterfaceModel(
            name="Loopback0",
            description="Test"
        )
        model = HostConfig(
            interfaces={
                existing_interface.name: existing_interface
            }
        )
        with self.subTest(msg="Get existing interface"):
            candidate = model._get_interface(existing_interface.name)
            self.assertEqual(existing_interface, candidate)

        with self.subTest(msg="Get non-existing interface"):
            candidate = model._get_interface("Loopback1000")
            self.assertTrue(candidate is None)

    def test_create_interface_01(self):
        # Create Empty Model
        model = HostConfig()

        with self.subTest(msg="Create interface on empty model"):
            interface = InterfaceModel(name="Loopback0")
            model._create_interface(interface=interface)
            self.assertEqual(model.interfaces[interface.name], interface)

        with self.subTest(msg="Try creating existing interface again - without force"):
            interface = InterfaceModel(name="Loopback0")
            with self.assertRaises(expected_exception=InterfaceAlreadyExists):
                model._create_interface(interface=interface)


        with self.subTest(msg="Try creating existing interface again - with force"):
            interface = InterfaceModel(name="Loopback0", description="New Interface")
            model._create_interface(interface=interface, force_create=True)
            self.assertEqual(model.interfaces[interface.name], interface)

    def test_get_or_create_interface_01(self):
        # Create Empty Model
        model = HostConfig()

        with self.subTest(msg="Create interface on empty model"):
            interface = InterfaceModel(name="Loopback0")
            model._get_or_create_interface(interface=interface)
            self.assertEqual(model.interfaces[interface.name], interface)

class TestHost(TestBaseNetModel):

    def test_get_or_create_interface_01(self):

        model = Host(name="Test-Host")

        with self.subTest(msg="Test invalid parameters - parameters"):
            with self.assertRaises(expected_exception=ValueError):
                model.get_or_create_interface()

        with self.subTest(msg="Test invalid parameters - missing name"):
            with self.assertRaises(expected_exception=ValueError):
                model.get_or_create_interface(interface={"description": "Test Description"})

        with self.subTest(msg="Test creating interface - 01 - Dict"):
            interface = {
                "name": "Loopback0",
                "l3_port": {
                    "ipv4": {
                        "addresses": [
                            {"address": "192.168.0.2"}
                        ]
                    }
                }
            }
            model.get_or_create_interface(
                interface=interface
            )
            interface = InterfaceModel.parse_obj(interface)
            self.assertEqual(model.config.interfaces[interface.name], interface)

        with self.subTest(msg="Test getting interface - 01 - Dict"):
            interface = {
                "name": "Loopback0",
                "l3_port": {
                    "ipv4": {
                        "addresses": [
                            {"address": "192.168.0.2"}
                        ]
                    }
                }
            }
            model.get_or_create_interface(
                interface=interface
            )
            interface = InterfaceModel.parse_obj(interface)
            self.assertEqual(model.config.interfaces[interface.name], interface)






if __name__ == '__main__':
    unittest.main()