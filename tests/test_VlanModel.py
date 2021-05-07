import unittest
from tests.BaseTestClass import BaseNetCmTestClass, BaseVendorIndependentTest
from netcm.models.VendorIndependent.VlanModel import VlanModel
from netcm.models.VendorIndependent.L2InterfaceModels import *
from netcm.models.VendorIndependent.L3InterfaceModels import *
from pydantic.error_wrappers import ValidationError


class TestVlanModel(BaseVendorIndependentTest):
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
