# AutoMojo Runtime Package Requirements

## 1. Introduction

### 1.1 Purpose
This document specifies the requirements for the runtime foundation that `codecraftai-runtime` historically owned: a comprehensive runtime environment management system for automation testing frameworks providing application lifecycle management, configuration handling, logging activation, and resource path management across different execution contexts.

That runtime foundation has now **moved into `codecraftai-this-app`** (`ccai.thisapp.{runtimevariables,paths,enumerations,activation}`). As a result, `codecraftai-runtime` is being **RETIRED**: its `runtimevariables.py`, `paths.py`, `enumerations.py`, and `activation.py` modules are now thin compatibility shims that re-export their `ccai.thisapp.*` counterparts, while `optionoverrides.py` (`AM_RUNTIME_OPTION_OVERRIDES`) remains as real code for now.

The functional requirements below therefore now constrain the relocated foundation in `ccai.thisapp` (with the exception of the override requirements, which `codecraftai-runtime`'s `optionoverrides.py` still satisfies). They are retained here as the authoritative behavioral specification during the migration, plus added retirement/shim requirements that constrain `codecraftai-runtime` itself.

### 1.2 Scope
The requirements cover the runtime foundation functionality (now owned by `ccai.thisapp`) including:
- Runtime profile activation and management
- Configuration variable management and environment integration
- File system path management and directory structure organization
- Logging system activation and configuration
- Error handling and validation mechanisms

They also cover the requirements specific to `codecraftai-runtime` during its retirement:
- The transparent re-export shims that preserve the `ccai.runtime.X` import paths
- The runtime overrides (`AM_RUNTIME_OPTION_OVERRIDES`) that remain real code in this package
- The migration/retirement plan toward removing the package once importers move to `ccai.thisapp`

### 1.3 Definitions and Acronyms
- **AM**: AutoMojo (prefix for environment variables)
- **Runtime Profile**: Execution context configuration (Command, Console, Service, Job)
- **Job Type**: Category of automation work (Build, Infrastructure, Orchestration, TestRun)
- **Presence Directory**: Base directory for application runtime files
- **Output Directory**: Directory where job results and artifacts are stored
- **Runtime Foundation**: The runtime variables, well-known paths, enumerations, and activation sequence — now owned by `ccai.thisapp`
- **Shim**: A thin compatibility module in `codecraftai-runtime` that re-exports symbols from its `ccai.thisapp` counterpart to preserve the legacy `ccai.runtime.X` import path

## 2. Functional Requirements

### 2.1 Runtime Profile Management

#### 2.1.1 Profile Activation
**REQ-PROF-001**: The system SHALL provide four distinct runtime profiles:
- Command: Standard command-line execution with stdout/stderr output
- Console: Interactive console execution with separate log files
- Service: Long-running service execution with log rotation
- Job: Batch job execution with structured output collection

**REQ-PROF-002**: The system SHALL prevent multiple profile activations within a single runtime instance.

**REQ-PROF-003**: Each profile activation SHALL configure appropriate logging mechanisms based on the execution context.

**REQ-PROF-004**: The system SHALL validate profile-specific requirements before activation (e.g., service name for service profile).

#### 2.1.2 Profile-Specific Behavior
**REQ-PROF-005**: Command profile SHALL activate standard file logging with both console and file output.

**REQ-PROF-006**: Console profile SHALL create temporary output directories and activate interactive console logging.

**REQ-PROF-007**: Service profile SHALL configure rotating log files and set appropriate log levels for long-running processes.

**REQ-PROF-008**: Job profile SHALL create job-type-specific output directory structures and activate standard file logging.

### 2.2 Configuration Management

#### 2.2.1 Variable Resolution
**REQ-CONF-001**: The system SHALL support three-tier configuration resolution:
1. Programmatic overrides (highest priority)
2. Environment variables
3. Default values (lowest priority)

**REQ-CONF-002**: All environment variables SHALL follow the `AM_*` naming convention.

**REQ-CONF-003**: The system SHALL provide type-safe access to configuration variables through descriptor patterns.

**REQ-CONF-004**: Configuration variables SHALL be categorized into logical groups:
- Build Information (release, branch, flavor, name, URL)
- Job Metadata (ID, type, owner, initiator, labels, tags)
- Logging Configuration (console and file log levels)
- Path Configuration (output, shared store, template paths)
- Debug Settings (breakpoints, debugger selection)
- Pipeline Information (ID, name, instance tracking)

#### 2.2.2 Runtime Overrides
**REQ-CONF-005**: The system SHALL provide programmatic override methods for all configuration variables.

**REQ-CONF-006**: Override methods SHALL validate input parameters and provide type safety.

**REQ-CONF-007**: The system SHALL support complex data type overrides including lists, dictionaries, and datetime objects.

**REQ-CONF-008**: Configuration changes SHALL be immediately available through variable accessors.

### 2.3 Path Management

#### 2.3.1 Directory Structure
**REQ-PATH-001**: The system SHALL create and manage a standardized directory structure:
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

**REQ-PATH-002**: Directory creation SHALL be lazy - directories are created only when first accessed.

**REQ-PATH-003**: The system SHALL support job-type-specific path templates with variable substitution.

**REQ-PATH-004**: Path generation SHALL use filesystem-safe timestamp formatting for directory names.

#### 2.3.2 Path Resolution Functions
**REQ-PATH-005**: The system SHALL provide path resolution functions for:
- Output directories (`get_path_for_output()`)
- Artifact storage (`get_path_for_artifacts()`)
- Diagnostic data (`get_path_for_diagnostics()`)
- Test case by-products (`get_path_for_testcase_by_products()`)
- Cached files (`get_directory_for_cached_files()`)
- Shared storage (`get_path_for_shared_store()`)
- Temporary files (`get_temporary_directory()`, `get_temporary_file()`)

**REQ-PATH-006**: Path functions SHALL automatically create directories if they do not exist (when create=True).

**REQ-PATH-007**: The system SHALL support both absolute and relative path resolution with proper expansion.

#### 2.3.3 Shared Storage
**REQ-PATH-008**: The system SHALL support shared storage directories accessible across multiple compute resources.

**REQ-PATH-009**: Shared storage configuration SHALL be machine-specific and not expand user home variables.

**REQ-PATH-010**: The system SHALL provide a flag indicating whether shared output directories are in use.

### 2.4 Job Type Management

#### 2.4.1 Job Type Support
**REQ-JOB-001**: The system SHALL support five job types:
- Unknown: Default/unspecified job type
- Build: Software build processes
- Infrastructure: Infrastructure setup and management
- Orchestration: Workflow orchestration tasks
- TestRun: Test execution jobs

**REQ-JOB-002**: Each job type SHALL have specific output directory templates and path configurations.

**REQ-JOB-003**: Job type SHALL determine available path functions (artifacts, diagnostics only available for non-Unknown jobs).

**REQ-JOB-004**: The system SHALL generate unique job IDs when not explicitly provided.

### 2.5 Logging Integration

#### 2.5.1 Logging Activation
**REQ-LOG-001**: The system SHALL integrate with the ccai logging framework for log activation.

**REQ-LOG-002**: Logging configuration SHALL be profile-specific with appropriate handlers and formatters.

**REQ-LOG-003**: The system SHALL support separate console and file log levels.

**REQ-LOG-004**: Service profile SHALL support log rotation with configurable maximum file size and backup count.

#### 2.5.2 Log File Management
**REQ-LOG-005**: Log files SHALL be created in job-specific directories based on the activation profile.

**REQ-LOG-006**: Log file names SHALL include configurable base names and appropriate extensions.

**REQ-LOG-007**: The system SHALL ensure log directories exist before attempting to write log files.

### 2.6 Python Module Management

#### 2.6.1 Module Discovery
**REQ-MOD-001**: The system SHALL provide functionality to collect Python modules from directory trees.

**REQ-MOD-002**: Module collection SHALL support maximum depth limits for directory traversal.

**REQ-MOD-003**: The system SHALL support Python namespaces by not requiring `__init__.py` files in root folders.

**REQ-MOD-004**: Module collection SHALL exclude `__init__.py` files from the results.

#### 2.6.2 Package Management
**REQ-MOD-005**: The system SHALL provide functionality to ensure directories are represented as Python packages.

**REQ-MOD-006**: Package creation SHALL automatically generate `__init__.py` files with optional documentation strings.

**REQ-MOD-007**: The system SHALL support code container directory resolution for modules and packages.

### 2.7 Relocation and Retirement (`codecraftai-runtime`)

#### 2.7.1 Foundation Relocation
**REQ-RETIRE-001**: The runtime foundation (runtime variables, well-known paths, enumerations, activation) SHALL be owned by `ccai.thisapp` in the modules `ccai.thisapp.{runtimevariables,paths,enumerations,activation}`.

**REQ-RETIRE-002**: `codecraftai-runtime`'s `runtimevariables.py`, `paths.py`, `enumerations.py`, and `activation.py` SHALL be thin compatibility shims that re-export their `ccai.thisapp.*` counterparts and SHALL NOT contain an independent implementation of the foundation.

**REQ-RETIRE-003**: Each shim SHALL re-export the full public surface of its `ccai.thisapp` counterpart so that existing `ccai.runtime.X` importers continue to work unchanged during the migration.

#### 2.7.2 Retained Real Code
**REQ-RETIRE-004**: `codecraftai-runtime` SHALL continue to ship `optionoverrides.py` as real code (`AM_RUNTIME_OPTION_OVERRIDES`), sourcing `ThisApplicationSingleton` and `RuntimeVariablesDesc` from `ccai.thisapp`.

**REQ-RETIRE-005**: The override requirements (REQ-CONF-005 through REQ-CONF-008) SHALL be satisfied by `codecraftai-runtime`'s `optionoverrides.py`; all other foundation requirements in this document SHALL be satisfied by `ccai.thisapp`.

#### 2.7.3 Pending Relocations and Removal
**REQ-RETIRE-006**: The test-reporting path helpers (`get_path_for_testresults`, `get_path_for_diagnostics`, `get_path_for_testcase_by_products`, and the summary-template/static-resource helpers) re-exported by the `paths.py` shim SHALL relocate to `codecraftai-integration-runtime` alongside the result recorder that consumes them.

**REQ-RETIRE-007**: New runtime-integrated test-execution work (e.g. `IntegratedTestJob`, runtime-backed output context/run metadata/recorder) SHALL belong to `codecraftai-integration-runtime`, not `codecraftai-runtime`.

**REQ-RETIRE-008**: Once all `ccai.runtime.X` importers have migrated to `ccai.thisapp` and a permanent home for `optionoverrides.py` is chosen, the shims SHALL be removed and the package retired.

## 3. Non-Functional Requirements

### 3.1 Performance Requirements

**REQ-PERF-001**: Directory creation operations SHALL use lazy initialization to minimize I/O operations.

**REQ-PERF-002**: Path resolution results SHALL be cached globally to avoid repeated calculations.

**REQ-PERF-003**: File system operations SHALL use efficient existence checking mechanisms.

**REQ-PERF-004**: Memory usage SHALL be minimized through proper object lifecycle management.

### 3.2 Reliability Requirements

**REQ-REL-001**: The system SHALL provide comprehensive error handling with specific exception types:
- `ConfigurationError` for invalid configuration values
- `SemanticError` for logic errors in activation or usage
- `RuntimeError` for general runtime failures

**REQ-REL-002**: All configuration validation SHALL occur before system activation.

**REQ-REL-003**: The system SHALL use guard clauses to prevent invalid state transitions.

**REQ-REL-004**: Resource cleanup SHALL be handled properly for temporary files and directories.

### 3.3 Maintainability Requirements

**REQ-MAINT-001**: Code SHALL prioritize debuggability over performance with clear error messages and traceability.

**REQ-MAINT-002**: Code SHALL prioritize readability over conciseness with explicit, verbose implementations.

**REQ-MAINT-003**: Each module SHALL have a single, well-defined responsibility following separation of concerns.

**REQ-MAINT-004**: The system SHALL follow consistent naming conventions as specified in the Code Craft AI Python Naming Conventions.

**REQ-MAINT-005**: Code structure SHALL follow the Code Craft AI Python Code Structure Standards.

### 3.4 Security Requirements

**REQ-SEC-001**: Path construction SHALL prevent path traversal attacks through controlled path building.

**REQ-SEC-002**: Directory creation SHALL use appropriate file system permissions.

**REQ-SEC-003**: Temporary file creation SHALL use secure temporary file mechanisms.

**REQ-SEC-004**: Environment variable validation SHALL include input sanitization.

**REQ-SEC-005**: Configuration overrides SHALL include type and range validation.

**REQ-SEC-006**: Sensitive configuration data SHALL be handled appropriately without logging or exposure.

### 3.5 Compatibility Requirements

**REQ-COMPAT-001**: The system SHALL maintain backward compatibility for existing variable names and API interfaces.

**REQ-COMPAT-002**: Default behavior SHALL be preserved across version updates.

**REQ-COMPAT-003**: Configuration migration paths SHALL be provided for major version changes.

**REQ-COMPAT-004**: The system SHALL support cross-platform operation on Darwin, Linux, Unix, and Windows.

### 3.6 Testability Requirements

> Because the foundation modules in `codecraftai-runtime` are now re-export shims, the real test surface in this package is limited to `optionoverrides.py` (and, optionally, shim re-export checks). Tests of the relocated foundation behavior belong with their home in `codecraftai-this-app`.

**REQ-TEST-001**: All functionality SHALL be testable using the unittest framework.

**REQ-TEST-002**: Tests SHALL verify individual components in isolation with proper test granularity.

**REQ-TEST-003**: The system SHALL support test environment isolation through mock environments and temporary directories.

**REQ-TEST-004**: Configuration state SHALL be verifiable through test interfaces.

**REQ-TEST-005**: Singleton management SHALL support proper test isolation and cleanup.

## 4. Integration Requirements

### 4.1 External Module Dependencies

**REQ-INT-001**: The system SHALL integrate with the following ccai modules:
- `ccai.errors` for exception handling and error reporting
- `ccai.thisapp` for the application singleton AND for the relocated runtime foundation (runtime variables, paths, enumerations, activation)
- `ccai.xmodules.xlogging` for logging system activation
- `ccai.xmodules.xdatetime` for date/time formatting and parsing
- `ccai.xmodules.fspath` for file system path utilities

**REQ-INT-002**: Integration SHALL be through well-defined interfaces that support module independence.

**REQ-INT-003**: The system SHALL handle missing or unavailable dependencies gracefully with appropriate error messages.

### 4.2 Application Lifecycle Integration

**REQ-INT-004**: The system SHALL integrate with application lifecycle phases:
1. Initialization: Variable resolution from environment
2. Activation: Profile-specific setup and logging configuration
3. Execution: Path management and resource allocation
4. Cleanup: Temporary resource management

**REQ-INT-005**: Context path integration SHALL map variables to appropriate framework contexts.

## 5. Extensibility Requirements

### 5.1 Extension Points

**REQ-EXT-001**: The system SHALL support addition of new activation profiles without modifying existing code.

**REQ-EXT-002**: Path resolution SHALL support pluggable path providers for custom directory structures.

**REQ-EXT-003**: Variable conversion SHALL support custom type converters for specialized data types.

**REQ-EXT-004**: Logging integration SHALL support additional logging backends through configuration.

### 5.2 Configuration Extensibility

**REQ-EXT-005**: New configuration variables SHALL be addable through the descriptor pattern without breaking existing functionality.

**REQ-EXT-006**: Override mechanisms SHALL be extensible to support new variable types and validation rules.

**REQ-EXT-007**: Environment variable mapping SHALL support custom naming patterns and conversion rules.

## 6. Acceptance Criteria

### 6.1 Functional Acceptance

**AC-FUNC-001**: All four runtime profiles (Command, Console, Service, Job) can be activated successfully with appropriate logging configuration.

**AC-FUNC-002**: Configuration variables can be set through environment variables, programmatic overrides, and default values with correct precedence.

**AC-FUNC-003**: Directory structures are created correctly for all job types with proper path resolution.

**AC-FUNC-004**: Path management functions return correct paths and create directories as needed.

**AC-FUNC-005**: Module discovery and package management functions work correctly with Python namespace support.

### 6.2 Non-Functional Acceptance

**AC-NONFUNC-001**: All error conditions produce appropriate exception types with clear error messages.

**AC-NONFUNC-002**: Performance requirements are met with lazy initialization and caching mechanisms.

**AC-NONFUNC-003**: Security requirements are satisfied with proper path validation and input sanitization.

**AC-NONFUNC-004**: All functionality is covered by unittest tests with proper isolation and cleanup.

**AC-NONFUNC-005**: Code follows the specified coding standards and naming conventions.

### 6.3 Integration Acceptance

**AC-INT-001**: Integration with external ccai modules works correctly without circular dependencies.

**AC-INT-002**: Application lifecycle integration provides proper initialization, activation, execution, and cleanup phases.

**AC-INT-003**: Context path mapping correctly associates variables with framework contexts.

## 7. Constraints and Assumptions

### 7.1 Technical Constraints

**CONST-001**: The system must be implemented in Python and compatible with the existing ccai framework architecture.

**CONST-002**: All environment variables must follow the `AM_*` naming convention for consistency.

**CONST-003**: The system must use the unittest framework for all testing as specified in repository conventions.

**CONST-004**: Code must prioritize debuggability and readability over performance optimizations.

### 7.2 Assumptions

**ASSUME-001**: The ccai framework modules (`ccai.errors`, `ccai.thisapp`, etc.) are available and properly installed.

**ASSUME-002**: The file system supports the required directory structure and permissions for path management.

**ASSUME-003**: Environment variables are available and accessible through the standard `os.environ` interface.

**ASSUME-004**: The application singleton pattern is properly implemented and maintained throughout the application lifecycle.