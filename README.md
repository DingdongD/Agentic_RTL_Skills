# Agentic RTL Skills

**One Codex Skill:** `agentic-rtl-skills`. This repository packages the complete workflow from RTL creation through validation, PPA and review behind **one entrypoint**, rather than exposing 11 independent skills.

## Install

```bash
git clone https://github.com/DingdongD/Agentic_RTL_Skills.git
mkdir -p ~/.codex/skills
cp -r Agentic_RTL_Skills/agentic-rtl-skills ~/.codex/skills/
```

For existing installations, remove only the eleven **obsolete skill directories created by this repository** before copying (after confirming you have no personal changes in them):

```bash
# Confirm contents before deletion; do NOT delete ~/.codex/skills itself.
for name in rtl-development rtl-simulation rtl-waveform-debug rtl-ppa rtl-goal-loop rtl-review rtl-coding-standard synopsys-dc synopsys-pt-sta synopsys-power sram-macro-analysis; do
  echo "$HOME/.codex/skills/$name"
done
```

`agentic-rtl-skills/SKILL.md` is the sole discoverable entry. The former 11 skill instructions are now documentation under `agentic-rtl-skills/workflows/`, not 11 independently installed skills.

## Layout

```text
agentic-rtl-skills/
  SKILL.md                  # Single orchestrating entrypoint
  workflows/                # 11 internal discipline playbooks
  references/               # Worked examples and contracts
  templates/                # Compiler_Codes-compatible RTL + DC/PT/Power starters
  scripts/                  # Style checker and SSH preflight
  adapters/                 # Remote transport, parsers and memory manifest
  configs/                  # Example JSON only, not credentials
  tests/                    # Python smoke checks
```

The workflow is inspired by [Booley](https://github.com/boldaxolotl/booley) (Apache-2.0) and aligns stylistically with [Compiler_Codes](https://github.com/DingdongD/Compiler_Codes). Templates are independently authored educational examples, not copied proprietary RTL. Synopsys Tcl remains version/PDK-specific and **no complete licensed remote EDA automation is yet validated**. A passing style checker is not equivalent to Verilator lint, simulation, full coverage or signoff PPA.

## Validation

From the aggregated Skill root:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python scripts/rtl_style_check.py --root /path/to/project --filelist rtl/filelist/top.f
```

These commands are examples until exercised on an actual RTL project. Keep credentials, memory compiler output, PDK/Liberty/LEF and private EDA reports outside the public repository.
