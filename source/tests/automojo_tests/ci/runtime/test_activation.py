import os
import tempfile
import unittest

from datetime import datetime
from unittest.mock import patch
from logging import FileHandler
from logging.handlers import RotatingFileHandler

from automojo.errors.exceptions import ConfigurationError, SemanticError

from automojo.xmodules.xlogging.levels import LogLevel

from automojo.ci.runtime import wellknown
from automojo.ci.runtime.contextpaths import ContextPaths

from automojo.ci.runtime.activation import (
    activate_profile_command,
    activate_profile_console,
    activate_profile_service,
    activate_profile_testrun,
    activate_profile_common,
    activate_runtime,
)
from automojo.ci.runtime.enumerations import ActivationProfile, JobType
from automojo.ci.runtime.runtimevariables import AM_RUNTIME_VARIABLES, DefaultValue
from automojo.ci.runtime.variablenames import AM_RUNTIME_VARNAMES
from automojo.ci.xlogging.foundations import LoggingDefaults


class ActivationTestCase(unittest.TestCase):
    def setUp(self):
        wellknown.CONTEXT_SINGLETON = None
        self.ctx = wellknown.ContextSingleton()
        self._orig_env = os.environ.copy()
        self._orig_runtime = {
            k: getattr(AM_RUNTIME_VARIABLES, k)
            for k in dir(AM_RUNTIME_VARIABLES)
            if k.isupper()
        }
        self.temp_presence = tempfile.mkdtemp()
        AM_RUNTIME_VARIABLES.AM_PRESENCE_DIRECTORY = self.temp_presence
        AM_RUNTIME_VARIABLES.AM_OUTPUT_DIRECTORY = None
        AM_RUNTIME_VARIABLES.AM_ACTIVATION_PROFILE = None
        AM_RUNTIME_VARIABLES.AM_LOG_LEVEL_CONSOLE = None
        AM_RUNTIME_VARIABLES.AM_INTERACTIVE_CONSOLE = False
        AM_RUNTIME_VARIABLES.AM_JOB_ID = DefaultValue.NotSet
        AM_RUNTIME_VARIABLES.AM_STARTTIME = datetime(2024, 1, 1)

    def tearDown(self):
        for key in list(os.environ.keys()):
            if key not in self._orig_env:
                os.environ.pop(key)
        os.environ.update(self._orig_env)
        for k, v in self._orig_runtime.items():
            setattr(AM_RUNTIME_VARIABLES, k, v)
        global CONTEXT_SINGLETON
        CONTEXT_SINGLETON = None


class TestActivationProfiles(ActivationTestCase):
    @patch('automojo.foundation.xlogging.foundations.logging_initialize')
    def test_activate_profile_command(self, mock_log_init):
        activate_profile_command()
        self.assertEqual(AM_RUNTIME_VARIABLES.AM_ACTIVATION_PROFILE, ActivationProfile.Command)
        self.assertEqual(AM_RUNTIME_VARIABLES.AM_JOB_TYPE, JobType.Unknown.value)
        self.assertIn(AM_RUNTIME_VARIABLES.AM_JOB_TYPE, os.environ[AM_RUNTIME_VARNAMES.AM_JOB_TYPE])
        self.assertTrue(os.path.isdir(AM_RUNTIME_VARIABLES.AM_OUTPUT_DIRECTORY))
        self.assertIs(LoggingDefaults.DefaultFileLoggingHandler, FileHandler)
        mock_log_init.assert_called_once()


    @patch('automojo.foundation.xlogging.foundations.logging_initialize')
    def test_command_profile_double_activation(self, mock_log_init):
        activate_profile_command()
        with self.assertRaises(SemanticError):
            activate_profile_command()
        mock_log_init.assert_called_once()

    @patch('automojo.foundation.xlogging.foundations.logging_initialize')
    def test_console_profile_interactive(self, mock_log_init):
        AM_RUNTIME_VARIABLES.AM_INTERACTIVE_CONSOLE = True
        activate_profile_console()
        self.assertEqual(AM_RUNTIME_VARIABLES.AM_ACTIVATION_PROFILE, ActivationProfile.Console)
        self.assertEqual(AM_RUNTIME_VARIABLES.AM_LOG_LEVEL_CONSOLE, LogLevel.QUIET)
        self.assertEqual(os.environ[AM_RUNTIME_VARNAMES.AM_LOG_LEVEL_CONSOLE], str(LogLevel.QUIET))
        self.assertEqual(os.environ[AM_RUNTIME_VARNAMES.AM_JOB_TYPE], JobType.Console.value)
        self.assertTrue(os.path.isdir(AM_RUNTIME_VARIABLES.AM_OUTPUT_DIRECTORY))
        self.assertIs(LoggingDefaults.DefaultFileLoggingHandler, RotatingFileHandler)
        mock_log_init.assert_called_once()

    @patch('automojo.foundation.xlogging.foundations.logging_initialize')
    def test_console_profile_noninteractive(self, mock_log_init):
        AM_RUNTIME_VARIABLES.AM_INTERACTIVE_CONSOLE = False
        AM_RUNTIME_VARIABLES.AM_LOG_LEVEL_CONSOLE = LogLevel.ERROR
        activate_profile_console()
        self.assertEqual(AM_RUNTIME_VARIABLES.AM_ACTIVATION_PROFILE, ActivationProfile.Console)
        self.assertEqual(AM_RUNTIME_VARIABLES.AM_LOG_LEVEL_CONSOLE, LogLevel.ERROR)
        self.assertFalse(AM_RUNTIME_VARNAMES.AM_LOG_LEVEL_CONSOLE in os.environ)
        self.assertIs(LoggingDefaults.DefaultFileLoggingHandler, RotatingFileHandler)
        mock_log_init.assert_called_once()

    @patch('automojo.foundation.xlogging.foundations.logging_initialize')
    def test_console_profile_double_activation(self, mock_log_init):
        activate_profile_console()
        with self.assertRaises(SemanticError):
            activate_profile_console()
        mock_log_init.assert_called_once()

    @patch('automojo.foundation.xlogging.foundations.logging_initialize')
    def test_service_profile_without_service_name(self, mock_log_init):
        AM_RUNTIME_VARIABLES.AM_SERVICE_NAME = None
        if AM_RUNTIME_VARNAMES.AM_SERVICE_NAME in os.environ:
            os.environ.pop(AM_RUNTIME_VARNAMES.AM_SERVICE_NAME)
        with self.assertRaises(ConfigurationError):
            activate_profile_service()
        mock_log_init.assert_not_called()

    @patch('automojo.foundation.xlogging.foundations.logging_initialize')
    def test_service_profile_with_service_name(self, mock_log_init):
        AM_RUNTIME_VARIABLES.AM_SERVICE_NAME = 'svc'
        activate_profile_service()
        self.assertEqual(AM_RUNTIME_VARIABLES.AM_ACTIVATION_PROFILE, ActivationProfile.Service)
        self.assertEqual(AM_RUNTIME_VARIABLES.AM_JOB_TYPE, JobType.Service.value)
        expected_dir = os.path.join(self.temp_presence, 'services', 'svc')
        self.assertEqual(AM_RUNTIME_VARIABLES.AM_OUTPUT_DIRECTORY, expected_dir)
        self.assertEqual(os.environ[AM_RUNTIME_VARNAMES.AM_OUTPUT_DIRECTORY], expected_dir)
        self.assertIs(LoggingDefaults.DefaultFileLoggingHandler, RotatingFileHandler)
        mock_log_init.assert_called_once()

    @patch('automojo.foundation.xlogging.foundations.logging_initialize')
    def test_testrun_profile_activation(self, mock_log_init):
        activate_profile_testrun()
        self.assertEqual(AM_RUNTIME_VARIABLES.AM_ACTIVATION_PROFILE, ActivationProfile.TestRun)
        self.assertEqual(AM_RUNTIME_VARIABLES.AM_LOG_LEVEL_CONSOLE, LogLevel.WARNING)
        self.assertEqual(AM_RUNTIME_VARIABLES.AM_JOB_TYPE, JobType.TestRun.value)
        self.assertEqual(os.environ[AM_RUNTIME_VARNAMES.AM_LOG_LEVEL_CONSOLE], str(LogLevel.WARNING))
        self.assertEqual(os.environ[AM_RUNTIME_VARNAMES.AM_JOB_TYPE], JobType.TestRun.value)
        mock_log_init.assert_called_once()

    @patch('automojo.foundation.xlogging.foundations.logging_initialize')
    def test_testrun_profile_double_activation(self, mock_log_init):
        activate_profile_testrun()
        with self.assertRaises(RuntimeError):
            activate_profile_testrun()
        mock_log_init.assert_called_once()

    def test_common_activation_generates_job_id_and_result_path(self):
        AM_RUNTIME_VARIABLES.AM_JOB_TYPE = JobType.Console
        AM_RUNTIME_VARIABLES.AM_JOB_ID = DefaultValue.NotSet
        activate_profile_common()
        jid = AM_RUNTIME_VARIABLES.AM_JOB_ID
        self.assertNotEqual(jid, DefaultValue.NotSet)
        self.assertEqual(self.ctx.lookup(ContextPaths.JOB_ID), jid)
        resdir = self.ctx.lookup(ContextPaths.RESULT_PATH_FOR_CONSOLE)
        self.assertTrue(resdir.startswith(os.path.join(self.temp_presence, 'results', 'console')))
        self.assertEqual(self.ctx.lookup(ContextPaths.OUTPUT_DIRECTORY), resdir)

    def test_common_activation_result_path_by_jobtype(self):
        for jobtype, ctx_path in (
            (JobType.Console, ContextPaths.RESULT_PATH_FOR_CONSOLE),
            (JobType.Orchestration, ContextPaths.RESULT_PATH_FOR_ORCHESTRATION),
            (JobType.Service, ContextPaths.RESULT_PATH_FOR_SERVICES),
            (JobType.TestRun, ContextPaths.RESULT_PATH_FOR_TESTS),
        ):
            with self.subTest(jobtype=jobtype):
                AM_RUNTIME_VARIABLES.AM_JOB_TYPE = jobtype
                AM_RUNTIME_VARIABLES.AM_OUTPUT_DIRECTORY = None
                activate_profile_common()
                outdir = self.ctx.lookup(ctx_path)
                self.assertTrue(outdir.startswith(os.path.join(self.temp_presence, 'results')))
                self.assertEqual(self.ctx.lookup(ContextPaths.OUTPUT_DIRECTORY), outdir)
                self.ctx = wellknown.ContextSingleton()

    @patch('automojo.foundation.xlogging.foundations.logging_initialize')
    def test_activate_runtime_dispatcher_and_unknown(self, mock_log_init):
        activate_runtime(profile=ActivationProfile.Command)
        self.assertEqual(AM_RUNTIME_VARIABLES.AM_ACTIVATION_PROFILE, ActivationProfile.Command)
        mock_log_init.assert_called_once()
        AM_RUNTIME_VARIABLES.AM_ACTIVATION_PROFILE = None
        mock_log_init.reset_mock()
        with self.assertRaises(SemanticError):
            activate_runtime(profile='bogus')
        mock_log_init.assert_not_called()


if __name__ == '__main__':
    unittest.main()
