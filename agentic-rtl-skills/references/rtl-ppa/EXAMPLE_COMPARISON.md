# Baseline/candidate PPA comparison example

The values here are placeholders. Never present them as measurements.

```json
{
  "baseline": {"commit": "<sha-A>", "cell_area_um2": null, "wns_ns": null, "power_mw": null},
  "candidate": {"commit": "<sha-B>", "cell_area_um2": null, "wns_ns": null, "power_mw": null},
  "shared_constraints": {
    "top": "compute_pe", "library_hash": "<hash>", "sdc_hash": "<hash>",
    "tool_versions": {}, "pvt_corner": "ss", "saif_hash": null
  }
}
```

Check consistency of hierarchy, library, SDC, corner, voltage, clock definition, macros, parasitics and activity before reporting a percentage. `null` is unknown. Yosys generic gates are not comparable to mapped Synopsys cell area. Pre-layout timing cannot be labeled signoff. A successful DC run with blackboxes or missing memory models is not a valid full-chip area result.
