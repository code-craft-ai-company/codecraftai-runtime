========================
Code Craft AI Runtime
========================

The ``codecraftai-runtime`` package provides the runtime-configuration and activation layer that codecraftai-based applications and tools share. It is responsible for establishing logging, runtime variables, and well-known paths early in a process's lifecycle so that downstream packages can rely on a consistent environment regardless of whether the caller is a CLI, a service, or a test runner.

Highlights
==========

- ``activation.py`` drives the activation sequence that wires up logging and registers the current ``ThisApplication`` singleton.
- ``runtimevariables.py`` defines the ``RuntimeVariables`` descriptor set with default-value handling.
- ``enumerations.py`` provides ``ActivationProfile`` and ``JobType``.
- ``paths.py`` centralises path discovery.
- ``optionoverrides.py`` supports CLI-level option overrides.

Repository Structure
====================

- ``development/`` - Runtime environment scripts.
- ``repository-setup/`` - Repository homing and setup scripts.
- ``source/packages/`` - Package source code.
- ``source/tests/`` - ``unittest``-based tests.
- ``specs/`` - Requirements, design, and task documentation.
- ``userguide/`` - Standards, conventions, and documentation.

Environment Setup
=================

When working in a Codex container:

.. code-block:: bash

   ./development/setup-agent-container

For local development:

.. code-block:: bash

   ./repository-setup/rehome-repository
   ./development/setup-envrionment

Running Tests
=============

Activate the virtual environment:

.. code-block:: bash

   source .venv/bin/activate

Run ``unittest`` tests:

.. code-block:: bash

   python -m unittest discover -s source/tests -p "test_*.py"

Standards and Conventions
=========================

- Naming conventions: ``userguide/10-02-naming-conventions.rst``
- Code organization: ``userguide/10-01-code-organization.rst``
- Coding standards: ``userguide/10-00-coding-standards.rst``

Additional Resources
====================

- User guide entry point: ``userguide/userguide.rst``
- Design documentation: ``specs/design.md``
- Requirements: ``specs/requirements.md``
