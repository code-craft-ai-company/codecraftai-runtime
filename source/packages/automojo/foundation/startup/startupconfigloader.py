"""
.. module:: startupconfigloader
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the :class:`StartupConfigLoader` object.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import Any, Optional, Protocol, Union

import os

from automojo.foundation.startup.wellknown import StartupConfigSingleton


class SettingConverter(Protocol):
    def __call__(self, string_value: str) -> Any:
        return


class StartupConfigLoader:
    """
        The :class:`StartupConfigLoader` object is utilized by other packages to load configuration
        out of a module specific section of the startup configuration file.
        
        Variables loaded during the startup configuration load phase of runtime startup, follow a specific
        pattern of load precedent.  A startup configuration variable can come from one of two places, from the
        startup configuration file, or from an environment variable.
        
        The :class:`StartupConfigLoader` enforces a common variable load rule which is that variable values found
        in the process environment, always take precedence over variable values found in a configuration
        file.
    """

    def __init__(self, config_section_name: str):
        """
            Initializes the loader for the specified configuration section.

            :param config_section_name: Name of the section to read from the startup configuration file.
        """
        self._config_section_name = config_section_name

        self._cparser = StartupConfigSingleton()
        self._conf_section = None
        if config_section_name in self._cparser:
            self._conf_section = self._cparser[config_section_name]

        return
    
    def get_variable_value(self, variable_name: str, default: Optional[str]=None, converter: Optional[SettingConverter] = None) -> Union[str, Any]:
        """
            The the value of a variable from the environment.  If an environment variable is not found look in the settings file.
            If the variable is not in the settings file, use the default value being passed in.

            :param variable_name: The name of the variable to lookup
            :param default: The default value to return if the variable is not found.
            :param converter: A lamba expression of function that will convert the str value to a consumable python type.

            :returns: A str value or type if a converter was passed.
        """

        vval = default

        if variable_name in os.environ:
            vval = os.environ[variable_name]
        elif self._conf_section is not None:
            if variable_name in self._conf_section:
                vval = self._conf_section[variable_name]

        if converter is not None and isinstance(vval, str):
            vval = converter(vval)

        return vval
