import unittest
from tests.BaseTestClass import TestBaseNetModel, TestVendorIndependentBase
from net_models.models.VendorIndependent.VlanModel import VlanModel


class TestVlanModel(TestVendorIndependentBase):
    TEST_CLASS = VlanModel

    def test_valid_01(self):
        test_payload = {
            "vlan_id": "100",
            "name": "Vlan-100"
        }
        test_obj = self.TEST_CLASS(**test_payload)
        self.assertTrue(
            all([hasattr(test_obj, x) for x in test_payload.keys()])
        )

if __name__ == '__main__':
    unittest.main()