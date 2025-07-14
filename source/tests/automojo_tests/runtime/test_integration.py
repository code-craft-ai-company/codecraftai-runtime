import unittest

from automojo.presence import wellknown
from automojo.presence.contextpaths import ContextPaths

from automojo.runtime import integration


class TestIntegration(unittest.TestCase):

    def setUp(self):
        wellknown.CONTEXT_SINGLETON = None
        self.ctx = wellknown.ContextSingleton()

    def test_get_job_info_returns_none_when_unset(self):
        self.assertIsNone(integration.get_job_info())

    def test_get_job_info_returns_cursor(self):
        info = {"id": "1"}
        self.ctx.insert(ContextPaths.JOB_INFO, info)
        cursor = integration.get_job_info()
        self.assertEqual(cursor.value, info)

    def test_get_job_id_returns_none_when_unset(self):
        self.assertIsNone(integration.get_job_id())

    def test_get_job_id_returns_value(self):
        self.ctx.insert(ContextPaths.JOB_ID, "jid")
        value = integration.get_job_id()
        self.assertEqual(value, "jid")

    def test_get_job_initiator_returns_none_when_unset(self):
        self.assertIsNone(integration.get_job_initiator())

    def test_get_job_initiator_returns_value(self):
        self.ctx.insert(ContextPaths.JOB_INITIATOR, "init")
        value = integration.get_job_initiator()
        self.assertEqual(value, "init")

    def test_get_job_label_returns_none_when_unset(self):
        self.assertIsNone(integration.get_job_label())

    def test_get_job_label_returns_value(self):
        self.ctx.insert(ContextPaths.JOB_LABEL, "label")
        value = integration.get_job_label()
        self.assertEqual(value, "label")

    def test_get_job_name_returns_none_when_unset(self):
        self.assertIsNone(integration.get_job_name())

    def test_get_job_name_returns_value(self):
        self.ctx.insert(ContextPaths.JOB_NAME, "name")
        value = integration.get_job_name()
        self.assertEqual(value, "name")

    def test_get_job_owner_returns_none_when_unset(self):
        self.assertIsNone(integration.get_job_owner())

    def test_get_job_owner_returns_value(self):
        self.ctx.insert(ContextPaths.JOB_OWNER, "owner")
        value = integration.get_job_owner()
        self.assertEqual(value, "owner")

    def test_get_job_type_returns_none_when_unset(self):
        self.assertIsNone(integration.get_job_type())

    def test_get_job_type_returns_value(self):
        self.ctx.insert(ContextPaths.JOB_TYPE, "type")
        value = integration.get_job_type()
        self.assertEqual(value, "type")

    def test_get_job_venue_returns_none_when_unset(self):
        self.assertIsNone(integration.get_job_venue())

    def test_get_job_venue_returns_value(self):
        self.ctx.insert(ContextPaths.JOB_VENUE, "venue")
        value = integration.get_job_venue()
        self.assertEqual(value, "venue")

    def test_get_pipeline_info_returns_none_when_unset(self):
        self.assertIsNone(integration.get_pipeline_info())

    def test_get_pipeline_info_returns_cursor(self):
        info = {"foo": "bar"}
        self.ctx.insert(ContextPaths.PIPELINE_INFO, info)
        cursor = integration.get_pipeline_info()
        self.assertEqual(cursor.value, info)

    def test_get_pipeline_id_returns_none_when_unset(self):
        self.assertIsNone(integration.get_pipeline_id())

    def test_get_pipeline_id_returns_value(self):
        self.ctx.insert(ContextPaths.PIPELINE_ID, "pid")
        value = integration.get_pipeline_id()
        self.assertEqual(value, "pid")

    def test_get_pipeline_instance_returns_none_when_unset(self):
        self.assertIsNone(integration.get_pipeline_instance())

    def test_get_pipeline_instance_returns_value(self):
        self.ctx.insert(ContextPaths.PIPELINE_INSTANCE, "inst")
        value = integration.get_pipeline_instance()
        self.assertEqual(value, "inst")

    def test_get_pipeline_name_returns_none_when_unset(self):
        self.assertIsNone(integration.get_pipeline_name())

    def test_get_pipeline_name_returns_value(self):
        self.ctx.insert(ContextPaths.PIPELINE_NAME, "pname")
        value = integration.get_pipeline_name()
        self.assertEqual(value, "pname")


if __name__ == "__main__":
    unittest.main()
