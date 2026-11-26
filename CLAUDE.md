@AGENTS.md

## Claude Code specifics
- Plan first for anything over ~30 lines: use plan mode, or the `planner` subagent.
- Delegate wide searches to the `scout` subagent and bulk edits to `implementer`, so the main context stays small.
- Before opening a PR, run the `reviewer` subagent on the diff.
- Skills in `.claude/skills/`: `spec`, `ticket-to-pr`, `ship`, `new-product`. Use them instead of improvising.
- Keep replies terse: no recaps of files you just wrote, no restating the plan.
