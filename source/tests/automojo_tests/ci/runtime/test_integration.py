import unittest

from automojo.presence.wellknown import CONTEXT_SINGLETON, ContextSingleton
from automojo.presence.contextpaths import ContextPaths

from automojo.ci.runtime.integration import (
    get_job_info,
    get_job_id,
    get_job_initiator,
    get_job_label,
    get_job_name,
    get_job_owner,
    get_job_type,
    get_job_venue,
    get_pipeline_info,
    get_pipeline_id,
    get_pipeline_instance,
    get_pipeline_name,
)


class TestIntegration(unittest.TestCase):

    def setUp(self):
        global CONTEXT_SINGLETON
        CONTEXT_SINGLETON = None
        self.ctx = ContextSingleton()

    def test_job_info_fetches_stored_data(self):
        info = {"id": "1"}
        self.ctx.insert(ContextPaths.JOB_INFO, info)
        self.assertDictEqual(get_job_info(), info)

    def test_job_field_getters_return_values(self):
        self.ctx.insert(ContextPaths.JOB_ID, "jid")
        self.ctx.insert(ContextPaths.JOB_INITIATOR, "init")
        self.ctx.insert(ContextPaths.JOB_LABEL, "label")
        self.ctx.insert(ContextPaths.JOB_NAME, "name")
        self.ctx.insert(ContextPaths.JOB_OWNER, "owner")
        self.ctx.insert(ContextPaths.JOB_TYPE, "type")
        self.ctx.insert(ContextPaths.JOB_VENUE, "venue")

        self.assertEqual(get_job_id(), "jid")
        self.assertEqual(get_job_initiator(), "init")
        self.assertEqual(get_job_label(), "label")
        self.assertEqual(get_job_name(), "name")
        self.assertEqual(get_job_owner(), "owner")
        self.assertEqual(get_job_type(), "type")
        self.assertEqual(get_job_venue(), "venue")

    def test_pipeline_field_getters_return_values(self):
        pipeline_info = {"foo": "bar"}
        self.ctx.insert(ContextPaths.PIPELINE_INFO, pipeline_info)
        self.ctx.insert(ContextPaths.PIPELINE_ID, "pid")
        self.ctx.insert(ContextPaths.PIPELINE_INSTANCE, "inst")
        self.ctx.insert(ContextPaths.PIPELINE_NAME, "pname")

        self.assertDictEqual(get_pipeline_info(), pipeline_info)
        self.assertEqual(get_pipeline_id(), "pid")
        self.assertEqual(get_pipeline_instance(), "inst")
        self.assertEqual(get_pipeline_name(), "pname")

    def test_getters_return_none_when_missing(self):
        self.assertIsNone(get_job_info())
        self.assertIsNone(get_job_id())
        self.assertIsNone(get_job_initiator())
        self.assertIsNone(get_job_label())
        self.assertIsNone(get_job_name())
        self.assertIsNone(get_job_owner())
        self.assertIsNone(get_job_type())
        self.assertIsNone(get_job_venue())
        self.assertIsNone(get_pipeline_info())
        self.assertIsNone(get_pipeline_id())
        self.assertIsNone(get_pipeline_instance())
        self.assertIsNone(get_pipeline_name())


if __name__ == "__main__":
    unittest.main()
