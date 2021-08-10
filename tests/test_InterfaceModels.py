import collections
import unittest
import json
import yaml
from pydantic.error_wrappers import ValidationError
from net_models.models.interfaces import *


from tests.BaseTestClass import TestVendorIndependentBase


class TestInterfaceSpanningTreeConfig(TestVendorIndependentBase):
    TEST_CLASS = InterfaceSpanningTreeConfig


class TestInterfaceSwitchportModel(TestVendorIndependentBase):
    TEST_CLASS = InterfaceSwitchportModel

    def test_valid_trunk_01(self):
        test_payload = {
            "mode": "trunk",
            "allowed_vlans": [10, 20, 30, 40],
            "untagged_vlan": 1
        }
        test_obj = self.TEST_CLASS(**test_payload)
        self.assertTrue(
            all([hasattr(test_obj, x) for x in test_payload.keys()])
        )

    def test_valid_trunk_from_json(self):
        test_payload = {
            "mode": "trunk",
            "allowed_vlans": [10, 20, 30, 40],
            "untagged_vlan": 1
        }
        test_obj = self.TEST_CLASS.parse_raw(json.dumps(test_payload))
        self.assertTrue(
            all([hasattr(test_obj, x) for x in test_payload.keys()])
        )


    # def test_invalid_trunk_01(model):
    #     test_payload = {
    #         "mode": "trunk",
    #         "allowed_vlans": [1, 2, 3, 4]
    #     }
    #     with model.assertRaisesRegex(expected_exception=ValidationError,
    #                                 expected_regex=r"Vlan 1 cannot be tagged if untagged_vlan is None."):
    #         test_obj = model.TEST_CLASS(**test_payload)

    # def test_invalid_trunk_02(model):
    #     test_payload = {
    #         "mode": "trunk",
    #         "allowed_vlans": [1, 2, 3, 4],
    #         "untagged_vlan": 2
    #     }
    #     with model.assertRaisesRegex(expected_exception=ValidationError,
    #                                 expected_regex=r"Vlan \d+ cannot be both tagged and untagged."):
    #         test_obj = model.TEST_CLASS(**test_payload)

    def test_duplicate_allowed(self):

        test_payload = {
            "mode": "trunk",
            "allowed_vlans": [1,2,2,3,4,5]
        }
        test_obj = self.TEST_CLASS(**test_payload)
        want = [1,2,3,4,5]
        have = test_obj.allowed_vlans
        self.assertEqual(want, have)


    def test_posponed_validation_01(self):
        test_obj = InterfaceSwitchportModel.construct()
        test_obj.mode = "trunk"
        test_obj.allowed_vlans = [10, 11, 12]
        try:
            test_obj.check()
        except ValidationError as e:
            self.fail(f"{repr(e)}")

    def test_posponed_validation_02(self):
        test_obj = InterfaceSwitchportModel.construct()
        test_obj.mode = "trunk"
        with self.assertRaises(ValidationError):
            test_obj.allowed_vlans = [5000]
            test_obj.check()



class TestInterfaceIPv4Address(TestVendorIndependentBase):
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


class TestInterfaceIPv6Address(TestVendorIndependentBase):
    TEST_CLASS = InterfaceIPv6Address

    def test_valid_01(self):
        test_payload = {
            "address": "123:4567:89ab:cdef:123:4567:89ab:cdef/64"
        }
        try:
            test_obj = self.TEST_CLASS(**test_payload)
        except Exception as e:
            self.fail(f"{self.TEST_CLASS.__name__} raised Exception: {repr(e)}")


class TestInterfaceIPv4Container(TestVendorIndependentBase):
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

    def test_valid_02(self):
        test_payload = {}
        try:
            test_obj = self.TEST_CLASS(**test_payload)
        except Exception as e:
            self.fail(f"{self.TEST_CLASS.__name__} raised Exception: {repr(e)}")


     
    def test_with_overlapping(self):
        test_payload = {
            "addresses": [
                {"address": "192.168.1.1/24"},
                {"address": "192.168.1.2/24"}
            ]
        }
        with self.assertRaisesRegex(ValidationError, expected_regex="Address 192.168.1.2/24 overlaps with 192.168.1.1/24"):
            test_obj = self.TEST_CLASS(**test_payload)


class TestInterfaceIPv6Container(TestVendorIndependentBase):
    TEST_CLASS = InterfaceIPv6Container


class TestRouteportModel(TestVendorIndependentBase):
    TEST_CLASS = InterfaceRouteportModel


class TestInterfaceModel(TestVendorIndependentBase):
    TEST_CLASS = InterfaceModel

    def test_valid_interface_names(self):
        test_cases = [
            {
                "test_name": "Loopback0",
                "data": {
                    "name": "Loopback0",
                },
                "result": "Loopback0"
            },
            {
                "test_name": "lo0",
                "data": {
                    "name": "lo0",
                },
                "result": "Loopback0"
            },
            {
                "test_name": "GigabitEthernet1/0/1",
                "data": {
                    "name": "GigabitEthernet1/0/1",
                },
                "result": "GigabitEthernet1/0/1"
            },
            {
                "test_name": "gi1/0/1",
                "data": {
                    "name": "gi1/0/1",
                },
                "result": "GigabitEthernet1/0/1"
            }
        ]
        for test_case in test_cases:
            with self.subTest(msg=test_case["test_name"]):
                want = test_case["result"]
                have = self.TEST_CLASS(**test_case["data"]).name
                self.assertEqual(want, have)

    def test_to_json(self):
        test_obj = self.TEST_CLASS(name="Vlan1")
        want = {"name": "Vlan1", "tags": ["virtual"]}
        output = test_obj.json(exclude_none=True)
        have = json.loads(output)
        self.assertEqual(want, have)

    def test_to_yaml(self):
        test_obj = self.TEST_CLASS(name="GigabitEthernet1/0/1", tags=["physical"], l2_port=InterfaceSwitchportModel(mode="access"))
        want = {"name": "GigabitEthernet1/0/1", "tags": ["l2", "physical"], "l2_port": {"mode": "access"}}
        output = test_obj.yaml(exclude_none=True)
        have = yaml.safe_load(output)
        self.assertEqual(want, have)


class TestInterfaceContainerModel(TestVendorIndependentBase):
    TEST_CLASS = InterfaceContainerModel

    def test_create_01(self):
        test_payload = {
            "interfaces": {
                "Loopback1": {
                    "name": "Loopback1",
                    "l3_port": {
                        "ipv4": {
                            "addresses": [
                                {
                                    "address": "192.168.1.1/32"
                                }
                            ]
                        }
                    }
                },
                "Loopback0": {
                    "name": "Loopback0",
                    "l3_port": {
                        "ipv4": {
                            "addresses": [
                                {
                                    "address": "192.168.1.1/32"
                                }
                            ]
                        }
                    }
                },
                "GigabitEthernet1/0/1.2": {
                    "name": "GigabitEthernet1/0/1.2",
                    "l2_port": {
                        "mode": "trunk"
                    }
                }
            }
        }
        with self.subTest("Test Init"):
            try:
                test_obj = self.TEST_CLASS(**test_payload)
            except Exception as e:
                self.fail(f"{self.TEST_CLASS.__name__} raised Exception: {repr(e)}")
        with self.subTest("OrderedDict"):
            test_obj = self.TEST_CLASS(**test_payload)
            self.assertIsInstance(test_obj.interfaces, collections.OrderedDict)


if __name__ == '__main__':
    unittest.main()
