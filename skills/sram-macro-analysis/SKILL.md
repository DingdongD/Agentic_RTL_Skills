---
name: sram-macro-analysis
description: Integrate SRAM memory-compiler macro manifests and validate matching Verilog, Liberty and LEF views for ASIC area/timing/power estimation.
---

# SRAM Macro Integration

Collect macro dimensions, number of ports, word widths, mux/column organization, byte enables, banking and target corner. Use `configs/memory.macros.example.json` as a *manifest*, not an executable compiler definition. Run vendor SRAM compiler only through a PDK-specific adapter with configured authorization. The public repository must never contain proprietary foundry libraries, generated restricted SRAM collateral, credentials or license strings.

Before DC/PT/power, ensure the macro instances resolve to consistent Verilog stubs/models and corner-matched Liberty. LEF/physical views are required for physical-area/routing workflows, not standalone DC logic synthesis. Report standard-cell area separately from macro area. Validate clocking, access latency, output register mode, read-during-write behavior and model/view consistency. Missing macro area/timing/power is a blocker, not zero.

## Guided example

Consult `references/EXAMPLE_MANIFEST.md` before using any SRAM macro model in synthesis, timing or power calculations.
