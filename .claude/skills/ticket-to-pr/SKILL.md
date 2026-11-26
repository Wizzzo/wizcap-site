---
name: ticket-to-pr
description: Take one ticket (GitHub issue, Jira, YouTrack, Linear, or pasted text) all the way to a reviewed, CI-green pull request. Use whenever asked to work a ticket, issue or task end to end, including in CI runs.
---
Inputs: ticket ID, title, body, URL. In CI these arrive in the prompt.

1. **Branch**: `git switch -c ticket/<ID>-<short-slug>` from the default branch.
2. **Spec**: if `docs/specs/<ID>-*.md` is missing, run the `spec` skill. If the ticket is too vague to write testable acceptance criteria, stop: comment the questions on the ticket/issue and exit without code.
3. **Plan**: for changes over ~30 lines, get a step plan from the `planner` subagent.
4. **Build**: hand the plan to the `implementer` subagent. It must end with `make ci` passing.
5. **Review**: run the `reviewer` subagent. Fix every bug/security/missing-test finding, rerun `make ci`.
6. **Status**: update `docs/STATUS.md` (≤6 lines).
7. **Commit & PR**: conventional commit `<type>(<ID>): <summary>`, push, then
   `gh pr create --title "<ID>: <title>" --body "<what/why, acceptance criteria checklist, Closes <ticket URL or #N>>"`.
8. Reply with the PR URL and one line on anything left for a human.

Hard limits: never push to the default branch, never edit CI workflows or secrets, never merge.
