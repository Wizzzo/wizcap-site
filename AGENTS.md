# AGENTS.md — WizCap site (wizcap-site)

> Source of truth for any AI agent. Keep it short.

## What this is
The public landing page and privacy policy for **WizCap**, a phone app that automatically transcribes videos, styles the captions and burns them in. App stores link to `privacy-policy.html`, so it must stay reachable at that exact path.

## Stack
Plain static HTML with inline CSS and no build step or JavaScript framework. It is served as static files (GitHub Pages or any web server).

## Commands
| Task | Command |
|---|---|
| Preview | `make dev` → http://localhost:8000 |
| Check (HTML parses, titles, local links) | `make ci` |

## Layout
- `index.html` — landing page (icon, one-line pitch, links)
- `privacy-policy.html` — privacy policy referenced by store listings
- `icon.png` — app icon
- `tools/check_site.py` — the CI check

## Rules
1. Keep pages dependency-free and fast: no external JS, no trackers, no web fonts.
2. Never rename or move `privacy-policy.html`.
3. Privacy policy changes must match what the app actually does (data collected, processing on-device vs cloud). Flag any uncertainty in the PR instead of guessing.
4. Keep text accessible: real headings, alt text on images, good contrast.
5. One ticket = one branch `ticket/<ID>-<slug>` = one PR; `make ci` must pass.
