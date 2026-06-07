"""
    .. module:: ccai.runtime.enumerations
    :synopsis: TEMPORARY compatibility shim.

    The runtime foundation moved to :mod:`ccai.thisapp.enumerations` as part of the
    testbase / integration-runtime refactor (Phase 1). This shim re-exports those symbols so
    existing ``ccai.runtime.enumerations`` importers keep working during the migration.

    REMOVE this shim when ``codecraftai-runtime`` is retired. See
    ``REFACTOR-TESTBASE-INTEGRATION-RUNTIME-ROADMAP.md`` at the monorepo root.
"""

from ccai.thisapp.enumerations import *  # noqa: F401,F403
from ccai.thisapp.enumerations import (  # noqa: F401
    ActivationProfile,
    JobType,
)
