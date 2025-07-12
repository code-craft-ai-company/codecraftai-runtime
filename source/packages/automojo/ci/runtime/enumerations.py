"""
.. module:: enumerations
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains runtime enumerations.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from enum import Enum

class ActivationProfile(str, Enum):
    Command = "command"
    Console = "console"
    Orchestration = "orchestration"
    Service = "service"
    TestRun = "testrun"

class JobType(str, Enum):
    Unknown = "unknown"
    Console = "console"
    Service = "service"
    TestRun = "testrun"
    Orchestration = "orchestration"
