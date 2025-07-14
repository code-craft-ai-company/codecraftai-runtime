import unittest
from unittest.mock import MagicMock, patch

import automojo.runtime.integration as integration


class DummyPaths:
    JOB_INFO = 'job_info'
    JOB_ID = 'job_id'
    JOB_INITIATOR = 'job_initiator'
    JOB_LABEL = 'job_label'
    JOB_NAME = 'job_name'
    JOB_OWNER = 'job_owner'
    JOB_TYPE = 'job_type'
    JOB_VENUE = 'job_venue'
    PIPELINE_INFO = 'pipeline_info'
    PIPELINE_ID = 'pipeline_id'
    PIPELINE_INSTANCE = 'pipeline_instance'
    PIPELINE_NAME = 'pipeline_name'


class IntegrationFunctionsTest(unittest.TestCase):

    def setUp(self):
        self.context = MagicMock()
        self.patch_ctx = patch.object(integration, 'ContextSingleton', return_value=self.context)
        self.patch_paths = patch.object(integration, 'ContextPaths', DummyPaths)
        self.patch_ctx.start()
        self.patch_paths.start()

    def tearDown(self):
        self.patch_ctx.stop()
        self.patch_paths.stop()

    def _check_lookup(self, func, path_attr, expected):
        self.context.lookup.reset_mock()
        self.context.lookup.return_value = expected
        result = func()
        self.context.lookup.assert_called_once_with(getattr(DummyPaths, path_attr))
        self.assertEqual(result, expected)

    def test_get_job_info(self):
        self._check_lookup(integration.get_job_info, 'JOB_INFO', {'info': 'val'})

    def test_get_job_id(self):
        self._check_lookup(integration.get_job_id, 'JOB_ID', 'jid')

    def test_get_job_initiator(self):
        self._check_lookup(integration.get_job_initiator, 'JOB_INITIATOR', 'initiator')

    def test_get_job_label(self):
        self._check_lookup(integration.get_job_label, 'JOB_LABEL', 'label')

    def test_get_job_name(self):
        self._check_lookup(integration.get_job_name, 'JOB_NAME', 'name')

    def test_get_job_owner(self):
        self._check_lookup(integration.get_job_owner, 'JOB_OWNER', 'owner')

    def test_get_job_type(self):
        self._check_lookup(integration.get_job_type, 'JOB_TYPE', 'type')

    def test_get_job_venue(self):
        self._check_lookup(integration.get_job_venue, 'JOB_VENUE', 'venue')

    def test_get_pipeline_info(self):
        self._check_lookup(integration.get_pipeline_info, 'PIPELINE_INFO', {'p': 1})

    def test_get_pipeline_id(self):
        self._check_lookup(integration.get_pipeline_id, 'PIPELINE_ID', 'pid')

    def test_get_pipeline_instance(self):
        self._check_lookup(integration.get_pipeline_instance, 'PIPELINE_INSTANCE', 'inst')

    def test_get_pipeline_name(self):
        self._check_lookup(integration.get_pipeline_name, 'PIPELINE_NAME', 'pname')


if __name__ == '__main__':
    unittest.main()
