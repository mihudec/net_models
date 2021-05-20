import re

from pydantic import constr, conint
from pydantic.typing import Literal

GENERIC_OBJECT_NAME = constr(strip_whitespace=True, regex=r"\S+")
GENERIC_INTERFACE_NAME = constr(strip_whitespace=True, regex=r"\S+")
VRF_NAME = constr(strip_whitespace=True, regex=r"\S+")
VLAN_ID = conint(ge=1, le=4095)
interface_name = constr(min_length=3)
SWITCHPORT_MODE = Literal["access", "trunk", "dynamic auto", "dynamic desirable", "dot1q-tunnel", "private-vlan host", "private-vlan promiscuous"]