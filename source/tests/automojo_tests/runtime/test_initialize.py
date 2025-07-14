import unittest
from unittest import mock

from automojo.runtime import initialize

class TestInitializeRuntime(unittest.TestCase):

    def setUp(self):
        initialize.AM_RUNTIME_STATE.INITIALIZED = False

    def test_initialize_sets_state_and_calls_dependencies(self):
        with mock.patch('automojo.runtime.initialize.establish_runtime_settings') as mock_establish, \
             mock.patch('automojo.runtime.runtimevariables.resolve_runtime_variables') as mock_resolve:
            initialize.initialize_runtime(name="am", home_dir="/tmp/home", settings_file="settings.ini",
                                          extension_modules="mods", logger_name="log", default_configuration={},
                                          service_name="svc")

            self.assertTrue(initialize.AM_RUNTIME_STATE.INITIALIZED)
            mock_establish.assert_called_once_with(name="am", home_dir="/tmp/home", settings_file="settings.ini",
                                                   extension_modules="mods", logger_name="log", default_configuration={},
                                                   service_name="svc")
            mock_resolve.assert_called_once_with()

