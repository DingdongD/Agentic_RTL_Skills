# Worked example catalog

These are newly authored educational templates (not copied from proprietary Compiler_Codes RTL). Source conventions were derived from modules linked in COMPILER_CODES_CONVENTIONS.md.

| Template | Lesson | What to adjust |
| --- | --- | --- |
| `../templates/compute_pe.sv` | `din_vld/dout_vld`, registered arithmetic, parameter widths | Operation, signed arithmetic, fixed latency |
| `../templates/fifo.sv` | `fifo_wr/fifo_rd/fifo_cnt`, full/empty, bankless memory | Depth=power-of-two, overflow/underflow assertions, simultaneous push/pop policy |
| `../templates/buffer.sv` | `lbuf_*` ports, synchronous read, valid alignment | SRAM macro semantics, banking, byte writes, conflicts |
| `../templates/controller.sv` | `din_st`, `busy`, `dout_vld`, sequencer | LATENCY>=1, abort/reset, backpressure |
| `../templates/top.sv` | Structural hierarchy, `u_` instance, named ports | Explicit widths and inter-engine protocols |
| `../templates/compute.f` | Explicit compilation units | Paths, tool working directory, optional includes |

## Counterexamples: do not imitate

**Wrong module/file naming**: file `MyMAC.sv`, module `myMAC` with instance `mac0`. Expected: `compute_mac.sv`, `compute_mac`, `u_compute_mac`; preserve external legacy names.

**Wrong pipeline**: a sequential `dout` is registered but `assign dout_vld=din_vld`. Data and valid correspond to different cycles; register valid alongside data.

**Wrong array**: writing all 64 modeled PEs with a single-cycle nested loop while claiming an 8x8 pipelined physical implementation. Require explicit resources, arbitration and latency.

**Wrong tree**: placing synthesis RTL under `rtl/tb/` or adding a module without modifying `rtl/filelist/compute.f`. Keep DUT, TB and generated outputs separate.

**Wrong macro abstraction**: treating a synchronous compiled SRAM as a zero-latency asynchronous read. Require matching cycle contract and Liberty/Verilog views.

**Wrong checks**: reporting lint passes from filename/style scans alone. Checker is supplemental; run real elaboration/simulation.
