"""
.. module:: extensionprotocolbase
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the ExtProtocol base type.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import Protocol

class ExtensionProtocolBase(Protocol):
    """
        Base protocol for extension factories.

        Subclasses must set ``ext_protocol_name`` to identify the protocol they
        implement.
    """

    ext_protocol_name = None

    def __init_subclass__(cls, *args, **kwargs):
        """
            Validates that derived classes specify ``ext_protocol_name``.
        """
        if cls.ext_protocol_name is None:
            errmsg = (
                "The 'protocol_name' class level field must be set on derived protocol types."
            )
            raise RuntimeError(errmsg)
        return super().__init_subclass__(*args, **kwargs)
