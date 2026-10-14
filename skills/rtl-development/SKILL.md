---
name: rtl-development
description: Implement or refactor Verilog/SystemVerilog hardware modules from explicit interface, handshake, reset and cycle-level specifications. Use for RTL implementation, microarchitecture edits and pipeline changes.
---

# RTL Development

## Workflow

1. Discover the top, hierarchy, source list, build targets, parameters, clocks, reset polarities and existing verification environment.
2. Record a design contract: ports/bit widths/signedness, ready-valid semantics, transactions, reset outputs, throughput, latency, ordering, flush/backpressure and corner cases.
3. Establish a baseline with the existing lint and simulation commands. Record pre-existing failures rather than hiding them.
4. Make the smallest bounded RTL changes. Use synthesizable constructs for synthesis targets, explicit sequential/combinational partitioning, complete assignments and deterministic reset behavior.
5. Audit widths, casting, truncation, signed math, overflow, blocking/nonblocking assignments, CDC, metastability and combinational loops.
6. Add directed tests for reset, stalls, first/last transaction, partial tiles, simultaneous requests, and any changed state transition.
7. Run lint and functional simulation, then cycle-by-cycle scoreboarding when timing is part of the contract. Treat an elaboration failure as infrastructure/design-build failure, not proof of functionality.
8. Report edited files, architecture choices, observed tests and residual risks. Never assert completion without new evidence.

## Non-negotiable checks

- Separate behavioral equivalence from latency equivalence.
- Preserve original mathematical and numerical contracts; specify rounding, saturation and handling of X/Z if relevant.
- In pipelined designs, track valid/data alignment and clock-enable behavior at every stage.
- For asynchronous crossings, apply proper synchronization or an asynchronous FIFO; do not simply synchronize multi-bit data.
- Do not quietly replace structural PE/array instances with single-cycle behavioral loops when cycle-accurate architecture is required.

See `rtl-simulation` and `rtl-review` for acceptance.

## Required repository coding convention

Before creating or modifying RTL, follow `rtl-coding-standard` and its Compiler_Codes naming/file-management references. Preserve existing ACTransformer-style names and update affected `filelist/*.f` manifests; avoid broad renaming without approval.

## Template-based implementation

Use `rtl-coding-standard/references/EXAMPLES.md` to select the closest compute PE, FIFO, buffer, controller or top example. Adapt the example to the actual interface and microarchitecture contract; the examples are educational, not reusable IP blocks. Require an updated explicit filelist and verify real module elaboration.
