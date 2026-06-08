"""
    .. module:: ccai.runtime.runtimevariables
    :synopsis: TEMPORARY compatibility shim.

    The runtime foundation moved to :mod:`ccai.thisapp.runtimevariables` as part of the
    testbase / integration-runtime refactor (Phase 1). This shim re-exports those symbols so
    existing ``ccai.runtime.runtimevariables`` importers keep working during the migration.

    REMOVE this shim when ``codecraftai-runtime`` is retired. See
    ``REFACTOR-TESTBASE-INTEGRATION-RUNTIME-ROADMAP.md`` at the monorepo root.
"""

from ccai.thisapp.runtimevariables import *  # noqa: F401,F403
from ccai.thisapp.runtimevariables import (  # noqa: F401
    DefaultValue,
    RuntimeVariablesDesc,
    RuntimeVariables,
    resolve_runtime_variables,
    get_runtime_seed,
    default_template_path_for_tests,
    default_job_seed,
)
