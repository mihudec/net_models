import ipaddress
from typing import OrderedDict # >= Python 3.7.2
from collections import OrderedDict as CollectionOrderedDict # > Python 3.9
from netcm.utils import get_interface_index

def ipv4_is_assignable(address: ipaddress.IPv4Interface) -> ipaddress.IPv4Interface:
    # Don't validate address if prefix is /31 or /32
    if int(address.with_prefixlen.split("/")[1]) in [31,32]:
        pass
    else:
        assert address.ip not in [
            address.network.network_address,
            address.network.broadcast_address], f"Invalid IPv4 Interface Address: {address}"
    return address


def sort_interface_dict(interfaces: OrderedDict):
    return CollectionOrderedDict(sorted(interfaces.items(), key=lambda x: get_interface_index(x[0])))