# Example Goal Ledger (inspired by Booley Goal Mode)

Booley's real `booley-goal` freezes named test variants and seeds and requires fresh evidence; this standalone skill **does not automatically enforce those semantics**. Treat this as a reviewable project-owned acceptance checklist.

```json
{
  "revision": "replace-with-git-sha",
  "target": "sim_compute_pe",
  "goals": [
    {"id": "compile", "type": "elaboration", "state": "pending", "evidence": null},
    {"id": "reset", "type": "simulation", "test": "reset", "seed": 1, "state": "pending", "evidence": null},
    {"id": "latency", "type": "cycle_count", "test": "one_transaction", "expected_cycles": 1, "state": "pending", "evidence": null},
    {"id": "timing", "type": "sta", "corner": "ss", "required_wns_ns": 0.0, "state": "pending", "evidence": null},
    {"id": "review", "type": "independent_review", "state": "pending", "evidence": null}
  ]
}
```

The latency example is for the supplied `compute_pe.sv` template only. A `pending` goal is never considered met. For seeded random testing, freeze the seed and parameters at entry. After any functional RTL edit, invalidate previous simulation evidence; after an SDC/library edit, invalidate STA/PPA evidence. Distinguish failed design, inconclusive test, and infrastructure error.
