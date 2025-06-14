import unittest
from datetime import datetime

from automojo.foundation.collections import wellknown
from automojo.foundation.collections.contextpaths import ContextPaths
from automojo.foundation.runtime.optionoverrides import AM_RUNTIME_OPTION_OVERRIDES
from automojo.foundation.runtime.runtimevariables import AM_RUNTIME_VARIABLES


class TestOptionOverrides(unittest.TestCase):

    def setUp(self):
        wellknown.CONTEXT_SINGLETON = None
        self.ctx = wellknown.ContextSingleton()

    def test_context_singleton_reset_creates_new_instance(self):
        first_id = id(self.ctx)
        wellknown.CONTEXT_SINGLETON = None
        new_ctx = wellknown.ContextSingleton()
        self.assertNotEqual(first_id, id(new_ctx))


    def _verify_override(self, func, ctx_path, attr, value):
        func(value)
        self.assertEqual(self.ctx.lookup(ctx_path), value)
        self.assertEqual(getattr(AM_RUNTIME_VARIABLES, attr), value)

    def test_override_build_release(self):
        self._verify_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_build_release,
            ContextPaths.BUILD_RELEASE,
            "AM_BUILD_RELEASE",
            "rel",
        )

    def test_override_build_branch(self):
        self._verify_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_build_branch,
            ContextPaths.BUILD_BRANCH,
            "AM_BUILD_BRANCH",
            "branch",
        )

    def test_override_build_flavor(self):
        self._verify_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_build_flavor,
            ContextPaths.BUILD_FLAVOR,
            "AM_BUILD_FLAVOR",
            "flavor",
        )

    def test_override_build_name(self):
        self._verify_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_build_name,
            ContextPaths.BUILD_NAME,
            "AM_BUILD_NAME",
            "name",
        )

    def test_override_build_url(self):
        self._verify_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_build_url,
            ContextPaths.BUILD_URL,
            "AM_BUILD_URL",
            "http://example",
        )

    def test_override_debug_breakpoints(self):
        self._verify_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_debug_breakpoints,
            ContextPaths.DEBUG_BREAKPOINTS,
            "AM_DEBUG_BREAKPOINTS",
            ["bp1", "bp2"],
        )

    def test_override_debug_debugger(self):
        self._verify_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_debug_debugger,
            ContextPaths.DEBUG_DEBUGGER,
            "AM_DEBUG_DEBUGGER",
            "debugger",
        )

    def test_override_job_id(self):
        self._verify_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_job_id,
            ContextPaths.JOB_ID,
            "AM_JOB_ID",
            "jid",
        )

    def test_override_job_initiator(self):
        self._verify_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_job_initiator,
            ContextPaths.JOB_INITIATOR,
            "AM_JOB_INITIATOR",
            "initiator",
        )

    def test_override_job_label(self):
        self._verify_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_job_label,
            ContextPaths.JOB_LABEL,
            "AM_JOB_LABEL",
            "label",
        )

    def test_override_job_name(self):
        self._verify_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_job_name,
            ContextPaths.JOB_NAME,
            "AM_JOB_NAME",
            "jobname",
        )

    def test_override_job_owner(self):
        self._verify_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_job_owner,
            ContextPaths.JOB_OWNER,
            "AM_JOB_OWNER",
            "owner",
        )

    def test_override_job_seed(self):
        self._verify_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_job_seed,
            ContextPaths.JOB_SEED,
            "AM_JOB_SEED",
            "seed",
        )

    def test_override_job_tag(self):
        self._verify_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_job_tag,
            ContextPaths.JOB_TAG,
            "AM_JOB_TAG",
            "tag",
        )

    def test_override_job_type(self):
        self._verify_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_job_type,
            ContextPaths.JOB_TYPE,
            "AM_JOB_TYPE",
            "type",
        )

    def test_override_loglevel_console(self):
        self._verify_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_loglevel_console,
            ContextPaths.LOGGING_LEVEL_CONSOLE,
            "AM_LOG_LEVEL_CONSOLE",
            "DEBUG",
        )

    def test_override_loglevel_file(self):
        self._verify_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_loglevel_file,
            ContextPaths.LOGGING_LEVEL_LOGFILE,
            "AM_LOG_LEVEL_FILE",
            "INFO",
        )

    def test_override_output_directory(self):
        self._verify_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_output_directory,
            ContextPaths.OUTPUT_DIRECTORY,
            "AM_OUTPUT_DIRECTORY",
            "/tmp/out",
        )

    def test_override_pipeline_id(self):
        self._verify_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_pipeline_id,
            ContextPaths.PIPELINE_ID,
            "AM_PIPELINE_ID",
            "plid",
        )

    def test_override_run_id(self):
        self._verify_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_run_id,
            ContextPaths.RUNID,
            "AM_RUN_ID",
            "rid",
        )

    def test_override_shared_store_directory(self):
        self._verify_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_shared_store_directory,
            ContextPaths.SHARED_STORE_DIRECTORY,
            "AM_SHARED_STORE_DIRECTORY",
            "/tmp/store",
        )

    def test_override_starttime(self):
        self._verify_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_starttime,
            ContextPaths.STARTTIME,
            "AM_STARTTIME",
            datetime(2020, 1, 1),
        )

    def test_override_testroot(self):
        self._verify_override(
            AM_RUNTIME_OPTION_OVERRIDES.override_testroot,
            ContextPaths.TESTROOT,
            "AM_TESTROOT",
            "/tmp/tests",
        )

    def test_override_pipeline_name_sets_instance_due_to_duplicate(self):
        AM_RUNTIME_OPTION_OVERRIDES.override_pipeline_name('instance')
        self.assertEqual(self.ctx.lookup(ContextPaths.PIPELINE_INSTANCE), 'instance')
        self.assertEqual(AM_RUNTIME_VARIABLES.AM_PIPELINE_INSTANCE, 'instance')
        self.assertFalse(self.ctx.exists(ContextPaths.PIPELINE_NAME))

    def test_multiple_overrides_accumulate(self):
        AM_RUNTIME_OPTION_OVERRIDES.override_build_branch('b1')
        AM_RUNTIME_OPTION_OVERRIDES.override_job_id('jid1')
        AM_RUNTIME_OPTION_OVERRIDES.override_output_directory('/tmp/od')

        self.assertEqual(self.ctx.lookup(ContextPaths.BUILD_BRANCH), 'b1')
        self.assertEqual(self.ctx.lookup(ContextPaths.JOB_ID), 'jid1')
        self.assertEqual(self.ctx.lookup(ContextPaths.OUTPUT_DIRECTORY), '/tmp/od')

        self.assertEqual(AM_RUNTIME_VARIABLES.AM_BUILD_BRANCH, 'b1')
        self.assertEqual(AM_RUNTIME_VARIABLES.AM_JOB_ID, 'jid1')
        self.assertEqual(AM_RUNTIME_VARIABLES.AM_OUTPUT_DIRECTORY, '/tmp/od')


if __name__ == '__main__':
    unittest.main()
