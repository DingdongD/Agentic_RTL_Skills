# RTL specification, generation and verification quality contract

Borrow ideas, not source code, from rtl-skills and verilog-generator.

1. Decompose requirements into ports, reset and clock domains, arithmetic,
   transactions, latency/II, corner cases, and explicit acceptance tests.
2. Use `contracts/schemas/architecture.schema.json` for architecture-level
   inputs. Do not reinterpret an undefined interface or reset behavior.
3. Generate an operator-reviewed implementation proposal and an independent
   Python reference model before creating RTL.
4. Require strict naming, no implicit nets, no unintended inferred latches,
   no hardcoded simulation success, no silencing lint warnings.
5. Preserve the existing repository hierarchy and coding conventions.
6. Generate testbench with reset, edge values, backpressure, randomized seeds,
   and protocol assertions. Never weaken original tests.
7. Run actual HDL lint/elaboration, simulation and available formal checks.
   Lack of installed tools is BLOCKED/NOT_RUN, not PASS.
8. Re-run every affected downstream test after patching RTL.
9. Artifact receipts include command, tool version, input revision, exit code,
   actual assertions, and reports.

The minimal `generation.rtl_scaffold` implementation intentionally supports
ONLY a synchronous-active-low enabled counter as a mechanically checked
example. It is NOT a free-form Verilog generator nor a model-backed testbench
generator. Real skill-driven generation is subject to all gates above.

No code is copied from either external repository.
