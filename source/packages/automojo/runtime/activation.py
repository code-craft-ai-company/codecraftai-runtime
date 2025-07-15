"""
.. module:: activation
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains methods that implement the activation process.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import Optional

import os
import tempfile
import uuid

from automojo.errors.exceptions import ConfigurationError, SemanticError
from automojo.errors.xtraceback import (
    TRACEBACK_CONFIG,
    VALID_MEMBER_TRACE_POLICY,
)

from automojo.xmodules.xcollections.context import Context
from automojo.xmodules.xlogging.levels import LogLevel

from automojo.presence.contextpaths import ContextPaths
from automojo.presence.wellknown import ContextSingleton # pylint: disable=wrong-import-position

from automojo.xmodules.xlogging.parameters import LoggingLocation, LoggingReduction
from automojo.xmodules.xlogging.activation import (
    activate_standard_file_logging,
    activate_interactive_console_logging,
    activate_service_logging
)

from automojo.runtime.enumerations import ActivationProfile, JobType
from automojo.runtime.variablenames import AM_RUNTIME_VARNAMES
from automojo.runtime.runtimevariables import AM_RUNTIME_VARIABLES, DefaultValue


def activate_profile_command():

    # Guard against attemps to activate more than one, activation profile.
    if AM_RUNTIME_VARIABLES.AM_ACTIVATION_PROFILE is not None:
        errmsg = "An attempt was made to activate multiple environment activation profiles. profile={}".format(
            AM_RUNTIME_VARIABLES.AM_ACTIVATION_PROFILE
        )
        raise SemanticError(errmsg)

    ctx = ContextSingleton()

    AM_RUNTIME_VARIABLES.AM_ACTIVATION_PROFILE = ActivationProfile.Command
    os.environ[AM_RUNTIME_VARNAMES.AM_JOB_TYPE] = AM_RUNTIME_VARIABLES.AM_JOB_TYPE

    _activate_profile_common(ctx)

    log_directory = AM_RUNTIME_VARIABLES.AM_LOG_DIRECTORY
    log_basename = AM_RUNTIME_VARIABLES.AM_LOG_BASENAME

    logging_location = LoggingLocation(log_directory, log_basename)

    console_level = AM_RUNTIME_VARIABLES.AM_LOG_LEVEL_CONSOLE
    file_level = AM_RUNTIME_VARIABLES.AM_LOG_LEVEL_CONSOLE

    activate_standard_file_logging(console_level, file_level, logging_location)

    return


def activate_profile_console():

    # Guard against attemps to activate more than one, activation profile.
    if AM_RUNTIME_VARIABLES.AM_ACTIVATION_PROFILE is not None:
        errmsg = "An attempt was made to activate multiple environment activation profiles. profile={}".format(
            AM_RUNTIME_VARIABLES.AM_ACTIVATION_PROFILE
        )
        raise SemanticError(errmsg)

    ctx = ContextSingleton()

    AM_RUNTIME_VARIABLES.AM_ACTIVATION_PROFILE = ActivationProfile.Console
    os.environ[AM_RUNTIME_VARNAMES.AM_JOB_TYPE] = AM_RUNTIME_VARIABLES.AM_JOB_TYPE

    temp_output_dir = tempfile.mkdtemp()
    AM_RUNTIME_VARIABLES.AM_OUTPUT_DIRECTORY = temp_output_dir

    def showlog():

        print("OUTPUT FOLDER: {}".format(AM_RUNTIME_VARIABLES.AM_OUTPUT_DIRECTORY))
        print("")

        return

    log_directory = AM_RUNTIME_VARIABLES.AM_LOG_DIRECTORY
    log_basename = AM_RUNTIME_VARIABLES.AM_LOG_BASENAME

    logging_location = LoggingLocation(log_directory, log_basename)

    file_level = AM_RUNTIME_VARIABLES.AM_LOG_LEVEL_CONSOLE

    _activate_profile_common(ctx)

    activate_interactive_console_logging(logging_location, file_level)

    return


def activate_profile_service(max_bytes: int = 10 * 1024 * 1024, backup_count: int = 10):

    # Guard against attempts to activate more than one, activation profile.
    if AM_RUNTIME_VARIABLES.AM_ACTIVATION_PROFILE is not None:
        errmsg = "An attempt was made to activate multiple environment activation profiles. profile={}".format(
            AM_RUNTIME_VARIABLES.AM_ACTIVATION_PROFILE
        )
        raise SemanticError(errmsg)

    AM_RUNTIME_VARIABLES.AM_ACTIVATION_PROFILE = ActivationProfile.Service

    service_name = AM_RUNTIME_VARIABLES.AM_SERVICE_NAME

    if service_name is None:
        if AM_RUNTIME_VARNAMES.AM_SERVICE_NAME not in os.environ:
            errmsg = "To use the Mojo Runtime to provide a service, you must " \
                    "set the '{}' environment variable.".format(AM_RUNTIME_VARNAMES.AM_SERVICE_NAME)
            raise ConfigurationError(errmsg)

        service_name = os.environ[AM_RUNTIME_VARNAMES.AM_SERVICE_NAME]

    ctx = ContextSingleton()

    AM_RUNTIME_VARIABLES.AM_LOG_LEVEL_CONSOLE = LogLevel.INFO
    AM_RUNTIME_VARIABLES.AM_SERVICE_NAME = service_name
    AM_RUNTIME_VARIABLES.AM_JOB_TYPE = JobType.Service.value
    AM_RUNTIME_VARIABLES.AM_OUTPUT_DIRECTORY = os.path.join(AM_RUNTIME_VARIABLES.AM_PRESENCE_DIRECTORY, "services", service_name)

    # For console activation we don't want to log to the console and we want
    # to point the logs to a different output folder
    os.environ[AM_RUNTIME_VARNAMES.AM_LOG_LEVEL_CONSOLE] = str(AM_RUNTIME_VARIABLES.AM_LOG_LEVEL_CONSOLE)
    os.environ[AM_RUNTIME_VARNAMES.AM_JOB_TYPE] = AM_RUNTIME_VARIABLES.AM_JOB_TYPE
    os.environ[AM_RUNTIME_VARNAMES.AM_OUTPUT_DIRECTORY] = str(AM_RUNTIME_VARIABLES.AM_OUTPUT_DIRECTORY)

    _activate_profile_common(ctx)

    log_directory = AM_RUNTIME_VARIABLES.AM_LOG_DIRECTORY
    log_basename = AM_RUNTIME_VARIABLES.AM_LOG_BASENAME

    logging_location = LoggingLocation(log_directory, log_basename)

    console_level = AM_RUNTIME_VARIABLES.AM_LOG_LEVEL_CONSOLE
    file_level = AM_RUNTIME_VARIABLES.AM_LOG_LEVEL_CONSOLE

    activate_service_logging(logging_location, console_level, file_level, max_bytes, backup_count)

    return


def activate_profile_job(job_type: JobType):
    
    # Guard against attemps to activate more than one, activation profile.
    if AM_RUNTIME_VARIABLES.AM_ACTIVATION_PROFILE is not None:
        errmsg = "An attempt was made to activate multiple environment activation profiles. profile={}".format(
            AM_RUNTIME_VARIABLES.AM_ACTIVATION_PROFILE
        )
        raise RuntimeError(errmsg)

    ctx = ContextSingleton()
    ctx.insert(ContextPaths.JOB_TYPE, job_type)

    AM_RUNTIME_VARIABLES.AM_ACTIVATION_PROFILE = ActivationProfile.Job

    AM_RUNTIME_VARIABLES.AM_JOB_TYPE = job_type

    _activate_profile_common(ctx)

    AM_RUNTIME_VARIABLES.AM_LOG_DIRECTORY =  AM_RUNTIME_VARIABLES.AM_OUTPUT_DIRECTORY

    log_directory = AM_RUNTIME_VARIABLES.AM_LOG_DIRECTORY
    log_basename = AM_RUNTIME_VARIABLES.AM_LOG_BASENAME

    logging_location = LoggingLocation(log_directory, log_basename)

    console_level = AM_RUNTIME_VARIABLES.AM_LOG_LEVEL_CONSOLE
    file_level = AM_RUNTIME_VARIABLES.AM_LOG_LEVEL_CONSOLE

    activate_standard_file_logging(logging_location, console_level, file_level)

    return


def _activate_profile_common(ctx: Context):
    """
    """
    
    from automojo.xmodules.xdatetime import DATETIME_FORMAT_FILESYSTEM

    # We set all the variables for config file options from the environment
    # we just loaded, these might get overridden late but that is ok
    current_traceback_policy = ctx.lookup(ContextPaths.DIAGNOSTICS_TRACEBACK_POLICY_OVERRIDE, default=None)
    if current_traceback_policy is None and TRACEBACK_CONFIG.TRACEBACK_POLICY_OVERRIDE is not None:
        if TRACEBACK_CONFIG.TRACEBACK_POLICY_OVERRIDE in VALID_MEMBER_TRACE_POLICY:
            ctx.insert(ContextPaths.DIAGNOSTICS_TRACEBACK_POLICY_OVERRIDE, TRACEBACK_CONFIG.TRACEBACK_POLICY_OVERRIDE)
        else:
            errmsg = "Invalid traceback policy environment value. TRACEBACK_POLICY_OVERRIDE={}".format(
                TRACEBACK_CONFIG.TRACEBACK_POLICY_OVERRIDE
            )
            raise ConfigurationError(errmsg)

    jobtype = ctx.lookup(ContextPaths.JOB_TYPE, default=AM_RUNTIME_VARIABLES.AM_JOB_TYPE)

    starttime_name = AM_RUNTIME_VARIABLES.AM_STARTTIME.strftime(DATETIME_FORMAT_FILESYSTEM)

    fill_dict = {
        "starttime": starttime_name
    }

    output_directory = None
    if AM_RUNTIME_VARIABLES.AM_JOB_ID is None or AM_RUNTIME_VARIABLES.AM_JOB_ID == DefaultValue.NotSet:
        AM_RUNTIME_VARIABLES.AM_JOB_ID = str(uuid.uuid4())

    # We want to pull the console and testresults value from the configuration, because if its not there it
    # will be set from the default_dir_template variable
    ctx.insert(ContextPaths.STARTTIME, AM_RUNTIME_VARIABLES.AM_STARTTIME)
    ctx.insert(ContextPaths.JOB_ID, AM_RUNTIME_VARIABLES.AM_JOB_ID)

    # Figure out which output directory to set as the current process output directory.  The output directory
    # determines where loggin will go and is different depending on the activation mode of the test framework
    
    if jobtype == JobType.Infrastructure:
        default_dir_template = os.path.join(AM_RUNTIME_VARIABLES.AM_PRESENCE_DIRECTORY, "results", "infrastructure", "%(starttime)s")
        outdir_template = ctx.lookup(ContextPaths.TEMPLATE_PATH_FOR_ORCHESTRATION, default=default_dir_template)
        output_directory = outdir_template % fill_dict
        ctx.insert(ContextPaths.RESULT_PATH_FOR_ORCHESTRATION, output_directory)
    elif jobtype == JobType.Orchestration:
        default_dir_template = os.path.join(AM_RUNTIME_VARIABLES.AM_PRESENCE_DIRECTORY, "results", "orchestration", "%(starttime)s")
        outdir_template = ctx.lookup(ContextPaths.TEMPLATE_PATH_FOR_ORCHESTRATION, default=default_dir_template)
        output_directory = outdir_template % fill_dict
        ctx.insert(ContextPaths.RESULT_PATH_FOR_ORCHESTRATION, output_directory)

    elif jobtype == JobType.Build:
        default_dir_template = os.path.join(AM_RUNTIME_VARIABLES.AM_PRESENCE_DIRECTORY, "results", "build", "%(starttime)s")
        outdir_template = ctx.lookup(ContextPaths.TEMPLATE_PATH_FOR_SERVICES, default=default_dir_template)
        output_directory = outdir_template % fill_dict
        ctx.insert(ContextPaths.RESULT_PATH_FOR_SERVICES, output_directory)

    elif jobtype == JobType.TestRun:
        if AM_RUNTIME_VARIABLES.AM_OUTPUT_DIRECTORY is None:
            default_dir_template = os.path.join(AM_RUNTIME_VARIABLES.AM_PRESENCE_DIRECTORY, "results", "testresults", "%(starttime)s")
            outdir_template = ctx.lookup(ContextPaths.TEMPLATE_PATH_FOR_TESTS, default=default_dir_template)
            output_directory = outdir_template % fill_dict
            ctx.insert(ContextPaths.RESULT_PATH_FOR_TESTS, output_directory)
        else:
            output_directory = AM_RUNTIME_VARIABLES.AM_OUTPUT_DIRECTORY % fill_dict
            ctx.insert(ContextPaths.RESULT_PATH_FOR_TESTS, output_directory)
    else:
        output_directory = os.getcwd()

    ctx.insert(ContextPaths.OUTPUT_DIRECTORY, output_directory)

    return

