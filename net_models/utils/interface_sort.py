from net_models.utils import get_logger
from net_models.utils.common import split_interface
import re
from typing import List, Union
LOGGER = get_logger(name="NetCm-InterfaceSort")

INTERFACE_TYPE_WEIGHT_MAP = {
    100: ["Loopback"],
    90: ["Vlan"],
    95: ["BDI"],
    80: ["Tunnel"],
    75: ["pseudowire"],

}
INTEFACE_TYPE_DEFAULT_WEIGHT = 50
INTEFACE_TYPE_MAX_WEIGHT = 255



def extract_numbers(text: str, max_length: int = 6) -> Union[List[int], None]:

    numbers = [0]*max_length
    NUMBER_REGEX = re.compile(pattern=r"\d+")
    SLOTS_REGEX = re.compile(pattern=r"^(?:\d+)(?:[\/]\d+)*")
    SUBINT_REGEX = re.compile(pattern=r"\.(?P<number>\d+)$")
    CHANNEL_REGEX = re.compile(pattern=r"\:(?P<number>\d+)")

    slots, subint, channel = (None, None, None)
    m = SLOTS_REGEX.search(string=text)
    if m:
        slots = [int(x.group(0)) for x in NUMBER_REGEX.finditer(string=m.group(0))]

    m = CHANNEL_REGEX.search(string=text)
    if m:
        channel = int(m.group("number"))

    m = SUBINT_REGEX.search(string=text)
    if m:
        subint = int(m.group("number"))

    if not any([slots, channel, subint]):
        LOGGER.error(f"Failed to extract numbers from {text}")
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


def get_weight_by_type(interface_type: str) -> int:
    for weight, interface_types in INTERFACE_TYPE_WEIGHT_MAP.items():
        if interface_type in interface_types:
            return weight
    return INTEFACE_TYPE_DEFAULT_WEIGHT

def get_interface_index(interface_name: str, max_length: int = 6, max_bits: int = 16) -> int:
    interface_type, numbers = split_interface(interface_name=interface_name)

    try:
        numbers, len_slots = extract_numbers(text=numbers, max_length=max_length)
    except ValueError as e:
        LOGGER.error(f"{repr(e)}")
        return 0

    binary_numbers = [format(x, f"0{max_bits}b") for x in numbers]
    weight = INTEFACE_TYPE_MAX_WEIGHT - get_weight_by_type(interface_type=interface_type)
    index = int(format(weight, "08b") + format(len_slots, "04b") + "".join(binary_numbers), 2)
    return index
