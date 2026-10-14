---
name: rtl-coding-standard
description: Enforce the Compiler_Codes/ACTransformer-compatible Verilog and SystemVerilog naming, module organization, filelist management, interface and synthesizable coding conventions. Use for creating, editing, organizing, reviewing or refactoring RTL and testbenches.
---

# Compiler_Codes-Compatible RTL Coding Standard

Use [the reference](references/COMPILER_CODES_CONVENTIONS.md) before creating or changing RTL. This is a **compatibility-oriented default**, not a license to copy third-party proprietary implementation text. Follow the current project's established conventions when they are more specific.

## Required workflow
1. Discover RTL roots, top module, filelists, build scripts, macro/includes, testbench hierarchy and synthesis targets.
2. Identify adjacent modules and reuse their naming/interface conventions; do not rename public interfaces solely for style.
3. Put each new hardware module in its functional engine directory and choose a matching `snake_case.sv` filename.
4. Update the appropriate explicit `filelist/*.f` or project manifest for simulation and synthesis; resolve includes and duplicates from the list's intended working directory.
5. Keep synthesizable design files separate from testbenches, generated files, scripts and output artifacts.
6. Enforce explicit widths/signedness, reset, pipeline alignment, hierarchical instantiation and memory interfaces. Avoid inferred latches and unsupported simulator-only hardware constructs.
7. Run applicable lint/elaboration and project regression after structural or filelist changes; do not assert lint passed if tools were not run.
8. Report every created/moved/renamed file and each changed filelist/top/test configuration.

## Naming rules
- Module/file: lower snake_case, file basename preferably matches module name; preserve established legacy exceptions.
- Parameters/localparams/macros: UPPER_SNAKE_CASE (`LBUF_DW`, `DATA_W`, `MACV_LAT`).
- Signals and ports: lower snake_case; preserve subsystem prefix (`ctc_lbuf_wr_req`, `lbuf_rdata`).
- Instances: `u_<function>` (`u_macn`, `u_ram`); generated instances get stable index labels.
- Clocks/resets: `clk` or qualified `core_clk`; active-low reset `rst_n`; do not change polarity/name implicitly.
- Handshakes: prefer surrounding project vocabulary (`_vld`, `_rdy`, `_req`, `_wr`, `_rd`), not arbitrary mixing.
- Width/count: existing conventions include `_DW`, `_AW`, `_BN`, `_RDLY`; match the engine.
- Pipeline stage: document `_d0`, `_d1`, `_dly`, `_reg` meaning; specify source/destination cycle.

## Style and compatibility
- Explicitly partition combinational/sequential logic; blocking assignments in combinational processes and nonblocking in clocked processes.
- Current Compiler_Codes source uses both `wire/reg/always` and SystemVerilog. Keep per-module style coherent; optional `logic/always_ff/always_comb` for **new** modules only when accepted by current toolchain.
- Treat legacy `<= #delay` simulation annotations as compatibility artifacts; do not introduce them into new synthesizable RTL.
- Prefer named port mapping and explicit parameter binding; preserve physical PE and memory hierarchy.
- Don't auto-rename or auto-format large pre-existing trees without user approval; prefer diagnostics for inherited inconsistencies.
- Module comments should describe role, ports, latency, reset, numeric contract and changes; do **not** reproduce copyright/proprietary headers from unrelated sources.

## File management
Use [the directory guide](references/RTL_FILE_MANAGEMENT.md). Avoid globs as authoritative synthesis source lists when a maintained filelist exists. Keep included `.vh/.svh` distinct from standalone compilation units. Never place generated netlists, waveforms, PDK contents, SRAM compiler outputs or licensed reports in the source tree.

## Acceptance
A style pass requires correct names/location/manifest plus actual lint/elaboration when available. A functional pass requires tests. A PPA pass requires tool evidence. Preserve all three verdicts independently.

## Mandatory examples and gates

Before authoring new code, read `references/EXAMPLES.md`, choose the closest original template in `templates/`, and inspect the corresponding real Compiler_Codes *convention* documented in `references/COMPILER_CODES_CONVENTIONS.md`. Use `references/ARCHITECTURE_CONTRACT.md` for cycle-critical PE/buffer/controller designs. Do not copy proprietary original RTL text or copyright headers into this repository.

For a changed project's source manifest, run (from this Skill directory or adjust the path):
```bash
python scripts/rtl_style_check.py --root /path/to/project --filelist rtl/filelist/compute.f
python -m unittest discover -s tests -v
```
The checker is deliberately conservative and supports a subset of common filelist syntax; nested lists require flattening or parser extension. A passing style check is not Verilator lint, functional verification, or physical validation. Add actual simulator/linter checks before accepting the implementation.
