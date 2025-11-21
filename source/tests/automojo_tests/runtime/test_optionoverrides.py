import unittest
from datetime import datetime

from automojo.runtime.optionoverrides import AM_RUNTIME_OPTION_OVERRIDES
from automojo.runtime.runtimevariables import AM_RUNTIME_VARIABLES
from automojo.presence.contextpaths import ContextPaths
from automojo.presence import wellknown
from automojo.xmodules.xcollections.context import Context


class OptionOverridesTestCase(unittest.TestCase):
    """Tests for functions in :mod:`automojo.runtime.optionoverrides`."""

    RUNTIME_ATTRS = [
        'AM_BUILD_RELEASE',
        'AM_BUILD_BRANCH',
        'AM_BUILD_FLAVOR',
        'AM_BUILD_NAME',
        'AM_BUILD_URL',
        'AM_DEBUG_BREAKPOINTS',
        'AM_DEBUG_DEBUGGER',
        'AM_JOB_ID',
        'AM_JOB_INITIATOR',
        'AM_JOB_LABEL',
        'AM_JOB_NAME',
        'AM_JOB_OWNER',
        'AM_JOB_SEED',
        'AM_JOB_TAG',
        'AM_JOB_TYPE',
        'AM_LOG_LEVEL_CONSOLE',
        'AM_LOG_LEVEL_FILE',
        'AM_OUTPUT_DIRECTORY',
        'AM_PIPELINE_ID',
        'AM_PIPELINE_INSTANCE',
        'AM_PIPELINE_NAME',
        'AM_RUN_ID',
        'AM_SHARED_STORE_DIRECTORY',
        'AM_STARTTIME',
        'AM_TESTROOT',
    ]

    def setUp(self):
        self._old_ctx = wellknown.CONTEXT_SINGLETON
        wellknown.CONTEXT_SINGLETON = Context()
        self._saved = {attr: getattr(AM_RUNTIME_VARIABLES, attr) for attr in self.RUNTIME_ATTRS}

    def tearDown(self):
        for attr, value in self._saved.items():
            setattr(AM_RUNTIME_VARIABLES, attr, value)
        wellknown.CONTEXT_SINGLETON = self._old_ctx

    def _check_override(self, func, attr_name, ctx_path, value):
        func(value)
        ctx = wellknown.ContextSingleton()
        self.assertEqual(getattr(AM_RUNTIME_VARIABLES, attr_name), value)
        self.assertEqual(ctx.lookup(ctx_path), value)

    def test_override_build_release(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_build_release,
            'AM_BUILD_RELEASE',
            ContextPaths.BUILD_RELEASE,
            'rel1'
        )

    def test_override_build_branch(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_build_branch,
            'AM_BUILD_BRANCH',
            ContextPaths.BUILD_BRANCH,
            'main'
        )

    def test_override_build_flavor(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_build_flavor,
            'AM_BUILD_FLAVOR',
            ContextPaths.BUILD_FLAVOR,
            'debug'
        )

    def test_override_build_name(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_build_name,
            'AM_BUILD_NAME',
            ContextPaths.BUILD_NAME,
            '1.0.0'
        )

    def test_override_build_url(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_build_url,
            'AM_BUILD_URL',
            ContextPaths.BUILD_URL,
            'https://build.example.com'
        )

    def test_override_debug_breakpoints(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_debug_breakpoints,
            'AM_DEBUG_BREAKPOINTS',
            ContextPaths.DEBUG_BREAKPOINTS,
            ['startup']
        )

    def test_override_debug_debugger(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_debug_debugger,
            'AM_DEBUG_DEBUGGER',
            ContextPaths.DEBUG_DEBUGGER,
            'pdb'
        )

    def test_override_job_id(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_job_id,
            'AM_JOB_ID',
            ContextPaths.JOB_ID,
            'job123'
        )

    def test_override_job_initiator(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_job_initiator,
            'AM_JOB_INITIATOR',
            ContextPaths.JOB_INITIATOR,
            'tester'
        )

    def test_override_job_label(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_job_label,
            'AM_JOB_LABEL',
            ContextPaths.JOB_LABEL,
            'nightly'
        )

    def test_override_job_name(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_job_name,
            'AM_JOB_NAME',
            ContextPaths.JOB_NAME,
            'unit-tests'
        )

    def test_override_job_owner(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_job_owner,
            'AM_JOB_OWNER',
            ContextPaths.JOB_OWNER,
            'owner1'
        )

    def test_override_job_seed(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_job_seed,
            'AM_JOB_SEED',
            ContextPaths.JOB_SEED,
            'seed123'
        )

    def test_override_job_tag(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_job_tag,
            'AM_JOB_TAG',
            ContextPaths.JOB_TAG,
            'tagA'
        )

    def test_override_job_type(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_job_type,
            'AM_JOB_TYPE',
            ContextPaths.JOB_TYPE,
            'manual'
        )

    def test_override_loglevel_console(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_loglevel_console,
            'AM_LOG_LEVEL_CONSOLE',
            ContextPaths.LOGGING_LEVEL_CONSOLE,
            'INFO'
        )

    def test_override_loglevel_file(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_loglevel_file,
            'AM_LOG_LEVEL_FILE',
            ContextPaths.LOGGING_LEVEL_LOGFILE,
            'DEBUG'
        )

    def test_override_output_directory(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_output_directory,
            'AM_OUTPUT_DIRECTORY',
            ContextPaths.OUTPUT_DIRECTORY,
            '/tmp/output'
        )

    def test_override_pipeline_id(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_pipeline_id,
            'AM_PIPELINE_ID',
            ContextPaths.PIPELINE_ID,
            'pipe-001'
        )

    def test_override_pipeline_name(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_pipeline_name,
            'AM_PIPELINE_INSTANCE',
            ContextPaths.PIPELINE_INSTANCE,
            'pipe-inst-1'
        )

    def test_override_run_id(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_run_id,
            'AM_RUN_ID',
            ContextPaths.RUNID,
            'run-123'
        )

    def test_override_shared_store_directory(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_shared_store_directory,
            'AM_SHARED_STORE_DIRECTORY',
            ContextPaths.SHARED_STORE_DIRECTORY,
            '/tmp/shared'
        )

    def test_override_starttime(self):
        value = datetime(2020, 1, 1, 12, 0, 0)
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_starttime,
            'AM_STARTTIME',
            ContextPaths.STARTTIME,
            value
        )

    def test_override_testroot(self):
        self._check_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_testroot,
            'AM_TESTROOT',
            ContextPaths.TESTROOT,
            '/path/to/tests'
        )


if __name__ == '__main__':
    unittest.main()
