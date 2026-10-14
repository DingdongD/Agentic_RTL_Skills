---
name: synopsys-power
description: Collect Synopsys PrimePower/PTPX estimated dynamic and leakage power using activity information and audited switching-activity coverage.
---

# Power with PrimePower / PTPX

Confirm installed PrimePower/PTPX license, executable and accepted Tcl commands before execution. Consume the *same* mapped netlist, libraries and timing constraints as STA. Prefer workload-representative SAIF with known hierarchy mapping; check annotated/unannotated signal counts and switching coverage. Record voltage, frequency, corner, leakage and internal/switching power, clock-network assumptions and whether parasitics exist. Do not report vectorless or pre-layout estimates as signoff power. Expose missing activity as `unknown` or an explicit lower-confidence vectorless mode; fail the power goal if evidence policy requires realistic activity. Never invent joules/op without a measured operation count and workload period.

## Guided example

Consult `references/EXAMPLE_ACTIVITY.md` to review SAIF provenance, signal mapping and activity completeness.
