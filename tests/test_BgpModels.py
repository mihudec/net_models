import unittest
from tests.BaseTestClass import BaseNetCmTestClass, BaseVendorIndependentTest
from netcm.models.routing.vi.BgpModels import *


class TestBgpTimers(BaseVendorIndependentTest):

    TEST_CLASS = BgpTimers


class TestBgpFallOver(BaseVendorIndependentTest):

    TEST_CLASS = BgpFallOver


class TestBgpNeighborBase(BaseVendorIndependentTest):

    TEST_CLASS = BgpNeighborBase


class TestBgpPeerGroup(BaseVendorIndependentTest):

    TEST_CLASS = BgpPeerGroup


class TestBgpNeighbor(BaseVendorIndependentTest):

    TEST_CLASS = BgpNeighbor


class TestBgpRedistributeEntry(BaseVendorIndependentTest):

    TEST_CLASS = BgpRedistributeEntry


class TestBgpAddressFamily(BaseVendorIndependentTest):

    TEST_CLASS = BgpAddressFamily


class TestRoutingBgpProcess(BaseVendorIndependentTest):

    TEST_CLASS = RoutingBgpProcess





if __name__ == '__main__':
    unittest.main()
