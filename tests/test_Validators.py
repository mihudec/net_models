import unittest
from pydantic.typing import List, Dict, Callable
from net_models.validators import *

class TestValidatorBase(unittest.TestCase):


    def test_common_testcase(self, test_cases: List[Dict], test_func: Callable):
        for test_case in test_cases:
            with self.subTest(msg=test_case["test_name"]):
                want = test_case["result"]
                have = test_func(**test_case["data"])
                self.assertEqual(want, have)


class TestExpandVlanRange(TestValidatorBase):

    def test_common_testcase(self):
        test_cases = [
            {
                "test_name": "Test-Integer-List-No-Duplicates",
                "data": {
                    "vlan_range": [1, 2, 3, 4, 5, 10]
                },
                "result": [1, 2, 3, 4, 5, 10]
            },
            {
                "test_name": "Test-Integer-List-With-Duplicates",
                "data": {
                    "vlan_range": [1, 2, 2, 3, 4, 4, 5, 10]
                },
                "result": [1, 2, 3, 4, 5, 10]
            },
            {
                "test_name": "Test-String-Range-01",
                "data": {
                    "vlan_range": "1-5,10"
                },
                "result": [1, 2, 3, 4, 5, 10]
            },
            {
                "test_name": "Test-Mixed-List-Range-01",
                "data": {
                    "vlan_range": ["1-3", 4, 5, "10"]
                },
                "result": [1, 2, 3, 4, 5, 10]
            },
            {
                "test_name": "Test-Mixed-List-Range-02",
                "data": {
                    "vlan_range": ["1-3", 3, "4-5", "10"]
                },
                "result": [1, 2, 3, 4, 5, 10]
            },

        ]
        super().test_common_testcase(test_cases=test_cases, test_func=expand_vlan_range)


    def test_invalid_range_01(self):

        with self.assertRaisesRegex(expected_exception=ValueError, expected_regex=f"Invalid 'vlan_range' element: 1-x."):
            result = expand_vlan_range(vlan_range="1-x")

    def test_invalid_range_02(self):

        with self.assertRaisesRegex(expected_exception=ValueError, expected_regex=f"Invalid 'vlan_range' element: 5-4. Range beggining >= end."):
            result = expand_vlan_range(vlan_range="5-4")

    def test_invalid_range_03(self):

        with self.assertRaisesRegex(expected_exception=TypeError, expected_regex=r"Invalid 'vlan_range' element type: <class 'NoneType'>. Expected Union\[str, int\]."):
            result = expand_vlan_range(vlan_range=[1, "2", None])

    def test_invalid_range_04(self):

        with self.assertRaisesRegex(expected_exception=TypeError, expected_regex=r"Invalid type of 'vlan_range'. Expected Union\[list, str\], got <class 'NoneType'>."):
            result = expand_vlan_range(vlan_range=None)

    def test_invalid_range_05(self):

        with self.assertRaisesRegex(expected_exception=ValueError, expected_regex=r"Invalid 'vlan_range' element: 1-3-5."):
            result = expand_vlan_range(vlan_range="1-3-5")

    def test_invalid_range_06(self):

        with self.assertRaisesRegex(expected_exception=ValueError, expected_regex=r"Invalid 'vlan_range' element: Foo."):
            result = expand_vlan_range(vlan_range="Foo")



class TestNormalizeInterfaceName(TestValidatorBase):

    def test_common_testcase(self):
        test_cases = [
            {
                "test_name": "Test-Ethernet-01",
                "data": {
                    "interface_name": "ethernet0/1"
                },
                "result": "Ethernet0/1"
            }
        ]
        super().test_common_testcase(test_cases=test_cases, test_func=normalize_interface_name)



del TestValidatorBase

if __name__ == '__main__':
    unittest.main()