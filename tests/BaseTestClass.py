import sys
import pathlib
import unittest
from netcm.models.BaseModels import BaseNetCmModel


class BaseNetCmTestClass(unittest.TestCase):

    TEST_CLASS = BaseNetCmModel

    def test_subclases_basemodel(self):
        self.assertTrue(issubclass(self.TEST_CLASS, BaseNetCmModel))

    def test_has_dict_method(self):
        self.assertTrue(hasattr(self.TEST_CLASS, "__dict__"))

    def test_has_from_dict(self):
        self.assertTrue(hasattr(self.TEST_CLASS, "__dict__"))

if __name__ == "__main__":
    unittest.main()