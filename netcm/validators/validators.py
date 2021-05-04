import ipaddress


def ipv4_is_assignable(address: ipaddress.IPv4Interface):
    assert address.ip not in [
        address.network.network_address, 
        address.network.broadcast_address], f"Invalid IPv4 Interface Address: {address}"
    return address