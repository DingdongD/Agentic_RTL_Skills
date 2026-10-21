# Compiler_Codes non-destructive integration contract

This workflow is mandatory when working against an existing compiler + CModel +
RTL project. Treat the existing project as an external source of truth.
Never copy a generic scaffold over an established tree.

## Modes
- **read_only** (default): inspect and report; do not write any target files.
- **patch**: operate only in a fresh dedicated worktree and on allowlisted files.
- **cross_layer**: requires explicit user authorization for changes to ISA,
  compiler lowering, CModel ABI, hardware-visible layout, or latency semantics.

## Required preflight
1. Record baseline full Git commit SHA and branch. Reject dirty baseline or
   establish and document a separate frozen clean reference.
2. Inventory module hierarchies, filelists, generated files, interfaces,
   simulation targets, compiler commands and existing tests. Do not assume paths.
3. Establish per-task allowlist from that inventory; example policy paths are
   placeholders, not permission to alter matching files.
4. Create a **separate git worktree** from the frozen baseline; never operate
   on main, master or the user's ordinary worktree.
5. Keep test fixtures and expected results immutable. Reject any patch that
   weakens tests, renames paths or changes public interfaces without explicit
   cross-layer authorization.
6. Run `python -m engine.repository_guard --root <worktree> --policy <policy.json> --base <SHA> --mode patch`
   from the skill root before every tool execution that consumes modified RTL.
7. The guard is a scope check, **not** a security sandbox or functional proof.
   Run original regressions plus directed tests, numerical and temporal oracle,
   and relevant compiler-to-RTL integration checks.
8. Store source SHA, contract SHA, tool versions, commands, exit codes, reports
   and failures as immutable candidate evidence. Any changed input invalidates
   downstream claims. Never silently rebaseline failures.
9. Generate a PR with the minimal diff and evidence manifest. No automatic merge.

## Cross-layer dependency triggers
- Port, reset, ready/valid, parameter ABI changes => module integration, TB,
  compiler emitter and downstream RTL simulations.
- ISA, tile shape, layout or addressing changes => compiler lowering, CModel,
  instruction encoding, DMA and RTL regression.
- Rounding/quantization changes => bit-exact numerical suite.
- Buffer/bank arbitration changes => cycle event trace, backpressure, hazard tests.
- Clock or SDC changes => CDC, STA, power and all affected PPA evidence.

## Acceptance statuses
PASS, FAIL, BLOCKED, INCONCLUSIVE, NOT_RUN, STALE.
File existence alone is not evidence of PASS. Tool calls and exits, explicit
assertions and artifact revision identity must be recorded.

## Candidate boundary
Do not claim that cycle accuracy or remote Synopsys execution is implemented
merely because this workflow describes it. Existing Tcl, SSH and report-parser
adapters require job lifecycle integration and live licensed-EDA validation.
