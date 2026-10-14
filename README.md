# Agentic RTL Skills

Codex Agent Skills for evidence-driven RTL development, verification and ASIC PPA evaluation.

The workflow is inspired by [Booley](https://github.com/boldaxolotl/booley) (Apache-2.0), but this repository is an independent Skills/adapters collection, **not** a fork of Booley's IDE, MCP server or sandbox.

## Available Skills

| Skill | Capability |
| --- | --- |
| `rtl-development` | Implement RTL against an explicit hardware contract |
| `rtl-coding-standard` | Compiler_Codes-compatible RTL naming, style and file management |
| `rtl-simulation` | Icarus/Verilator or configured Booley simulation |
| `rtl-waveform-debug` | VCD/FST cycle and handshake diagnosis |
| `rtl-goal-loop` | Evidence-backed acceptance goals |
| `rtl-review` | Functional, numerical, timing and evidence review |
| `rtl-ppa` | Two-tier ASIC PPA: Yosys/OpenROAD quick checks and commercial EDA |
| `synopsys-dc` | Synthesis, mapped area, constraints and netlist evidence |
| `synopsys-pt-sta` | PrimeTime setup/hold, WNS/TNS and timing coverage |
| `synopsys-power` | PrimePower/PTPX power and SAIF activity coverage |
| `sram-macro-analysis` | SRAM compiler manifest, macro views and integration checks |

## Install in Codex

```bash
git clone https://github.com/DingdongD/Agentic_RTL_Skills.git
mkdir -p ~/.codex/skills
cp -r Agentic_RTL_Skills/skills/* ~/.codex/skills/
```

## Remote ASIC evaluation architecture

```text
Codex goal + RTL contract
        |
  lint / simulation / coverage           (project toolchain)
        |
  PPA backend selection
       /            \
Yosys/OpenROAD     SSH -> licensed EDA host
fast estimate             |
                 DC synthesis + mapped netlist
                           |
                     PrimeTime STA
                           |
                PrimePower/PTPX + SAIF
                           |
                   normalized evidence
                           |
                Agent diagnosis + repair
```

The open-source flow is valuable for fast iterations; **DC/PT/PTPX reports are technology-dependent and do not become physical signoff merely by using commercial tools**. Functional/code coverage belongs to a simulator such as VCS; PrimeTime's timing analysis coverage is a different metric.

### Configuration

- `configs/eda_servers.example.json`: remote host/tool references; use a **private** `configs/eda_servers.json` for real host addresses.
- `configs/design.example.json`: RTL top, file list, SDC, process corner, power/area goals.
- `configs/memory.macros.example.json`: SRAM module instances and corner-matched views.
- `templates/dc/run.tcl`, `templates/pt/run.tcl`, `templates/power/run.tcl`: starting Tcl templates requiring site-specific qualification.
- `adapters/ssh_runner.py`: key-based, strict-host-key SSH transport primitives.
- `adapters/memory_adapter.py`: macro manifest validation.
- `adapters/report_parser.py`: conservative extraction of a few report metrics.
- `skills/rtl-ppa/references/REMOTE_SYNOPSYS.md`: evidence and security requirements.

### Status and limits

**Implemented:** standalone Skill descriptions, sample JSON, SSH command transport primitives, Tcl template starting points and limited metric parsers.

**Not yet implemented or verified:** automatic staging/launch of a complete DC->PT->Power pipeline, VCS coverage ingestion, vendor-specific SRAM compiler invocation, full PDK/library validation, full PT/PTPX report schemas, activity-coverage enforcement, real licensed EDA execution and physical-design extraction. These are engineering extension points, **not** capabilities of the current release. Do not report PPA numbers until the actual remote job runs and its artifacts are verified.

## Security and reproducibility

Use SSH agent/key and previously verified host keys; never store passwords or license secrets in JSON. Do not upload proprietary PDK, Liberty/LEF, SRAM collaterals or private reports to this public repository. Runs should use isolated directories and retain configuration/source hashes, tool versions, reports and baseline/candidate identity. Do not allow a model to inject unreviewed shell/Tcl into a trusted EDA host.

## Attribution

Ideas adapted from [Booley](https://github.com/boldaxolotl/booley) (Apache-2.0, respective contributors). No source implementation has been copied. Original instructions and wrappers are maintained separately.
