# Agentic RTL Skills repository

Reusable Codex Skills for RTL verification and PPA workflows.

- Add a skill under `skills/<name>/SKILL.md` with frontmatter `name` and `description`; keep each self-contained.
- Respect the documented flow distinctions: simulation/code coverage, STA analysis coverage, mapped synthesis area, activity-aware power.
- Do not claim a tool ran unless command logs and evidence exist for the actual revision.
- Do not silently weaken design contracts, timing/area targets, corner conditions or numerical equivalence.
- Remote EDA execution is opt-in. Use strong SSH host-key verification and separate proprietary collateral from source control.
- Never store real server secrets, foundry libraries, generated SRAM macros or licensed binaries in this public repository.
- The Tcl templates are unqualified examples until tested against the target EDA version, licensed features and process libraries.
- Preserve provenance to Booley for the conceptual workflow; do not imply these skills implement Booley's MCP runtime.

- All generated/modified RTL should follow `skills/rtl-coding-standard/SKILL.md` and its Compiler_Codes reference conventions, including `rtl/hdl` organization, explicit `rtl/filelist` management and compatible module/port naming. Do not bulk-rename legacy RTL.
