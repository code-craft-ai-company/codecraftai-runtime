import os, sys; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "source", "packages")))
import unittest
import os
import tempfile

from automojo.foundation.fspath import (
    expand_path,
    get_expanded_path,
    normalize_name_for_path,
    ensure_directory_is_package
)

class TestFSPath(unittest.TestCase):

    def test_expand_and_get_expanded_path(self):
        with tempfile.TemporaryDirectory() as td:
            os.environ['TDIR'] = td
            p1 = expand_path('~/')
            self.assertTrue(os.path.isdir(p1))
            p2 = expand_path('$TDIR/file')
            self.assertEqual(p2, os.path.join(td, 'file'))
            p3 = get_expanded_path('~/dummy')
            self.assertEqual(p3, os.path.abspath(os.path.expanduser('~/dummy')))

    def test_normalize_name_for_path(self):
        self.assertEqual(normalize_name_for_path('Test:Value,Name'), 'TestValueName')

    def test_ensure_directory_is_package(self):
        with tempfile.TemporaryDirectory() as td:
            ensure_directory_is_package(td)
            self.assertTrue(os.path.exists(os.path.join(td, '__init__.py')))

if __name__ == '__main__':
    unittest.main()
