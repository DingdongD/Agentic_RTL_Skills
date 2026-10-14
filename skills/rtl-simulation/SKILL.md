---
name: rtl-simulation
description: Reproducibly compile and simulate RTL with Icarus, Verilator or a configured Booley simulation target; validate functional or cycle-level behavior with explicit oracles and saved evidence.
---

# RTL Simulation

## Prepare

Identify DUT, testbench, top, parameterization, simulator, source ordering, defines, clock/reset, stimulus and expected outputs. Prefer project build scripts/Makefile/FuseSoC rather than reconstructing an incomplete ad-hoc file list.

When Booley is installed and configured:
```bash
booley targets --for sim
booley flow sim --target <DECLARED_SIM_TARGET> --test <DECLARED_TEST>
```
Only use target/test names actually listed by the project. Otherwise run its existing Icarus, Verilator or cocotb test commands and capture exact versions and arguments.

## Validation protocol

1. Ensure the testbench has an explicit oracle: assertions, golden vectors, scoreboard or deterministic reference model.
2. Use directed edge cases before random/parameter sweeps. Log fixed seeds and relevant parameter values.
3. For cycle contracts, compare transaction outputs **and their accepted/produced cycles**, accounting for ready-valid stalls.
4. Distinguish compilation/elaboration error, test failure, simulator timeout, inconclusive run and tool absence.
5. On failure, minimize a reproducer; inspect logs/waveforms; change one hypothesis at a time; rerun the failing test and regression set.
6. Include trace and coverage where supported; line coverage alone does not prove protocol correctness.
7. Store revision, tool version, command, target, seed, verdict, cycle count and artifact paths. Evidence from previous RTL revisions must be revalidated.

## Portable examples (adapt to the project's own file list)

```bash
iverilog -g2012 -s tb_top -o build/sim.vvp -f rtl_files.f
vvp build/sim.vvp
verilator --lint-only --timing -f rtl_files.f --top-module dut_top
```

The examples are templates, not executed validation. If the top or testbench are different, edit them accordingly.
