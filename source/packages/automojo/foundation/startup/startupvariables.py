"""
.. module:: startupvariables
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the most basic variables required to begin the startup
               of a customized mojo environment.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []


from automojo.foundation.startup.startupsettings import AM_STARTUP_DEFAULTS
from automojo.foundation.startup.startupvariablenames import AM_STARTUP_VARIABLE_NAMES
from automojo.foundation.startup.startupconfigloader import StartupConfigLoader

from automojo.foundation.collections.contextpaths import ContextPaths
from automojo.foundation.collections.wellknown import ContextSingleton

class AM_STARTUP_VARIABLES:

    AM_NAME = AM_STARTUP_DEFAULTS.AM_NAME
    AM_PRESENCE_DIRECTORY = AM_STARTUP_DEFAULTS.AM_PRESENCE_DIRECTORY
    AM_SETTINGS_FILE = AM_STARTUP_DEFAULTS.AM_SETTINGS_FILE
    AM_EXTENSION_MODULES = AM_STARTUP_DEFAULTS.AM_EXTENSION_MODULES
 

def resolve_startup_variables():

    ctx = ContextSingleton()

    config_parser = StartupConfigLoader("DEFAULT")

    AM_STARTUP_VARIABLES.AM_NAME = config_parser.get_variable_value(
        AM_STARTUP_VARIABLE_NAMES.AM_NAME, default=AM_STARTUP_DEFAULTS.AM_NAME)
    
    ctx.insert(ContextPaths.PRESENCE_NAME, AM_STARTUP_VARIABLES.AM_NAME)

    AM_STARTUP_VARIABLES.AM_PRESENCE_DIRECTORY = config_parser.get_variable_value(
        AM_STARTUP_VARIABLE_NAMES.AM_PRESENCE_DIRECTORY, default=AM_STARTUP_DEFAULTS.AM_PRESENCE_DIRECTORY)

    ctx.insert(ContextPaths.PRESENCE_HOME_DIRECTORY, AM_STARTUP_VARIABLES.AM_PRESENCE_DIRECTORY)

    AM_STARTUP_VARIABLES.AM_EXTENSION_MODULES = config_parser.get_variable_value(
        AM_STARTUP_VARIABLE_NAMES.AM_EXTENSION_MODULES, default=AM_STARTUP_DEFAULTS.AM_EXTENSION_MODULES)
    
    ctx.insert(ContextPaths.PRESENCE_EXTENSION_MODULES, AM_STARTUP_VARIABLES.AM_EXTENSION_MODULES)

    return
