---
name: ship
description: Pre-release checklist and release notes. Use when asked to ship, release, deploy, cut a version or check if main is ready to go out.
---
1. `git log --oneline <last-tag>..HEAD` → group commits by type into release notes (Added / Changed / Fixed).
2. Check, and report each as ✅/❌ with one line:
   - `make ci` green on the release commit
   - `.env.example` lists every env var the code reads (`grep -rE "getenv|environ|process.env"`)
   - DB migrations present for every model change, and reversible
   - No secrets or debug flags in the diff (`DEBUG=True`, keys, tokens)
   - Dockerfile builds from pinned dependencies
   - Rollback path is known (previous image tag / revert commit)
3. If all ✅: propose the version bump (semver) and the tag command. Do not tag or deploy unless explicitly told to.
