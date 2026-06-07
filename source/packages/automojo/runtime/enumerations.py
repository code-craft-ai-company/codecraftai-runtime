"""
    .. module:: automojo.runtime.enumerations
    :synopsis: TEMPORARY compatibility shim.

    The runtime foundation moved to :mod:`automojo.thisapp.enumerations` as part of the
    testbase / integration-runtime refactor (Phase 1). This shim re-exports those symbols so
    existing ``automojo.runtime.enumerations`` importers keep working during the migration.

    REMOVE this shim when ``automojo-runtime`` is retired. See
    ``REFACTOR-TESTBASE-INTEGRATION-RUNTIME-ROADMAP.md`` at the monorepo root.
"""

from automojo.thisapp.enumerations import *  # noqa: F401,F403
from automojo.thisapp.enumerations import (  # noqa: F401
    ActivationProfile,
    JobType,
)
