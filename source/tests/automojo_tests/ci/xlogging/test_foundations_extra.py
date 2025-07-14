import os
import logging
import unittest
from io import StringIO
from tempfile import TemporaryDirectory, NamedTemporaryFile
import contextlib

from automojo.ci.runtime.contextpaths import ContextPaths
from automojo.ci.runtime.wellknown import ContextSingleton

from automojo.foundation.xlogging import foundations
from automojo.foundation.xlogging.foundations import (
    EnhancedLogger,
    EnhancedRootLogger,
    LessThanRecordFilter,
    GreaterOrEqualRecordFilter,
    SWAPPABLE_HOOKS,
    logging_initialize,
    logging_create_branch_logger,
)


class _CaptureHandler(logging.Handler):
    """Simple logging handler to capture log records."""

    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(record)


class TestFoundationsExtra(unittest.TestCase):
    def setUp(self):
        self._stdout_orig = SWAPPABLE_HOOKS.HOOK_SYS_STDOUT
        self._stderr_orig = SWAPPABLE_HOOKS.HOOK_SYS_STDERR
        self._root_level = logging.getLogger().level
        self.stdout_buffer = StringIO()
        self.stderr_buffer = StringIO()
        SWAPPABLE_HOOKS.HOOK_SYS_STDOUT = self.stdout_buffer
        SWAPPABLE_HOOKS.HOOK_SYS_STDERR = self.stderr_buffer
        logging.getLogger().setLevel(logging.NOTSET)

    def tearDown(self):
        SWAPPABLE_HOOKS.HOOK_SYS_STDOUT = self._stdout_orig
        SWAPPABLE_HOOKS.HOOK_SYS_STDERR = self._stderr_orig
        logging.getLogger().setLevel(self._root_level)

    def test_render_outputs_to_log_and_stdout(self):
        logger = EnhancedLogger("render_test")
        logger.setLevel(logging.INFO)
        logger.propagate = False
        cap_handler = _CaptureHandler()
        logger.addHandler(cap_handler)

        logger.render("hello")

        self.assertEqual(cap_handler.records[0].getMessage(), "hello")
        self.assertIn("hello", self.stdout_buffer.getvalue())

    def test_section_logs_header(self):
        logger = EnhancedLogger("section_test")
        logger.setLevel(logging.NOTSET)
        logger.propagate = False
        cap_handler = _CaptureHandler()
        logger.addHandler(cap_handler)

        logger.section("start")

        self.assertFalse(cap_handler.records)
        self.assertIn("START", self.stdout_buffer.getvalue())

    def test_test_begin_and_end_messages(self):
        logger = EnhancedLogger("test_case")
        logger.propagate = False
        cap_handler = _CaptureHandler()
        logger.addHandler(cap_handler)

        logger.test_begin("case1", foo=1)
        logger.test_end("case1")

        msgs = [r.getMessage() for r in cap_handler.records]
        self.assertIn("TEST BEGIN - case1", msgs[0])
        self.assertIn("foo = 1", msgs[0])
        self.assertEqual("TEST END - case1", msgs[1])
        self.assertIn("TEST END - case1", self.stdout_buffer.getvalue())

    def test_record_filters(self):
        lt_filter = LessThanRecordFilter(logging.WARNING)
        ge_filter = GreaterOrEqualRecordFilter(logging.WARNING)

        record_info = logging.LogRecord("n", logging.INFO, "", 0, "msg", None, None)
        record_warn = logging.LogRecord("n", logging.WARNING, "", 0, "msg", None, None)

        self.assertTrue(lt_filter.filter(record_info))
        self.assertFalse(lt_filter.filter(record_warn))
        self.assertFalse(ge_filter.filter(record_info))
        self.assertTrue(ge_filter.filter(record_warn))

    def test_adopt_children(self):
        root = logging.getLogger()
        child = logging.getLogger("child")
        self.assertIs(child.parent, root)

        new_root = EnhancedRootLogger(logging.NOTSET)
        try:
            new_root.adopt_children(root)
            self.assertIs(child.parent, new_root)
        finally:
            child.parent = root

    def test_logging_create_branch_logger(self):
        logger = logging.getLogger("branch")
        logger.addHandler(logging.StreamHandler(StringIO()))
        with NamedTemporaryFile() as tmp:
            out = StringIO()
            with contextlib.redirect_stdout(out):
                logging_create_branch_logger("branch", tmp.name, logging.INFO)
            self.assertEqual(len(logger.handlers), 1)
            self.assertIsInstance(logger.handlers[0], logging.FileHandler)
            self.assertEqual(logger.handlers[0].level, logging.INFO)
            logger.handlers[0].close()
            self.assertIn("blah", out.getvalue())

    def _init_logging_context(self, outdir):
        ctx = ContextSingleton()
        ctx._store.clear()  # reset
        ctx.insert(ContextPaths.OUTPUT_DIRECTORY, outdir)
        ctx.insert(ContextPaths.LOGGING_LEVEL_CONSOLE, "INFO")
        ctx.insert(ContextPaths.LOGGING_LEVEL_LOGFILE, "DEBUG")
        ctx.insert(ContextPaths.LOGGING_LOGNAME, "{jobtype}.log")
        ctx.insert(ContextPaths.JOB_TYPE, "unittest")
        ctx.insert(ContextPaths.LOGGING_BRANCHED, [])

    def test_logging_initialize(self):
        old_root = logging.getLogger()
        with TemporaryDirectory() as tmpdir:
            self._init_logging_context(tmpdir)
            try:
                foundations.logging_initialized = False
                foundations.last_logfile = None
                logfile = logging_initialize(reinitialize=True)
                expected = os.path.join(tmpdir, "unittest.log")
                self.assertEqual(logfile, expected)
                self.assertIsInstance(logging.getLogger(), EnhancedRootLogger)
                root_logger = logging.getLogger()
                streams = [h for h in root_logger.handlers if isinstance(h, logging.StreamHandler)]
                self.assertGreaterEqual(len(streams), 2)
                found = any(
                    any(isinstance(f, LessThanRecordFilter) for f in h.filters)
                    for h in streams
                )
                self.assertTrue(found)
            finally:
                new_root = logging.getLogger()
                for h in list(new_root.handlers):
                    new_root.removeHandler(h)
                    h.close()
                logging.root = old_root
                logging.Logger.root = old_root
                logging.Logger.manager.root = old_root
                foundations.logging_initialized = False
                foundations.last_logfile = None

    def test_logging_initialize_idempotent(self):
        old_root = logging.getLogger()
        with TemporaryDirectory() as tmpdir:
            self._init_logging_context(tmpdir)
            try:
                foundations.logging_initialized = False
                foundations.last_logfile = None
                first = logging_initialize(reinitialize=True)
                second = logging_initialize()
                self.assertEqual(first, second)
            finally:
                new_root = logging.getLogger()
                for h in list(new_root.handlers):
                    new_root.removeHandler(h)
                    h.close()
                logging.root = old_root
                logging.Logger.root = old_root
                logging.Logger.manager.root = old_root
                foundations.logging_initialized = False
                foundations.last_logfile = None

