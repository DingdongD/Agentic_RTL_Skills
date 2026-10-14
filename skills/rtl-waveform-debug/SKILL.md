---
name: rtl-waveform-debug
description: Investigate RTL failures by querying actual VCD/FST transitions, ready-valid handshakes, state changes, and cycle-by-cycle dataflow instead of guessing from source code.
---

# Waveform Debugging

1. Reproduce the failure with the exact simulator configuration, parameters, test and seed.
2. Enable a narrowly scoped trace; record waveform path, timescale and relevant clock domain.
3. Start from the first failing assertion or output mismatch, then inspect the preceding dependency chain rather than only the final symptom.
4. Compare reset release, enables, valid/ready handshakes, FIFO occupancy, state transitions, pipeline registers, and output data at clock boundaries.
5. Verify off-by-one errors using accepted input cycle versus output-valid cycle, not just timestamp differences.
6. Distinguish unknown values, uninitialized state, un-driven nets, and genuine functional mismatches.
7. Produce a small timeline with signal names and exact cycles, root-cause hypothesis, and tests to falsify it.

If Booley's `bwave` is installed, inspect `bwave --help` and use its `wave`, `signal`, `find`, `sample`, or `distance` commands as supported by the installed version. Otherwise use an installed VCD/FST parser or viewer. Do not claim traces were inspected unless the actual artifact was opened.

A useful diagnosis reports **observed waveform evidence**, expected behavior, root cause, minimal RTL/testbench repair and fresh regression results.

## Worked example

Read `references/HANDSHAKE_CASE.md` for a buffer request/valid timing investigation; account for nonblocking-assignment scheduling and macro access latency. The table is hypothetical, not measured waveform evidence.
