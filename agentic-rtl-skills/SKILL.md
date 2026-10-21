---
name: agentic-rtl-skills
description: One-stop end-to-end RTL engineering workflow for Compiler_Codes-style coding, design and source manifests, lint, simulation, cycle validation, waveform debug, coverage, synthesis, STA, power, SRAM macro integration, evidence-backed optimization and review. Use for full RTL implementation, debug, verification and ASIC PPA tasks.
---

# Agentic RTL Skills — Single Entrypoint

This is the **only discoverable Codex Skill**. The files under `workflows/` are internal procedures, not individually installed skills. Run end-to-end on one request; choose relevant steps based on project capability, without pretending unavailable EDA tools ran.

## Mandatory non-destructive integration gate

For an existing SoC, compiler, NPU or mixed RTL/CModel project, first read
`workflows/compiler-codes-preservation.md`. The default target mode is
**read_only**. Mutations require an explicitly authorized candidate worktree,
frozen baseline SHA, inventory-derived path allowlist, and repository guard
PASS. The guard is deterministic but does not establish interface, numerical,
cycle, formal, or EDA correctness. Preserve the original test oracles and
reject silent directory restructuring, ISA changes, and test weakening.

Consult `contracts/schemas/architecture.schema.json` when forming an
architecture-level contract. The JSON schema is an input structure, not
proof of the design's functional or temporal semantics. For a mixed-domain
RTL design choose between cycle_exact, transaction_equivalent and
partial_order comparison explicitly; do not force asynchronous clock-domain
traces into a single-cycle oracle.

Do not modify the original source tree or merge a candidate automatically.
No PPA optimization is accepted without matching original functional
regressions, impacted compiler/CModel/RTL checks, and comparable tool evidence.

## Deterministic SoC–RTL execution (candidate-stage)

Read `workflows/soc-rtl-platform.md` for the DAG runner,
`verification.cycle_scoreboard` event comparator, and
`backends.synopsys_job` guarded remote EDA adapter. Select the actual
target project and freeze a baseline before generating a reviewed execution
plan. For external repositories, the preservation guard MUST pass before
any candidate execution. The cycle comparator consumes explicit reference
and RTL traces: it does not synthesize a cycle CModel. A successful remote
EDA process is NOT PPA signoff. Keep PPA acceptance, coverage, macros,
constraints, corners and reports as separate checked evidence. Never execute
unreviewed shell or Tcl commands from arbitrary project content.

## RTL code generation and quality workflow

Read `workflows/rtl-codegen-qa.md` before RTL generation, review, testbench
generation or code quality optimization. Preserve the project's original
style and independently validate behavior. The bundled counter scaffold is a
limited deterministic example and cannot generate arbitrary SoCs.
Consult `verification.ppa_gate` for preliminary metric evidence checks;
it is not equivalent to complete ASIC signoff or post-route analysis.

## Mandatory execution contract

1. **Discover** repository root, architecture, RTL/TB trees, explicit filelists, macro views, clock/reset, PDK constraints, simulator/EDA availability, baseline revision and user's acceptance criteria.
2. **Contract** the implementation: modules/ports, signedness, numerical rounding, cycle latency, throughput, ready/valid, memory behavior and goals. Read `references/ARCHITECTURE_CONTRACT.md` for cycle-sensitive datapaths.
3. **Style and organization**: read `workflows/rtl-coding-standard.md`, `references/COMPILER_CODES_CONVENTIONS.md`, `references/RTL_FILE_MANAGEMENT.md`, `references/EXAMPLES.md`. Select the closest original template in `templates/`. Preserve legacy naming; update `filelist/*.f`.
4. **Implement** smallest well-scoped RTL changes following `workflows/rtl-development.md`; create/update directed tests and assertions.
5. **Validate** source manifests and run the optional `scripts/rtl_style_check.py`, then lint and elaborate. Fix actual design failures instead of suppressing rules.
6. **Simulate** using `workflows/rtl-simulation.md`: reset, stress, numerical reference model, backpressure, edge-case, latency and seeded regressions. Capture explicit oracle and evidence. For failures use `workflows/rtl-waveform-debug.md`.
7. **Coverage**: distinguish functional/code coverage (VCS/Verilator etc.) from PrimeTime timing-analysis coverage. Unavailable coverage remains unknown, not pass.
8. **PPA**: follow `workflows/rtl-ppa.md`. Prefer open-source quick checks; use `workflows/synopsys-dc.md`, `workflows/synopsys-pt-sta.md`, `workflows/synopsys-power.md` and `workflows/sram-macro-analysis.md` for authorized remote ASIC evaluation. Validate real library/SRAM corner, SDC, netlist, parasitics and SAIF assumptions. Remote templates are not a fully implemented dispatcher.
9. **Optimize** according to `workflows/rtl-goal-loop.md`, treating previous evidence affected by code/constraints changes as stale. Rerun relevant checks after each repair.
10. **Review** independently according to `workflows/rtl-review.md`; report source revision, tests and seeds, observed cycle count, area/timing/power with provenance, coverage, limits and unresolved goals.

## Adaptive path

- **New module / refactor:** style → contract → implement → lint → simulation → cycle scoreboarding → PPA (when available) → review.
- **Bugfix:** reproduce → waveform/root cause → minimal repair → full relevant regression → review.
- **PPA optimization:** freeze baseline → simulation → comparable synth/STA/power → bounded change → fresh functional/cycle/PPA evidence.
- **Environment incomplete:** complete every locally runnable gate, explicitly mark non-executed gates `blocked` or `not_run`; never hallucinate signoff.

## Paths and invocation

Paths in internal documents historically referred to separate `skills/<name>/` folders. Under this aggregation, resolve all relative resources **from this Skill root**:
- `workflows/<name>.md`
- `references/<name>/...` for domain-specific examples, or `references/...` for coding conventions.
- `templates/...`, `scripts/...`, `adapters/...`, `configs/...`, `tests/...`.

Example:
```bash
python scripts/rtl_style_check.py --root /path/to/design --filelist rtl/filelist/top.f
python -m unittest discover -s tests -p 'test_*.py' -v
```
These commands should be executed **from the Skill root**, or with explicit paths. The lexical checker cannot replace actual HDL lint/elaboration. Do not run remote scripts without user-authorized server configuration and verified host identity.

## Tool safety and provenance

No password or PDK content in public Git. Use strict host-key checking and licensed tools only on authorized environments. Standalone files here capture Booley-inspired flow design but do not implement its Goal Mode backend or hardened sandbox. At every gate distinguish PASS, FAIL, INCONCLUSIVE, BLOCKED and NOT_RUN. Completion claims must cite artifacts from the current revision.
