#!/usr/bin/env python3
"""Rewrite the traffic table in README.md from GitHub's traffic API.

The badges are static shields URLs with the numbers baked in, because the
dynamic download badges this page used before rendered "rate limited by
upstream service" on every request, and the pepy replacement returned the same
placeholder for every package. Static badges cannot break; this script is what
keeps them from going stale.

Needs a token with repo scope (traffic is owner-only). Run:
    GH_TOKEN=... python scripts/refresh_traffic.py
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import pathlib
import re
import urllib.request

OWNER = "GuoCheng24"
REPOS = ["worldmodel-from-scratch", "topocheck", "sciglyph", "scholarcheck", "docxaudit",
         "kakeya-conjecture-lab", "breakthrough-harness", "world-model-map",
         "ct-reconstruction-harness"]
PYPI = {"scholarcheck": "scholarcheck", "sciglyph": "sciglyph", "docxaudit": "docxaudit"}
ROOT = pathlib.Path(__file__).resolve().parents[1]


def api(path: str) -> dict:
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={"Authorization": f"Bearer {os.environ['GH_TOKEN']}",
                 "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def pypi_month(name: str) -> int | None:
    try:
        with urllib.request.urlopen(
                f"https://pypistats.org/api/packages/{name}/recent", timeout=30) as r:
            return json.load(r)["data"]["last_month"]
    except Exception:
        return None          # rate-limited or offline: fall back to a plain link


def badge(label: str, value: str, colour: str) -> str:
    q = lambda t: t.replace(" ", "%20").replace("-", "--").replace("/", "%2F")
    return f"![](https://img.shields.io/badge/{q(label)}-{q(value)}-{colour})"


def main() -> int:
    rows = []
    for name in REPOS:
        t = api(f"/repos/{OWNER}/{name}/traffic/clones")
        rows.append((name, t["count"], t["uniques"]))
    rows.sort(key=lambda r: -r[1])

    out = ["| Repository | Clones · unique people (14 d to DATE) | PyPI |", "|---|---|---|"]
    for name, count, uniques in rows:
        link = f"[{name}](https://github.com/{OWNER}/{name})"
        cell = (f"{badge('clones', str(count), '1f6feb')} {badge('people', str(uniques), '555')}"
                if count else "*too new to have traffic*")
        if name in PYPI:
            n = pypi_month(PYPI[name])
            p = (badge("PyPI", f"{n}/month", "0b6e4f") if n
                 else f"[on PyPI](https://pypistats.org/packages/{PYPI[name]})")
        else:
            p = "—"
        out.append(f"| {link} | {cell} | {p} |")

    today = _dt.date.today().isoformat()
    table = "\n".join(out).replace("14 d to DATE", f"14 d to {today}")
    readme = ROOT / "README.md"
    s = readme.read_text(encoding="utf-8")
    s = re.sub(r"\| Repository \| Clones[^\n]*\n\|---\|---\|---\|\n(?:\|[^\n]*\n)+",
               table + "\n", s, count=1)
    s = re.sub(r"over the fourteen days to \d{4}-\d{2}-\d{2}",
               f"over the fourteen days to {today}", s)
    readme.write_text(s, encoding="utf-8")
    print(f"refreshed {len(rows)} repositories on {today}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
