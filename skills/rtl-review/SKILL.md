---
name: rtl-review
description: Independently review RTL changes for functional bugs, handshake/reset/CDC hazards, numerical equivalence, untested conditions and weak or stale verification evidence.
---

# RTL Review

Review the **diff and the test evidence**, not the author's explanation. First identify the spec, baseline and edited interfaces. Use an independent agent/context where available, but do not treat another model's opinion as test evidence.

Check:
- reset semantics, first-cycle behavior, signedness, bit widths, truncation, overflow and X propagation;
- ready-valid ordering, backpressure stability, stalls, FIFO full/empty and concurrent operations;
- FSM reachability, inferred latches, parameter corner cases and clock-domain crossing;
- cycle count, PE mapping, memory interfaces and whether claimed throughput is physically realizable;
- missing directed/random tests, missing assertions, weak test oracles and modified tests that conceal regressions;
- comparability of PPA runs: same hierarchy, library, constraints, macros and tool version.

Return findings ordered by severity with exact file/line references where available, a small reproducer, expected versus actual behavior, and a proposed corrective test. State explicitly which claims have executable evidence and which are unverified. Do not declare a pass for checks not run.

Final review decision: `accept`, `changes_required` or `insufficient_evidence`; separate engineering recommendations from measured failures.
