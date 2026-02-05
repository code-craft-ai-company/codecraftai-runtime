"""
.. module:: automojo.foundation.runtime
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Runtime helper package.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

try:
    from automojo.thisapp.contextpaths import ContextPaths

    # Polyfill for missing attributes in older versions of automojo-this-app
    # These are required by automojo.runtime.runtimevariables
    if not hasattr(ContextPaths, "TEMPLATE_PATH_FOR_BUILD"):
        setattr(ContextPaths, "TEMPLATE_PATH_FOR_BUILD", "TEMPLATE_PATH_FOR_BUILD")
    if not hasattr(ContextPaths, "TEMPLATE_PATH_FOR_INFRASTRUCTURE"):
        setattr(ContextPaths, "TEMPLATE_PATH_FOR_INFRASTRUCTURE", "TEMPLATE_PATH_FOR_INFRASTRUCTURE")
    if not hasattr(ContextPaths, "RESULT_PATH_FOR_BUILD"):
        setattr(ContextPaths, "RESULT_PATH_FOR_BUILD", "RESULT_PATH_FOR_BUILD")
    if not hasattr(ContextPaths, "RESULT_PATH_FOR_INFRASTRUCTURE"):
        setattr(ContextPaths, "RESULT_PATH_FOR_INFRASTRUCTURE", "RESULT_PATH_FOR_INFRASTRUCTURE")

except ImportError:
    pass
