import importlib
import io
import os
import sys
import unittest
from unittest.mock import patch

from automojo.foundation.runtime.enumerations import ActivationProfile, JobType
from automojo.foundation.runtime.variablenames import AM_RUNTIME_VARNAMES
from automojo.foundation.xlogging.levels import LogLevel
from automojo.errors.exceptions import ConfigurationError, SemanticError

class TestActivation(unittest.TestCase):

    def setUp(self):
        import automojo.foundation.collections.wellknown as wellknown
        self._prior_context = wellknown.CONTEXT_SINGLETON
        wellknown.CONTEXT_SINGLETON = None

        import automojo.foundation.runtime.runtimevariables as runtimevariables
        import automojo.foundation.runtime.activation as activation
        import automojo.foundation.xlogging.foundations as foundations
        self.runtimevariables = importlib.reload(runtimevariables)
        self.activation = importlib.reload(activation)
        self.foundations = importlib.reload(foundations)

        for var in (
            AM_RUNTIME_VARNAMES.AM_JOB_TYPE,
            AM_RUNTIME_VARNAMES.AM_OUTPUT_DIRECTORY,
            AM_RUNTIME_VARNAMES.AM_LOG_LEVEL_CONSOLE,
            AM_RUNTIME_VARNAMES.AM_SERVICE_NAME,
        ):
            os.environ.pop(var, None)

    def tearDown(self):
        import automojo.foundation.collections.wellknown as wellknown
        wellknown.CONTEXT_SINGLETON = self._prior_context

        importlib.reload(self.runtimevariables)
        for var in (
            AM_RUNTIME_VARNAMES.AM_JOB_TYPE,
            AM_RUNTIME_VARNAMES.AM_OUTPUT_DIRECTORY,
            AM_RUNTIME_VARNAMES.AM_LOG_LEVEL_CONSOLE,
            AM_RUNTIME_VARNAMES.AM_SERVICE_NAME,
        ):
            os.environ.pop(var, None)

    def test_activate_profile_command_basic(self):
        with patch('automojo.foundation.xlogging.foundations.logging_initialize') as mock_init:
            self.activation.activate_profile_command()
            from automojo.foundation.xlogging.foundations import LoggingDefaults
            import logging
            self.assertIs(LoggingDefaults.DefaultFileLoggingHandler, logging.FileHandler)
            self.assertEqual(
                self.runtimevariables.AM_RUNTIME_VARIABLES.AM_ACTIVATION_PROFILE,
                ActivationProfile.Command
            )
            self.assertEqual(
                os.environ[AM_RUNTIME_VARNAMES.AM_JOB_TYPE],
                JobType.Unknown.value
            )
            self.assertTrue(
                os.path.isdir(self.runtimevariables.AM_RUNTIME_VARIABLES.AM_OUTPUT_DIRECTORY)
            )
            mock_init.assert_called_once()

    def test_activate_profile_console_interactive(self):
        self.runtimevariables.AM_RUNTIME_VARIABLES.AM_INTERACTIVE_CONSOLE = True
        self.runtimevariables.AM_RUNTIME_VARIABLES.AM_LOG_LEVEL_CONSOLE = None
        fake_out = io.StringIO()
        with patch('automojo.foundation.xlogging.foundations.logging_initialize') as mock_init, \
             patch.object(sys, 'stdout', fake_out):
            self.activation.activate_profile_console()
            output = fake_out.getvalue()
        from automojo.foundation.xlogging.foundations import LoggingDefaults
        import logging
        self.assertIs(LoggingDefaults.DefaultFileLoggingHandler, logging.handlers.RotatingFileHandler)
        self.assertIn('OUTPUT FOLDER:', output)
        self.assertEqual(os.environ[AM_RUNTIME_VARNAMES.AM_LOG_LEVEL_CONSOLE], str(LogLevel.QUIET))
        self.assertEqual(os.environ[AM_RUNTIME_VARNAMES.AM_JOB_TYPE], JobType.Console.value)
        self.assertEqual(
            self.runtimevariables.AM_RUNTIME_VARIABLES.AM_ACTIVATION_PROFILE,
            ActivationProfile.Console
        )
        mock_init.assert_called_once()

    def test_activate_profile_console_noninteractive(self):
        self.runtimevariables.AM_RUNTIME_VARIABLES.AM_INTERACTIVE_CONSOLE = False
        with patch('automojo.foundation.xlogging.foundations.logging_initialize') as mock_init:
            self.activation.activate_profile_console()
        from automojo.foundation.xlogging.foundations import LoggingDefaults
        import logging
        self.assertIs(LoggingDefaults.DefaultFileLoggingHandler, logging.handlers.RotatingFileHandler)
        self.assertNotIn(AM_RUNTIME_VARNAMES.AM_LOG_LEVEL_CONSOLE, os.environ)
        self.assertEqual(os.environ[AM_RUNTIME_VARNAMES.AM_JOB_TYPE], JobType.Console.value)
        self.assertEqual(
            self.runtimevariables.AM_RUNTIME_VARIABLES.AM_ACTIVATION_PROFILE,
            ActivationProfile.Console
        )
        mock_init.assert_called_once()

    def test_activate_profile_service_requires_name(self):
        with patch('automojo.foundation.xlogging.foundations.logging_initialize'):
            with self.assertRaises(ConfigurationError):
                self.activation.activate_profile_service()

            # Reset activation profile and provide the service name
            self.runtimevariables.AM_RUNTIME_VARIABLES.AM_ACTIVATION_PROFILE = None
            self.runtimevariables.AM_RUNTIME_VARIABLES.AM_SERVICE_NAME = 'svc'

            self.activation.activate_profile_service()
            from automojo.foundation.xlogging.foundations import LoggingDefaults
            import logging
            self.assertIs(LoggingDefaults.DefaultFileLoggingHandler, logging.handlers.RotatingFileHandler)
            outdir = os.environ[AM_RUNTIME_VARNAMES.AM_OUTPUT_DIRECTORY]
            self.assertIn(
                os.path.join('services', 'svc'),
                os.path.normpath(outdir)
            )

    def test_activate_profile_testrun_sets_warning_level(self):
        with patch('automojo.foundation.xlogging.foundations.logging_initialize') as mock_init:
            self.activation.activate_profile_testrun()
            from automojo.foundation.xlogging.foundations import LoggingDefaults
            import logging
            self.assertIs(LoggingDefaults.DefaultFileLoggingHandler, logging.FileHandler)
            self.assertEqual(os.environ[AM_RUNTIME_VARNAMES.AM_LOG_LEVEL_CONSOLE], str(LogLevel.WARNING))
            self.assertEqual(os.environ[AM_RUNTIME_VARNAMES.AM_JOB_TYPE], JobType.TestRun.value)
            self.assertEqual(
                self.runtimevariables.AM_RUNTIME_VARIABLES.AM_ACTIVATION_PROFILE,
                ActivationProfile.TestRun
            )
            mock_init.assert_called_once()

    def test_activate_runtime_dispatch(self):
        with patch.object(self.activation, 'activate_profile_command') as mock_cmd, \
             patch.object(self.activation, 'activate_profile_console') as mock_console, \
             patch.object(self.activation, 'activate_profile_service') as mock_service, \
             patch.object(self.activation, 'activate_profile_testrun') as mock_test:
            self.activation.activate_runtime(profile=ActivationProfile.Command)
            mock_cmd.assert_called_once()
            self.activation.activate_runtime(profile=ActivationProfile.Console)
            mock_console.assert_called_once()
            self.activation.activate_runtime(profile=ActivationProfile.Service)
            mock_service.assert_called_once()
            self.activation.activate_runtime(profile=ActivationProfile.TestRun)
            mock_test.assert_called_once()
            with self.assertRaises(SemanticError):
                self.activation.activate_runtime(profile=None)

if __name__ == '__main__':
    unittest.main()
