"""
    .. module:: ccai.runtime.activation
    :synopsis: TEMPORARY compatibility shim.

    The runtime foundation moved to :mod:`ccai.thisapp.activation` as part of the
    testbase / integration-runtime refactor (Phase 1). This shim re-exports those symbols so
    existing ``ccai.runtime.activation`` importers keep working during the migration.

    REMOVE this shim when ``codecraftai-runtime`` is retired. See
    ``REFACTOR-TESTBASE-INTEGRATION-RUNTIME-ROADMAP.md`` at the monorepo root.
"""

from ccai.thisapp.activation import *  # noqa: F401,F403
from ccai.thisapp.activation import (  # noqa: F401
    activate_profile_command,
    activate_profile_console,
    activate_profile_service,
    activate_profile_job,
)
