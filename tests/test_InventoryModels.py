import unittest

from net_models.inventory import *

from tests import TestBaseNetModel


class TestGroup(TestBaseNetModel):

    def test_get_all_groups(self):
        group = Group(
            name="A",
            children={
                "B": Group(
                    name="B",
                    children={
                        "C": Group(name="C"),
                        "D": Group(name="D")
                    }
                )
            }
        )
        group_dict = group.get_flat_children()
        print({k:v.serial_dict(include={'config'}, exclude_none=True) for k, v in group_dict.items()})


if __name__ == '__main__':
    unittest.main()