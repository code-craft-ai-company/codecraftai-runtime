"""
    .. module:: automojo.runtime.paths
    :synopsis: TEMPORARY compatibility shim.

    The runtime foundation moved to :mod:`automojo.thisapp.paths` as part of the
    testbase / integration-runtime refactor (Phase 1). This shim re-exports those symbols so
    existing ``automojo.runtime.paths`` importers keep working during the migration.

    NOTE: the test-reporting path helpers (``get_path_for_testresults``,
    ``get_path_for_diagnostics``, ``get_path_for_testcase_by_products``,
    ``get_summary_html_template_source``, ``get_summary_static_resource_*``) relocate again to
    ``automojo-integration-runtime`` in Phase 3, alongside the recorder that consumes them.

    REMOVE this shim when ``automojo-runtime`` is retired. See
    ``REFACTOR-TESTBASE-INTEGRATION-RUNTIME-ROADMAP.md`` at the monorepo root.
"""

from automojo.thisapp.paths import *  # noqa: F401,F403
from automojo.thisapp.paths import (  # noqa: F401
    collect_python_modules,
    ensure_directory_is_package,
    get_directory_for_cached_files,
    get_directory_for_code_container,
    get_path_for_artifacts,
    get_path_for_output,
    get_path_for_shared_store,
    get_path_for_diagnostics,
    get_path_for_testresults,
    get_path_for_testcase_by_products,
    get_presence_directory,
    get_summary_html_template_source,
    get_summary_static_resource_dest_dir,
    get_summary_static_resource_src_dir,
    get_temporary_directory,
    get_temporary_file,
    normalize_name_for_path,
    utilizing_shared_output_path,
)
