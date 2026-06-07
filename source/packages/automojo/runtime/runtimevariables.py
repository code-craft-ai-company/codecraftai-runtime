"""
    .. module:: automojo.runtime.runtimevariables
    :synopsis: TEMPORARY compatibility shim.

    The runtime foundation moved to :mod:`automojo.thisapp.runtimevariables` as part of the
    testbase / integration-runtime refactor (Phase 1). This shim re-exports those symbols so
    existing ``automojo.runtime.runtimevariables`` importers keep working during the migration.

    REMOVE this shim when ``automojo-runtime`` is retired. See
    ``REFACTOR-TESTBASE-INTEGRATION-RUNTIME-ROADMAP.md`` at the monorepo root.
"""

from automojo.thisapp.runtimevariables import *  # noqa: F401,F403
from automojo.thisapp.runtimevariables import (  # noqa: F401
    DefaultValue,
    RuntimeVariablesDesc,
    RuntimeVariables,
    resolve_runtime_variables,
    get_runtime_seed,
    default_template_path_for_tests,
    default_job_seed,
)
