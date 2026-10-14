---
name: synopsys-dc
description: Prepare remote Synopsys Design Compiler synthesis, read mapped area and timing reports, and preserve implementation provenance for ASIC RTL.
---

# Synopsys Design Compiler

Read `configs/eda_servers.example.json`, `configs/design.example.json`, and `templates/dc/run.tcl`. Use **private, ignored** copies for remote host and foundry paths. Require explicit design top, a complete source list, process/library corner and SDC. Run a remote preflight for host authenticity, license availability and command installation before synthesis. Use a unique remote directory for each run; never overwrite other jobs. DC reports logical mapped synthesis, **not** post-route area or signoff power. Capture `check_design`, area, constraints, mapped Verilog, SDC, logs, tool version and exact input hashes. Treat missing macros, black boxes and failed `link` as fatal to a complete area claim. Compare only matched libraries, constraints, hierarchy and version.
