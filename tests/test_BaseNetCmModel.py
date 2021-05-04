import unittest
from netcm.models.BaseModels import BaseNetCmModel
from tests.BaseTestClass import BaseNetCmTestClass


class TestBaseNetCmModel(BaseNetCmTestClass):
    
    TEST_CLASS = BaseNetCmModel

    
if __name__ == "__main__":
    unittest.main()