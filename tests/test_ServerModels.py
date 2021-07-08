from tests.BaseTestClass import TestBaseNetModel, TestVendorIndependentBase

from net_models.models.services.vi.ServerModels import *

from pydantic import ValidationError


class VendorIndependentServerTest(TestVendorIndependentBase):
    TEST_CLASS = ServerPropertiesBase

    def test_subclasses_server_model(self):
        self.assertTrue(issubclass(self.TEST_CLASS, ServerBase))


class TestServerPropertiesBase(VendorIndependentServerTest):
    TEST_CLASS = ServerPropertiesBase


class TestNtpKey(TestVendorIndependentBase):
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
                "data": {
                    "server": "10.0.0.1",
                    "src_interface": "Loopback0",
                    "key_id": 1
                }
            }
        ]
        for test_case in test_cases:
            with self.subTest(msg=test_case["test_name"]):
                try:
                    test_obj = self.TEST_CLASS(**test_case["data"])
                except Exception as e:
                    self.fail(f"{self.TEST_CLASS.__name__} raised Exception: {repr(e)}")


class TestNtpAccessGroups(TestVendorIndependentBase):
    TEST_CLASS = NtpAccessGroups

    def test_valid_01(self):
        test_cases = [
            {
                "test_name": "Test-Valid-01",
                "data": {
                    "serve_only": 1,
                    "query_only": "NTP-QUERY-ONLY",
                    "serve": "ACL-NTP-SERVE",
                    "peer": "ACL-NTP-PEERS"
                }
            }
        ]
        for test_case in test_cases:
            test_obj = self.TEST_CLASS(**test_case["data"])


class TestNtpConfig(TestVendorIndependentBase):
    TEST_CLASS = NtpConfig


class TestLoggingServer(VendorIndependentServerTest):
    TEST_CLASS = AaaServer


class TestRadiusServer(VendorIndependentServerTest):
    TEST_CLASS = RadiusServer

    def test_init_valid(self):
        test_cases = [
            {
                "test_name": "Test-01",
                "data": {
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
                    test_obj = self.TEST_CLASS(**test_case["data"])
                except Exception as e:
                    self.fail(f"{self.TEST_CLASS.__name__} raised Exception: {repr(e)}")


class TestTacacsServer(VendorIndependentServerTest):
    TEST_CLASS = TacacsServer

    def test_init_valid(self):
        test_cases = [
            {
                "test_name": "Test-01",
                "data": {
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
                    test_obj = self.TEST_CLASS(**test_case["data"])
                except Exception as e:
                    self.fail(f"{self.TEST_CLASS.__name__} raised Exception: {repr(e)}")


class TestRadiusServerGroup(VendorIndependentServerTest):
    TEST_CLASS = RadiusServerGroup

    def test_valid_01(self):
        test_cases = [
            {
                "test_name": "Test-Valid-01",
                "data": {
                    "name": "RADIUS-TEST-GROUP",
                    "servers": [
                        {
                            "name": "RADIUS-1",
                            "server": "192.0.2.1",
                            "key": {
                                "encryption_type": 0,
                                "value": "SuperSecret"
                            }
                        },
                        {
                            "name": "RADIUS-2",
                            "server": "192.0.2.2",
                            "key": {
                                "encryption_type": 0,
                                "value": "SuperSecret"
                            }
                        }
                    ]
                }
            }
        ]
        for test_case in test_cases:
            with self.subTest(msg=test_case["test_name"]):
                try:
                    test_obj = self.TEST_CLASS(**test_case["data"])
                except Exception as e:
                    self.fail(f"{self.TEST_CLASS.__name__} raised Exception: {repr(e)}")

    def test_duplicate_names_01(self):
        data = {
            "name": "RADIUS-TEST-GROUP",
            "servers": [
                {
                    "name": "RADIUS-1",
                    "server": "192.0.2.1",
                    "key": {
                        "encryption_type": 0,
                        "value": "SuperSecret"
                    }
                },
                {
                    "name": "RADIUS-1",
                    "server": "192.0.2.2",
                    "key": {
                        "encryption_type": 0,
                        "value": "SuperSecret"
                    }
                }
            ]
        }

        with self.assertRaisesRegex(expected_exception=ValidationError,
                                    expected_regex=r"Server names must be unique\."):
            test_obj = self.TEST_CLASS(**data)

    def test_duplicate_servers_01(self):
        data = {
            "name": "RADIUS-TEST-GROUP",
            "servers": [
                {
                    "name": "RADIUS-1",
                    "server": "192.0.2.1",
                    "key": {
                        "encryption_type": 0,
                        "value": "SuperSecret"
                    }
                },
                {
                    "name": "RADIUS-2",
                    "server": "192.0.2.1",
                    "key": {
                        "encryption_type": 0,
                        "value": "SuperSecret"
                    }
                }
            ]
        }

        with self.assertRaisesRegex(expected_exception=ValidationError,
                                    expected_regex=r"Server addresses must be unique\."):
            test_obj = self.TEST_CLASS(**data)


class TestLoggingDiscriminator(TestVendorIndependentBase):
    TEST_CLASS = LoggingDiscriminator

    def test_valid_01(self):
        test_obj = LoggingDiscriminator(
            name="DROP-IFD",
            actions=[
                LoggingDiscriminatorAction(
                    match="mnemonics",
                    value="IFDOWN",
                    action="drops"
                )
            ]

        )


class TestLoggingServer(VendorIndependentServerTest):
    TEST_CLASS = LoggingServer

    def test_valid_01(self):
        test_cases = [
            {
                "test_name": "Test-Valid-01",
                "data": {
                    "server": "192.0.2.1",
                    "protocol": "tcp",
                    "port": 1514,
                    "src_interface": "Loopback0",
                    "discriminator": "DROP-IFD"
                }
            }
        ]
        for test_case in test_cases:
            with self.subTest(msg=test_case["test_name"]):
                test_obj = self.TEST_CLASS.parse_obj(test_case["data"])


class TestLogginConfig(TestVendorIndependentBase):
    TEST_CLASS = LoggingConfig

    def test_valid_01(self):
        test_cases = [
            {
                "test_name": "Test-Valid-01",
                "data": {
                    "servers": [
                        {
                            "server": "192.0.2.1",
                            "protocol": "tcp",
                            "port": 1514,
                            "src_interface": "Loopback0",
                            "discriminator": "DROP-IFD"
                        },
                        {
                            "server": "192.0.2.2",
                            "protocol": "tcp",
                            "port": 1514,
                            "src_interface": "Loopback0",
                        }
                    ]
                }
            }
        ]
        for test_case in test_cases:
            with self.subTest(msg=test_case["test_name"]):
                test_obj = self.TEST_CLASS.parse_obj(test_case["data"])

    def test_raises_duplicate_servers(self):
        data = {
            "servers": [
                {
                    "server": "192.0.2.1",
                    "protocol": "tcp",
                    "port": 1514,
                    "src_interface": "Loopback0",
                    "discriminator": "DROP-IFDOWN"
                },
                {
                    "server": "192.0.2.1",
                    "protocol": "tcp",
                    "port": 1514,
                    "src_interface": "Loopback0",
                }
            ]
        }

        with self.assertRaisesRegex(expected_exception=ValidationError, expected_regex=r".*"):
            test_obj = self.TEST_CLASS.parse_obj(data)

    def test_raises_missing_discriminator(self):
        pass


if __name__ == '__main__':
    unittest.main()
