import unittest
from tests.BaseTestClass import BaseNetCmTestClass
from netcm.models.AbstractModels.InterfaceAbstractModel import InterfaceAbstractModel


class TestInterfaceAbstractModel(BaseNetCmTestClass):

    TEST_CLASS = InterfaceAbstractModel

    def test_has_name(self):
        test_obj = InterfaceAbstractModel(name="")
        print(test_obj.name)


if __name__ == "__main__":
    unittest.main()