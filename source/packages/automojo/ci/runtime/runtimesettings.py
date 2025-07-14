"""
.. module:: runtimedefaults
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains defaults that can be overridden to customize the runtime.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import Optional


from automojo.configuration.configurationsettings import (
    establish_configuration_settings,
    AM_CONFIG_DEFAULTS
)

class AM_RUNTIME_DEFAULTS(AM_CONFIG_DEFAULTS):

    AM_LOGGER_NAME = None
    AM_SERVICE_NAME = None


RUNTIME_SETTINGS_ESTABLISHED = False


def establish_runtime_settings(*, name: Optional[str]=None, home_dir: Optional[str]=None, settings_file: Optional[str]=None,
                               extension_modules: Optional[str]=None, logger_name: Optional[str]=None,
                               log_basename: Optional[str]=None, log_directory: Optional[str]=None,
                               default_configuration: Optional[dict]=None, **other):
    
    global RUNTIME_SETTINGS_ESTABLISHED

    if not RUNTIME_SETTINGS_ESTABLISHED:
        RUNTIME_SETTINGS_ESTABLISHED = True

        establish_configuration_settings(name=name, home_dir=home_dir, settings_file=settings_file, extension_modules=extension_modules,
                                         log_basename=log_basename, log_directory=log_directory,
                                         default_configuration=default_configuration, **other)

        if logger_name is not None:
            AM_RUNTIME_DEFAULTS.AM_LOGGER_NAME = logger_name
        else:
            AM_RUNTIME_DEFAULTS.AM_LOGGER_NAME = AM_RUNTIME_DEFAULTS.AM_NAME.upper()

    return
