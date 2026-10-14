---
name: rtl-goal-loop
description: Drive iterative RTL engineering against mandatory evidence-backed functional, cycle, area, timing, coverage and review goals, inspired by Booley Goal Mode.
---

# Evidence-Backed RTL Goal Loop

## Entry contract

Translate the task into a goal ledger containing goal ID, scope, pass criterion, required tool, test/target, baseline and acceptance threshold. Typical independent goals: RTL compilation, named functional tests, exact output codes, cycle ceiling, critical path, area budget and review.

A goal is not satisfied by an agent statement. It needs tool evidence from the **current RTL revision** and the exact configured build variant.

## Loop

1. Capture baseline revision and current goal ledger. Mark all unevaluated goals `pending`.
2. Run the cheapest relevant check first: lint → narrow directed simulation → full regression → synthesis/timing → review.
3. Normalize every result to `pass`, `fail`, `inconclusive` or `infrastructure_error`. Record run ID, revision, command, target, tool version, seed, metric and artifact path.
4. Diagnose a failed goal with the smallest reproducible case. Propose and implement a bounded repair.
5. Invalidate evidence affected by the RTL, testbench, constraints or tool-configuration change. Re-run all affected goals.
6. Do not silently relax thresholds, skip tests or substitute a different implementation for the intended architecture. Obtain explicit user approval for changing a goal.
7. Stop when all mandatory goals have fresh evidence, or report precise blockers and unmet goals. Independent review should evaluate actual diffs and artifacts.

## Example ledger

```yaml
revision: "<git SHA>"
goals:
  - id: sim-reset
    check: simulation
    target: "<declared target>"
    criterion: "reset test passes"
    status: pending
  - id: latency
    check: cycle-count
    criterion: "accepted input to output <= specified cycles"
    status: pending
  - id: area
    check: synthesis
    criterion: "same library, area increase <= specified budget"
    status: pending
```

This is an instruction-level goal loop, **not** Booley's internal Goal Mode database or its freshness validator. A scripted production implementation must persist and verify these fields.
