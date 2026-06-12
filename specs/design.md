# Code Craft AI Runtime Package Design Document

## Overview

The `ccai.runtime` package historically provided a comprehensive runtime environment management system for automation testing frameworks. It handled application lifecycle, configuration management, logging activation, and resource path management across different execution contexts (command-line, console, service, and job modes).

That runtime foundation has now **moved into `codecraftai-this-app`**. The runtime variables, well-known-path helpers, enumerations, and activation sequence now live in `ccai.thisapp.{runtimevariables,paths,enumerations,activation}`. As a result, `codecraftai-runtime` is being **RETIRED**: its `runtimevariables.py`, `paths.py`, `enumerations.py`, and `activation.py` modules are now thin compatibility shims that re-export their counterparts from `ccai.thisapp.*` so existing `ccai.runtime.X` importers keep working during the migration. The package still ships a real `optionoverrides.py` (`AM_RUNTIME_OPTION_OVERRIDES`) for now.

This document therefore describes two things: (1) the design of the runtime foundation as it now exists in `ccai.thisapp`, and (2) the retirement/relocation shim layer that `codecraftai-runtime` currently provides.

## Architecture

### Relocation Map

The runtime foundation moved as follows. The left column is the legacy import path that the shims preserve; the right column is the authoritative home in `codecraftai-this-app`:

| Legacy module (shim)              | Authoritative home                        |
| --------------------------------- | ----------------------------------------- |
| `ccai.runtime.runtimevariables` | `ccai.thisapp.runtimevariables`     |
| `ccai.runtime.paths`            | `ccai.thisapp.paths`                |
| `ccai.runtime.enumerations`     | `ccai.thisapp.enumerations`         |
| `ccai.runtime.activation`       | `ccai.thisapp.activation`           |
| `ccai.runtime.optionoverrides`  | (remains real code in `codecraftai-runtime`) |

### Current Components

The `codecraftai-runtime` package now consists of:

1. **Activation Shim** (`activation.py`) - Re-exports `activate_profile_command/console/service/job` from `ccai.thisapp.activation`.
2. **Runtime Variables Shim** (`runtimevariables.py`) - Re-exports `RuntimeVariables`, `RuntimeVariablesDesc`, `DefaultValue`, `resolve_runtime_variables`, and the seed/template helpers from `ccai.thisapp.runtimevariables`.
3. **Option Overrides** (`optionoverrides.py`) - **Real code that remains in this package**: programmatic configuration override mechanisms (`AM_RUNTIME_OPTION_OVERRIDES`).
4. **Path Management Shim** (`paths.py`) - Re-exports the well-known-path helpers from `ccai.thisapp.paths`.
5. **Enumerations Shim** (`enumerations.py`) - Re-exports `ActivationProfile` and `JobType` from `ccai.thisapp.enumerations`.

> NOTE: The test-reporting path helpers (`get_path_for_testresults`, `get_path_for_diagnostics`, `get_path_for_testcase_by_products`, and the summary-template/static-resource helpers) are re-exported by the `paths.py` shim today, but they are slated to relocate again to `codecraftai-integration-runtime` alongside the result recorder that consumes them.

### Design Principles

The relocated foundation (now in `ccai.thisapp`) and the shim layer both follow these key design principles:

- **Debuggability over Performance**: Code prioritizes clear error messages and traceability
- **Readability over Conciseness**: Explicit, verbose code for maintainability
- **Separation of Concerns**: Each module has a distinct responsibility
- **Configuration Flexibility**: Multiple ways to configure runtime behavior
- **Context Awareness**: Different behavior based on execution context

The shim layer adds one additional principle:

- **Transparent Relocation**: The shims must re-export the full public surface of their `ccai.thisapp` counterparts so that existing `ccai.runtime.X` importers keep working unchanged during the migration.

## Module Details

> The module behavior below describes the relocated foundation, which now lives in `ccai.thisapp`. In `codecraftai-runtime` these modules (except `optionoverrides`) are thin shims that re-export the corresponding symbols.

### Activation Module (relocated to `ccai.thisapp.activation`)

**Purpose**: Manages the activation of different runtime profiles and their associated logging configurations.

**Key Functions**:
- `activate_profile_command()` - Activates command-line execution profile
- `activate_profile_console()` - Activates interactive console profile  
- `activate_profile_service()` - Activates long-running service profile
- `activate_profile_job()` - Activates job execution profile with output management

**Design Patterns**:
- **Guard Pattern**: Prevents multiple profile activations
- **Template Method**: Common activation logic in `_activate_profile_common()`
- **Strategy Pattern**: Different logging strategies per profile

**Key Responsibilities**:
- Profile lifecycle management
- Output directory structure creation
- Logging system activation
- Job type-specific path configuration

### Runtime Variables Module (relocated to `ccai.thisapp.runtimevariables`)

**Purpose**: Provides centralized access to all runtime configuration variables with environment variable integration.

**Key Classes**:
- `RuntimeVariablesDesc` - Variable descriptors with defaults and context paths
- `RuntimeVariables` - Accessor class for runtime configuration
- `DefaultValue` - Sentinel values for unset configurations

**Configuration Categories**:
- **Build Information**: Release, branch, flavor, name, URL
- **Job Metadata**: ID, type, owner, initiator, labels, tags
- **Logging Configuration**: Console and file log levels
- **Path Configuration**: Output, shared store, template paths
- **Debug Settings**: Breakpoints, debugger selection
- **Pipeline Information**: ID, name, instance tracking

**Design Patterns**:
- **Descriptor Pattern**: Variable access through descriptors
- **Singleton Pattern**: Global application state management
- **Accessor Pattern**: Controlled variable access

### Option Overrides Module (remains in `codecraftai-runtime`)

**Purpose**: Provides programmatic interfaces for overriding runtime configuration at runtime. This is the **one module that remains as real code** in `codecraftai-runtime`; it imports `ThisApplicationSingleton` and `RuntimeVariablesDesc` from `ccai.thisapp`.

**Key Features**:
- Type-safe override methods (`AM_RUNTIME_OPTION_OVERRIDES`) for each configuration variable
- Integration with the `ccai.thisapp` application singleton for state management
- Support for complex data types (lists, dictionaries, datetime objects)

**Override Categories**:
- Build configuration overrides
- Job metadata overrides  
- Debug configuration overrides
- Logging level overrides
- Path and directory overrides
- Pipeline and run tracking overrides

**Design Patterns**:
- **Facade Pattern**: Simplified interface for complex configuration
- **Command Pattern**: Each override method encapsulates a configuration change

### Path Management Module (relocated to `ccai.thisapp.paths`)

**Purpose**: Manages file system paths and directory structures for different runtime contexts.

**Key Functions**:
- **Output Management**: `get_path_for_output()`, `get_path_for_artifacts()`
- **Diagnostics**: `get_path_for_diagnostics()`, `get_path_for_testcase_by_products()`
- **Caching**: `get_directory_for_cached_files()`
- **Shared Storage**: `get_path_for_shared_store()`
- **Temporary Files**: `get_temporary_directory()`, `get_temporary_file()`

**Directory Structure**:
```
{presence_dir}/
├── cache/
├── results/
│   ├── infrastructure/{starttime}/
│   ├── orchestration/{starttime}/
│   ├── build/{starttime}/
│   └── testresults/{starttime}/
│       ├── artifacts/{label}/
│       ├── diagnostics/{label}/
│       └── tc-by-products/{test_id}/
└── services/{service_name}/
```

**Design Patterns**:
- **Factory Pattern**: Path creation based on job type
- **Lazy Initialization**: Directories created on first access
- **Template Method**: Path generation with variable substitution

### Enumerations Module (relocated to `ccai.thisapp.enumerations`)

**Purpose**: Defines runtime type constants and execution context enumerations.

**Key Enumerations**:
- `ActivationProfile`: Command, Console, Job, Service
- `JobType`: Unknown, Build, Infrastructure, Orchestration, TestRun

**Usage Context**:
- **Service**: Long-running processes with log rotation
- **Command**: Standard CLI applications with stdout/stderr
- **Console**: Interactive applications with separate logging
- **Job**: Batch processes with structured output collection

## Integration Points

### External Dependencies

The relocated foundation (in `ccai.thisapp`) and the remaining `optionoverrides.py` integrate with several external ccai modules:

- `ccai.errors` - Exception handling and error reporting
- `ccai.thisapp` - Application singleton, runtime variables, paths, enumerations, and activation (now the **home** of the relocated foundation)
- `ccai.xmodules.xlogging` - Logging system activation
- `ccai.xmodules.xdatetime` - Date/time formatting and parsing
- `ccai.xmodules.fspath` - File system path utilities

### Relationship to `codecraftai-integration-runtime`

The integration test-job layer that was once envisioned to live alongside this runtime now lives in the separate `codecraftai-integration-runtime` package, which hosts `IntegratedTestJob` and the runtime-backed output context, run metadata, and result recorder. New runtime-integrated test-execution work belongs there, not in `codecraftai-runtime`. The test-reporting path helpers re-exported by the `paths.py` shim are slated to follow the recorder into `codecraftai-integration-runtime`.

### Application Lifecycle Integration

The runtime foundation integrates with the application lifecycle through:

1. **Initialization**: Variable resolution from environment
2. **Activation**: Profile-specific setup and logging configuration
3. **Execution**: Path management and resource allocation
4. **Cleanup**: Temporary resource management

## Configuration Management

### Variable Resolution Order

1. Programmatic overrides (highest priority) — via `AM_RUNTIME_OPTION_OVERRIDES` in this package
2. Environment variables
3. Default values (lowest priority)

### Environment Variable Mapping

All runtime variables follow the `AM_*` naming convention:
- `AM_JOB_TYPE` → Job execution type
- `AM_OUTPUT_DIRECTORY` → Base output path
- `AM_LOG_LEVEL_CONSOLE` → Console logging level
- `AM_PRESENCE_DIR` → Application presence directory

### Context Path Integration

Variables can be mapped to context paths for framework integration:
- Build information → Build context
- Job metadata → Job context  
- Logging configuration → Logging context
- Path configuration → Path context

## Error Handling

### Exception Types

- `ConfigurationError` - Invalid configuration values
- `SemanticError` - Logic errors in activation or usage
- `RuntimeError` - General runtime failures

### Error Prevention

- **Guard Clauses**: Prevent invalid state transitions
- **Validation**: Type and value checking on configuration
- **Defensive Programming**: Null checks and default handling

## Testing Strategy

Because the foundation modules are now re-export shims, the real test surface in this package is limited to `optionoverrides.py`. Tests of the relocated runtime variables, paths, enumerations, and activation behavior belong with their home in `codecraftai-this-app`.

### Test Categories

1. **Option Override Tests**: Verify `AM_RUNTIME_OPTION_OVERRIDES` writes the correct values through the `ccai.thisapp` application singleton.
2. **Shim Re-export Tests** (optional): Verify each shim re-exports the expected symbols from its `ccai.thisapp` counterpart.

### Test Patterns

- **Mock Environment**: Isolated environment variable testing
- **Singleton Management**: Proper test isolation
- **State Verification**: Configuration state validation

## Migration and Retirement

### Retirement Plan

`codecraftai-runtime` is slated for removal once all importers have migrated to `ccai.thisapp`. The migration proceeds as follows:

1. **Phase 1 (done)**: Move the runtime foundation into `ccai.thisapp`; replace the foundation modules here with thin re-export shims.
2. **Phase 3 (pending)**: Relocate the test-reporting path helpers (and the recorder that consumes them) into `codecraftai-integration-runtime`.
3. **Retirement (pending)**: Migrate all `ccai.runtime.X` importers to `ccai.thisapp.X`, decide on a permanent home for `optionoverrides.py`, then delete the shims and retire the package.

### Backward Compatibility

- **Transparent Imports**: The shims preserve the `ccai.runtime.X` import paths so existing importers keep working unchanged.
- **Variable Naming**: Consistent `AM_*` naming conventions are preserved by the relocated foundation.
- **API Stability**: The shims forward the full public surface of their `ccai.thisapp` counterparts.

## Conclusion

The `codecraftai-runtime` package no longer owns the runtime foundation — that foundation now lives in `codecraftai-this-app`. What remains here is a thin compatibility layer (re-export shims for runtime variables, paths, enumerations, and activation) plus the still-real `optionoverrides.py`. The package's role is now transitional: to keep `ccai.runtime.X` importers working while they migrate to `ccai.thisapp`, after which the package is slated for retirement.
