import logging
import os
import sys
import tempfile
import types
import unittest

from automojo.foundation.extension.extensionfactory import ExtensionFactory
from automojo.foundation.extension.utilities import (
    import_by_name,
    is_subclass_of_extension_factory,
    load_and_set_extension_factory_type,
    scan_amr_factories_namespace,
    scan_for_descendant_modules,
)


class TestUtilities(unittest.TestCase):

    def test_import_by_name_returns_existing(self):
        dummy = types.ModuleType("dummy_mod")
        sys.modules["dummy_mod"] = dummy
        try:
            result = import_by_name("dummy_mod")
            self.assertIs(result, dummy)
        finally:
            del sys.modules["dummy_mod"]

    def test_import_by_name_imports_new_module(self):
        with tempfile.TemporaryDirectory() as td:
            modfile = os.path.join(td, "dmodule.py")
            with open(modfile, "w") as f:
                f.write("value = 42\n")
            sys.path.insert(0, td)
            try:
                result = import_by_name("dmodule")
                self.assertEqual(result.value, 42)
            finally:
                sys.path.pop(0)
                sys.modules.pop("dmodule", None)

    def test_is_subclass_of_extension_factory(self):
        class Child(ExtensionFactory):
            pass

        self.assertTrue(is_subclass_of_extension_factory(Child))
        self.assertFalse(is_subclass_of_extension_factory(ExtensionFactory))
        self.assertFalse(is_subclass_of_extension_factory(int))

    def _write_module(self, directory, name, contents):
        modfile = os.path.join(directory, f"{name}.py")
        with open(modfile, "w") as f:
            f.write(contents)
        return modfile

    def test_load_and_set_extension_factory_type_single(self):
        with tempfile.TemporaryDirectory() as td:
            self._write_module(
                td,
                "singlemod",
                "from automojo.foundation.extension.extensionfactory import ExtensionFactory\n"
                "class AF(ExtensionFactory):\n    pass\n",
            )
            sys.path.insert(0, td)
            try:
                cls = load_and_set_extension_factory_type("singlemod")
                self.assertIsNotNone(cls)
                self.assertEqual(cls.__name__, "AF")
            finally:
                sys.path.pop(0)
                sys.modules.pop("singlemod", None)

    def test_load_and_set_extension_factory_type_multiple(self):
        with tempfile.TemporaryDirectory() as td:
            self._write_module(
                td,
                "multimod",
                "from automojo.foundation.extension.extensionfactory import ExtensionFactory\n"
                "class AFactory(ExtensionFactory):\n    pass\n"
                "class BFactory(ExtensionFactory):\n    pass\n",
            )
            sys.path.insert(0, td)
            try:
                logger = logging.getLogger()
                with self.assertLogs(logger, level="WARNING") as cm:
                    cls = load_and_set_extension_factory_type("multimod")
                self.assertIn("Only one ExtensionPoints class is allowed", cm.output[0])
                self.assertEqual(cls.__name__, "AFactory")
            finally:
                sys.path.pop(0)
                sys.modules.pop("multimod", None)

    def test_load_and_set_extension_factory_type_none(self):
        with tempfile.TemporaryDirectory() as td:
            self._write_module(
                td,
                "emptymod",
                "value = 1\n",
            )
            sys.path.insert(0, td)
            try:
                logger = logging.getLogger()
                with self.assertLogs(logger, level="WARNING") as cm:
                    cls = load_and_set_extension_factory_type("emptymod")
                self.assertIn("without an `ExtensionPoints` derived class", cm.output[0])
                self.assertIsNone(cls)
            finally:
                sys.path.pop(0)
                sys.modules.pop("emptymod", None)

    def test_scan_amr_factories_namespace_discovers(self):
        with tempfile.TemporaryDirectory() as td:
            factories_dir = os.path.join(td, "automojo", "factories")
            os.makedirs(factories_dir)
            self._write_module(factories_dir, "example", "value = 5\n")
            sys.path.insert(0, td)
            try:
                modules = scan_amr_factories_namespace()
                self.assertIn("automojo.factories.example", modules)
            finally:
                sys.path.pop(0)
                sys.modules.pop("automojo.factories.example", None)

    def test_scan_for_descendant_modules_builds_names(self):
        with tempfile.TemporaryDirectory() as td:
            os.makedirs(os.path.join(td, "sub"))
            self._write_module(td, "a", "")
            self._write_module(os.path.join(td, "sub"), "b", "")
            mods = scan_for_descendant_modules(td, module_prefix="myprefix")
            self.assertIn("myprefix.a", mods)
            self.assertIn("myprefix.sub.b", mods)


if __name__ == "__main__":
    unittest.main()
