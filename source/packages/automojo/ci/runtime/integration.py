"""
.. module:: integration
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Runtime integration helpers used by testing frameworks.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import Dict

from automojo.foundation.collections.contextpaths import ContextPaths
from automojo.foundation.collections.wellknown import ContextSingleton


def get_job_info() -> Dict[str, str]:

    ctx = ContextSingleton()

    rtnval = ctx.lookup(ContextPaths.JOB_INFO)

    return rtnval

def get_job_id() -> str:

    ctx = ContextSingleton()

    rtnval = ctx.lookup(ContextPaths.JOB_ID)

    return rtnval

def get_job_initiator() -> str:

    ctx = ContextSingleton()

    rtnval = ctx.lookup(ContextPaths.JOB_INITIATOR)

    return rtnval

def get_job_label() -> str:

    ctx = ContextSingleton()

    rtnval = ctx.lookup(ContextPaths.JOB_LABEL)

    return rtnval

def get_job_name() -> str:

    ctx = ContextSingleton()

    rtnval = ctx.lookup(ContextPaths.JOB_NAME)

    return rtnval

def get_job_owner() -> str:

    ctx = ContextSingleton()

    rtnval = ctx.lookup(ContextPaths.JOB_OWNER)

    return rtnval

def get_job_type() -> str:

    ctx = ContextSingleton()

    rtnval = ctx.lookup(ContextPaths.JOB_TYPE)

    return rtnval

def get_job_venue() -> str:

    ctx = ContextSingleton()

    rtnval = ctx.lookup(ContextPaths.JOB_VENUE)

    return rtnval

def get_pipeline_info() -> Dict[str, str]:

    ctx = ContextSingleton()

    rtnval = ctx.lookup(ContextPaths.PIPELINE_INFO)

    return rtnval

def get_pipeline_id() -> str:

    ctx = ContextSingleton()

    rtnval = ctx.lookup(ContextPaths.PIPELINE_ID)

    return rtnval

def get_pipeline_instance() -> str:

    ctx = ContextSingleton()

    rtnval = ctx.lookup(ContextPaths.PIPELINE_INSTANCE)

    return rtnval

def get_pipeline_name() -> str:

    ctx = ContextSingleton()

    rtnval = ctx.lookup(ContextPaths.PIPELINE_NAME)

    return rtnval