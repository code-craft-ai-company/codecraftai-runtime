# AutoMojo Runtime Package Design Document

## Overview

The `automojo.runtime` package provides a comprehensive runtime environment management system for automation testing frameworks. It handles application lifecycle, configuration management, logging activation, and resource path management across different execution contexts (command-line, console, service, and job modes).

## Architecture

### Core Components

The runtime package consists of five main modules:

1. **Activation Module** (`activation.py`) - Manages runtime profile activation and logging setup
2. **Runtime Variables** (`runtimevariables.py`) - Centralized configuration and environment variable management
3. **Option Overrides** (`optionoverrides.py`) - Programmatic configuration override mechanisms
4. **Path Management** (`paths.py`) - File system path resolution and directory management
5. **Enumerations** (`enumerations.py`) - Runtime type definitions and constants

### Design Principles

The package follows these key design principles:

- **Debuggability over Performance**: Code prioritizes clear error messages and traceability
- **Readability over Conciseness**: Explicit, verbose code for maintainability
- **Separation of Concerns**: Each module has a distinct responsibility
- **Configuration Flexibility**: Multiple ways to configure runtime behavior
- **Context Awareness**: Different behavior based on execution context

## Module Details

### Activation Module

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

### Runtime Variables Module

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

### Option Overrides Module

**Purpose**: Provides programmatic interfaces for overriding runtime configuration at runtime.

**Key Features**:
- Type-safe override methods for each configuration variable
- Integration with application singleton for state management
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

### Path Management Module

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

### Enumerations Module

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

The runtime package integrates with several external automojo modules:

- `automojo.errors` - Exception handling and error reporting
- `automojo.thisapp` - Application singleton and variable management
- `automojo.xmodules.xlogging` - Logging system activation
- `automojo.xmodules.xdatetime` - Date/time formatting and parsing
- `automojo.xmodules.fspath` - File system path utilities

### Application Lifecycle Integration

The runtime package integrates with the application lifecycle through:

1. **Initialization**: Variable resolution from environment
2. **Activation**: Profile-specific setup and logging configuration
3. **Execution**: Path management and resource allocation
4. **Cleanup**: Temporary resource management

## Configuration Management

### Variable Resolution Order

1. Programmatic overrides (highest priority)
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

### Test Categories

1. **Unit Tests**: Individual function and method testing
2. **Integration Tests**: Module interaction testing
3. **Configuration Tests**: Environment variable handling
4. **Path Tests**: Directory creation and management

### Test Patterns

- **Mock Environment**: Isolated environment variable testing
- **Temporary Directories**: Safe file system testing
- **Singleton Management**: Proper test isolation
- **State Verification**: Configuration state validation

## Performance Considerations

### Optimization Strategies

- **Lazy Loading**: Directories created only when needed
- **Caching**: Path resolution results cached globally
- **Minimal I/O**: Efficient directory existence checking
- **Memory Management**: Proper cleanup of temporary resources

### Resource Management

- **Directory Lifecycle**: Automatic creation, manual cleanup
- **File Handles**: Proper resource disposal
- **Memory Usage**: Minimal object retention
- **Temporary Files**: Automatic cleanup strategies

## Security Considerations

### Path Security

- **Path Traversal Prevention**: Controlled path construction
- **Permission Management**: Appropriate directory permissions
- **Temporary File Security**: Secure temporary file creation
- **Shared Resource Access**: Controlled shared directory access

### Configuration Security

- **Environment Variable Validation**: Input sanitization
- **Default Value Security**: Safe default configurations
- **Override Validation**: Type and range checking
- **Sensitive Data Handling**: Appropriate handling of credentials

## Future Extensibility

### Extension Points

- **New Activation Profiles**: Additional runtime contexts
- **Custom Path Providers**: Pluggable path resolution
- **Variable Converters**: Custom type conversion
- **Logging Integrations**: Additional logging backends

### Backward Compatibility

- **Variable Naming**: Consistent naming conventions
- **API Stability**: Stable public interfaces
- **Configuration Migration**: Smooth upgrade paths
- **Default Behavior**: Preserved default behaviors

## Conclusion

The automojo runtime package provides a robust, flexible foundation for automation testing frameworks. Its modular design, comprehensive configuration management, and context-aware behavior make it suitable for diverse execution environments while maintaining debuggability and maintainability as core principles.