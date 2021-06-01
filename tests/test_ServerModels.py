from tests.BaseTestClass import BaseNetCmTestClass, BaseVendorIndependentTest

from netcm.models.services.vi.ServerModels import *

class VendorIndependentServerTest(BaseVendorIndependentTest):

    TEST_CLASS = ServerPropertiesBase

    def test_subclasses_server_model(self):
        self.assertTrue(issubclass(self.TEST_CLASS, ServerBase))


class TestServerPropertiesBase(VendorIndependentServerTest):

    TEST_CLASS = ServerPropertiesBase


class TestNtpKey(BaseVendorIndependentTest):

    TEST_CLASS = NtpKey

    def test_valid_init(self):
        test_cases = [
            {
                "test_name": "Test-Valid-01",
                "data": {
                    "key_id": 1,
                    "method": "md5",
                    "encryption_type": 0,
                    "value": "SuperSecret"
                }
            }
        ]
        for test_case in test_cases:
            with self.subTest(msg=test_case["test_name"]):
                try:
                    test_obj = self.TEST_CLASS(**test_case["data"])
                except Exception as e:
                    self.fail(f"{self.TEST_CLASS.__name__} raised Exception: {repr(e)}")


class TestNtpServer(VendorIndependentServerTest):

    TEST_CLASS = NtpServer

    def test_init_valid(self):
        test_cases = [
            {
                "test_name": "Test-01",
                "payload": {
                    "server": "10.0.0.1",
                    "src_interface": "Loopback0",
                    "key_id": 1
                }
            }
        ]
        for test_case in test_cases:
            with self.subTest(msg=test_case["test_name"]):
                try:
                    test_obj = self.TEST_CLASS(**test_case["payload"])
                except Exception as e:
                    self.fail(f"{self.TEST_CLASS.__name__} raised Exception: {repr(e)}")


class TestLoggingServer(VendorIndependentServerTest):

    TEST_CLASS = AaaServer


class TestRadiusServer(VendorIndependentServerTest):

    TEST_CLASS = RadiusServer

    def test_init_valid(self):
        test_cases = [
            {
                "test_name": "Test-01",
                "payload": {
                    "server": "10.0.0.1",
                    "name": "Radius-01",
                    "key": {
                        "value": "Abc123!",
                        "encryption_type": "7"
                    },
                    "single_connection": True,
                    "timeout": 30
                }
            }
        ]
        for test_case in test_cases:
            with self.subTest(msg=test_case["test_name"]):
                try:
                    test_obj = self.TEST_CLASS(**test_case["payload"])
                except Exception as e:
                    self.fail(f"{self.TEST_CLASS.__name__} raised Exception: {repr(e)}")


class TestTacacsServer(VendorIndependentServerTest):

    TEST_CLASS = TacacsServer

    def test_init_valid(self):
        test_cases = [
            {
                "test_name": "Test-01",
                "payload": {
                    "server": "10.0.0.1",
                    "name": "Tacacs-01",
                    "key": {
                        "value": "Abc123!",
                        "encryption_type": "7"
                    },
                    "single_connection": True,
                    "timeout": 30
                }
            }
        ]
        for test_case in test_cases:
            with self.subTest(msg=test_case["test_name"]):
                try:
                    test_obj = self.TEST_CLASS(**test_case["payload"])
                except Exception as e:
                    self.fail(f"{self.TEST_CLASS.__name__} raised Exception: {repr(e)}")



if __name__ == '__main__':
    unittest.main()