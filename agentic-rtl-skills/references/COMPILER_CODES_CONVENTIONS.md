# Coding conventions derived from Compiler_Codes (ACTransformer-DS)

Reference repository: https://github.com/DingdongD/Compiler_Codes
Inspected locations:
- `rtl/ACTransformer_DS/rtl/hdl/buf_mgr/buf_mgr.sv`
- `rtl/ACTransformer_DS/rtl/hdl/common/fifo/sfifo.sv`
- `rtl/ACTransformer_DS/rtl/hdl/ctc/ct_cluster_ds/tdp/tdp_macn_ds.sv`
- `rtl/ACTransformer_DS/rtl/filelist/ctc.f`

These files provide **observed conventions**, not a claim that all RTL files in the source repository follow one perfect standard.

## Observed
- Files and modules lower `snake_case`: `buf_mgr.sv`, `tdp_macn_ds.sv`, `sfifo.sv`.
- Uppercase parameter names, often condensed: `LBUF_BN`, `LBUF_AW`, `LBUF_DW`, `CWBUF_RDLY`, `IN_DAT_WIDTH`, `MACV_LAT`.
- Signals: `core_clk`, `rst_n`, `din_vld`, `dout_vld`, `ctc_lbuf_wr_req`, `lbuf_emac_rd_rdy`.
- Instances: `u_macn`, `u_acc_32`, `u_ram`.
- Pipeline: `dout_vld_reg`, `din_st_dly_reg`, `fifo_ef_d0`.
- Fine hierarchy: `hdl/ctc/ct_cluster_ds/{common,ct_ctrl,mixed_precision,pp,tdp,top}/`, `hdl/common/{fifo,ram,sync,...}/`.
- Source filelists: `filelist/ctc.f` explicitly enumerates sources and references `../macro/ctc_define.vh`.
- Legacy compatibility: many modules use `input wire`, `reg`, `always @(posedge clk or negedge rst_n)`, rather than enforcing `logic/always_ff`.
- Design comments use functional sections and may contain historical metadata.

## Normative additions (quality improvements, not universal facts about legacy code)
- Standardize port/group indentation for newly written modules; use named port connections.
- Avoid `casex`, incomplete combinational assignments and implicit nets.
- Use explicit signed/unsigned casts and carefully sized constants.
- Where practical, provide an explicit `default_nettype none` policy compatible with surrounding includes.
- Ensure handshake assertions cover data stability under stall and conservation of transfers.
- Never treat a behavioral array updated in one cycle as a physical PE pipeline if latency matters.
- Record fixed memory read latency and read-during-write behavior with the instantiated macro.
- Preserve existing RTL when reorganization risks affecting simulation, synthesis or architectural equivalence.

## Naming examples

| Role | Example |
|---|---|
| Functional module | `tdp_macn_ds` |
| Structural instance | `u_macn` |
| Input | `din_vld` |
| Output | `dout_vld` |
| Bank write request | `ctc_lbuf_wr_req` |
| Ready response | `lbuf_ctc_wr_rdy` |
| Memory data width | `LBUF_DW` |
| Clock and reset | `core_clk`, `rst_n` |
| Registered delayed valid | `dout_vld_reg` |

No fixed universal preference between `_vld` and `_valid` should override a stable upstream module interface.
