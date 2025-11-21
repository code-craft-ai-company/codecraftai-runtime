import importlib
import os
import unittest
from unittest import mock
from datetime import datetime
from uuid import UUID

from automojo.runtime import runtimevariables

class RuntimeVariablesTests(unittest.TestCase):

    def setUp(self):
        # Reload module to reset class attributes before each test
        self.runtimevariables = importlib.reload(runtimevariables)

    def test_get_runtime_seed_returns_expected_value(self):
        self.runtimevariables.AM_RUNTIME_VARIABLES.AM_JOB_SEED = 'myseed'
        self.assertEqual('myseed', self.runtimevariables.get_runtime_seed())

    def test_resolve_generates_seed_when_not_set(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            self.runtimevariables.resolve_runtime_variables()
        seed = self.runtimevariables.AM_RUNTIME_VARIABLES.AM_JOB_SEED
        self.assertNotEqual(seed, self.runtimevariables.DefaultValue.NotSet)
        # Validate seed is a uuid string
        UUID(seed)

    def test_resolve_uses_environment_seed(self):
        with mock.patch.dict(os.environ, {'AM_JOB_SEED': 'seed123'}, clear=True):
            self.runtimevariables.resolve_runtime_variables()
        self.assertEqual('seed123', self.runtimevariables.AM_RUNTIME_VARIABLES.AM_JOB_SEED)

    def test_resolve_parses_starttime_timestamp(self):
        start_time = '2025-01-02T03:04:05.123456'
        with mock.patch.dict(os.environ, {'AM_STARTTIME': start_time}, clear=True):
            self.runtimevariables.resolve_runtime_variables()
        expected = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%f')
        self.assertEqual(expected, self.runtimevariables.AM_RUNTIME_VARIABLES.AM_STARTTIME)

    def test_resolve_parses_shared_output_directory_bool(self):
        with mock.patch.dict(os.environ, {'AM_HAS_SHARED_OUTPUT_DIRECTORY': 'true'}, clear=True):
            self.runtimevariables.resolve_runtime_variables()
        self.assertTrue(self.runtimevariables.AM_RUNTIME_VARIABLES.AM_HAS_SHARED_OUTPUT_DIRECTORY)

if __name__ == '__main__':
    unittest.main()
