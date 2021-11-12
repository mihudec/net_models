import re
import unittest

import yaml

from pydantic.typing import Type

from net_models.fields import DoubleQoutedString, Jinja2String, IosInterfaceName, BaseInterfaceName, JuniperInterfaceName
from net_models.utils.CustomYamlDumper import CustomYamlDumper
from net_models.models.BaseModels import BaseNetModel
from net_models.models.interfaces import InterfaceServicePolicy

class TestDoubleQuotedString(unittest.TestCase):

    def test_01(self):

        test_value = "Foo"
        self.assertIsInstance(DoubleQoutedString(test_value), DoubleQoutedString)


class TestJinja2String(unittest.TestCase):

    TESTED_CLASS = Jinja2String

    def test_01(self):
        test_value = "{{ i_am_jinja_var }}"
        for validator in self.TESTED_CLASS.__get_validators__():
            validated = validator(test_value)
            self.assertIsInstance(validated, self.TESTED_CLASS)


    def test_dump_01(self):

        test_data = {
            "foo": self.TESTED_CLASS("{{ bar }}")
        }
        have_yaml = yaml.dump(data=test_data, Dumper=CustomYamlDumper)
        want_yaml = 'foo: "{{ bar }}"\n'
        self.assertEqual(have_yaml, want_yaml)

    def test_dump_02(self):
        test_data = {
            "foo": {
                "bar": self.TESTED_CLASS("{{ bar }}")
            }
        }
        have_yaml = yaml.dump(data=test_data, Dumper=CustomYamlDumper)
        want_yaml = 'foo:\n  bar: "{{ bar }}"\n'
        self.assertEqual(have_yaml, want_yaml)


    def test_model_dump(self):

        model = InterfaceServicePolicy(input=self.TESTED_CLASS("{{ PM_TEMPLATE_01 }}"))
        # print(type(model.input))
        # print(model.yaml())
        self.assertIsInstance(model.input, self.TESTED_CLASS)



class ModelWithInterface(BaseNetModel):

    interface: BaseInterfaceName

class TestBaseInterfaceName(unittest.TestCase):

    TEST_CLASS = BaseInterfaceName

    def test_init_subclass(self):

        print(self.TEST_CLASS._registry)

    def test_init(self):
        instance = BaseInterfaceName('Gi1/0/1')
        with self.subTest(msg="Is instance of BaseInterfaceName"):
            self.assertIsInstance(instance, BaseInterfaceName)
        with self.subTest(msg="Is instance of IosInterfaceName"):
            self.assertIsInstance(instance, IosInterfaceName)
        with self.subTest(msg="Can be __eq__ with plain string"):
            self.assertEqual('GigabitEthernet1/0/1', instance)
        with self.subTest(msg="Can be re searched"):
            m = re.search(pattern='Gi', string=instance)
            self.assertEqual('Gi', m.group(0))
        with self.subTest(msg="Can be JSON serialized"):
            pass
        with self.subTest(msg="Can be YAML serialized"):
            yaml.dump(data={})
        with self.subTest(msg="Extract Numbers"):
            print(instance.extract_numbers())
        with self.subTest(msg="Get Weight"):
            print(instance.get_weight())
        with self.subTest(msg="Get Index"):
            print(instance.get_index())

    def test_pydantic_parse(self):
        data = {
            "interface": "Gi1/0/1"
        }
        model = ModelWithInterface.parse_obj(data)
        self.assertIsInstance(model.interface, IosInterfaceName)

    def test_pydantic_parse_1(self):
        data = {
            "interface": "xe-1/0/1"
        }
        model = ModelWithInterface.parse_obj(data)
        self.assertIsInstance(model.interface, JuniperInterfaceName)



class TestIosInterfaceName(unittest.TestCase):

    def test_init(self):
        interface_names = ['GigabitEthernet1/0/1', 'Vlan1', 'Loopback0']
        for interface_name_str in interface_names:
            instance = IosInterfaceName(interface_name_str)
            model = None
            with self.subTest(msg=f"{interface_name_str} - Is instance of BaseInterfaceName"):
                self.assertIsInstance(instance, BaseInterfaceName)
            with self.subTest(msg=f"{interface_name_str} - Is instance of IosInterfaceName"):
                self.assertIsInstance(instance, IosInterfaceName)
            with self.subTest(msg=f"{interface_name_str} - Can be __eq__ with plain string"):
                self.assertEqual(interface_name_str, instance)
            with self.subTest(msg=f"{interface_name_str} - Can be JSON serialized"):
                model = ModelWithInterface(interface=interface_name_str)
                print(model.json())
            with self.subTest(msg=f"{interface_name_str} - Can be YAML serialized"):
                model = ModelWithInterface(interface=interface_name_str)
                print(model.yaml())


class TestJuniperInterfaceName(unittest.TestCase):

    def test_init(self):
        interface_names = ['xe-1/0/1']
        instance = JuniperInterfaceName('xe-1/0/1')
        with self.subTest(msg="Is instance of BaseInterfaceName"):
            self.assertIsInstance(instance, BaseInterfaceName)
        with self.subTest(msg="Is instance of IosInterfaceName"):
            self.assertIsInstance(instance, JuniperInterfaceName)
        with self.subTest(msg="Can be __eq__ with plain string"):
            self.assertEqual('xe-1/0/1', instance)
        with self.subTest(msg="Short can be __eq__ with plain string"):
            self.assertEqual('xe-1/0/1', instance.short)
        with self.subTest(msg="Can be JSON serialized"):
            pass
        with self.subTest(msg="Can be YAML serialized"):
            yaml.dump(data={})




if __name__ == '__main__':
    unittest.main()