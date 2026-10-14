# Agentic RTL Skills repository

This repository contains reusable Codex skills, not synthesized hardware.

- Each skill lives at `skills/<name>/SKILL.md` with YAML frontmatter containing `name` and `description`.
- Keep each skill self-contained and focused on one engineering activity.
- Commands in skills are examples unless clearly identified as actual tested commands.
- Separate functional, cycle, and PPA verification; never infer one from another.
- Do not claim results without executing the corresponding EDA tool.
- Never weaken a user's hardware specification or acceptance goal without consent.
- Keep upstream Booley attribution in README and do not copy its implementation without checking licensing and notices.
