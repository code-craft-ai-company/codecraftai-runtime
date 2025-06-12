import os
import sys
import unittest
import tempfile

from automojo.foundation.extension.dynamicextension import (
    DynamicExtension,
    collect_extensions_under_code_container,
    collect_extensions_under_folder,
    generate_extension_key,
)

class TestDynamicExtension(unittest.TestCase):

    def test_collect_extensions_and_key(self):
        with tempfile.TemporaryDirectory() as td:
            pkgdir = os.path.join(td, 'pkg')
            os.makedirs(pkgdir)
            with open(os.path.join(pkgdir, '__init__.py'), 'w'):
                pass
            with open(os.path.join(pkgdir, 'ext.py'), 'w') as f:
                f.write('from automojo.foundation.extension.dynamicextension import DynamicExtension\n'
                        'class Child(DynamicExtension):\n    pass\n')
            sys.path.insert(0, td)
            try:
                import importlib
                pkg = importlib.import_module('pkg')
                exts = collect_extensions_under_code_container(pkg, DynamicExtension)
                names = [name for name, _ in exts]
                self.assertIn('Child', names)

                exts2 = collect_extensions_under_folder(pkgdir, DynamicExtension, module_base='pkg')
                names2 = [name for name, _ in exts2]
                self.assertIn('Child', names2)

                key = generate_extension_key('a', 'b', 'c')
                self.assertEqual(key, 'a/b/c')
            finally:
                sys.path.pop(0)

if __name__ == '__main__':
    unittest.main()
