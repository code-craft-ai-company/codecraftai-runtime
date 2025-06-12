
import unittest

from automojo.foundation.xconvert import parse_bool, safe_as_bytes, safe_as_str

class TestXConvert(unittest.TestCase):

    def test_parse_bool_valid(self):
        self.assertTrue(parse_bool("true"))
        self.assertTrue(parse_bool("yes"))
        self.assertTrue(parse_bool("1"))
        self.assertFalse(parse_bool("false"))
        self.assertFalse(parse_bool("no"))
        self.assertFalse(parse_bool("0"))

    def test_parse_bool_invalid(self):
        with self.assertRaises(ValueError):
            parse_bool("maybe")

    def test_safe_as_bytes_and_str(self):
        self.assertEqual(safe_as_bytes("abc"), b"abc")
        self.assertEqual(safe_as_str(b"abc"), "abc")

if __name__ == "__main__":
    unittest.main()
