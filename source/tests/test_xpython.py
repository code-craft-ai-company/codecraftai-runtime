import os, sys; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "source", "packages")))
import unittest
import tempfile
import sys
import os

from automojo.foundation.xpython import in_python_path, prepend_python_path, append_python_path

class TestXPython(unittest.TestCase):

    def test_python_path_manipulation(self):
        with tempfile.TemporaryDirectory() as td:
            # Ensure not in path
            if td in sys.path:
                sys.path.remove(td)
            os.environ.pop('PYTHONPATH', None)

            self.assertFalse(in_python_path(td))
            prepend_python_path(td)
            self.assertTrue(sys.path[0].rstrip(os.sep) == td.rstrip(os.sep))
            self.assertTrue(in_python_path(td))

            append_python_path(td)  # should not duplicate
            self.assertEqual(sys.path.count(td), 1)

if __name__ == '__main__':
    unittest.main()
