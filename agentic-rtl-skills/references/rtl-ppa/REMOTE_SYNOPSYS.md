# Remote Synopsys evidence contract

Use Yosys/OpenROAD for fast lint/synthesis iterations; remote DC/PT/PTPX for technology-specific ASIC data. These tools produce different fidelity levels, so do not directly equate their area numbers.

1. Resolve the configured server, secure identity and tool versions.
2. Verify project paths and library permissions **on the remote machine**.
3. Stage immutable RTL/filelist/SDC snapshots to a unique remote run directory.
4. Record source commit/hash, top, corner, clock constraints and command version.
5. Run functional/RTL regressions before expensive synthesis.
6. Run DC and verify link, blackboxes and mapped netlist.
7. Run PT, audit check_timing and analysis coverage, then evaluate WNS/TNS.
8. Run PTPX only when configured, preserving SAIF provenance and activity coverage.
9. Integrate memory macro Liberty and account for macro area independently.
10. Normalize missing or inconclusive metrics to null; never silently pass goals.
11. Compare baseline/candidate only under the same library, clock, corner, tool and constraints.
12. Return logs, execution status, hashes, quantitative metrics and limitations.

`adapters/ssh_runner.py` is an SSH transport primitive only. Tcl files under `templates/` are starting templates requiring site-specific validation; this release **does not automatically submit licensed tool runs or guarantee remote preflight**.

Security: strict host-key checking; SSH agents or keys instead of stored passwords; no `StrictHostKeyChecking=no`; whitelist tool commands; do not treat user-supplied shell fragments as safe; do not upload PDK data to GitHub. Keep private configs outside tracked repository.
