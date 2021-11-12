import re
from collections import UserString
from pydantic import constr, conint
from pydantic.typing import Literal, Dict, List, Type, Tuple

from net_models.validators import *
from net_models.config import LOGGER_FIELDS
from net_models.utils import get_logger, BASE_INTERFACE_REGEX, INTERFACE_NAMES

LOGGER = LOGGER_FIELDS


BASE_INTERFACE_NAME = constr(regex=BASE_INTERFACE_REGEX.pattern)
INTERFACE_NAME = constr(regex=BASE_INTERFACE_REGEX.pattern)

# INTERFACE_NAME = Literal['Ethernet', 'FastEthernet', 'GigabitEthernet', 'TenGigabitEthernet', 'TwentyFiveGigE', 'FortyGigabitEthernet', 'HundredGigE', 'Port-channel', 'Tunnel', 'Vlan', 'BDI', 'Loopback', 'Serial', 'pseudowire']
GENERIC_OBJECT_NAME = constr(strip_whitespace=True, regex=r"\S+")
GENERIC_INTERFACE_NAME = constr(strip_whitespace=True, regex=r"\S+")
LAG_MODE = Literal["active", "passive", "desirable", "auto", "on"]

VRF_NAME = constr(strip_whitespace=True, regex=r"\S+")
VLAN_ID = conint(ge=1, le=4094)
BRIDGE_DOMAIN_ID = conint(ge=1)
CLASS_OF_SERVICE = conint(ge=0, le=7)
ROUTE_MAP_NAME = GENERIC_OBJECT_NAME
ASN = conint(ge=1, le=4294967295)



AFI = Literal["ipv4", "ipv6", "vpnv4", "vpnv6"]
SAFI = Literal["unicast", "multicast"]

ISIS_LEVEL = Literal['level-1', 'level-2']
HSRP_GROUP_NAME = constr(regex=r'\S{1,25}')
interface_name = constr(min_length=3)
SWITCHPORT_MODE = Literal["access", "trunk", "dynamic auto", "dynamic desirable", "dot1q-tunnel", "private-vlan host", "private-vlan promiscuous"]

PRIVILEGE_LEVEL = conint(ge=0, le=15)
AAA_METHOD_NAME = Union[Literal['default'], GENERIC_OBJECT_NAME]


ROUTE_TARGET = constr(regex=r"((?:(?:\d{1,3}\.){3}(?:\d{1,3}))|(?:\d+)):(\d+)")
ROUTE_DISTINGUISHER = ROUTE_TARGET
L2_PROTOCOL = Literal['R4', 'R5', 'R6', 'R8', 'R9', 'RA', 'RB', 'RC', 'RD', 'RF', 'cdp', 'dot1x', 'dtp', 'elmi', 'esmc', 'lacp', 'lldp', 'pagp', 'ptppd', 'stp', 'udld', 'vtp']


class BaseInterfaceName(str):
    _registry = {}

    INTERFACE_NAMES: Dict[str, str] = None
    INTERFACE_REGEX: Type[re.Pattern] = None
    DELIMITER: str = ""
    INTERFACE_TYPE_WEIGHT_MAP: Dict[int, List[str]] = None
    INTEFACE_TYPE_MAX_WEIGHT: int = 255
    INTEFACE_TYPE_DEFAULT_WEIGHT: int = 50

    def __init_subclass__(cls, **kwargs):
        if cls not in cls._registry.keys():
            cls._registry[cls] = None

    def __new__(cls, v):
        if not isinstance(v, (str, UserString)):
            msg = f"Interface name has to be str, got {type(v)}"
            LOGGER.error(msg=msg)
            raise TypeError(f"Interface name has to be str, got {type(v)}")
        subclass = None
        validated_v = None
        for subclass_candidate in cls._registry.keys():
            try:
                validated_v = subclass_candidate.normalize_interface_name(interface_name=v)
                subclass = subclass_candidate
                break
            except Exception as e:
                pass
        if subclass is not None:
            return super().__new__(subclass, validated_v)
        else:
            v = cls.validate_name(v=v)
            return super().__new__(cls, v)


    @classmethod
    def split_interface(cls, interface_name: str) -> Tuple[str, str]:
        try:
            match = re.match(pattern=cls.INTERFACE_REGEX, string=interface_name)
        except TypeError as e:
            LOGGER.error("Expected string or bytes-like object, cannot match on '{}'".format(type(interface_name)))
            return (None, None)
        if match:
            return [match.group("type"), match.group("numbers")]
        else:
            LOGGER.error("Given interface '{}' did not match parsing pattern.".format(interface_name))
            return (None, None)

    @classmethod
    def normalize_interface_name(cls, interface_name: str) -> str:
        interface_type, interface_num = cls.split_interface(interface_name=interface_name)
        if any([x is None for x in [interface_type, interface_num]]):
            msg = f"Failed to split interface_name '{interface_name}'"
            raise ValueError(msg)

        match_found = False
        if interface_type in cls.INTERFACE_NAMES.keys():
            match_found = True
            interface_name = interface_type + cls.DELIMITER + interface_num

        if not match_found:
            for full_type, short_types in cls.INTERFACE_NAMES.items():
                for short_type in short_types:
                    if interface_type.lower().startswith(short_type.lower()):
                        match_found = True
                        interface_name = full_type + cls.DELIMITER + interface_num

        if not match_found:
            msg = f"Given interface name does not comply with valid interface names for {cls.__name__}. Given: {interface_name}, Expected: {list(INTERFACE_NAMES.keys())}"
            LOGGER.error(msg=msg)
            raise AssertionError(msg)
        else:
            return interface_name

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_name

    @classmethod
    def validate_name(cls, v: str):
        return cls.__new__(cls, v)

    @property
    def interface_type(self):
        return self.split_interface(interface_name=self)[0]

    @property
    def interface_number(self):
        return self.split_interface(interface_name=self)[1]

    @property
    def short(self):
        return f"{self.INTERFACE_NAMES[self.interface_type][0]}{self.interface_number}"

    @property
    def long(self):
        self.normalize_interface_name(interface_name=self)

    def extract_numbers(self, max_length: int = 6) -> Union[List[int], None]:

        interface_number = self.interface_number
        numbers = [0]*max_length
        NUMBER_REGEX = re.compile(pattern=r"\d+")
        SLOTS_REGEX = re.compile(pattern=r"^(?:\d+)(?:[\/]\d+)*")
        SUBINT_REGEX = re.compile(pattern=r"\.(?P<number>\d+)$")
        CHANNEL_REGEX = re.compile(pattern=r"\:(?P<number>\d+)")

        slots, subint, channel = (None, None, None)
        m = SLOTS_REGEX.search(string=interface_number)
        if m:
            slots = [int(x.group(0)) for x in NUMBER_REGEX.finditer(string=m.group(0))]

        m = CHANNEL_REGEX.search(string=interface_number)
        if m:
            channel = int(m.group("number"))

        m = SUBINT_REGEX.search(string=interface_number)
        if m:
            subint = int(m.group("number"))

        if not any([slots, channel, subint]):
            LOGGER.error(f"Failed to extract numbers from {interface_number}")
            return None

        if subint:
            numbers[-1] = subint
        if channel:
            numbers[-2] = channel

        if len(slots) > (max_length - 2):
            msg = f"Cannot unpack {len(slots)} slots with max_length == {max_length}"
            LOGGER.error(msg)
            raise ValueError(msg)
        else:
            offset = (max_length - 2) - len(slots)
            for index, slot in enumerate(slots):
                numbers[offset + index] = slot
        return numbers, len(slots)

    def get_weight(self) -> int:
        interface_type = self.interface_type
        for weight, interface_types in self.INTERFACE_TYPE_WEIGHT_MAP.items():
            if interface_type in interface_types:
                return weight
        return self.INTEFACE_TYPE_DEFAULT_WEIGHT

    def get_index(self, max_length: int = 6, max_bits: int = 16) -> int:
        interface_type, numbers = self.interface_type, self.interface_number

        try:
            numbers, len_slots = self.extract_numbers()
            LOGGER.debug(msg=f"Numbers: {numbers}, LenSlots: {len_slots}")
        except ValueError as e:
            LOGGER.error(f"{repr(e)}")
            return 0

        binary_numbers = [format(x, f"0{max_bits}b") for x in numbers]
        reverse_weight = self.INTEFACE_TYPE_MAX_WEIGHT - self.get_weight()
        index_binary = format(reverse_weight, "08b") + format(len_slots, "04b") + "".join(binary_numbers)
        index = int(index_binary, 2)
        LOGGER.debug(msg=f"Interface: '{interface_name}' LenSlots: {len_slots} Index: {index} IndexBinary: {index_binary}")
        return index



class IosInterfaceName(BaseInterfaceName):

    INTERFACE_REGEX = re.compile(pattern=r"(?P<type>^[A-z]{2,}(?:[A-z\-])*)(?P<numbers>\d+(?:\/\d+)*(?:\:\d+)?(?:\.\d+)?)(\s*)$")
    DELIMITER = ""
    INTERFACE_NAMES = {
        "Ethernet": ["Et", "Eth"],
        "FastEthernet": ["Fa"],
        "GigabitEthernet": ["Gi"],
        "TenGigabitEthernet": ["Te"],
        "TwentyFiveGigE": ["Twe"],
        "FortyGigabitEthernet": ["Fo"],
        "HundredGigE": ["Hu"],
        "Port-channel": ["Po"],
        "Tunnel": ["Tu"],
        "Vlan": ["Vl"],
        "BDI": ["BDI"],
        "Loopback": ["Lo"],
        "Serial": ["Se"],
        "pseudowire": ["pw"],
        "CEM": ["CEM"]
    }
    INTERFACE_TYPE_WEIGHT_MAP = {
        100: ["Loopback"],
        95: ["Vlan"],
        90: ["BDI"],
        80: ["Tunnel"],
        75: ["pseudowire"],
        40: ['Port-channel']

    }

class JuniperInterfaceName(BaseInterfaceName):

    INTERFACE_REGEX = re.compile(pattern=r"(?P<type>^[A-z]{2,}(?:[A-z\-])*)-(?P<numbers>\d+(?:\/\d+)*(?:\:\d+)?(?:\.\d+)?)(\s*)$")
    DELIMITER = "-"
    INTERFACE_NAMES = {
        "xe": ["xe"]
    }
    INTERFACE_TYPE_WEIGHT_MAP = {}


    @property
    def short(self):
        return f"{self.INTERFACE_NAMES[self.interface_type][0]}{self.DELIMITER}{self.interface_number}"

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


class DoubleQoutedString(str):

    pass

class Jinja2String(DoubleQoutedString):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_jinja

    @classmethod
    def validate_jinja(cls, v: str):
        jinja_pattern = re.compile(pattern=r"^\{\{.*?\}\}$", flags=re.MULTILINE)
        if not jinja_pattern.match(v):
            msg = f"Jinja2 String must start with '{{{{' and end with '}}}}'. Got '{v}'"
            # LOGGER.warning(msg=msg)
            raise AssertionError(msg)
        return cls(v)

JINJA_OR_NAME = Union[Jinja2String, GENERIC_OBJECT_NAME]