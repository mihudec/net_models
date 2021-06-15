import re
from net_models.utils import get_logger
from pydantic.typing import Union, List, Tuple

BASE_INTERFACE_REGEX = re.compile(pattern=r"(?P<type>[A-z]{2,}(?:[A-z\-])*)(?P<numbers>\d+(?:\/\d+)*(?:\:\d+)?(?:\.\d+)?)")

INTERFACE_NAMES = {
    "Ethernet": ["Eth", "Et"],
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
    "pseudowire": ["pw"]

}

LOGGER = get_logger(name="NetCm-Utils")

def split_interface(interface_name: str) -> Union[Tuple[str, str], Tuple[None, None]]:
    pattern = re.compile(pattern=r"(?P<type>[A-z]{2,}(?:[A-z\-])*)(?P<numbers>\d+(?:\/\d+)*(?:\:\d+)?(?:\.\d+)?)")
    try:
        match = re.match(pattern=BASE_INTERFACE_REGEX, string=interface_name)
    except TypeError as e:
        LOGGER.error("Expected string or bytes-like object, cannot match on '{}'".format(type(interface_name)))
        return (None, None)
    if match:
        return [match.group("type"), match.group("numbers")]
    else:
        LOGGER.error("Given interface {} did not match parsing pattern.".format(interface_name))
        return (None, None)
