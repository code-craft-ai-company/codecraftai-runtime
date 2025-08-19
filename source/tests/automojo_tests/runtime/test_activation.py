import os
import unittest
from unittest import mock
from datetime import datetime

from automojo.runtime import activation
from automojo.xmodules.xdatetime import DATETIME_FORMAT_FILESYSTEM
from automojo.runtime.enumerations import ActivationProfile, JobType
from automojo.runtime.runtimevariables import AM_RUNTIME_VARIABLES


class ActivationProfileTests(unittest.TestCase):

    def setUp(self):
        # Save environment and runtime variable state
        self._saved_env = os.environ.copy()
        self._saved_profile = AM_RUNTIME_VARIABLES.AM_ACTIVATION_PROFILE
        self._saved_job_type = AM_RUNTIME_VARIABLES.AM_JOB_TYPE
        self._saved_output_dir = AM_RUNTIME_VARIABLES.AM_OUTPUT_DIRECTORY
        self._saved_console_level = AM_RUNTIME_VARIABLES.AM_LOG_LEVEL_CONSOLE
        self._saved_service_name = AM_RUNTIME_VARIABLES.AM_SERVICE_NAME

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self._saved_env)
        AM_RUNTIME_VARIABLES.AM_ACTIVATION_PROFILE = self._saved_profile
        AM_RUNTIME_VARIABLES.AM_JOB_TYPE = self._saved_job_type
        AM_RUNTIME_VARIABLES.AM_OUTPUT_DIRECTORY = self._saved_output_dir
        AM_RUNTIME_VARIABLES.AM_LOG_LEVEL_CONSOLE = self._saved_console_level
        AM_RUNTIME_VARIABLES.AM_SERVICE_NAME = self._saved_service_name

    def test_activate_runtime_dispatches(self):
        with mock.patch.object(activation, 'activate_profile_console') as mock_console:
            activation.activate_runtime(profile=ActivationProfile.Console)
            mock_console.assert_called_once()

    def test_activate_profile_service_requires_service_name(self):
        AM_RUNTIME_VARIABLES.AM_SERVICE_NAME = None
        with self.assertRaises(activation.ConfigurationError):
            activation.activate_profile_service()

    def test_activate_profile_service_uses_environment_name(self):
        AM_RUNTIME_VARIABLES.AM_SERVICE_NAME = None
        os.environ[activation.AM_RUNTIME_VARNAMES.AM_SERVICE_NAME] = 'testsvc'
        fake_jobtype = mock.Mock()
        fake_jobtype.Service = mock.Mock(value='Service')
        with mock.patch.object(activation, 'JobType', fake_jobtype), \
             mock.patch.object(activation, 'activate_service_logging') as mlog, \
             mock.patch.object(activation, 'activate_profile_common') as mcommon:
            activation.activate_profile_service()
            self.assertEqual(AM_RUNTIME_VARIABLES.AM_SERVICE_NAME, 'testsvc')
            self.assertIn('testsvc', AM_RUNTIME_VARIABLES.AM_OUTPUT_DIRECTORY)
            mcommon.assert_called_once()
            mlog.assert_called_once()


class ActivationCommonTests(unittest.TestCase):

    def setUp(self):
        self.ctx = activation.ContextSingleton()
        self.ctx._store.clear()
        self._saved_output = AM_RUNTIME_VARIABLES.AM_OUTPUT_DIRECTORY
        self._saved_job_id = AM_RUNTIME_VARIABLES.AM_JOB_ID
        self._saved_starttime = AM_RUNTIME_VARIABLES.AM_STARTTIME

    def tearDown(self):
        self.ctx._store.clear()
        AM_RUNTIME_VARIABLES.AM_OUTPUT_DIRECTORY = self._saved_output
        AM_RUNTIME_VARIABLES.AM_JOB_ID = self._saved_job_id
        AM_RUNTIME_VARIABLES.AM_STARTTIME = self._saved_starttime

    def test_activate_profile_job_output_directory_template(self):
        AM_RUNTIME_VARIABLES.AM_OUTPUT_DIRECTORY = '/tmp/out_%(starttime)s'
        fixed_time = datetime(2020, 1, 1, 1, 1, 1)
        AM_RUNTIME_VARIABLES.AM_STARTTIME = fixed_time
        activation.activate_profile_job(job_type=JobType.TestRun)
        expected = '/tmp/out_' + fixed_time.strftime(DATETIME_FORMAT_FILESYSTEM)
        self.assertEqual(self.ctx.lookup(activation.ContextPaths.OUTPUT_DIRECTORY), expected)

