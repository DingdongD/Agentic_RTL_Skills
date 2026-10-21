# Real Compiler_Codes verification matrix

The public Compiler_Codes repository contains `cyclesim/ACTransformerCycleSim`
with Python resource/RTL-like scheduling tests. It also distinguishes ACSim_DS
functional CModel from the Python cycle simulator and original SystemC ACTSim.
The public ACTSim status states that the CTC tensor path is an uncalibrated stub
and the original SystemC simulator is not an end-to-end golden reference.

## CI tier: genuinely executable public integration
Clone the upstream repo read-only at a pinned full SHA and run:
`python -m integrations.compiler_codes --root <checkout> --out <report.json>`
The runner selects portable unit tests with no private ACompiler fixtures.
This checks the actual upstream Python code; it **does not** establish
CModel-to-Verilog bit/cycle equivalence. Its PASS must be labeled portable.

## Hardware tier: requires explicit reference artifacts
To validate CModel vs actual RTL: record one workload and input/weight hashes;
run ACSim_DS or a validated numerical oracle; simulate actual matched RTL using
the identical workload; normalize signed widths, rounding, reset and transaction
time; emit two JSONL traces and use the cycle scoreboard. Do not fabricate RTL
trace from the Python model or compare a reference trace to itself. Fail closed
when real package, CModel binary, RTL simulation or signal adapter unavailable.

## ASIC tier
A licensed DC/PT/PTPX environment and PDK/SRAM views are required. No public CI
runner can claim those signoff results. Physical placement estimates require
a real mapped technology netlist, legal libraries and SDC.
