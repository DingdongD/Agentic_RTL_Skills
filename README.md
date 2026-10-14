# Agentic RTL Skills

Reusable [Codex Agent Skills](https://developers.openai.com/codex/skills) for evidence-driven RTL engineering.

Inspired by the [Booley](https://github.com/boldaxolotl/booley) agentic RTL workflow. These are **original, standalone workflow instructions**, not a copy of Booley's IDE, EDA backends, sandbox or MCP server.

## Skills

| Skill | Purpose |
| --- | --- |
| `rtl-development` | Implement RTL from a timing/interface contract |
| `rtl-simulation` | Run reproducible functional and cycle-level simulation |
| `rtl-waveform-debug` | Trace signal-level failures using VCD/FST |
| `rtl-ppa` | Compare RTL area and timing under controlled synthesis conditions |
| `rtl-goal-loop` | Iterate against immutable, evidence-backed acceptance goals |
| `rtl-review` | Independently review correctness, verification and PPA evidence |

Each directory contains a `SKILL.md` with Codex-compatible YAML frontmatter. Install by copying selected skill directories into `$CODEX_HOME/skills/` (normally `~/.codex/skills/`), or place them in your project's `.agents/skills/` if your Codex environment supports repository-local skills.

## Engineering contract

1. Capture interface and observable timing behavior **before modifying RTL**.
2. Identify top module, parameters, clock/reset, simulators and expected tests.
3. Keep baseline and candidate configurations identical except for the intentional change.
4. Never equate a successful tool exit with proven functional correctness without a test oracle.
5. Treat failure, timeout, missing tooling and inconclusive evidence differently.
6. Store command, tool versions, source revision, parameters, seed, logs and measured values.
7. Re-run relevant checks after each material code change; old evidence is stale.
8. Never invent synthesis measurements or claim cycle accuracy from non-cycle-accurate models.
9. Prefer worktrees or isolated branches; never force-push, delete evidence or bypass safeguards without explicit authorization.

## Optional tooling

This collection uses an **adapter model**: existing `booley flow sim/lint/synth` targets are preferred when properly configured; otherwise use the project's established Verilator/Icarus/Yosys/OpenROAD commands. The skills do not install or bundle these tools. Optional Booley integration requires a separately configured Booley environment; see upstream [setup](https://github.com/boldaxolotl/booley/blob/main/docs/user/SETUP.md) and [flow reference](https://github.com/boldaxolotl/booley/blob/main/docs/user/FLOW_REFERENCE.md).

## Provenance and license

Conceptual inspiration: Booley, copyright its respective contributors, Apache-2.0. Source: https://github.com/boldaxolotl/booley . No upstream source code is included in this extraction. The upstream license and attribution are linked rather than claiming this repository redistributes Booley itself.

This first release includes instruction-only skills. It makes **no claim of automated EDA validation** until run against an actual RTL project.
