---
name: spec
description: Write a feature spec in docs/specs/ from a ticket, idea or conversation. Use when asked to spec, scope or plan a feature, or before implementing anything without a spec.
---
1. Get the ticket ID (or make one: `F-<yyyymmdd>-<slug>`) and the raw request.
2. Have the `scout` subagent list the files and modules involved. Do not read the codebase yourself.
3. Copy `docs/specs/_TEMPLATE.md` to `docs/specs/<ID>-<slug>.md` and fill it in. Acceptance criteria must be testable; "Out of scope" must list at least one tempting extra.
4. If a decision has long-term impact (new dependency, data model, hosting), also add an ADR in `docs/decisions/`.
5. Reply with the spec path and the open questions only.
