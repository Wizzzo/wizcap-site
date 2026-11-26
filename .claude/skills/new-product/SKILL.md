---
name: new-product
description: Bootstrap a new product repo from the studio kit — AGENTS.md, specs, CI, Claude workflows, Makefile. Use when starting a new app, game, site or service, or when adopting the kit in an existing repo.
---
1. Ask only what you can't infer: product one-liner, target users, platform (web / mobile / API / game), and whether the repo already exists.
2. Copy from the studio kit: `AGENTS.md`, `CLAUDE.md`, `.claude/`, `docs/`, `.github/workflows/`, `Makefile.example` → `Makefile`, `scripts/tracker.py`.
3. Fill `AGENTS.md` for real: stack, commands, layout, rules, gotchas. Inspect the repo (via `scout`) rather than guessing. Stay under 120 lines.
4. Wire the Makefile targets (`setup dev lint format test ci`) to the stack's real tools. Add one smoke test so `make ci` proves something.
5. Write `docs/specs/MVP-001-<slug>.md`: the smallest version worth putting in front of a user.
6. Run `make ci`. Commit on branch `chore/studio-bootstrap`, open a PR.
7. Reply with: PR URL, the secrets the owner must add (`CLAUDE_CODE_OAUTH_TOKEN`, `STUDIO_GH_TOKEN`, tracker tokens), and the MVP spec path.
