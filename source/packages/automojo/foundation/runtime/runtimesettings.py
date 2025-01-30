"""
.. module:: runtimedefaults
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains defaults that can be overridden to customize the runtime.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []


from typing import Optional

from mojo.startup.presencesettings import AM_PRESENCE_DEFAULTS
from mojo.startup.wellknown import StartupConfigSingleton

from mojo.config.configurationsettings import (
    AM_CONFIG_DEFAULTS,
    establish_config_settings
)

default_config = {}

startup_config = StartupConfigSingleton()
if "DEFAULT" in startup_config:
    default_config = startup_config["DEFAULT"]

class AM_RUNTIME_DEFAULTS(AM_CONFIG_DEFAULTS):

    AM_LOGGER_NAME = "MJR"
    AM_SERVICE_NAME = None


RUNTIME_SETTINGS_ESTABLISHED = False

def establish_runtime_settings(*, name: Optional[str]=None, home_dir: Optional[str]=None, settings_file: Optional[str]=None,
                               extension_modules: Optional[str]=None, logger_name: Optional[str]=None, default_configuration: dict=None,
                               service_name: Optional[str]=None, **other):
    
    global RUNTIME_SETTINGS_ESTABLISHED

    if not RUNTIME_SETTINGS_ESTABLISHED:
        RUNTIME_SETTINGS_ESTABLISHED = True

        establish_config_settings(name=name, home_dir=home_dir, settings_file=settings_file, extension_modules=extension_modules,
                                  default_configuration=default_configuration, **other)

        if logger_name is not None:
            AM_RUNTIME_DEFAULTS.AM_LOGGER_NAME = logger_name
        else:
            AM_RUNTIME_DEFAULTS.AM_LOGGER_NAME = AM_PRESENCE_DEFAULTS.AM_NAME.upper()

        if service_name is not None:
            AM_RUNTIME_DEFAULTS.AM_SERVICE_NAME = service_name

    return
