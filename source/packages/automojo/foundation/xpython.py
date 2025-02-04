"""
.. module:: xpython
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains additional helper functions for modifying the root
               python behavior

.. note:: The modules that are named `xsomething` like this module are prefixed with an `x` character to
          indicate they extend the functionality of a base python module and the `x` is pre-pended to
          prevent module name collisions with python modules.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


import os
import sys

from automojo.foundation.fspath import expand_path

def in_python_path(dir_to_check: str) -> bool:
    """
        Checks if a directory is in the PYTHONPATH in the current python process.
    """
    dir_to_check = expand_path(dir_to_check).rstrip(os.sep)

    found = False

    for nxt_item in sys.path:
        nxt_item = expand_path(nxt_item.rstrip(os.sep))
        if nxt_item == dir_to_check:
            found = True
            break

    return found


def prepend_python_path(dir_to_add: str) -> None:
    """
        Prepends a directory to the PYTHONPATH in the current python process and also modifies
        'PYTHONPATH' so the child processes will also see inherit the extension
        of 'PYTHONPATH'.
    """
    found = in_python_path(dir_to_add)

    if not found:
        sys.path.insert(0, dir_to_add)
        if "PYTHONPATH" in os.environ:
            os.environ["PYTHONPATH"] = dir_to_add + os.pathsep + os.environ["PYTHONPATH"]
        else:
            os.environ["PYTHONPATH"] = dir_to_add

    return

def append_python_path(dir_to_add: str) -> None:
    """
        Appends a directory to the PYTHONPATH in the current python process and also modifies
        'PYTHONPATH' so the child processes will also see inherit the extension
        of 'PYTHONPATH'.
    """
    found = in_python_path(dir_to_add)

    if not found:
        sys.path.append(dir_to_add)
        if "PYTHONPATH" in os.environ:
            os.environ["PYTHONPATH"] = os.environ["PYTHONPATH"] + os.pathsep + dir_to_add
        else:
            os.environ["PYTHONPATH"] = dir_to_add

    return