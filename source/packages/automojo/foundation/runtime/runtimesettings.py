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

from automojo.foundation.startup.startupsettings import AM_STARTUP_DEFAULTS, establish_presence_settings
from automojo.foundation.startup.wellknown import StartupConfigSingleton


default_config = {}

startup_config = StartupConfigSingleton()
if "DEFAULT" in startup_config:
    default_config = startup_config["DEFAULT"]

class AM_RUNTIME_DEFAULTS(AM_STARTUP_DEFAULTS):

    AM_LOGGER_NAME = None
    AM_SERVICE_NAME = None


RUNTIME_SETTINGS_ESTABLISHED = False

def establish_runtime_settings(*, name: Optional[str]=None, home_dir: Optional[str]=None, settings_file: Optional[str]=None,
                               extension_modules: Optional[str]=None, logger_name: Optional[str]=None, default_configuration: dict=None,
                               service_name: Optional[str]=None, **other):
    
    global RUNTIME_SETTINGS_ESTABLISHED

    if not RUNTIME_SETTINGS_ESTABLISHED:
        RUNTIME_SETTINGS_ESTABLISHED = True

        establish_presence_settings(name=name, home_dir=home_dir, settings_file=settings_file, extension_modules=extension_modules, **other)

        if logger_name is not None:
            AM_RUNTIME_DEFAULTS.AM_LOGGER_NAME = logger_name
        else:
            AM_RUNTIME_DEFAULTS.AM_LOGGER_NAME = AM_STARTUP_DEFAULTS.AM_NAME.upper()

        if service_name is not None:
            AM_RUNTIME_DEFAULTS.AM_SERVICE_NAME = service_name

    return
