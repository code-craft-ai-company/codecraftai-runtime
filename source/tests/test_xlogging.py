import os, sys; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "source", "packages")))
import unittest

from automojo.foundation.xlogging.foundations import format_log_section_header, LOGGING_SECTION_MARKER_LENGTH

class TestXLogging(unittest.TestCase):

    def test_format_log_section_header(self):
        header = format_log_section_header('title')
        lines = header.strip().split('\n')
        self.assertEqual(len(lines[0]), LOGGING_SECTION_MARKER_LENGTH)
        self.assertIn('TITLE', lines[0])

if __name__ == '__main__':
    unittest.main()
