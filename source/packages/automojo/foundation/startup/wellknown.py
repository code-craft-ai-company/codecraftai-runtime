"""
.. module:: wellknown
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that provides a wellknow startup configuration singleton.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


import os
import threading

from configparser import ConfigParser


# NOTE: This code is loaded super early where there is likely to only be a single thread
#       so there is likely no need for any locking.

STARTUP_CONFIG_PARSER = None

SINGLETON_LOCK = threading.RLock()


def StartupConfigSingleton():

    global STARTUP_CONFIG

    SINGLETON_LOCK.acquire()
    try:
        if STARTUP_CONFIG is None:
            STARTUP_CONFIG = ConfigParser()

            from automojo.foundation.startup.startupvariables import AM_STARTUP_VARIABLES
            
            if os.path.exists(AM_STARTUP_VARIABLES.AM_SETTINGS_FILE):
                STARTUP_CONFIG.read(AM_STARTUP_VARIABLES.AM_SETTINGS_FILE)
    finally:
        SINGLETON_LOCK.release()

    return STARTUP_CONFIG
