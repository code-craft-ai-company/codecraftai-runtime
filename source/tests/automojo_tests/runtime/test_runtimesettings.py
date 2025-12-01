import unittest
from unittest.mock import patch

try:
    from automojo.runtime import runtimesettings
except ImportError:  # pragma: no cover - runtime settings helper removed
    runtimesettings = None

@unittest.skipIf(runtimesettings is None, "runtime settings helper is not available in the updated runtime package")
class TestEstablishRuntimeSettings(unittest.TestCase):

    def setUp(self):
        runtimesettings.RUNTIME_SETTINGS_ESTABLISHED = False
        runtimesettings.AM_RUNTIME_DEFAULTS.AM_NAME = "AUTOMOJO"
        runtimesettings.AM_RUNTIME_DEFAULTS.AM_LOGGER_NAME = None

    def test_default_logger_name_uppercase(self):
        def stub_establish_configuration_settings(**kwargs):
            if kwargs.get('name'):
                runtimesettings.AM_RUNTIME_DEFAULTS.AM_NAME = kwargs['name']
        with patch('automojo.runtime.runtimesettings.establish_configuration_settings', side_effect=stub_establish_configuration_settings):
            runtimesettings.establish_runtime_settings(name="demo")
        self.assertTrue(runtimesettings.RUNTIME_SETTINGS_ESTABLISHED)
        self.assertEqual(runtimesettings.AM_RUNTIME_DEFAULTS.AM_LOGGER_NAME, "DEMO")

    def test_custom_logger_name_used(self):
        with patch('automojo.runtime.runtimesettings.establish_configuration_settings'):
            runtimesettings.establish_runtime_settings(logger_name="CUSTOM")
        self.assertEqual(runtimesettings.AM_RUNTIME_DEFAULTS.AM_LOGGER_NAME, "CUSTOM")

    def test_called_only_once(self):
        with patch('automojo.runtime.runtimesettings.establish_configuration_settings') as mock_establish:
            runtimesettings.establish_runtime_settings(logger_name="ONE")
            runtimesettings.establish_runtime_settings(logger_name="TWO")
            self.assertEqual(mock_establish.call_count, 1)
        self.assertEqual(runtimesettings.AM_RUNTIME_DEFAULTS.AM_LOGGER_NAME, "ONE")

if __name__ == '__main__':
    unittest.main()
