"""
.. module:: extensionfactory
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the ExtFactory base type.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


class ExtensionFactory:
    """
        Base class for extension factories.

        Extension factory classes inherit from this type in order to
        participate in the extension discovery and creation process.
    """

    PRECEDENCE = 0
