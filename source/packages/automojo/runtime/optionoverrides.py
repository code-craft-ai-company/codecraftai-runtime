"""
.. module:: optionoverrides
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains override mechanisms for the environment variable
               names used to initialize a global context for a python application

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import List

from datetime import datetime

from automojo.presence.contextpaths import ContextPaths
from automojo.presence.wellknown import ContextSingleton

from automojo.runtime.runtimevariables import AM_RUNTIME_VARIABLES

class AM_RUNTIME_OPTION_OVERRIDES:

    @staticmethod
    def override_build_release(release: str):
        """
            This override function provides a mechanism overriding the AM_BUILD_BRANCH
            variable and context configuration setting.

            :param release: The name of the release associated with a build.
        """
        ctx = ContextSingleton()
        ctx.insert(ContextPaths.BUILD_RELEASE, release)

        AM_RUNTIME_VARIABLES.AM_BUILD_RELEASE = release
        return

    @staticmethod
    def override_build_branch(branch_name: str):
        """
            This override function provides a mechanism overriding the AM_BUILD_BRANCH
            variable and context configuration setting.

            :param branch: The name of the branch the build came from.
        """
        ctx = ContextSingleton()
        ctx.insert(ContextPaths.BUILD_BRANCH, branch_name)

        AM_RUNTIME_VARIABLES.AM_BUILD_BRANCH = branch_name
        return

    @staticmethod
    def override_build_flavor(build_flavor: str):
        """
            This override function provides a mechanism overriding the AM_BUILD_FLAVOR
            variable and context configuration setting.

            :param build_flavor: The flavor of the build associated with a job.
        """
        ctx = ContextSingleton()
        ctx.insert(ContextPaths.BUILD_FLAVOR, build_flavor)

        AM_RUNTIME_VARIABLES.AM_BUILD_FLAVOR = build_flavor
        return

    @staticmethod
    def override_build_name(build_name: str):
        """
            This override function provides a mechanism overriding the AM_BUILD_NAME
            variable and context configuration setting.

            :param build_name: The build version of the build.
        """
        ctx = ContextSingleton()
        ctx.insert(ContextPaths.BUILD_NAME, build_name)

        AM_RUNTIME_VARIABLES.AM_BUILD_NAME = build_name
        return

    @staticmethod
    def override_build_url(build_url: str):
        """
            This override function provides a mechanism overriding the AM_BUILD_URL
            variable and context configuration setting.

            :param build_url: The url associated with the build.
        """
        ctx = ContextSingleton()
        ctx.insert(ContextPaths.BUILD_URL, build_url)

        AM_RUNTIME_VARIABLES.AM_BUILD_URL = build_url
        return

    @staticmethod
    def override_debug_breakpoints(breakpoints: List[str]):
        """
            This override function provides a mechanism overriding the AM_BREAKPOINTS
            variable and context configuration setting.

            :param breakpoints: A list of wellknown breakpoints that have been activated.
        """
        ctx = ContextSingleton()
        ctx.insert(ContextPaths.DEBUG_BREAKPOINTS, breakpoints)

        AM_RUNTIME_VARIABLES.AM_DEBUG_BREAKPOINTS = breakpoints
        return

    @staticmethod
    def override_debug_debugger(debugger: str):
        """
            This override function provides a mechanism overriding the AM_DEBUGGER
            variable and context configuration setting.

            :param debugger: The name of the debugger to setup.
        """
        ctx = ContextSingleton()
        ctx.insert(ContextPaths.DEBUG_DEBUGGER, debugger)

        AM_RUNTIME_VARIABLES.AM_DEBUG_DEBUGGER = debugger
        return

    @staticmethod
    def override_job_id(job_id: str):
        """
            This override function provides a mechanism overriding the AM_JOB_ID
            variable and context configuration setting.

            :param runid: A uuid string that represents the instance of this automation run.
        """
        ctx = ContextSingleton()
        ctx.insert(ContextPaths.JOB_ID, job_id)

        AM_RUNTIME_VARIABLES.AM_JOB_ID = job_id
        return

    @staticmethod
    def override_job_initiator(job_initiator: str):
        """
            This override function provides a mechanism overriding the AM_JOB_INITIATOR
            variable and context configuration setting.

            :param job_initiator: The name of the initiator of the job.
        """
        ctx = ContextSingleton()
        ctx.insert(ContextPaths.JOB_INITIATOR, job_initiator)

        AM_RUNTIME_VARIABLES.AM_JOB_INITIATOR = job_initiator

        return

    @staticmethod
    def override_job_label(job_label: str):
        """
            This override function provides a mechanism overriding the AM_JOB_LABEL
            variable and context configuration setting.

            :param job_label: The name of the label if any the job was run under.
        """
        ctx = ContextSingleton()
        ctx.insert(ContextPaths.JOB_LABEL, job_label)

        AM_RUNTIME_VARIABLES.AM_JOB_LABEL = job_label

        return

    @staticmethod
    def override_job_name(job_name: str):
        """
            This override function provides a mechanism overriding the AM_JOB_NAME
            variable and context configuration setting.

            :param job_name: The name of the job.
        """
        ctx = ContextSingleton()
        ctx.insert(ContextPaths.JOB_NAME, job_name)

        AM_RUNTIME_VARIABLES.AM_JOB_NAME = job_name

        return

    @staticmethod
    def override_job_owner(job_owner: str):
        """
            This override function provides a mechanism overriding the AM_JOB_OWNER
            variable and context configuration setting.

            :param job_owner: The name of the owner of the job.
        """
        ctx = ContextSingleton()
        ctx.insert(ContextPaths.JOB_OWNER, job_owner)

        AM_RUNTIME_VARIABLES.AM_JOB_OWNER = job_owner

        return
    
    @staticmethod
    def override_job_seed(job_seed: str):
        """
            This override function provides a mechanism overriding the AM_JOB_SEED
            variable and context configuration setting.

            :param job_seed: The type of the job.
        """
        ctx = ContextSingleton()
        ctx.insert(ContextPaths.JOB_SEED, job_seed)

        AM_RUNTIME_VARIABLES.AM_JOB_SEED = job_seed

        return

    @staticmethod
    def override_job_tag(job_tag: str):
        """
            This override function provides a mechanism overriding the AM_JOB_TAG
            variable and context configuration setting.

            :param job_tag: The tags for the job.
        """
        ctx = ContextSingleton()
        ctx.insert(ContextPaths.JOB_TAG, job_tag)

        AM_RUNTIME_VARIABLES.AM_JOB_TAG = job_tag

        return

    @staticmethod
    def override_job_type(job_type: str):
        """
            This override function provides a mechanism overriding the AM_JOB_TYPE
            variable and context configuration setting.

            :param job_owner: The type of the job.
        """
        ctx = ContextSingleton()
        ctx.insert(ContextPaths.JOB_TYPE, job_type)

        AM_RUNTIME_VARIABLES.AM_JOB_TYPE = job_type

        return

    @staticmethod
    def override_loglevel_console(level: str):
        """
            This override function provides a mechanism overriding the AM_LOG_LEVEL_CONSOLE
            variable and context configuration setting.

            :param level: The console logging level.
        """
        ctx = ContextSingleton()
        ctx.insert(ContextPaths.LOGGING_LEVEL_CONSOLE, level)

        AM_RUNTIME_VARIABLES.AM_LOG_LEVEL_CONSOLE = level
        return

    @staticmethod
    def override_loglevel_file(level: str):
        """
            This override function provides a mechanism overriding the AM_LOG_LEVEL_FILE
            variable and context configuration setting.

            :param level: The file log level.
        """
        ctx = ContextSingleton()
        ctx.insert(ContextPaths.LOGGING_LEVEL_LOGFILE, level)

        AM_RUNTIME_VARIABLES.AM_LOG_LEVEL_FILE = level
        return

    @staticmethod
    def override_output_directory(output_directory: str):
        """
            This override function provides a mechanism overriding the AM_STARTTIME
            variable and context configuration setting.

            :param output_directory: The base directory that all output artifacts will be written under.
        """
        ctx = ContextSingleton()
        ctx.insert(ContextPaths.OUTPUT_DIRECTORY, output_directory)

        AM_RUNTIME_VARIABLES.AM_OUTPUT_DIRECTORY = output_directory
        return

    @staticmethod
    def override_pipeline_id(pipeline_id: str):
        """
            This override function provides a mechanism overriding the AM_PIPELINE_ID
            variable and context configuration setting.

            :param pipeline_id: A uuid string that represents a unique pipeline.
        """
        ctx = ContextSingleton()
        ctx.insert(ContextPaths.PIPELINE_ID, pipeline_id)

        AM_RUNTIME_VARIABLES.AM_PIPELINE_ID = pipeline_id
        return

    @staticmethod
    def override_pipeline_name(pipeline_name: str):
        """
            This override function provides a mechanism overriding the AM_PIPELINE_NAME
            variable and context configuration setting.

            :param pipeline_name: A string that contains the name for a given pipeline.
        """
        ctx = ContextSingleton()
        ctx.insert(ContextPaths.PIPELINE_NAME, pipeline_name)

        AM_RUNTIME_VARIABLES.AM_PIPELINE_NAME = pipeline_name
        return

    @staticmethod
    def override_pipeline_name(pipeline_instance: str):
        """
            This override function provides a mechanism overriding the AM_PIPELINE_NAME
            variable and context configuration setting.

            :param pipeline_instance: A uuid string that represents the instance of a given pipeline.
        """
        ctx = ContextSingleton()
        ctx.insert(ContextPaths.PIPELINE_INSTANCE, pipeline_instance)

        AM_RUNTIME_VARIABLES.AM_PIPELINE_INSTANCE = pipeline_instance
        return

    @staticmethod
    def override_run_id(run_id: str):
        """
            This override function provides a mechanism overriding the AM_RUN_ID
            variable and context configuration setting.

            :param runid: A uuid string that represents the instance of this automation run.
        """
        ctx = ContextSingleton()
        ctx.insert(ContextPaths.RUNID, run_id)

        AM_RUNTIME_VARIABLES.AM_RUN_ID = run_id
        return

    @staticmethod
    def override_shared_store_directory(store_dir: str):
        """
            This override function provides a mechanism overriding the AM_SHARED_STORE_DIRECTORY
            variable and context configuration setting.

            :param store_dir: The shared store directory.
        """
        ctx = ContextSingleton()
        ctx.insert(ContextPaths.SHARED_STORE_DIRECTORY, store_dir)

        AM_RUNTIME_VARIABLES.AM_SHARED_STORE_DIRECTORY = store_dir
        return

    @staticmethod
    def override_starttime(starttime: datetime):
        """
            This override function provides a mechanism overriding the AM_STARTTIME
            variable and context configuration setting.

            :param starttime: The date and time to set as the starttime of this run.
        """
        ctx = ContextSingleton()
        ctx.insert(ContextPaths.STARTTIME, starttime)

        AM_RUNTIME_VARIABLES.AM_STARTTIME = starttime
        return

    @staticmethod
    def override_testroot(testroot: str):
        """
            This override function provides a mechanism overriding the AM_TESTROOT
            variable and context configuration setting.

            :param testroot: The full path of the root of the tests folder.
        """
        ctx = ContextSingleton()
        ctx.insert(ContextPaths.TESTROOT, testroot)

        AM_RUNTIME_VARIABLES.AM_TESTROOT = testroot
        return
