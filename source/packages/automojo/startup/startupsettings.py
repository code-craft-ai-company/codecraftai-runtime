"""
.. module:: startupsettings
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the settings necessary to establish a presence on the users machine.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import Optional

import os


class AMR_STARTUP_DEFAULTS:

    AMR_NAME = "AMR"
    AMR_PRESENCE_DIRECTORY = os.path.expanduser(os.path.join("~", AMR_NAME.lower()))
    AMR_SETTINGS_FILE = os.path.join(AMR_PRESENCE_DIRECTORY, "amr-settings.config")
    AMR_EXTENSION_MODULES = ""


STARTUP_SETTINGS_ESTABLISHED = False


def establish_presence_settings(*, name: Optional[str]=None, presence_dir: Optional[str]=None, settings_file: Optional[str]=None, extension_modules: Optional[str]=None, **other):
    """
        The `establish_extension_settings` method is called to modify the name and home folder of the environment.  This is accomplished
        by overloading a the 'Startup' defaults.  The name and home directory might still be changed later during the 'Parameterize' phase.

        :param name: A one word name for the environment.
        :param presence_dir: The app folder underneath the home directory where the framework establishes
                             a presence for settings, configuration, and results.
        :param settings_file: The path to the settings initiliazation file.
        :param extension_modules: A comma seperated list of full module names.

    """

    global STARTUP_SETTINGS_ESTABLISHED

    if not STARTUP_SETTINGS_ESTABLISHED:
        STARTUP_SETTINGS_ESTABLISHED = True

        if name is not None:
            AMR_STARTUP_DEFAULTS.AMR_NAME = name
        if presence_dir is not None:
            AMR_STARTUP_DEFAULTS.AMR_PRESENCE_DIRECTORY = presence_dir
        if settings_file is not None:
            AMR_STARTUP_DEFAULTS.AMR_SETTINGS_FILE = settings_file
        if extension_modules is not None:
            AMR_STARTUP_DEFAULTS.AMR_EXTENSION_MODULES = extension_modules

    return

