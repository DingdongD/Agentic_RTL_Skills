---
name: synopsys-pt-sta
description: Assess Synopsys PrimeTime setup/hold, constraints and timing-analysis coverage using mapped netlists and technology libraries.
---

# PrimeTime STA

Start only from a successfully linked mapped netlist, SDC and correct Liberty models, including SRAM. Prefer post-placement or post-route parasitics when available; otherwise label the result **pre-layout estimate**. Run `check_timing`, analysis coverage, max and min path reports, constraints, WNS and TNS at declared process, voltage and temperature corners. A positive WNS alone is not proof of timing closure: audit unconstrained endpoints, missing clocks, false paths, I/O constraints and CDC. Record clock period, uncertainty, output loads, input delays, corner and parasitic provenance. Never confuse STA analysis coverage with RTL functional/code coverage.
