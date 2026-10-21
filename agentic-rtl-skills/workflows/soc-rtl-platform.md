# SoC–RTL platform: implemented interfaces and evidence limits

**Single Skill:** `agentic-rtl-skills/SKILL.md`. This is not a second skill.

## DAG orchestration
`python -m engine.flow_engine --plan plan.json --root <candidate-root> --state <outside-candidate>/flow-state.json`
Plans contain nodes {id, deps, command: argv[], inputs, outputs, timeout_seconds}.
The runner fingerprints explicit inputs, command and dependency fingerprints.
It reruns changed candidates, reuses successful artifacts only when outputs exist,
blocks dependent nodes after failures and writes atomic JSON snapshots.
Plans are trusted reviewed configuration, not safe inputs from arbitrary PRs.
Run the repository guard first; do not run uncontrolled commands from a user
repository without operator review. State cache does not substitute for proofs.

## Cycle comparison
`python -m verification.cycle_scoreboard --reference model.jsonl --rtl rtl.jsonl --mode cycle_exact --out report.json`
Each JSONL record requires domain, cycle, kind, txn_id and payload.
Modes: cycle_exact (ordered event sequence), transaction_equivalent (multiset
of events with cycle ignored), partial_order (same ordered events per domain;
cross-domain interleaving ignored). The latter **does not prove** asynchronous
FIFO/CDC synchronizer correctness, legal causality, physical metastability
behavior, or synchronization latency; these need explicit invariants and CDC
checks. Transaction-level matching does not prove protocol timing.

## Synopsys job adapter
`python -m backends.synopsys_job --config <private-server-config> --server <id> --manifest reviewed-job.json --results <local-out> --approve-live`
Manifest: schema_version=1, job_id, stage=dc|pt|power, inputs (existing
local files with distinct basenames, including run_tcl), run_tcl,
tool_setup_reviewed=true, environment (reviewed variables), timeout_seconds.
Tcl must be explicitly reviewed, and include the proper RTL list, top, SDC,
Liberty, corners, plus correctly named tool-specific run command. The adapter
uploads only explicitly listed files, executes under an isolated directory,
captures exit status and log. A successful process is *not* sufficient for
PPA acceptance. Use report_parser, constraint coverage, source provenance,
netlist/macro checks, and an independent PPA gate. Tool license and technology
files must never be committed. Not yet tested against live Synopsys tools.

## Milestone limits
This increment provides a minimal executable DAG engine, trace comparator,
and gated SSH job runner. It does NOT provide true cycle CModel generation,
compiler lowering impact analysis, formal/CDC signoff, placement/routing,
full job queue/cancellation/restart, log-to-PPA acceptance, or complete SoC
design-space exploration. Those remain separate engineering milestones.
