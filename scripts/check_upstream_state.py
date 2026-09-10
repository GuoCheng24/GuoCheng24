#!/usr/bin/env python3
"""Claims this page makes about other people's repositories must match those repositories.

The contributions table says a pull request is merged, or open, or that an issue produced two
fixes. Those are statements about state that lives somewhere else and changes without warning:
a maintainer merges, a contributor's fix lands, an issue is closed as intended-behaviour. The
number-checker next to this one guards figures that come from a file I control; nothing guarded
the half of the page that describes what other people did with the work.

Every claim below names a repository, a number, whether it is an issue or a pull request, and
the state the page asserts. A claim that no longer holds fails, and the page has to be edited
rather than quietly becoming wrong.

    python scripts/check_upstream_state.py          # needs network; GITHUB_TOKEN raises the rate limit
    ALLOW_OFFLINE=1 python scripts/check_upstream_state.py
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://api.github.com/repos/{repo}/{kind}/{num}"

# (repo, number, issues|pulls, state the README asserts)
CLAIMS = [
    ("vllm-project/vllm", 55634, "issues", "open"),
    ("vllm-project/vllm", 55940, "pulls", "open"),
    ("vllm-project/vllm", 55837, "pulls", "closed"),
    ("vllm-project/vllm", 34333, "issues", "open"),
    ("odlgroup/odl", 1730, "pulls", "open"),
    ("odlgroup/odl", 359, "issues", "open"),
    ("InternScience/MLEvolve", 8, "pulls", "merged"),
    ("InternScience/MLEvolve", 9, "pulls", "merged"),
    ("github/awesome-copilot", 2854, "pulls", "merged"),
    ("github/awesome-copilot", 2938, "pulls", "merged"),
    ("InternScience/InternAgent", 27, "pulls", "open"),
    ("ResearAI/DeepScientist", 110, "pulls", "open"),
]

MERGED_CLAIMED_IN_PROSE = 4     # "Four of the pull requests are merged"


def fetch(url):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json",
                                               "User-Agent": "check-upstream-state"})
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def actual_state(repo, num, kind):
    d = fetch(API.format(repo=repo, kind=kind, num=num))
    if kind == "pulls" and d.get("merged_at"):
        return "merged"
    return d["state"]


def main() -> int:
    readme = " ".join(open(os.path.join(ROOT, "README.md"), encoding="utf-8").read().split())
    failures = []
    merged = 0
    for repo, num, kind, claimed in CLAIMS:
        try:
            got = actual_state(repo, num, kind)
        except urllib.error.HTTPError as exc:
            if exc.code in (403, 429) and not os.environ.get("GITHUB_TOKEN"):
                print(f"  rate-limited without a token at {repo}#{num}; "
                      f"{'skipping' if os.environ.get('ALLOW_OFFLINE') else 'failing'}")
                return 0 if os.environ.get("ALLOW_OFFLINE") else 1
            print(f"  {repo}#{num}: {exc}")
            return 0 if os.environ.get("ALLOW_OFFLINE") else 1
        except Exception as exc:                                   # noqa: BLE001
            print(f"  {repo}#{num}: could not fetch: {exc}")
            return 0 if os.environ.get("ALLOW_OFFLINE") else 1
        merged += got == "merged"
        ok = got == claimed
        print(f"  {repo}#{num:<6} page says {claimed:<7} upstream says {got:<7} {'ok' if ok else 'MISMATCH'}")
        if not ok:
            failures.append(f"{repo}#{num}: page says {claimed}, upstream says {got}")
        # the page must actually link what it claims
        if f"/{repo}/{'pull' if kind == 'pulls' else 'issues'}/{num}" not in readme:
            failures.append(f"{repo}#{num}: state is claimed but the page does not link it")

    print(f"\n  merged pull requests: {merged}; the prose says {MERGED_CLAIMED_IN_PROSE}")
    if merged != MERGED_CLAIMED_IN_PROSE:
        failures.append(f"prose says {MERGED_CLAIMED_IN_PROSE} merged, the table now has {merged}")
    word = {4: "Four", 5: "Five", 6: "Six", 7: "Seven"}.get(merged)
    if word and f"{word} of the pull requests are merged" not in readme:
        failures.append(f"the prose does not say '{word} of the pull requests are merged'")

    if failures:
        print("\n" + "\n".join(f"  the page no longer matches upstream: {f}" for f in failures))
        return 1
    print("  every claim about someone else's repository still holds")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
