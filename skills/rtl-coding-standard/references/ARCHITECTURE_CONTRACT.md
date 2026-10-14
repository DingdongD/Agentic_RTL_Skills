# Microarchitecture contract — optional machine-readable project requirement

A coding style cannot prove structural fidelity. For each cycle-sensitive module write a reviewed contract similar to:

```json
{
  "module": "tdp_macn_ds",
  "source_file": "rtl/hdl/compute/tdp/tdp_macn_ds.sv",
  "clock": "clk",
  "reset": {"signal": "rst_n", "active_low": true},
  "arithmetic": {"input_format": "bf16", "accumulator_format": "fp32", "rounding": "documented_per_stage"},
  "parallelism": {"lanes": 16, "physical_pe_instances": "verify_in_elaborated_netlist"},
  "latency": {"cycles": null, "definition": "accepted input edge to output-valid edge"},
  "throughput": {"inputs_per_cycle": null},
  "memory": {"banks": null, "read_latency": null},
  "testbench": {"cycle_scoreboard": "required", "backpressure": "as_applicable"}
}
```

Values of `null` mean **unknown**, not zero. This example is NOT a measured contract for Compiler_Codes' original TDP. Do not assert a throughput/latency without tracing the instantiated design and verifying simulation. Verify any PE-count claim structurally; a parameter named LANES does not demonstrate real parallel execution.
