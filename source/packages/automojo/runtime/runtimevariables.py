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
from automojo.thisapp.personavariables import PersonaVariablesDesc, PersonaVariables
from automojo.thisapp.wellknown import ThisApplicationSingleton

from automojo.runtime.enumerations import JobType


class DefaultValue:
    NotSet = "(not-set)"


class RuntimeVariablesDesc(PersonaVariablesDesc):

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


class RuntimeVariables(PersonaVariables):
    """
        Container for all the configuration variables that can be passed via environmental variables.
    """

    AM_OUTPUT_DIRECTORY = AppVarAccessor(RuntimeVariablesDesc.AM_OUTPUT_DIRECTORY)

    AM_HAS_SHARED_OUTPUT_DIRECTORY = AppVarAccessor(RuntimeVariablesDesc.AM_HAS_SHARED_OUTPUT_DIRECTORY)
    AM_SHARED_STORE_DIRECTORY = AppVarAccessor(RuntimeVariablesDesc.AM_SHARED_STORE_DIRECTORY)

    AM_ACTIVATION_PROFILE = AppVarAccessor(RuntimeVariablesDesc.AM_ACTIVATION_PROFILE)

    AM_AUTOMATION_POD = AppVarAccessor(RuntimeVariablesDesc.AM_AUTOMATION_POD)

    AM_BUILD_RELEASE = AppVarAccessor(RuntimeVariablesDesc.AM_BUILD_RELEASE)
    AM_BUILD_BRANCH = AppVarAccessor(RuntimeVariablesDesc.AM_BUILD_BRANCH)
    AM_BUILD_FLAVOR = AppVarAccessor(RuntimeVariablesDesc.AM_BUILD_FLAVOR)
    AM_BUILD_NAME = AppVarAccessor(RuntimeVariablesDesc.AM_BUILD_NAME)
    AM_BUILD_URL = AppVarAccessor(RuntimeVariablesDesc.AM_BUILD_URL)

    AM_DEBUG_BREAKPOINTS = AppVarAccessor(RuntimeVariablesDesc.AM_DEBUG_BREAKPOINTS)
    AM_DEBUG_DEBUGGER = AppVarAccessor(RuntimeVariablesDesc.AM_DEBUG_DEBUGGER)

    AM_INTERACTIVE_CONSOLE = AppVarAccessor(RuntimeVariablesDesc.AM_INTERACTIVE_CONSOLE)

    AM_RUN_ID = AppVarAccessor(RuntimeVariablesDesc.AM_RUN_ID)

    AM_PIPELINE_ID = AppVarAccessor(RuntimeVariablesDesc.AM_PIPELINE_ID)
    AM_PIPELINE_NAME = AppVarAccessor(RuntimeVariablesDesc.AM_PIPELINE_NAME)
    AM_PIPELINE_INSTANCE = AppVarAccessor(RuntimeVariablesDesc.AM_PIPELINE_INSTANCE)

    AM_JOB_CLASS = AppVarAccessor(RuntimeVariablesDesc.AM_JOB_CLASS)
    AM_JOB_ID = AppVarAccessor(RuntimeVariablesDesc.AM_JOB_ID)
    AM_JOB_TYPE = AppVarAccessor(RuntimeVariablesDesc.AM_JOB_TYPE)
    AM_JOB_INITIATOR = AppVarAccessor(RuntimeVariablesDesc.AM_JOB_INITIATOR)
    AM_JOB_LABEL = AppVarAccessor(RuntimeVariablesDesc.AM_JOB_LABEL)
    AM_JOB_NAME = AppVarAccessor(RuntimeVariablesDesc.AM_JOB_NAME)
    AM_JOB_OWNER = AppVarAccessor(RuntimeVariablesDesc.AM_JOB_OWNER)
    AM_JOB_SEED = AppVarAccessor(RuntimeVariablesDesc.AM_JOB_SEED)
    AM_JOB_TAG = AppVarAccessor(RuntimeVariablesDesc.AM_JOB_TAG)
    AM_JOB_VENUE = AppVarAccessor(RuntimeVariablesDesc.AM_JOB_VENUE)

    AM_LOG_LEVEL_CONSOLE = AppVarAccessor(RuntimeVariablesDesc.AM_LOG_LEVEL_CONSOLE)
    AM_LOG_LEVEL_FILE = AppVarAccessor(RuntimeVariablesDesc.AM_LOG_LEVEL_FILE)

    AM_RESULTS_STATIC_SUMMARY_TEMPLATE = AppVarAccessor(RuntimeVariablesDesc.AM_RESULTS_STATIC_SUMMARY_TEMPLATE)
    AM_RESULTS_STATIC_RESOURCE_DEST_DIR = AppVarAccessor(RuntimeVariablesDesc.AM_RESULTS_STATIC_RESOURCE_DEST_DIR)
    AM_RESULTS_STATIC_RESOURCE_SRC_DIR = AppVarAccessor(RuntimeVariablesDesc.AM_RESULTS_STATIC_RESOURCE_SRC_DIR)

    AM_STARTTIME = AppVarAccessor(RuntimeVariablesDesc.AM_STARTTIME)

    AM_TESTROOT = AppVarAccessor(RuntimeVariablesDesc.AM_TESTROOT)


def get_runtime_seed() -> str:
    rtnval = RuntimeVariables.AM_JOB_SEED
    return rtnval


def resolve_runtime_variables():

    this_app = ThisApplicationSingleton()
    this_app.resolve_variable_set(RuntimeVariablesDesc)

    return