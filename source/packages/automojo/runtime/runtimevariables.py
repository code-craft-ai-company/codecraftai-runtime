"""
.. module:: runtimevariables
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains the :class:`AM_RUNTIME_VARIABLES`
              object which is used store the environment variables.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

import os

from datetime import datetime
from uuid import uuid4

from automojo.xmodules.xconvert import parse_bool
from automojo.xmodules.xdatetime import (
    parse_datetime, DATETIME_FORMAT_FILESYSTEM, DATETIME_FORMAT_TIMESTAMP
)
from automojo.xmodules.xlogging.levels import LogLevel

from automojo.thisapp.appvardesc import AppVarDesc
from automojo.thisapp.appvaraccessor import AppVarAccessor
from automojo.thisapp.personavariables import PersonaVariables
from automojo.thisapp.wellknown import ThisApplicationSingleton

from automojo.runtime.enumerations import JobType


class DefaultValue:
    NotSet = "(not-set)"


class RuntimeVariablesDesc(PersonaVariables):

    AM_ACTIVATION_PROFILE = AppVarDesc(default=None)
    AM_AUTOMATION_POD = AppVarDesc(default=DefaultValue.NotSet)

    AM_BUG_SERVER_TYPE = AppVarDesc()
    AM_BUG_SERVER_ENDPOINT = AppVarDesc()
    AM_BUG_PROJECTS = AppVarDesc()
    AM_BUG_TEAM = AppVarDesc()
    AM_BUG_USERNAME = AppVarDesc()
    AM_BUG_TOKEN = AppVarDesc()

    AM_BUILD_RELEASE = AppVarDesc(default=DefaultValue.NotSet)
    AM_BUILD_BRANCH = AppVarDesc(default=DefaultValue.NotSet)
    AM_BUILD_FLAVOR = AppVarDesc(default=DefaultValue.NotSet)
    AM_BUILD_NAME = AppVarDesc(default=DefaultValue.NotSet)
    AM_BUILD_URL = AppVarDesc(default=DefaultValue.NotSet)

    AM_DEBUG_BREAKPOINTS = AppVarDesc(default=None)
    AM_DEBUG_DEBUGGER = AppVarDesc(default=None)

    AM_INTERACTIVE_CONSOLE = AppVarDesc(default=False)

    AM_RUN_ID = AppVarDesc(default=DefaultValue.NotSet)

    AM_PIPELINE_ID = AppVarDesc(default=DefaultValue.NotSet)
    AM_PIPELINE_NAME = AppVarDesc(default=DefaultValue.NotSet)
    AM_PIPELINE_INSTANCE = AppVarDesc(default=DefaultValue.NotSet)

    AM_JOB_CLASS = AppVarDesc(default=DefaultValue.NotSet)
    AM_JOB_ID = AppVarDesc(default=DefaultValue.NotSet)
    AM_JOB_INITIATOR = AppVarDesc(default=DefaultValue.NotSet)
    AM_JOB_LABEL = AppVarDesc(default=DefaultValue.NotSet)
    AM_JOB_NAME = AppVarDesc(default=DefaultValue.NotSet)
    AM_JOB_OWNER = AppVarDesc(default=DefaultValue.NotSet)
    AM_JOB_SEED = AppVarDesc(default=DefaultValue.NotSet)
    AM_JOB_TAG = AppVarDesc(default=DefaultValue.NotSet)
    AM_JOB_TYPE = AppVarDesc(default=JobType.Unknown.value)
    AM_JOB_VENUE = AppVarDesc(default=DefaultValue.NotSet)

    AM_LOG_LEVEL_CONSOLE = AppVarDesc(default=LogLevel.WARNING)
    AM_LOG_LEVEL_FILE = AppVarDesc(default=LogLevel.DEBUG)
    
    AM_LOG_BASENAME = AppVarDesc(default=None)
    AM_LOG_DIRECTORY = AppVarDesc(default=None)

    AM_LOGGER_NAME = AppVarDesc(default=None)

    AM_OUTPUT_DIRECTORY = AppVarDesc(default=None)

    AM_HAS_SHARED_OUTPUT_DIRECTORY = AppVarDesc(default=False)
    AM_SHARED_STORE_DIRECTORY = AppVarDesc(default=None)

    AM_RESULTS_STATIC_SUMMARY_TEMPLATE = AppVarDesc(default=None)
    AM_RESULTS_STATIC_RESOURCE_DEST_DIR = AppVarDesc(default=None)
    AM_RESULTS_STATIC_RESOURCE_SRC_DIR = AppVarDesc(default=None)

    AM_STARTTIME = AppVarDesc(default=datetime.now())

    AM_TESTROOT = AppVarDesc(default=None)


class RuntimeVariables:
    """
        Container for all the configuration variables that can be passed via environmental variables.
    """

    AM_OUTPUT_DIRECTORY = AppVarAccessor()

    AM_HAS_SHARED_OUTPUT_DIRECTORY = AppVarAccessor()
    AM_SHARED_STORE_DIRECTORY = AppVarAccessor()

    AM_ACTIVATION_PROFILE = AppVarAccessor()

    AM_AUTOMATION_POD = AppVarAccessor()

    AM_BUILD_RELEASE = AppVarAccessor()
    AM_BUILD_BRANCH = AppVarAccessor()
    AM_BUILD_FLAVOR = AppVarAccessor()
    AM_BUILD_NAME = AppVarAccessor()
    AM_BUILD_URL = AppVarAccessor()

    AM_DEBUG_BREAKPOINTS = AppVarAccessor()
    AM_DEBUG_DEBUGGER = AppVarAccessor()

    AM_INTERACTIVE_CONSOLE = AppVarAccessor()

    AM_RUN_ID = AppVarAccessor()

    AM_PIPELINE_ID = AppVarAccessor()
    AM_PIPELINE_NAME = AppVarAccessor()
    AM_PIPELINE_INSTANCE = AppVarAccessor()

    AM_JOB_CLASS = AppVarAccessor()
    AM_JOB_ID = AppVarAccessor()
    AM_JOB_TYPE = AppVarAccessor()
    AM_JOB_INITIATOR = AppVarAccessor()
    AM_JOB_LABEL = AppVarAccessor()
    AM_JOB_NAME = AppVarAccessor()
    AM_JOB_OWNER = AppVarAccessor()
    AM_JOB_SEED = AppVarAccessor()
    AM_JOB_TAG = AppVarAccessor()
    AM_JOB_VENUE = AppVarAccessor()

    AM_LOG_BASENAME = AppVarAccessor()
    AM_LOG_DIRECTORY = AppVarAccessor()
    AM_LOG_LEVEL_CONSOLE = AppVarAccessor()
    AM_LOG_LEVEL_FILE = AppVarAccessor()

    AM_RESULTS_STATIC_SUMMARY_TEMPLATE = AppVarAccessor()
    AM_RESULTS_STATIC_RESOURCE_DEST_DIR = AppVarAccessor()
    AM_RESULTS_STATIC_RESOURCE_SRC_DIR = AppVarAccessor()

    AM_STARTTIME = AppVarAccessor()

    AM_TESTROOT = AppVarAccessor()


def get_runtime_seed() -> str:
    rtnval = RuntimeVariables.AM_JOB_SEED
    return rtnval


def resolve_runtime_variables():

    this_app = ThisApplicationSingleton()

    this_app.resolve_variable_set(RuntimeVariablesDesc)

    return