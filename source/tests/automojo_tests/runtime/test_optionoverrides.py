import os
import shutil
import tempfile
import unittest
from datetime import datetime

from automojo.runtime.optionoverrides import AM_RUNTIME_OPTION_OVERRIDES
from automojo.runtime.runtimevariables import RuntimeVariables, RuntimeVariablesDesc
from automojo.runtime.runtimecontextpaths import RuntimeContextPaths
from automojo.thisapp import wellknown
from automojo.thisapp.appvaraccessor import AppVarAccessor
from automojo.thisapp.thisapplication import ThisApplication


class OptionOverridesTestCase(unittest.TestCase):
    """Tests for functions in :mod:`automojo.runtime.optionoverrides`."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.context_store = {}

        AppVarAccessor._this_app = None

        self.this_app = ThisApplication(
            name="testruntime",
            logger_name="testruntime",
            log_basename="testruntime",
            presence_dir=self.temp_dir,
            log_directory=os.path.join(self.temp_dir, "logs"),
            settings_file=os.path.join(self.temp_dir, "settings.config"),
            extensions="",
            service_name=None,
            context_insert=self.context_store.__setitem__,
            from_establish_app_persona=True
        )
        wellknown.THISAPPLICATION_SINGLETON = self.this_app

        self.this_app.override_variable_value(RuntimeVariablesDesc.AM_PRESENCE_DIR, self.temp_dir)
        self.this_app.override_variable_value(RuntimeVariablesDesc.AM_LOG_DIRECTORY, os.path.join(self.temp_dir, "logs"))

    def tearDown(self):
        wellknown.THISAPPLICATION_SINGLETON = None
        AppVarAccessor._this_app = None
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _check_override(self, func, attr_name, ctx_path, value):
        func(value)
        self.assertEqual(getattr(RuntimeVariables, attr_name), value)
        self.assertEqual(self.context_store.get(ctx_path), value)

    def test_override_build_release(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_build_release,
            'AM_BUILD_RELEASE',
            RuntimeContextPaths.BUILD_RELEASE,
            'rel1'
        )

    def test_override_build_branch(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_build_branch,
            'AM_BUILD_BRANCH',
            RuntimeContextPaths.BUILD_BRANCH,
            'main'
        )

    def test_override_build_flavor(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_build_flavor,
            'AM_BUILD_FLAVOR',
            RuntimeContextPaths.BUILD_FLAVOR,
            'debug'
        )

    def test_override_build_name(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_build_name,
            'AM_BUILD_NAME',
            RuntimeContextPaths.BUILD_NAME,
            '1.0.0'
        )

    def test_override_build_url(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_build_url,
            'AM_BUILD_URL',
            RuntimeContextPaths.BUILD_URL,
            'https://build.example.com'
        )

    def test_override_debug_breakpoints(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_debug_breakpoints,
            'AM_DEBUG_BREAKPOINTS',
            RuntimeContextPaths.DEBUG_BREAKPOINTS,
            'startup'
        )

    def test_override_debug_debugger(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_debug_debugger,
            'AM_DEBUG_DEBUGGER',
            RuntimeContextPaths.DEBUG_DEBUGGER,
            'pdb'
        )

    def test_override_job_id(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_job_id,
            'AM_JOB_ID',
            RuntimeContextPaths.JOB_ID,
            'job123'
        )

    def test_override_job_initiator(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_job_initiator,
            'AM_JOB_INITIATOR',
            RuntimeContextPaths.JOB_INITIATOR,
            'tester'
        )

    def test_override_job_label(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_job_label,
            'AM_JOB_LABEL',
            RuntimeContextPaths.JOB_LABEL,
            'nightly'
        )

    def test_override_job_name(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_job_name,
            'AM_JOB_NAME',
            RuntimeContextPaths.JOB_NAME,
            'unit-tests'
        )

    def test_override_job_owner(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_job_owner,
            'AM_JOB_OWNER',
            RuntimeContextPaths.JOB_OWNER,
            'owner1'
        )

    def test_override_job_seed(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_job_seed,
            'AM_JOB_SEED',
            RuntimeContextPaths.JOB_SEED,
            'seed123'
        )

    def test_override_job_tag(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_job_tag,
            'AM_JOB_TAG',
            RuntimeContextPaths.JOB_TAG,
            'tagA'
        )

    def test_override_job_type(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_job_type,
            'AM_JOB_TYPE',
            RuntimeContextPaths.JOB_TYPE,
            'manual'
        )

    def test_override_loglevel_console(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_loglevel_console,
            'AM_LOG_LEVEL_CONSOLE',
            RuntimeContextPaths.LOGGING_LEVEL_CONSOLE,
            'INFO'
        )

    def test_override_loglevel_file(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_loglevel_file,
            'AM_LOG_LEVEL_FILE',
            RuntimeContextPaths.LOGGING_LEVEL_LOGFILE,
            'DEBUG'
        )

    def test_override_output_directory(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_output_directory,
            'AM_OUTPUT_DIRECTORY',
            RuntimeContextPaths.OUTPUT_DIRECTORY,
            '/tmp/output'
        )

    def test_override_pipeline_id(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_pipeline_id,
            'AM_PIPELINE_ID',
            RuntimeContextPaths.PIPELINE_ID,
            'pipe-001'
        )

    def test_override_pipeline_name(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_pipeline_name,
            'AM_PIPELINE_INSTANCE',
            RuntimeContextPaths.PIPELINE_INSTANCE,
            'pipe-inst-1'
        )

    def test_override_run_id(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_run_id,
            'AM_RUN_ID',
            RuntimeContextPaths.RUNID,
            'run-123'
        )

    def test_override_shared_store_directory(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_shared_store_directory,
            'AM_SHARED_STORE_DIRECTORY',
            RuntimeContextPaths.SHARED_STORE_DIRECTORY,
            '/tmp/shared'
        )

    def test_override_starttime(self):
        value = datetime(2020, 1, 1, 12, 0, 0)
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_starttime,
            'AM_STARTTIME',
            RuntimeContextPaths.STARTTIME,
            value.isoformat()
        )

    def test_override_testroot(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_testroot,
            'AM_TESTROOT',
            RuntimeContextPaths.TESTROOT,
            '/path/to/tests'
        )


if __name__ == '__main__':
    unittest.main()
