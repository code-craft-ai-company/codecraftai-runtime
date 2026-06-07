
import sys
import os
from unittest.mock import MagicMock

# Add source/packages to path
sys.path.insert(0, os.path.abspath("source/packages"))

# Mock dependencies
mock_modules = [
    "ccai.errors.exceptions",
    "ccai.xmodules.fspath",
    "ccai.xmodules.xconvert",
    "ccai.xmodules.xdatetime",
    "ccai.xmodules.xlogging.levels",
    "ccai.thisapp.appvardesc",
    "ccai.thisapp.appvaraccessor",
    "ccai.thisapp.personavariables",
    "ccai.thisapp.wellknown",
    # We do NOT mock ccai.thisapp.contextpaths completely, we want to control ContextPaths
    "ccai.thisapp.enumerations"
]

for mod_name in mock_modules:
    sys.modules[mod_name] = MagicMock()

# Setup ContextPaths mock with MISSING attributes
class MockContextPaths:
    # Existing attributes
    TEMPLATE_PATH_FOR_TESTS = "TEMPLATE_PATH_FOR_TESTS"
    RESULT_PATH_FOR_TESTS = "RESULT_PATH_FOR_TESTS"
    RESULT_PATH_FOR_ORCHESTRATION = "RESULT_PATH_FOR_ORCHESTRATION"
    RESULT_PATH_FOR_SERVICES = "RESULT_PATH_FOR_SERVICES"
    TEMPLATE_PATH_FOR_ORCHESTRATION = "TEMPLATE_PATH_FOR_ORCHESTRATION"
    TEMPLATE_PATH_FOR_SERVICES = "TEMPLATE_PATH_FOR_SERVICES"

    # Other common ones
    BUILD_RELEASE = "BUILD_RELEASE"
    BUILD_BRANCH = "BUILD_BRANCH"
    BUILD_FLAVOR = "BUILD_FLAVOR"
    BUILD_NAME = "BUILD_NAME"
    BUILD_URL = "BUILD_URL"
    DEBUG_BREAKPOINTS = "DEBUG_BREAKPOINTS"
    DEBUG_DEBUGGER = "DEBUG_DEBUGGER"
    DIAGNOSTICS_POSTRUN = "DIAGNOSTICS_POSTRUN"
    DIAGNOSTICS_PRERUN = "DIAGNOSTICS_PRERUN"
    DIAGNOSTICS_TRACEBACK_POLICY_OVERRIDE = "DIAGNOSTICS_TRACEBACK_POLICY_OVERRIDE"
    RUNID = "RUNID"
    PIPELINE_ID = "PIPELINE_ID"
    PIPELINE_NAME = "PIPELINE_NAME"
    PIPELINE_INSTANCE = "PIPELINE_INSTANCE"
    JOB_CLASS = "JOB_CLASS"
    JOB_ID = "JOB_ID"
    JOB_INITIATOR = "JOB_INITIATOR"
    JOB_LABEL = "JOB_LABEL"
    JOB_NAME = "JOB_NAME"
    JOB_OWNER = "JOB_OWNER"
    JOB_SEED = "JOB_SEED"
    JOB_TAG = "JOB_TAG"
    JOB_TYPE = "JOB_TYPE"
    JOB_VENUE = "JOB_VENUE"
    LOGGING_LEVEL_CONSOLE = "LOGGING_LEVEL_CONSOLE"
    LOGGING_LEVEL_LOGFILE = "LOGGING_LEVEL_LOGFILE"
    OUTPUT_DIRECTORY = "OUTPUT_DIRECTORY"
    OUTPUT_DIRECTORY_IS_SHARED = "OUTPUT_DIRECTORY_IS_SHARED"
    SHARED_STORE_DIRECTORY = "SHARED_STORE_DIRECTORY"
    STARTTIME = "STARTTIME"
    TESTROOT = "TESTROOT"

    # Missing attributes
    # TEMPLATE_PATH_FOR_BUILD = "TEMPLATE_PATH_FOR_BUILD"
    # TEMPLATE_PATH_FOR_INFRASTRUCTURE = "TEMPLATE_PATH_FOR_INFRASTRUCTURE"
    # RESULT_PATH_FOR_BUILD = "RESULT_PATH_FOR_BUILD"
    # RESULT_PATH_FOR_INFRASTRUCTURE = "RESULT_PATH_FOR_INFRASTRUCTURE"

mock_contextpaths_mod = MagicMock()
mock_contextpaths_mod.ContextPaths = MockContextPaths
sys.modules["ccai.thisapp.contextpaths"] = mock_contextpaths_mod

# Import RuntimeVariables to trigger the error
print("Attempting to import ccai.thisapp.runtimevariables...")
try:
    from ccai.thisapp import runtimevariables
    print("Import successful!")
except AttributeError as e:
    # Check if the error is related to AM_OUTPUT_DIRECTORY which is expected
    # because we are mocking everything including AppVarAccessor which might try to access something
    print(f"Import failed with AttributeError: {e}")
    # We want to continue to check the variables if possible, but if import failed, we can't.
    # However, the goal is to pass the import if ContextPaths are correct.
    # The error "Mock object has no attribute 'AM_OUTPUT_DIRECTORY'" suggests
    # that something in the module body is trying to access an attribute on a Mock
    # that doesn't exist, likely AppVarAccessor(RuntimeVariablesDesc.AM_OUTPUT_DIRECTORY)
    # where RuntimeVariablesDesc is also being mocked or interacting with mocks.
    # Let's inspect the file content to understand why it fails.
except Exception as e:
    print(f"Import failed with unexpected error: {type(e).__name__}: {e}")

# Check if AM_TEMPLATE_PATH_FOR_INFRASTRUCTURE is present (should NOT be)
try:
    if hasattr(runtimevariables.RuntimeVariables, 'AM_TEMPLATE_PATH_FOR_INFRASTRUCTURE'):
        print("ERROR: AM_TEMPLATE_PATH_FOR_INFRASTRUCTURE is still present!")
    else:
        print("SUCCESS: AM_TEMPLATE_PATH_FOR_INFRASTRUCTURE is absent.")
except NameError:
    pass

# Check if AM_TEMPLATE_PATH_FOR_BUILD is present (should be)
try:
    if hasattr(runtimevariables.RuntimeVariables, 'AM_TEMPLATE_PATH_FOR_BUILD'):
        print("SUCCESS: AM_TEMPLATE_PATH_FOR_BUILD is present.")
    else:
        print("ERROR: AM_TEMPLATE_PATH_FOR_BUILD is missing!")
except NameError:
    pass
