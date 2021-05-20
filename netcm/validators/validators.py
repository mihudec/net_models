import ipaddress
from collections import OrderedDict
from netcm.utils import get_interface_index, get_logger
from pydantic.typing import List, Union

LOGGER = get_logger(name="NetCm-Validators")

def ipv4_is_assignable(address: ipaddress.IPv4Interface) -> ipaddress.IPv4Interface:
    # Don't validate address if prefix is /31 or /32
    if int(address.with_prefixlen.split("/")[1]) in [31,32]:
        pass
    else:
        assert address.ip not in [
            address.network.network_address,
            address.network.broadcast_address], f"Invalid IPv4 Interface Address: {address}"
    return address


def sort_interface_dict(interfaces: OrderedDict) -> OrderedDict:
    return OrderedDict(sorted(interfaces.items(), key=lambda x: get_interface_index(x[0])))

def remove_duplicates_and_sort(data: List) -> List:
    return sorted(set(data))

def expand_vlan_range(vlan_range: Union[List[int], str]) -> List[int]:
    vlan_list = []

    if isinstance(vlan_range, list):
        for item in vlan_range:
            if isinstance(item, int):
                vlan_list.append(item)
            elif isinstance(item, str):
                if "-" not in item:
                    try:
                        vlan_list.append(int(item))
                    except Exception as e:
                        msg = f"Invalid 'vlan_range' element: {item}."
                        LOGGER.error(msg=msg)
                        raise ValueError(msg)
                else:
                    split_result = item.split("-")
                    if len(split_result) != 2:
                        msg = f"Invalid 'vlan_range' element: {item}."
                        LOGGER.error(msg=msg)
                        raise ValueError(msg)
                    else:
                        start, stop = (None, None)
                        try:
                            start, stop = map(int, split_result)
                        except Exception as e:
                            msg = f"Invalid 'vlan_range' element: {item}."
                            LOGGER.error(msg=msg)
                            raise ValueError(msg)

                        if start >= stop:
                                raise ValueError(f"Invalid 'vlan_range' element: {item}. Range beggining >= end.")
                        vlan_list.extend(range(start, stop+1))
            else:
                raise TypeError(f"Invalid 'vlan_range' element type: {type(item)}. Expected Union[str, int].")
    elif isinstance(vlan_range, str):
        if vlan_range in ["all", "none"]:
            return vlan_range
        vlan_list = expand_vlan_range(vlan_range=vlan_range.split(","))
    else:
        raise TypeError(f"Invalid type of 'vlan_range'. Expected Union[list, str], got {type(vlan_range)}.")

    try:
        vlan_list = sorted(set(vlan_list))
    except Exception as e:
        raise
    return vlan_list