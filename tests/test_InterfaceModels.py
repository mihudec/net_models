import unittest
from tests.BaseTestClass import BaseNetCmTestClass, BaseVendorIndependentTest
from netcm.models.VendorIndependent.InterfaceModel import InterfaceModel
from netcm.models.VendorIndependent.L2InterfaceModels import *
from netcm.models.VendorIndependent.L3InterfaceModels import *
from pydantic.error_wrappers import ValidationError


class TestInterfaceSpanningTreeConfig(BaseVendorIndependentTest):

    TEST_CLASS = InterfaceSpanningTreeConfig


class TestInterfaceSwitchportModel(BaseVendorIndependentTest):

    TEST_CLASS = InterfaceSwitchportModel

    def test_valid_trunk_01(self):
        test_payload = {
            "mode": "trunk",
            "tagged_vlans": [10,20,30,40],
            "untagged_vlan": 1
        }
        test_obj = InterfaceSwitchportModel(**test_payload)
        self.assertTrue(
            all([hasattr(test_obj, x) for x in test_payload.keys()])
        )

    def test_invalid_trunk_01(self):
        test_payload = {
            "mode": "trunk",
            "tagged_vlans": [1,2,3,4]
        }
        with self.assertRaisesRegex(expected_exception=ValidationError, expected_regex=r"Vlan 1 cannot be tagged if untagged_vlan is None."):
            InterfaceSwitchportModel(**test_payload)

    def test_invalid_trunk_02(self):
        test_payload = {
            "mode": "trunk",
            "tagged_vlans": [1,2,3,4],
            "untagged_vlan": 2
        }
        with self.assertRaisesRegex(expected_exception=ValidationError, expected_regex=r"Vlan \d+ cannot be both tagged and untagged."):
            InterfaceSwitchportModel(**test_payload)


class TestInterfaceIPv4Address(BaseVendorIndependentTest):

    TEST_CLASS = InterfaceIPv4Address

    def test_valid_01(self):
        test_payload = {
            "address": "192.168.1.1/24"
        }
        try:
            test_obj = self.TEST_CLASS(**test_payload)
        except Exception as e:
            self.fail(f"{self.TEST_CLASS.__name__} raised Exception: {repr(e)}")

    def test_invalid_01(self):
        test_payload = {
            "address": "192.168.1.0/24"
        }
        with self.assertRaisesRegex(ValidationError, expected_regex=r"Invalid IPv4 Interface Address: 192.168.1.0/24"):
            test_obj = self.TEST_CLASS(**test_payload)
        

class TestInterfaceIPv6Address(BaseVendorIndependentTest):

    TEST_CLASS = InterfaceIPv6Address

    def test_valid_01(self):
        test_payload = {
            "address": "123:4567:89ab:cdef:123:4567:89ab:cdef/64"
        }
        try:
            test_obj = self.TEST_CLASS(**test_payload)
        except Exception as e:
            self.fail(f"{self.TEST_CLASS.__name__} raised Exception: {repr(e)}")


class TestInterfaceIPv4Container(BaseVendorIndependentTest):

    TEST_CLASS = InterfaceIPv4Container

    def test_valid_01(self):
        test_payload = {
            "addresses": [
                {"address": "192.168.1.1/24"},
                {"address": "10.0.0.1/24", "secondary": True}
            ]
        }
        try:
            test_obj = self.TEST_CLASS(**test_payload)
        except Exception as e:
            self.fail(f"{self.TEST_CLASS.__name__} raised Exception: {repr(e)}")


class TestInterfaceIPv6Container(BaseVendorIndependentTest):

    TEST_CLASS = InterfaceIPv6Container


class TestRouteportAbstractModel(BaseVendorIndependentTest):

    TEST_CLASS = InterfaceRouteportModel
    

class TestInterfaceAbstractModel(BaseVendorIndependentTest):

    TEST_CLASS = InterfaceModel

    def test_has_name(self):
        test_obj = InterfaceModel(name="Vl1")
        self.assertTrue(hasattr(test_obj, "name"))


if __name__ == "__main__":
    unittest.main()