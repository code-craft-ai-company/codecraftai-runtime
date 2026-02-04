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

from automojo.thisapp.wellknown import ThisApplicationSingleton

from automojo.runtime.runtimevariables import RuntimeVariablesDesc

class AM_RUNTIME_OPTION_OVERRIDES:

    @staticmethod
    def override_build_release(release: str):
        """
            This override function provides a mechanism overriding the AM_BUILD_BRANCH
            variable and context configuration setting.

            :param release: The name of the release associated with a build.
        """
        this_app = ThisApplicationSingleton()
        this_app.override_variable_value(RuntimeVariablesDesc.AM_BUILD_RELEASE, release)
        return

    @staticmethod
    def override_build_branch(branch_name: str):
        """
            This override function provides a mechanism overriding the AM_BUILD_BRANCH
            variable and context configuration setting.

            :param branch: The name of the branch the build came from.
        """
        this_app = ThisApplicationSingleton()
        this_app.override_variable_value(RuntimeVariablesDesc.AM_BUILD_BRANCH, branch_name)
        return

    @staticmethod
    def override_build_flavor(build_flavor: str):
        """
            This override function provides a mechanism overriding the AM_BUILD_FLAVOR
            variable and context configuration setting.

            :param build_flavor: The flavor of the build associated with a job.
        """
        this_app = ThisApplicationSingleton()
        this_app.override_variable_value(RuntimeVariablesDesc.AM_BUILD_FLAVOR, build_flavor)
        return

    @staticmethod
    def override_build_name(build_name: str):
        """
            This override function provides a mechanism overriding the AM_BUILD_NAME
            variable and context configuration setting.

            :param build_name: The build version of the build.
        """
        this_app = ThisApplicationSingleton()
        this_app.override_variable_value(RuntimeVariablesDesc.AM_BUILD_NAME, build_name)
        return

    @staticmethod
    def override_build_url(build_url: str):
        """
            This override function provides a mechanism overriding the AM_BUILD_URL
            variable and context configuration setting.

            :param build_url: The url associated with the build.
        """
        this_app = ThisApplicationSingleton()
        this_app.override_variable_value(RuntimeVariablesDesc.AM_BUILD_URL, build_url)
        return

    @staticmethod
    def override_debug_breakpoints(breakpoints: List[str]):
        """
            This override function provides a mechanism overriding the AM_BREAKPOINTS
            variable and context configuration setting.

            :param breakpoints: A list of wellknown breakpoints that have been activated.
        """
        this_app = ThisApplicationSingleton()
        this_app.override_variable_value(RuntimeVariablesDesc.AM_DEBUG_BREAKPOINTS, breakpoints)
        return

    @staticmethod
    def override_debug_debugger(debugger: str):
        """
            This override function provides a mechanism overriding the AM_DEBUGGER
            variable and context configuration setting.

            :param debugger: The name of the debugger to setup.
        """
        this_app = ThisApplicationSingleton()
        this_app.override_variable_value(RuntimeVariablesDesc.AM_DEBUG_DEBUGGER, debugger)
        return

    @staticmethod
    def override_job_id(job_id: str):
        """
            This override function provides a mechanism overriding the AM_JOB_ID
            variable and context configuration setting.

            :param runid: A uuid string that represents the instance of this automation run.
        """
        this_app = ThisApplicationSingleton()
        this_app.override_variable_value(RuntimeVariablesDesc.AM_JOB_ID, job_id)
        return

    @staticmethod
    def override_job_initiator(job_initiator: str):
        """
            This override function provides a mechanism overriding the AM_JOB_INITIATOR
            variable and context configuration setting.

            :param job_initiator: The name of the initiator of the job.
        """
        this_app = ThisApplicationSingleton()
        this_app.override_variable_value(RuntimeVariablesDesc.AM_JOB_INITIATOR, job_initiator)
        return

    @staticmethod
    def override_job_label(job_label: str):
        """
            This override function provides a mechanism overriding the AM_JOB_LABEL
            variable and context configuration setting.

            :param job_label: The name of the label if any the job was run under.
        """
        this_app = ThisApplicationSingleton()
        this_app.override_variable_value(RuntimeVariablesDesc.AM_JOB_LABEL, job_label)
        return

    @staticmethod
    def override_diagnostics_postrun(diags: dict):
        """
            This override function provides a mechanism for overriding the AM_DIAGNOSTICS_POSTRUN
            variable and context configuration settings.
        
            :param diags: A dictionary of diagnostics details to capture.
        """
        this_app = ThisApplicationSingleton()
        this_app.override_variable_value(RuntimeVariablesDesc.AM_DIAGNOSTICS_POSTRUN, diags)
        return

    @staticmethod
    def override_diagnostics_prerun(diags: dict):
        """
            This override function provides a mechanism for overriding the AM_DIAGNOSTICS_PRERUN
            variable and context configuration settings.
        
            :param diags: A dictionary of diagnostics details to capture.
        """
        this_app = ThisApplicationSingleton()
        this_app.override_variable_value(RuntimeVariablesDesc.AM_DIAGNOSTICS_PRERUN, diags)
        return

    @staticmethod
    def override_job_name(job_name: str):
        """
            This override function provides a mechanism overriding the AM_JOB_NAME
            variable and context configuration setting.

            :param job_name: The name of the job.
        """
        this_app = ThisApplicationSingleton()
        this_app.override_variable_value(RuntimeVariablesDesc.AM_JOB_NAME, job_name)
        return

    @staticmethod
    def override_job_owner(job_owner: str):
        """
            This override function provides a mechanism overriding the AM_JOB_OWNER
            variable and context configuration setting.

            :param job_owner: The name of the owner of the job.
        """
        this_app = ThisApplicationSingleton()
        this_app.override_variable_value(RuntimeVariablesDesc.AM_JOB_OWNER, job_owner)
        return
    
    @staticmethod
    def override_job_seed(job_seed: str):
        """
            This override function provides a mechanism overriding the AM_JOB_SEED
            variable and context configuration setting.

            :param job_seed: The type of the job.
        """
        this_app = ThisApplicationSingleton()
        this_app.override_variable_value(RuntimeVariablesDesc.AM_JOB_SEED, job_seed)
        return

    @staticmethod
    def override_job_tag(job_tag: str):
        """
            This override function provides a mechanism overriding the AM_JOB_TAG
            variable and context configuration setting.

            :param job_tag: The tags for the job.
        """
        this_app = ThisApplicationSingleton()
        this_app.override_variable_value(RuntimeVariablesDesc.AM_JOB_TAG, job_tag)
        return

    @staticmethod
    def override_job_type(job_type: str):
        """
            This override function provides a mechanism overriding the AM_JOB_TYPE
            variable and context configuration setting.

            :param job_owner: The type of the job.
        """
        this_app = ThisApplicationSingleton()
        this_app.override_variable_value(RuntimeVariablesDesc.AM_JOB_TYPE, job_type)
        return

    @staticmethod
    def override_loglevel_console(level: str):
        """
            This override function provides a mechanism overriding the AM_LOG_LEVEL_CONSOLE
            variable and context configuration setting.

            :param level: The console logging level.
        """
        this_app = ThisApplicationSingleton()
        this_app.override_variable_value(RuntimeVariablesDesc.AM_LOG_LEVEL_CONSOLE, level)
        return

    @staticmethod
    def override_loglevel_file(level: str):
        """
            This override function provides a mechanism overriding the AM_LOG_LEVEL_FILE
            variable and context configuration setting.

            :param level: The file log level.
        """
        this_app = ThisApplicationSingleton()
        this_app.override_variable_value(RuntimeVariablesDesc.AM_LOG_LEVEL_FILE, level)
        return

    @staticmethod
    def override_output_directory(output_directory: str):
        """
            This override function provides a mechanism overriding the AM_STARTTIME
            variable and context configuration setting.

            :param output_directory: The base directory that all output artifacts will be written under.
        """
        this_app = ThisApplicationSingleton()
        this_app.override_variable_value(RuntimeVariablesDesc.AM_OUTPUT_DIRECTORY, output_directory)
        return

    @staticmethod
    def override_pipeline_id(pipeline_id: str):
        """
            This override function provides a mechanism overriding the AM_PIPELINE_ID
            variable and context configuration setting.

            :param pipeline_id: A uuid string that represents a unique pipeline.
        """
        this_app = ThisApplicationSingleton()
        this_app.override_variable_value(RuntimeVariablesDesc.AM_PIPELINE_ID, pipeline_id)
        return

    @staticmethod
    def override_pipeline_name(pipeline_name: str):
        """
            This override function provides a mechanism overriding the AM_PIPELINE_NAME
            variable and context configuration setting.

            :param pipeline_name: A string that contains the name for a given pipeline.
        """
        this_app = ThisApplicationSingleton()
        this_app.override_variable_value(RuntimeVariablesDesc.AM_PIPELINE_NAME, pipeline_name)
        return

    @staticmethod
    def override_pipeline_instance(pipeline_instance: str):
        """
            This override function provides a mechanism overriding the AM_PIPELINE_INSTANCE
            variable and context configuration setting.

            :param pipeline_instance: A uuid string that represents the instance of a given pipeline.
        """
        this_app = ThisApplicationSingleton()
        this_app.override_variable_value(RuntimeVariablesDesc.AM_PIPELINE_INSTANCE, pipeline_instance)
        return

    @staticmethod
    def override_run_id(run_id: str):
        """
            This override function provides a mechanism overriding the AM_RUN_ID
            variable and context configuration setting.

            :param runid: A uuid string that represents the instance of this automation run.
        """
        this_app = ThisApplicationSingleton()
        this_app.override_variable_value(RuntimeVariablesDesc.AM_RUN_ID, run_id)
        return

    @staticmethod
    def override_shared_store_directory(store_dir: str):
        """
            This override function provides a mechanism overriding the AM_SHARED_STORE_DIRECTORY
            variable and context configuration setting.

            :param store_dir: The shared store directory.
        """
        this_app = ThisApplicationSingleton()
        this_app.override_variable_value(RuntimeVariablesDesc.AM_SHARED_STORE_DIRECTORY, store_dir)
        return

    @staticmethod
    def override_starttime(starttime: datetime):
        """
            This override function provides a mechanism overriding the AM_STARTTIME
            variable and context configuration setting.

            :param starttime: The date and time to set as the starttime of this run.
        """
        this_app = ThisApplicationSingleton()
        this_app.override_variable_value(RuntimeVariablesDesc.AM_STARTTIME, starttime)
        return

    @staticmethod
    def override_testroot(testroot: str):
        """
            This override function provides a mechanism overriding the AM_TESTROOT
            variable and context configuration setting.

            :param testroot: The full path of the root of the tests folder.
        """
        this_app = ThisApplicationSingleton()
        this_app.override_variable_value(RuntimeVariablesDesc.AM_TESTROOT, testroot)
        return
