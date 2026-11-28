#!/usr/bin/env python3
"""Static-site check: every HTML file parses, has a <title>, and every local href/src exists."""
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.has_title = [], False

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.has_title = True
        for k, v in attrs:
            if k in ("href", "src") and v:
                self.refs.append(v)


def local_target(ref: str):
    u = urlparse(ref)
    if u.scheme or u.netloc or ref.startswith(("#", "mailto:", "tel:")):
        return None
    return u.path or None


errors = []
pages = sorted(p for p in ROOT.rglob("*.html") if ".git" not in p.parts)
for page in pages:
    c = Collector()
    c.feed(page.read_text(encoding="utf-8"))
    rel = page.relative_to(ROOT)
    if not c.has_title:
        errors.append(f"{rel}: missing <title>")
    for ref in c.refs:
        target = local_target(ref)
        if target and not (page.parent / target.lstrip("/") if not target.startswith("/") else ROOT / target.lstrip("/")).exists():
            errors.append(f"{rel}: broken link {ref}")

print("\n".join(errors) or f"ok: {len(pages)} pages")
sys.exit(1 if errors else 0)
