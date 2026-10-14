---
name: rtl-ppa
description: Analyze ASIC RTL area, timing and power with matched baseline/candidate constraints, using fast Yosys/OpenROAD or remote Synopsys DC, PrimeTime, PrimePower/PTPX and SRAM macro evidence.
---

# Two-Tier RTL PPA

Choose the analysis fidelity: fast Yosys/OpenROAD estimates for iteration, or configured Synopsys DC/PT/PTPX for technology-mapped area, STA and activity-informed power. Neither proves post-route signoff unless real physical implementation, extraction, corners and timing/power models are provided.

## Baseline contract

Freeze RTL git revision, hierarchy, parameters, tool versions, library/PDK identity, process/voltage/temperature corners, clocks, SDC, SRAM macro views, input activity and run flags. Do not compare unaligned experiments.

## Open-source backend

Prefer the project's existing synthesis flow. When Booley is properly configured, inspect declared targets with `booley targets --for synth` and invoke `booley flow synth --target <ACTUAL_TARGET>`. Otherwise run the existing Yosys/OpenROAD scripts. Do not mistake generic cell count for mapped physical area.

## Synopsys backend

Follow [remote integration](references/REMOTE_SYNOPSYS.md). Use the separate `synopsys-dc`, `synopsys-pt-sta`, `synopsys-power`, `sram-macro-analysis` Skills. DC generates the mapped netlist and preliminary area; PrimeTime verifies setup/hold and constraint/analysis coverage; PrimePower/PTPX estimates leakage/dynamic power from the mapped netlist and workload activity. Simulation code/functional coverage requires VCS or another simulator, not PrimeTime.

Stop on unresolved macro instances, unlinked designs, unconstrained timing, missing SDC or unqualified PVT libraries. Treat missing switching activity and absent SRAM macro models as explicit evidence gaps, not zero contributions.

Report objective, absolute baseline/candidate measurements and units, deltas, run status, constraints/corner, activity provenance, macro/standard-cell partitioning, critical paths, timing violations, limitations and saved evidence paths. Never invent PPA measurements.
