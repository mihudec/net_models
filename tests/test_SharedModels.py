from tests.BaseTestClass import TestBaseNetModel, TestVendorIndependentBase

from net_models.models.BaseModels.SharedModels import *

from pydantic import ValidationError


class TestKeyBase(TestVendorIndependentBase):

    TEST_CLASS = KeyBase

    def test_valid_01(self):
        test_cases = [
            {
                "test_name": "Test-xyz",
                "data": {
                    "encryption_type": 0,
                    "value": "SuperSecret"
                }
            }
        ]
        for test_case in test_cases:
            with self.subTest(msg=test_case["test_name"]):
                test_obj = self.TEST_CLASS(**test_case["data"])


class TestKeyChain(TestVendorIndependentBase):

    TEST_CLASS = KeyChain

    def test_valid_01(self):
        test_cases = [
            {
                "test_name": "Test-xyz",
                "data": {
                    "name": "KC-01",
                    "keys_list": [
                        {
                            "encryption_type": 0,
                            "value": "SuperSecret"
                        }
                    ]
                }
            }
        ]
        for test_case in test_cases:
            with self.subTest(msg=test_case["test_name"]):
                test_obj = self.TEST_CLASS(**test_case["data"])



if __name__ == '__main__':
    unittest.main()
