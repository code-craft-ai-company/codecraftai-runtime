import os, sys; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "source", "packages")))
import unittest
from automojo.foundation.xformatting import (
    indent_line, indent_lines, indent_lines_list, split_and_indent_lines,
    format_command_result
)

class TestXFormatting(unittest.TestCase):

    def test_indent_helpers(self):
        self.assertEqual(indent_line('abc', 2, 2), '    abc')
        self.assertEqual(indent_lines('a\nb', 1, 2), '  a\n  b')
        self.assertEqual(indent_lines_list(['a', 'b'], 1, 2), ['  a', '  b'])
        self.assertEqual(split_and_indent_lines('  a\n  b', 1, 2), ['  a', '  b'])

    def test_format_command_result(self):
        msg = format_command_result('MSG', 'cmd', 0, 'out', 'err', [0], 'TARGET')
        self.assertIn('MSG', msg)
        self.assertIn('COMMAND cmd', msg)
        self.assertIn('STATUS: 0', msg)
        self.assertIn('EXPECTED: [0]', msg)
        self.assertIn('TARGET: TARGET', msg)
        self.assertIn('STDOUT:', msg)
        self.assertIn('STDERR:', msg)

if __name__ == '__main__':
    unittest.main()
