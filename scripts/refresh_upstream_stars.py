#!/usr/bin/env python3
"""Keep the star counts in the contributions table current, or remove the claim.

The table said "91k stars" next to vLLM while the repository had 92,579, and
said nothing at all next to github/awesome-copilot, which has 39,339 and two
merged pull requests - the second-largest repository in the table, unlabelled.
Both are the same defect: a number about somebody else's repository, written by
hand, on a page that is otherwise checked.

Stars move every day, so this is not a check that fails. It is a rewrite that
runs daily alongside the traffic table, and the page is committed with whatever
it found. What it will not do is invent a figure: a repository it cannot reach
keeps the text that is already there, and says so.

    python scripts/refresh_upstream_stars.py            # rewrite in place
    python scripts/refresh_upstream_stars.py --check    # fail if anything moved
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")

# A table row opens with a link to the upstream repository and may carry a
# " — <something> stars" annotation, possibly followed by other notes.
ROW = re.compile(
    r"^(\| \[(?P<slug>[\w.-]+/[\w.-]+)\]\(https://github\.com/(?P=slug)\))"
    r"(?P<ann>[^|]*)",
    re.M)


def human(n):
    """39339 -> '39k'; 3334 -> '3.3k'; 443 -> '443'. Rounded down, never up:
    a star count that rounds up reads as a claim the repository has not met."""
    if n < 1000:
        return str(n)
    if n < 10_000:
        return f"{n // 100 / 10:.1f}k"
    return f"{n // 1000}k"


def stars(slug, token=None):
    """Over HTTP, or through the `gh` CLI where only that has a working path.

    Some machines reach GitHub only through a proxy that `gh` is configured for
    and urllib is not; on those, the direct request fails at DNS and the
    fallback is the difference between running and not.
    """
    req = urllib.request.Request(f"https://api.github.com/repos/{slug}",
                                 headers={"Accept": "application/vnd.github+json"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)["stargazers_count"]
    except (urllib.error.URLError, TimeoutError):
        import shutil
        import subprocess
        if not shutil.which("gh"):
            raise
        env = {**os.environ, "NO_PROXY": "", "no_proxy": ""}
        p = subprocess.run(["gh", "api", f"repos/{slug}", "--jq", ".stargazers_count"],
                           capture_output=True, text=True, timeout=60, env=env)
        if p.returncode != 0 or not p.stdout.strip().isdigit():
            raise
        return int(p.stdout.strip())


def main(argv):
    check = "--check" in argv
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    with open(README, encoding="utf-8") as fh:
        text = fh.read()

    moved, unreachable = [], []

    def rewrite(m):
        slug, ann = m.group("slug"), m.group("ann")
        try:
            n = stars(slug, token)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            unreachable.append(f"{slug}: {exc}")
            return m.group(0)
        label = f" — {human(n)} stars"
        # keep any note that is not the star count itself
        rest = re.sub(r"\s*—\s*[\d.,k]+\s*stars\s*", "", ann)
        rest = rest.strip().lstrip("—·").strip()
        new_ann = label + (f" · {rest}" if rest else "") + " "
        if new_ann != ann:
            moved.append(f"{slug}: {ann.strip()!r} -> {new_ann.strip()!r}")
        return m.group(1) + new_ann

    out = ROW.sub(rewrite, text)
    for line in moved:
        print(f"  {line}")
    for line in unreachable:
        print(f"  could not reach {line}")
    if unreachable and not moved:
        print("  nothing rewritten; the text already there is kept rather than guessed at")
    if check:
        if moved:
            print(f"\n{len(moved)} star count(s) have moved since this page was written")
            return 1
        print("every star count on the page matches its repository")
        return 0
    if moved:
        with open(README, "w", encoding="utf-8") as fh:
            fh.write(out)
        print(f"\nrewrote {len(moved)} row(s)")
    else:
        print("nothing to rewrite")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
