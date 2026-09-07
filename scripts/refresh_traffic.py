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

import collections
import datetime as _dt
import json
import os
import pathlib
import re
import urllib.request

OWNER = "GuoCheng24"
REPOS = ["worldmodel-from-scratch", "topocheck", "sciglyph", "scholarcheck", "docxaudit",
         "kakeya-conjecture-lab", "breakthrough-harness", "world-model-map",
         "ct-reconstruction-harness", "ifeval-reproduction"]
PYPI = {"scholarcheck": "scholarcheck", "sciglyph": "sciglyph", "docxaudit": "docxaudit"}
ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = "https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json"
RAW = "https://raw.githubusercontent.com/GuoCheng24/GuoCheng24/main/data/traffic.json"


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


def mark_stale() -> int:
    """No token: say when the numbers were last verified rather than let them rot quietly."""
    readme = ROOT / "README.md"
    s = readme.read_text(encoding="utf-8")
    note = ("\n*Last verified against the API on the date above; this page could not re-check them "
            "today because no traffic token is configured.*\n")
    marker = "*Last verified against the API"
    if marker not in s:
        s = s.replace("\n### How I work", note + "\n### How I work", 1)
        readme.write_text(s, encoding="utf-8")
        print("marked the table as unverified")
    return 0



def dyn(query: str, label: str, colour: str) -> str:
    """A live shields query against the committed file, not a number baked into a URL."""
    import urllib.parse as _u
    return (f"https://img.shields.io/badge/dynamic/json?url={_u.quote(RAW, safe='')}"
            f"&query={_u.quote(query, safe='')}&label={_u.quote(label)}&color={colour}")

def main() -> int:
    if "--mark-stale" in os.sys.argv:
        return mark_stale()

    # GitHub counts an Actions checkout as a clone, so raw totals include this
    # account's own CI - on the first version of this page that was 13-56% of
    # every repository's traffic. Days with no workflow run in that repository
    # are the closest available estimate of outside interest.
    snapshot = {"recorded": _dt.date.today().isoformat(),
                "source": "GET /repos/%s/{repo}/traffic/clones - visible only to the repository owner" % OWNER,
                "window": "the 14 days ending on the recorded date",
                "caveat": ("Raw totals include this account's own CI checkouts. 'ci_free' restricts "
                           "to days on which no workflow ran in that repository."),
                "repos": {}, "pypi": {},
                "pypi_source": "GET https://pypistats.org/api/packages/{pkg}/recent - public, anyone can re-run it"}
    hist_path0 = ROOT / "data" / "traffic.json"
    prev_pypi = {}
    if hist_path0.exists():
        _h = json.loads(hist_path0.read_text())
        if _h:
            prev_pypi = _h[-1].get("pypi", {})

    rows = []
    for name in REPOS:
        t = api(f"/repos/{OWNER}/{name}/traffic/clones")
        runs = api(f"/repos/{OWNER}/{name}/actions/runs?per_page=100").get("workflow_runs", [])
        ci_days = collections.Counter(r["created_at"][:10] for r in runs)
        daily = [{"t": d["timestamp"][:10], "c": d["count"], "u": d["uniques"],
                  "ci_runs": ci_days.get(d["timestamp"][:10], 0)} for d in t.get("clones", [])]
        clean = [d for d in daily if d["ci_runs"] == 0]
        clean_u = sum(d["u"] for d in clean)
        rows.append((name, t.get("count", 0), t.get("uniques", 0), clean_u))
        snapshot["repos"][name] = {
            "count": t.get("count", 0), "uniques": t.get("uniques", 0),
            "ci_free": {"days": len(clean), "clones": sum(d["c"] for d in clean), "uniques": clean_u},
            "daily": daily}
        if name in PYPI:
            # pypistats rate-limits aggressively. A miss must not silently drop the
            # package from the file, because the badge then renders "no result" -
            # which is exactly the failure mode the static badges were replaced to
            # avoid. Carry the previous value forward and record when it was taken.
            n = pypi_month(PYPI[name])
            if n:
                snapshot["pypi"][name] = {"last_month": n, "as_of": snapshot["recorded"]}
            elif prev_pypi.get(name):
                snapshot["pypi"][name] = prev_pypi[name]
                print(f"  {name}: pypistats rate-limited, carrying forward "
                      f"{prev_pypi[name]['last_month']} from {prev_pypi[name].get('as_of','?')}")

    hist_path = ROOT / "data" / "traffic.json"
    hist_path.parent.mkdir(exist_ok=True)
    hist = json.loads(hist_path.read_text()) if hist_path.exists() else []
    if hist and hist[-1]["recorded"] == snapshot["recorded"]:
        hist[-1] = snapshot
    else:
        hist.append(snapshot)
    hist_path.write_text(json.dumps(hist, indent=1, ensure_ascii=False) + "\n")

    rows.sort(key=lambda r: -r[3])
    today = _dt.date.today().isoformat()
    out = [f"| Repository | People who cloned it, CI excluded ({today}) | Raw total | PyPI / month |",
           "|---|---|---|---|"]
    for name, count, uniques, clean_u in rows:
        repo_link = f"[{name}](https://github.com/{OWNER}/{name})"
        if count == 0:
            cell, raw = "*too new to have traffic*", "—"
        else:
            cell = f"[![]({dyn(f'$[-1:].repos.{name}.ci_free.uniques', 'people', '1f6feb')})]({DATA})"
            raw = f"[![]({dyn(f'$[-1:].repos.{name}.uniques', 'incl. CI', '555')})]({DATA})"
        pcell = (f"[![]({dyn(f'$[-1:].pypi.{name}.last_month', 'PyPI/month', '0b6e4f')})]"
                 f"(https://pypistats.org/packages/{PYPI[name]})" if name in PYPI else "—")
        out.append(f"| {repo_link} | {cell} | {raw} | {pcell} |")
    table = "\n".join(out)

    readme = ROOT / "README.md"
    body = readme.read_text(encoding="utf-8").split("\n")
    try:
        a = next(k for k, l in enumerate(body) if l.startswith("| Repository |"))
    except StopIteration:
        raise SystemExit("traffic table header not found in README.md")
    b = a
    while b < len(body) and body[b].startswith("|"):
        b += 1
    readme.write_text("\n".join(body[:a] + table.split("\n") + body[b:]), encoding="utf-8")
    print(f"refreshed {len(rows)} repositories on {today}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
