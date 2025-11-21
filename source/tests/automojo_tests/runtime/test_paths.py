import os
import shutil
import tempfile
import unittest

from automojo.presence.contextpaths import ContextPaths
from automojo.presence.wellknown import ContextSingleton
from automojo.runtime import paths
from automojo.runtime.enumerations import JobType
from automojo.runtime.runtimevariables import AM_RUNTIME_VARIABLES


class PathsTestCase(unittest.TestCase):

    def setUp(self):
        # create isolated temp directory for each test
        self.workdir = tempfile.mkdtemp()
        # clear context and setup minimal paths
        self.ctx = ContextSingleton()
        self.ctx._store.clear()

        self.presence_dir = os.path.join(self.workdir, "presence")
        self.output_dir = os.path.join(self.workdir, "output")
        self.shared_dir = os.path.join(self.workdir, "shared")
        os.makedirs(self.presence_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.shared_dir, exist_ok=True)

        self.ctx.insert(ContextPaths.PRESENCE_HOME_DIRECTORY, self.presence_dir)
        self.ctx.insert(ContextPaths.OUTPUT_DIRECTORY, self.output_dir)
        self.ctx.insert(ContextPaths.SHARED_STORE_DIRECTORY, self.shared_dir)
        self.ctx.insert(ContextPaths.RESULT_PATH_FOR_TESTS, os.path.join(self.output_dir, "testresults"))
        self.ctx.insert(ContextPaths.OUTPUT_DIRECTORY_IS_SHARED, True)

        # save globals and reset
        self.prev_globals = {
            'DIR_PRESENCE_DIRECTORY': paths.DIR_PRESENCE_DIRECTORY,
            'DIR_CACHE_DIRECTORY': paths.DIR_CACHE_DIRECTORY,
            'DIR_DIAGNOSTICS_DIRECTORY': paths.DIR_DIAGNOSTICS_DIRECTORY,
            'DIR_RESULTS_DIRECTORY': paths.DIR_RESULTS_DIRECTORY,
            'DIR_SHARED_STORE_DIRECTORY': paths.DIR_SHARED_STORE_DIRECTORY,
            'DIR_TESTRESULTS_DIRECTORY': paths.DIR_TESTRESULTS_DIRECTORY,
            'DIR_TESTCASE_BYPRODUCTS_DIRECTORY': paths.DIR_TESTCASE_BYPRODUCTS_DIRECTORY,
        }
        paths.DIR_PRESENCE_DIRECTORY = None
        paths.DIR_CACHE_DIRECTORY = None
        paths.DIR_DIAGNOSTICS_DIRECTORY = None
        paths.DIR_RESULTS_DIRECTORY = None
        paths.DIR_SHARED_STORE_DIRECTORY = None
        paths.DIR_TESTRESULTS_DIRECTORY = None
        paths.DIR_TESTCASE_BYPRODUCTS_DIRECTORY = None

        self.prev_job_type = AM_RUNTIME_VARIABLES.AM_JOB_TYPE
        AM_RUNTIME_VARIABLES.AM_JOB_TYPE = JobType.TestRun

        # Some implementations of paths expect a NotSet value on JobType
        self.added_notset = False
        if not hasattr(JobType, "NotSet"):
            setattr(JobType, "NotSet", JobType.Unknown)
            self.added_notset = True

    def tearDown(self):
        shutil.rmtree(self.workdir, ignore_errors=True)
        # restore globals
        paths.DIR_PRESENCE_DIRECTORY = self.prev_globals['DIR_PRESENCE_DIRECTORY']
        paths.DIR_CACHE_DIRECTORY = self.prev_globals['DIR_CACHE_DIRECTORY']
        paths.DIR_DIAGNOSTICS_DIRECTORY = self.prev_globals['DIR_DIAGNOSTICS_DIRECTORY']
        paths.DIR_RESULTS_DIRECTORY = self.prev_globals['DIR_RESULTS_DIRECTORY']
        paths.DIR_SHARED_STORE_DIRECTORY = self.prev_globals['DIR_SHARED_STORE_DIRECTORY']
        paths.DIR_TESTRESULTS_DIRECTORY = self.prev_globals['DIR_TESTRESULTS_DIRECTORY']
        paths.DIR_TESTCASE_BYPRODUCTS_DIRECTORY = self.prev_globals['DIR_TESTCASE_BYPRODUCTS_DIRECTORY']

        AM_RUNTIME_VARIABLES.AM_JOB_TYPE = self.prev_job_type
        self.ctx._store.clear()

        if self.added_notset:
            delattr(JobType, "NotSet")

    def test_collect_python_modules_depth_limit(self):
        root = os.path.join(self.workdir, "mods")
        os.makedirs(os.path.join(root, "sub", "deep"), exist_ok=True)
        with open(os.path.join(root, "m1.py"), "w") as f:
            f.write("pass")
        with open(os.path.join(root, "sub", "m2.py"), "w") as f:
            f.write("pass")
        with open(os.path.join(root, "sub", "deep", "m3.py"), "w") as f:
            f.write("pass")

        found = paths.collect_python_modules(root, max_depth=1)
        expected = {os.path.join(root, "m1.py"), os.path.join(root, "sub", "m2.py")}
        self.assertEqual(set(found), expected)

    def test_ensure_directory_is_package(self):
        pkg = os.path.join(self.workdir, "pkg")
        os.makedirs(pkg)
        paths.ensure_directory_is_package(pkg, package_title="Title")
        init_file = os.path.join(pkg, "__init__.py")
        self.assertTrue(os.path.exists(init_file))
        with open(init_file, "r") as f:
            contents = f.read()
        self.assertIn("Title", contents)

    def test_get_directory_for_code_container(self):
        import automojo.runtime.paths as mod
        dpath = paths.get_directory_for_code_container(mod)
        self.assertTrue(dpath.endswith(os.path.join("automojo", "runtime")))

    def test_normalize_name_for_path(self):
        name = "My Module: test,1.2;3"
        norm = paths.normalize_name_for_path(name)
        self.assertEqual(norm, "MyModuletest123")

    def test_get_temporary_directory_and_file(self):
        temp_dir = paths.get_temporary_directory()
        self.assertTrue(temp_dir.startswith(self.output_dir))
        tmp_file = paths.get_temporary_file(suffix=".txt", prefix="temp_")
        self.assertTrue(tmp_file.startswith(temp_dir))
        self.assertTrue(tmp_file.endswith(".txt"))

    def test_get_path_for_artifacts_created(self):
        label = "art"
        apath = paths.get_path_for_artifacts(label)
        self.assertTrue(apath.startswith(os.path.join(self.output_dir, "artifacts")))
        self.assertTrue(os.path.exists(apath))
