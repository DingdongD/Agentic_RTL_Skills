# Example: registered PE simulation

DUT: `rtl-coding-standard/templates/compute_pe.sv` (copy into your project and update its manifest). The DUT samples `din_vld` at an active edge and registers `dout` and `dout_vld` on that edge. Do not add an extra cycle in the scoreboard.

Use the project's existing testbench to check:
- reset deasserted: `dout_vld=0` before first accepted sample;
- one valid input, including carry-out;
- valid=0 gap does not produce a result;
- back-to-back valid inputs return corresponding results each edge;
- DATA_W parameter variants such as 8, 16 and 32.

Example lint (not a claim of a verified run):
```bash
verilator --lint-only --top-module compute_pe rtl/hdl/compute/pe/compute_pe.sv
```

A true regression must save simulator version, source hash, parameterization, seed, testbench assertions and observed results. Avoid declaring “cycle-accurate” just because a waveform exists.
