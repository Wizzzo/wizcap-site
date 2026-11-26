#!/usr/bin/env python3
"""Tracker-agnostic ticket adapter. Stdlib only, so it runs anywhere.

  tracker.py get     --source jira --id ABC-12          # print ticket as markdown
  tracker.py comment --source youtrack --id APP-3 --text "PR: ..."

Sources and the env vars each needs:
  github    gh CLI auth (GH_TOKEN)
  jira      JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN   (Jira Cloud REST v3)
  youtrack  YOUTRACK_BASE_URL, YOUTRACK_TOKEN           (permanent token)
  linear    LINEAR_API_KEY

Add a tracker = add one get_<name>() and one comment_<name>().
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request


def _env(name: str) -> str:
    val = os.environ.get(name)
    if not val:
        sys.exit(f"missing env var {name}")
    return val


def _http(method: str, url: str, headers: dict, body: dict | None = None) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Accept", "application/json")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    for k, v in headers.items():
        req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read()
    return json.loads(raw) if raw else {}


def _md(tid: str, title: str, url: str, body: str) -> str:
    return f"# {tid} — {title}\n\nURL: {url}\n\n{body or '(no description)'}\n"


def adf_to_text(node) -> str:
    """Flatten Atlassian Document Format to plain text."""
    if node is None:
        return ""
    if isinstance(node, str):
        return node
    if node.get("type") == "text":
        return node.get("text", "")
    parts = [adf_to_text(c) for c in node.get("content", [])]
    sep = "\n" if node.get("type") in ("doc", "bulletList", "orderedList") else ""
    out = sep.join(parts)
    if node.get("type") in ("paragraph", "heading", "listItem", "codeBlock"):
        out += "\n"
    return out


# ---- GitHub -------------------------------------------------------------
def get_github(tid: str) -> str:
    raw = subprocess.check_output(
        ["gh", "issue", "view", tid, "--json", "number,title,body,url"]
    )
    d = json.loads(raw)
    return _md(f"#{d['number']}", d["title"], d["url"], d["body"])


def comment_github(tid: str, text: str) -> None:
    subprocess.check_call(["gh", "issue", "comment", tid, "--body", text])


# ---- Jira Cloud ---------------------------------------------------------
def _jira_headers() -> dict:
    tok = base64.b64encode(
        f"{_env('JIRA_EMAIL')}:{_env('JIRA_API_TOKEN')}".encode()
    ).decode()
    return {"Authorization": f"Basic {tok}"}


def get_jira(tid: str) -> str:
    base = _env("JIRA_BASE_URL").rstrip("/")
    key = urllib.parse.quote(tid)
    d = _http(
        "GET",
        f"{base}/rest/api/3/issue/{key}?fields=summary,description",
        _jira_headers(),
    )
    f = d["fields"]
    return _md(tid, f["summary"], f"{base}/browse/{tid}", adf_to_text(f.get("description")).strip())


def comment_jira(tid: str, text: str) -> None:
    base = _env("JIRA_BASE_URL").rstrip("/")
    body = {
        "body": {
            "type": "doc",
            "version": 1,
            "content": [{"type": "paragraph", "content": [{"type": "text", "text": text}]}],
        }
    }
    _http("POST", f"{base}/rest/api/3/issue/{urllib.parse.quote(tid)}/comment", _jira_headers(), body)


# ---- YouTrack -----------------------------------------------------------
def _yt() -> tuple[str, dict]:
    return _env("YOUTRACK_BASE_URL").rstrip("/"), {"Authorization": f"Bearer {_env('YOUTRACK_TOKEN')}"}


def get_youtrack(tid: str) -> str:
    base, h = _yt()
    d = _http("GET", f"{base}/api/issues/{urllib.parse.quote(tid)}?fields=idReadable,summary,description", h)
    return _md(d["idReadable"], d["summary"], f"{base}/issue/{d['idReadable']}", d.get("description") or "")


def comment_youtrack(tid: str, text: str) -> None:
    base, h = _yt()
    _http("POST", f"{base}/api/issues/{urllib.parse.quote(tid)}/comments", h, {"text": text})


# ---- Linear -------------------------------------------------------------
def _linear(query: str, variables: dict) -> dict:
    d = _http(
        "POST",
        "https://api.linear.app/graphql",
        {"Authorization": _env("LINEAR_API_KEY")},
        {"query": query, "variables": variables},
    )
    if d.get("errors"):
        sys.exit(f"linear error: {d['errors']}")
    return d["data"]


def get_linear(tid: str) -> str:
    q = "query($id:String!){issue(id:$id){id identifier title description url}}"
    i = _linear(q, {"id": tid})["issue"]
    return _md(i["identifier"], i["title"], i["url"], i.get("description") or "")


def comment_linear(tid: str, text: str) -> None:
    uuid = _linear("query($id:String!){issue(id:$id){id}}", {"id": tid})["issue"]["id"]
    m = "mutation($i:CommentCreateInput!){commentCreate(input:$i){success}}"
    _linear(m, {"i": {"issueId": uuid, "body": text}})


SOURCES = ("github", "jira", "youtrack", "linear")


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("get", "comment"):
        s = sub.add_parser(name)
        s.add_argument("--source", required=True, choices=SOURCES)
        s.add_argument("--id", required=True)
        if name == "comment":
            s.add_argument("--text", required=True)
    a = p.parse_args(argv)
    fn = globals()[f"{a.cmd}_{a.source}"]
    if a.cmd == "get":
        sys.stdout.write(fn(a.id))
    else:
        fn(a.id, a.text)


if __name__ == "__main__":
    main()
