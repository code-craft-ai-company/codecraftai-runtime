# AutoMojo Runtime Package Retirement Tasks

## Overview

This document outlines the tasks for **retiring `automojo-runtime`** by relocating its runtime foundation into `automojo-this-app` and reducing this package to thin compatibility shims plus the still-real `optionoverrides.py`.

The runtime foundation (runtime variables, well-known paths, enumerations, activation) has **moved into `automojo.thisapp.{runtimevariables,paths,enumerations,activation}`**. `automojo-runtime`'s `runtimevariables.py`, `paths.py`, `enumerations.py`, and `activation.py` are now thin re-export shims. `optionoverrides.py` (`AM_RUNTIME_OPTION_OVERRIDES`) remains as real code for now. The tasks below track that relocation/retirement rather than a from-scratch build-out of a standalone foundation package.

## Task Categories

### 1. Foundation Relocation Tasks (this-app)
### 2. Shim and Retained-Code Tasks (runtime)
### 3. Pending Relocation Tasks (integration-runtime)
### 4. Importer Migration and Removal Tasks
### 5. Testing and Documentation Tasks

---

## 1. Foundation Relocation Tasks (this-app)

### TASK-RELOC-001: Move Runtime Foundation into `automojo.thisapp`
**Status**: Done  
**Priority**: Critical  
**Requirements**: REQ-RETIRE-001  
**Description**: Move the runtime variables, well-known paths, enumerations, and activation sequence into `automojo.thisapp`.
**Acceptance Criteria**:
- `RuntimeVariables`, `RuntimeVariablesDesc`, `DefaultValue`, `resolve_runtime_variables`, and the seed/template helpers live in `automojo.thisapp.runtimevariables`
- The well-known-path helpers live in `automojo.thisapp.paths`
- `ActivationProfile` and `JobType` live in `automojo.thisapp.enumerations`
- `activate_profile_command/console/service/job` live in `automojo.thisapp.activation`

**Implementation Steps**:
1. Relocate the foundation modules into `automojo.thisapp`
2. Update internal cross-references to use `automojo.thisapp.*`
3. Confirm the relocated foundation satisfies the functional requirements in `requirements.md`

---

## 2. Shim and Retained-Code Tasks (runtime)

### TASK-SHIM-001: Replace Foundation Modules with Re-export Shims
**Status**: Done  
**Priority**: Critical  
**Requirements**: REQ-RETIRE-002, REQ-RETIRE-003  
**Description**: Replace `automojo-runtime`'s foundation modules with thin shims that re-export the `automojo.thisapp.*` counterparts.
**Acceptance Criteria**:
- `automojo.runtime.runtimevariables`, `.paths`, `.enumerations`, and `.activation` re-export the full public surface of their `automojo.thisapp` counterparts
- The shims contain no independent implementation of the foundation
- Existing `automojo.runtime.X` importers keep working unchanged
- Each shim documents that it is temporary and points to its `automojo.thisapp` home

**Implementation Steps**:
1. Replace each foundation module body with `from automojo.thisapp.<module> import *` plus an explicit re-export list
2. Add a "TEMPORARY compatibility shim" module docstring to each
3. Verify the re-exported symbol set matches the `automojo.thisapp` counterpart

### TASK-SHIM-002: Keep `optionoverrides.py` as Real Code
**Status**: Done  
**Priority**: High  
**Requirements**: REQ-RETIRE-004, REQ-CONF-005 through REQ-CONF-008  
**Description**: Retain `optionoverrides.py` (`AM_RUNTIME_OPTION_OVERRIDES`) as real code in `automojo-runtime`, sourcing its dependencies from `automojo.thisapp`.
**Acceptance Criteria**:
- `optionoverrides.py` imports `ThisApplicationSingleton` from `automojo.thisapp.wellknown` and `RuntimeVariablesDesc` from `automojo.thisapp.runtimevariables`
- Override methods exist for all configuration variables
- Complex data types (lists, dictionaries, datetime) are supported

**Implementation Steps**:
1. Repoint `optionoverrides.py` imports at `automojo.thisapp`
2. Confirm overrides write through the `automojo.thisapp` application singleton
3. Keep the override unit tests green

---

## 3. Pending Relocation Tasks (integration-runtime)

### TASK-PENDING-001: Relocate Test-Reporting Path Helpers to `automojo-integration-runtime`
**Status**: Pending  
**Priority**: Medium  
**Requirements**: REQ-RETIRE-006  
**Description**: Move the test-reporting path helpers re-exported by the `paths.py` shim into `automojo-integration-runtime` alongside the result recorder that consumes them.
**Acceptance Criteria**:
- `get_path_for_testresults`, `get_path_for_diagnostics`, `get_path_for_testcase_by_products`, and the summary-template/static-resource helpers move to `automojo-integration-runtime`
- The recorder that consumes those helpers references the new location
- The `paths.py` shim no longer needs to re-export the relocated helpers

**Implementation Steps**:
1. Identify the recorder/path-helper coupling consumed by `IntegratedTestJob`
2. Move the helpers to `automojo-integration-runtime`
3. Update the recorder and remove the corresponding re-exports from the `paths.py` shim

### TASK-PENDING-002: Keep Runtime-Integrated Work in `automojo-integration-runtime`
**Status**: Ongoing  
**Priority**: Medium  
**Requirements**: REQ-RETIRE-007  
**Description**: Ensure new runtime-integrated test-execution work (`IntegratedTestJob`, runtime-backed output context/run metadata/recorder) lands in `automojo-integration-runtime`, not `automojo-runtime`.
**Acceptance Criteria**:
- No new test-execution components are added to `automojo-runtime`
- `automojo-integration-runtime` remains the home for runtime-backed test-job work

**Implementation Steps**:
1. Route any new runtime-integrated work to `automojo-integration-runtime`
2. Reject additions of foundation/test-execution code to `automojo-runtime`

---

## 4. Importer Migration and Removal Tasks

### TASK-MIGRATE-001: Migrate `automojo.runtime.X` Importers to `automojo.thisapp.X`
**Status**: Pending  
**Priority**: High  
**Requirements**: REQ-RETIRE-008  
**Description**: Migrate every consumer that imports the foundation from `automojo.runtime.*` over to `automojo.thisapp.*`.
**Acceptance Criteria**:
- No remaining importers depend on `automojo.runtime.{runtimevariables,paths,enumerations,activation}`
- Importers reference `automojo.thisapp.*` directly

**Implementation Steps**:
1. Inventory all `automojo.runtime.X` foundation importers across the monorepo
2. Repoint each importer at `automojo.thisapp.X`
3. Track remaining importers until the count reaches zero

### TASK-MIGRATE-002: Decide Permanent Home for `optionoverrides.py`
**Status**: Pending  
**Priority**: Medium  
**Requirements**: REQ-RETIRE-004, REQ-RETIRE-008  
**Description**: Choose a permanent home for `optionoverrides.py` (`AM_RUNTIME_OPTION_OVERRIDES`) ahead of package retirement.
**Acceptance Criteria**:
- A target package is selected for the overrides module
- The decision is documented and the override unit tests follow the module

**Implementation Steps**:
1. Evaluate `automojo.thisapp` (or another package) as the override home
2. Move the module and its tests to the chosen home
3. Update importers of `AM_RUNTIME_OPTION_OVERRIDES`

### TASK-MIGRATE-003: Remove Shims and Retire `automojo-runtime`
**Status**: Pending  
**Priority**: Medium  
**Requirements**: REQ-RETIRE-008  
**Description**: After importers migrate and `optionoverrides.py` has a permanent home, delete the shims and retire the package.
**Acceptance Criteria**:
- The four re-export shims are removed
- `automojo-runtime` no longer ships foundation modules
- The package is retired from the monorepo dependency graph

**Implementation Steps**:
1. Confirm TASK-MIGRATE-001 and TASK-MIGRATE-002 are complete
2. Delete the shim modules
3. Retire the package and update dependents

---

## 5. Testing and Documentation Tasks

### TASK-TEST-001: Maintain Option Override Tests
**Status**: Ongoing  
**Priority**: High  
**Requirements**: REQ-TEST-001, REQ-CONF-005 through REQ-CONF-008  
**Description**: Keep `test_optionoverrides.py` green; it is the real test surface that remains in `automojo-runtime`.
**Acceptance Criteria**:
- `test_optionoverrides.py` verifies override methods write through the `automojo.thisapp` application singleton
- Tests run under the unittest framework with proper isolation

**Implementation Steps**:
1. Keep the override tests aligned with the `automojo.thisapp` dependencies
2. Ensure test isolation/cleanup of singleton state

### TASK-TEST-002: Add Optional Shim Re-export Checks
**Status**: Optional  
**Priority**: Low  
**Requirements**: REQ-RETIRE-003  
**Description**: Optionally verify each shim re-exports the expected symbol set from its `automojo.thisapp` counterpart.
**Acceptance Criteria**:
- A test asserts the shim's exported names match the counterpart's public surface (or the explicit re-export list)

**Implementation Steps**:
1. Enumerate expected re-exports for each shim
2. Assert importability of each symbol from the `automojo.runtime.X` path

### TASK-DOC-001: Keep Retirement Narrative Consistent
**Status**: Ongoing  
**Priority**: Medium  
**Requirements**: REQ-RETIRE-001, REQ-RETIRE-008  
**Description**: Keep `AGENTS.md`, this spec set, and the shim docstrings consistent on the relocation/retirement narrative.
**Acceptance Criteria**:
- Documentation describes the foundation as owned by `automojo.thisapp`
- Documentation describes `automojo-runtime` as a retiring shim package that still ships `optionoverrides.py`
- No documentation claims the test-reporting path helpers or runtime-integrated work have moved to `automojo-integration-runtime` ahead of the code

**Implementation Steps**:
1. Reconcile `AGENTS.md`, `design.md`, `requirements.md`, and shim docstrings
2. Reflect only what is already true on disk

---

## Task Dependencies and Execution Order

### Phase 1: Relocation (Done)
1. TASK-RELOC-001: Move runtime foundation into `automojo.thisapp`
2. TASK-SHIM-001: Replace foundation modules with re-export shims
3. TASK-SHIM-002: Keep `optionoverrides.py` as real code

### Phase 2: Pending Relocation (In Flight)
1. TASK-PENDING-001: Relocate test-reporting path helpers to `automojo-integration-runtime`
2. TASK-PENDING-002: Keep runtime-integrated work in `automojo-integration-runtime`

### Phase 3: Migration and Removal (Pending)
1. TASK-MIGRATE-001: Migrate importers to `automojo.thisapp`
2. TASK-MIGRATE-002: Decide permanent home for `optionoverrides.py`
3. TASK-MIGRATE-003: Remove shims and retire the package

### Phase 4: Ongoing Quality
1. TASK-TEST-001: Maintain option override tests
2. TASK-TEST-002: Add optional shim re-export checks
3. TASK-DOC-001: Keep retirement narrative consistent

## Success Criteria

### Completion Metrics
- The runtime foundation is fully owned by `automojo.thisapp`
- `automojo-runtime`'s foundation modules are thin shims with no independent implementation
- `optionoverrides.py` remains real and green under tests until it is given a permanent home
- All `automojo.runtime.X` foundation importers have migrated to `automojo.thisapp`
- The shims are removed and the package is retired

### Quality Gates
- Existing `automojo.runtime.X` importers keep working while the shims remain
- The override unit tests pass consistently
- Documentation reflects only what is already true on disk

## Risk Mitigation

### Technical Risks
- **Hidden Importers**: Inventory thoroughly before removing shims (TASK-MIGRATE-001)
- **Premature Claims**: Do not advertise relocations (test-reporting helpers, integrated work) ahead of the code
- **Singleton State Leakage**: Maintain test isolation for the override tests

### Project Risks
- **Scope Creep**: Do not add new foundation/test-execution code to the retiring package
- **Coordination**: Sequence importer migration before shim removal

## Conclusion

`automojo-runtime` is no longer a standalone foundation package — the runtime foundation now lives in `automojo-this-app`. The remaining work is to keep the compatibility shims and `optionoverrides.py` healthy, complete the pending relocation of test-reporting helpers to `automojo-integration-runtime`, migrate importers to `automojo.thisapp`, and then remove the shims and retire the package.
