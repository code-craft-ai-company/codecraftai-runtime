"""
.. module:: wellknown
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the :class:`ConfiguredSuperFactorySingleton` function
               which provides a singleton instance of the SuperFactory type.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []


import threading

from automojo.errors.exceptions import SemanticError

from automojo.foundation.startup.startupvariables import AM_STARTUP_VARIABLES, resolve_startup_variables

from automojo.foundation.extension.extensionsuperfactory import ExtensionSuperFactory


SINGLETON_LOCK = threading.RLock()

CONFIGURED_SUPER_FACTORY = None


def ConfiguredSuperFactorySingleton():

    global CONFIGURED_SUPER_FACTORY

    SINGLETON_LOCK.acquire()
    try:
        if CONFIGURED_SUPER_FACTORY is None:
            extension_modules = []

            if AM_STARTUP_VARIABLES.AM_EXTENSION_MODULES is None:
                errmsg = "You must first call 'resolve_presence_variables' before attempting to create a ExtensionSuperFactory singleton."
                raise SemanticError(errmsg)

            extension_modules_value: str = AM_STARTUP_VARIABLES.AM_EXTENSION_MODULES
            extension_modules_value.strip()

            if len(extension_modules_value) > 0:
                extension_modules = extension_modules_value.split(",")
            
            CONFIGURED_SUPER_FACTORY = ExtensionSuperFactory(extension_modules)
    finally:
        SINGLETON_LOCK.release()

    return CONFIGURED_SUPER_FACTORY

