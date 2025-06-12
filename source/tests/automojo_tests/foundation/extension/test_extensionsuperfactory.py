import sys
import types
import unittest
from unittest.mock import patch

from automojo.foundation.extension.extensionprotocolbase import ExtensionProtocolBase
from automojo.foundation.extension.extensionsuperfactory import ExtensionSuperFactory


class ExampleProtocol(ExtensionProtocolBase):
    ext_protocol_name = "example"

    def create_thing(self, value):
        raise NotImplementedError()

    def get_type(self):
        raise NotImplementedError()

    def get_many_types(self):
        raise NotImplementedError()


def make_factory(module_name: str, precedence: int, prefix: str):
    module = types.ModuleType(module_name)
    code = f"""
from automojo.foundation.extension.extensionfactory import ExtensionFactory
class {prefix}Factory(ExtensionFactory):
    PRECEDENCE = {precedence}
    ext_protocol_name = 'example'
    @staticmethod
    def create_thing(value):
        return '{prefix}:' + str(value)
    @staticmethod
    def get_type():
        return '{prefix}Type'
    @staticmethod
    def get_many_types():
        return ['{prefix}1', '{prefix}2']
"""
    exec(code, module.__dict__)
    sys.modules[module_name] = module
    return getattr(module, f"{prefix}Factory")


class TestExtensionSuperFactory(unittest.TestCase):
    def test_init_sorts_factories_by_precedence(self):
        fac_a = make_factory('mod_a', 2, 'A')
        fac_b = make_factory('mod_b', 1, 'B')
        mapping = {'mod_a': fac_a, 'mod_b': fac_b}
        with patch('automojo.foundation.extension.extensionsuperfactory.scan_amr_factories_namespace', return_value=[]), \
             patch('automojo.foundation.extension.extensionsuperfactory.load_and_set_extension_factory_type', side_effect=lambda n: mapping[n]):
            esf = ExtensionSuperFactory(['mod_a', 'mod_b'])
        self.assertEqual(esf.extension_factories, [fac_b, fac_a])

    def test_add_factory_module_appends_and_resorts(self):
        fac_a = make_factory('mod_a', 2, 'A')
        fac_b = make_factory('mod_b', 1, 'B')
        mapping = {'mod_a': fac_a, 'mod_b': fac_b}
        with patch('automojo.foundation.extension.extensionsuperfactory.scan_amr_factories_namespace', return_value=[]), \
             patch('automojo.foundation.extension.extensionsuperfactory.load_and_set_extension_factory_type', side_effect=lambda n: mapping[n]):
            esf = ExtensionSuperFactory(['mod_a'])
            esf.add_factory_module('mod_b')
        self.assertEqual(esf.factory_modules, ['mod_a', 'mod_b'])
        self.assertEqual(esf.extension_factories, [fac_b, fac_a])

    def test_create_instance_by_order_selects_last_match(self):
        fac_a = make_factory('mod_a', 1, 'A')
        fac_b = make_factory('mod_b', 2, 'B')
        mapping = {'mod_a': fac_a, 'mod_b': fac_b}
        with patch('automojo.foundation.extension.extensionsuperfactory.scan_amr_factories_namespace', return_value=[]), \
             patch('automojo.foundation.extension.extensionsuperfactory.load_and_set_extension_factory_type', side_effect=lambda n: mapping[n]):
            esf = ExtensionSuperFactory(['mod_a', 'mod_b'])
            inst = esf.create_instance_by_order(ExampleProtocol.create_thing, 'x')
        self.assertEqual(inst, 'B:x')

    def test_create_instance_for_each_collects_all_instances(self):
        fac_a = make_factory('mod_a', 1, 'A')
        fac_b = make_factory('mod_b', 2, 'B')
        mapping = {'mod_a': fac_a, 'mod_b': fac_b}
        with patch('automojo.foundation.extension.extensionsuperfactory.scan_amr_factories_namespace', return_value=[]), \
             patch('automojo.foundation.extension.extensionsuperfactory.load_and_set_extension_factory_type', side_effect=lambda n: mapping[n]):
            esf = ExtensionSuperFactory(['mod_a', 'mod_b'])
            inst_list = esf.create_instance_for_each(ExampleProtocol.create_thing, 'x')
        self.assertEqual(inst_list, ['A:x', 'B:x'])

    def test_get_override_types_by_order_returns_last_type(self):
        fac_a = make_factory('mod_a', 1, 'A')
        fac_b = make_factory('mod_b', 2, 'B')
        mapping = {'mod_a': fac_a, 'mod_b': fac_b}
        with patch('automojo.foundation.extension.extensionsuperfactory.scan_amr_factories_namespace', return_value=[]), \
             patch('automojo.foundation.extension.extensionsuperfactory.load_and_set_extension_factory_type', side_effect=lambda n: mapping[n]):
            esf = ExtensionSuperFactory(['mod_a', 'mod_b'])
            typ = esf.get_override_types_by_order(ExampleProtocol.get_type)
        self.assertEqual(typ, 'BType')

    def test_iterate_override_types_for_each_yields_expected_sequence(self):
        fac_a = make_factory('mod_a', 1, 'A')
        fac_b = make_factory('mod_b', 2, 'B')
        mapping = {'mod_a': fac_a, 'mod_b': fac_b}
        with patch('automojo.foundation.extension.extensionsuperfactory.scan_amr_factories_namespace', return_value=[]), \
             patch('automojo.foundation.extension.extensionsuperfactory.load_and_set_extension_factory_type', side_effect=lambda n: mapping[n]):
            esf = ExtensionSuperFactory(['mod_a', 'mod_b'])
            seq = list(esf.iterate_override_types_for_each(ExampleProtocol.get_many_types))
        self.assertEqual(seq, ['A1', 'A2', 'B1', 'B2'])

    def test_factory_modules_and_extension_factories_return_copies(self):
        fac_a = make_factory('mod_a', 1, 'A')
        mapping = {'mod_a': fac_a}
        with patch('automojo.foundation.extension.extensionsuperfactory.scan_amr_factories_namespace', return_value=[]), \
             patch('automojo.foundation.extension.extensionsuperfactory.load_and_set_extension_factory_type', side_effect=lambda n: mapping[n]):
            esf = ExtensionSuperFactory(['mod_a'])
            mods = esf.factory_modules
            exts = esf.extension_factories
            mods.append('new_mod')
            exts.clear()
        self.assertEqual(esf.factory_modules, ['mod_a'])
        self.assertEqual(esf.extension_factories, [fac_a])


if __name__ == '__main__':
    unittest.main()
