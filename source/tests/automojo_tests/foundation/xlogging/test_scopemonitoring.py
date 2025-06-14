import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

from automojo.foundation.xlogging import scopemonitoring
from automojo.foundation.xlogging.scopemonitoring import MonitoredScope
from automojo.waiting.waitmodel import TimeoutContext


class TestScopeMonitoring(unittest.TestCase):

    def _create_scope(self, end_offset: timedelta, notify_delay=timedelta(seconds=0)):
        tc = TimeoutContext(1)
        tc.mark_begin()
        tc._end_time = datetime.now() + end_offset
        return MonitoredScope("label", "msg", tc, notify_delay=notify_delay)

    def test_monitored_scope_comparison_operators(self):
        sooner = self._create_scope(timedelta(seconds=1))
        later = self._create_scope(timedelta(seconds=2))

        self.assertLess(sooner, later)
        self.assertLessEqual(sooner, later)
        self.assertGreater(later, sooner)
        self.assertGreaterEqual(later, sooner)
        self.assertNotEqual(sooner, later)
        self.assertFalse(sooner == later)

    def test_monitored_scope_expired_property(self):
        scope = self._create_scope(timedelta(seconds=1), notify_delay=timedelta(seconds=0))
        self.assertFalse(scope.expired)
        scope._timeout_ctx._end_time = datetime.now() - timedelta(seconds=1)
        self.assertTrue(scope.expired)

    def test_trigger_notification_runs_diagnostic_once(self):
        scope = self._create_scope(timedelta(seconds=-1), notify_delay=timedelta(seconds=0))
        counter = {"count": 0}

        def diag():
            counter["count"] += 1
            return "diag"

        scope.set_diagnostic(diag)
        with patch('automojo.foundation.xlogging.scopemonitoring.logger') as mock_logger:
            scope.trigger_notification()
            scope.trigger_notification()

            self.assertEqual(counter["count"], 1)
            mock_logger.error.assert_called_once()

    def test_monitored_scope_with_context_registers_monitor(self):
        scopemonitoring.ScopeMonitor.instance = None
        scopemonitoring.ScopeMonitor.initialized = False
        scopemonitoring.global_scope_monitor = None

        with MonitoredScope(
            "label",
            "msg",
            TimeoutContext(1),
            notify_delay=timedelta(seconds=0),
        ) as scope:
            monitor = scopemonitoring.global_scope_monitor
            self.assertIn(scope, monitor._monitors)
            self.assertFalse(scope.exited)

        self.assertTrue(scope.exited)

    def test_scope_monitor_register_orders_scopes(self):
        scopemonitoring.ScopeMonitor.instance = None
        scopemonitoring.ScopeMonitor.initialized = False
        scopemonitoring.global_scope_monitor = None

        with MonitoredScope(
            "label",
            "msg",
            TimeoutContext(3),
            notify_delay=timedelta(seconds=0),
        ) as first:
            pass

        with MonitoredScope(
            "label",
            "msg",
            TimeoutContext(1),
            notify_delay=timedelta(seconds=0),
        ) as second:
            pass

        with MonitoredScope(
            "label",
            "msg",
            TimeoutContext(2),
            notify_delay=timedelta(seconds=0),
        ) as third:
            pass

        monitor = scopemonitoring.global_scope_monitor
        ordered = [second, third, first]
        self.assertEqual(monitor._monitors, ordered)

    def test_scope_monitor_monitor_tick_removes_expired_scopes(self):
        scopemonitoring.ScopeMonitor.instance = None
        scopemonitoring.ScopeMonitor.initialized = False
        scopemonitoring.global_scope_monitor = None

        with MonitoredScope(
            "label",
            "msg",
            TimeoutContext(1),
            notify_delay=timedelta(seconds=0),
        ) as expired:
            pass

        with MonitoredScope(
            "label",
            "msg",
            TimeoutContext(60),
            notify_delay=timedelta(seconds=0),
        ) as active:
            pass

        expired.trigger_notification = MagicMock()
        expired._timeout_ctx._end_time = datetime.now() - timedelta(seconds=2)

        monitor = scopemonitoring.global_scope_monitor
        monitor._monitor_tick()

        expired.trigger_notification.assert_called_once()
        self.assertEqual(monitor._monitors, [active])


if __name__ == '__main__':
    unittest.main()
