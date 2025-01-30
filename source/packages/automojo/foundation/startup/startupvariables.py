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


class AM_STARTUP_VARIABLES:

    AM_NAME = AM_STARTUP_DEFAULTS.AM_NAME
    AM_PRESENCE_DIRECTORY = AM_STARTUP_DEFAULTS.AM_PRESENCE_DIRECTORY
    AM_SETTINGS_FILE = AM_STARTUP_DEFAULTS.AM_SETTINGS_FILE
    AM_EXTENSION_MODULES = AM_STARTUP_DEFAULTS.AM_EXTENSION_MODULES
 

def resolve_startup_variables():

    config_parser = StartupConfigLoader("DEFAULT")

    AM_STARTUP_VARIABLES.AM_EXTENSION_MODULES = config_parser.read(
        AM_STARTUP_VARIABLE_NAMES.AM_EXTENSION_MODULES, AM_STARTUP_DEFAULTS.AM_EXTENSION_MODULES)

    return
