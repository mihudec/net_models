import re
from collections import UserString
from pydantic import constr, conint
from pydantic.typing import Literal

from net_models.validators import *
from net_models.config import LOGGER_FIELDS
from net_models.utils import get_logger, BASE_INTERFACE_REGEX, INTERFACE_NAMES

LOGGER = LOGGER_FIELDS


BASE_INTERFACE_NAME = constr(regex=BASE_INTERFACE_REGEX.pattern)
INTERFACE_NAME = constr(regex=BASE_INTERFACE_REGEX.pattern)

# INTERFACE_NAME = Literal['Ethernet', 'FastEthernet', 'GigabitEthernet', 'TenGigabitEthernet', 'TwentyFiveGigE', 'FortyGigabitEthernet', 'HundredGigE', 'Port-channel', 'Tunnel', 'Vlan', 'BDI', 'Loopback', 'Serial', 'pseudowire']
GENERIC_OBJECT_NAME = constr(strip_whitespace=True, regex=r"\S+")
GENERIC_INTERFACE_NAME = constr(strip_whitespace=True, regex=r"\S+")
LAG_MODE = Literal["active", "pasive", "desirable", "auto", "on"]

VRF_NAME = constr(strip_whitespace=True, regex=r"\S+")
VLAN_ID = conint(ge=1, le=4094)
BRIDGE_DOMAIN_ID = conint(ge=1)
CLASS_OF_SERVICE = conint(ge=0, le=7)
ROUTE_MAP_NAME = GENERIC_OBJECT_NAME
ASN = conint(ge=1, le=4294967295)



AFI = Literal["ipv4", "ipv6", "vpnv4", "vpnv6"]
SAFI = Literal["unicast", "multicast"]

interface_name = constr(min_length=3)
SWITCHPORT_MODE = Literal["access", "trunk", "dynamic auto", "dynamic desirable", "dot1q-tunnel", "private-vlan host", "private-vlan promiscuous"]

PRIVILEGE_LEVEL = conint(ge=0, le=15)
AAA_METHOD_NAME = Union[Literal['default'], GENERIC_OBJECT_NAME]


ROUTE_TARGET = constr(regex=r"((?:(?:\d{1,3}\.){3}(?:\d{1,3}))|(?:\d+)):(\d+)")
ROUTE_DISTINGUISHER = ROUTE_TARGET
L2_PROTOCOL = Literal['R4', 'R5', 'R6', 'R8', 'R9', 'RA', 'RB', 'RC', 'RD', 'RF', 'cdp', 'dot1x', 'dtp', 'elmi', 'esmc', 'lacp', 'lldp', 'pagp', 'ptppd', 'stp', 'udld', 'vtp']



class InterfaceName(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_name

    @classmethod
    def validate_name(cls, v: str):
        if not isinstance(v, (str, UserString)):
            msg = f"Interface name has to be str, got {type(v)}"
            LOGGER.error(msg=msg)
            raise TypeError(f"Interface name has to be str, got {type(v)}")
        # This is ordinary <class 'str'>
        interface_name = normalize_interface_name(interface_name=v)
        return interface_name
