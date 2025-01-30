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


from automojo.startup.startupsettings import AMR_STARTUP_DEFAULTS
from automojo.startup.startupvariablenames import AMR_STARTUP_VARIABLE_NAMES
from automojo.startup.startupconfigloader import StartupConfigLoader


class AMR_STARTUP_VARIABLES:

    AMR_NAME = AMR_STARTUP_DEFAULTS.AMR_NAME
    AMR_PRESENCE_DIRECTORY = AMR_STARTUP_DEFAULTS.AMR_PRESENCE_DIRECTORY
    AMR_SETTINGS_FILE = AMR_STARTUP_DEFAULTS.AMR_SETTINGS_FILE
    AMR_EXTENSION_MODULES = AMR_STARTUP_DEFAULTS.AMR_EXTENSION_MODULES
 

def resolve_startup_variables():

    config_parser = StartupConfigLoader("DEFAULT")

    AMR_STARTUP_VARIABLES.AMR_EXTENSION_MODULES = config_parser.read(
        AMR_STARTUP_VARIABLE_NAMES.AMR_EXTENSION_MODULES, AMR_STARTUP_DEFAULTS.AMR_EXTENSION_MODULES)

    return
