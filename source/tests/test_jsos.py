import os, sys; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "source", "packages")))
import unittest
import tempfile
import os
import json

from automojo.foundation.jsos import load_jsos_stream_from_file, CHAR_RECORD_SEPERATOR

class TestJSOS(unittest.TestCase):

    def test_load_jsos_stream_from_file(self):
        records = [{"a": 1}, {"b": 2}]
        with tempfile.NamedTemporaryFile('w', delete=False) as tf:
            for rec in records:
                tf.write(json.dumps(rec) + CHAR_RECORD_SEPERATOR)
            fname = tf.name
        try:
            loaded = load_jsos_stream_from_file(fname)
            self.assertEqual(loaded, records)
        finally:
            os.remove(fname)

if __name__ == '__main__':
    unittest.main()
