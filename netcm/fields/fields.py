from pydantic import (
    conint,
    constr
)


vlan_id = conint(ge=1, le=4095)
interface_name = constr(min_length=3)