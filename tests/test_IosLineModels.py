from tests.BaseTestClass import TestBaseNetModel, TestVendorIndependentBase

from net_models.models.services.cisco_ios.IosLineModels import IosLineConfig

from pydantic import ValidationError


class TestIosLineConfig(TestVendorIndependentBase):

    TEST_CLASS = IosLineConfig
    RESOURCE_DIR = TestVendorIndependentBase.RESOURCE_DIR.joinpath("line").joinpath("cisco_ios")

if __name__ == '__main__':
    unittest.main()



