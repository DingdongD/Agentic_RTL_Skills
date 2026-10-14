# DC run walkthrough (template, not executed)

1. Read private remote profile and the project `design.json`.
2. Run `python scripts/remote_preflight.py --config configs/eda_servers.json --server synopsys-primary`. This checks executable discoverability only, not licenses.
3. Validate sources, RTL top and constraints. Stage only approved files into unique remote job directory.
4. Run qualified `templates/dc/run.tcl` using the site's DC version.
5. Inspect `check_design.rpt`, `references.rpt`, `area.rpt`, `violations.rpt` and `mapped.v`.
6. Report mapped area separately from macro area, and flag all unlinked/missing cells.

No general-purpose dispatcher has been validated here. Do not execute site-specific shell commands from untrusted JSON fields.
