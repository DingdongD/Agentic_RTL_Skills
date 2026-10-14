---
name: rtl-ppa
description: Evaluate RTL synthesis area, timing and resource tradeoffs, including apples-to-apples baseline comparison using Booley, Yosys, OpenROAD or configured FPGA flows.
---

# RTL PPA Evaluation

## Baseline and controls

1. Record the exact revision, top, hierarchy, parameters, sources, timing constraints, libraries/PDK, target frequency, synthesis flags and tool versions.
2. Reproduce a baseline before optimizing; verify that the proposed revision remains functionally equivalent or deliberately changes the stated contract.
3. Use the project's existing synthesis target. Optional configured Booley commands:
```bash
booley targets --for synth
booley flow synth --target <DECLARED_SYNTH_TARGET>
```
4. Otherwise use the repository's Yosys/OpenROAD/Vivado build; don't synthesize an arbitrary reduced hierarchy and report it as full-chip area.
5. Distinguish generic synthesis cell counts, technology-mapped area, placed area, critical-path delay, slack and power estimates. Do not call an unconstrained Yosys cell count a physical area measurement.
6. Ensure timing constraints and physical corner assumptions are identical between baseline and candidate.
7. Report both absolute and percentage changes with metric units, timing feasibility and tradeoffs.

## Acceptance

- PPA improvement must not bypass regression, reset/handshake correctness, or architecture constraints.
- Account for buffers, pipelines, control, SRAM/macros and routing model limitations.
- For power, specify whether switching activity, voltage, frequency and physical parasitics were actually modeled.
- Report unavailable values as unknown; never make up area, timing or energy numbers.
