#!/usr/bin/env python3
"""Numbers this page quotes about a repository must match that repository's results.

This page once advertised "FBP 31.05 ... TGV at 34.51 held out, against a published
34.41" for ct-reconstruction-harness on the same day that repository's README
withdrew those numbers: they were means over the first 16 of 3553 test images,
which run 0.8 dB easy. A reader clicking through found the repo disowning what the
page claimed. Nothing checked across the boundary, so it survived.

Every entry below names a repository, the raw URL of a results file it commits, and
the (json path -> value) pairs this page quotes from it. A quoted number that no
longer matches, to the precision it is written at, fails.

    python scripts/check_quoted_numbers.py
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request

RAW = "https://raw.githubusercontent.com/GuoCheng24/{repo}/main/{path}"

QUOTED = [
    {
        "repo": "ct-reconstruction-harness",
        "path": "results/evaluation_n128.json",
        "checks": [
            ("tv_aniso_official_recipe.psnr_mean", 33.00, 2),
            ("tv_aniso_official_recipe.psnr_se", 0.33, 2),
            ("paired.tgv_minus_tv_aniso.mean", 0.70, 2),
            ("paired.tgv_minus_tv_aniso.se", 0.04, 2),
            ("paired.tgv_minus_tv_aniso.wins", 125, None),
            ("paired.tgv_minus_tv_aniso.n", 128, None),
            ("published_challenge_set.TV", 33.36, 2),
        ],
    },
]


def dig(d, path):
    for k in path.split("."):
        d = d[k]
    return d


def main() -> int:
    failures = []
    for entry in QUOTED:
        url = RAW.format(repo=entry["repo"], path=entry["path"])
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                data = json.load(r)
        except Exception as exc:                       # noqa: BLE001
            print(f"  {entry['repo']}: could not fetch {entry['path']}: {exc}")
            return 0 if os.environ.get("ALLOW_OFFLINE") else 1
        for path, quoted, places in entry["checks"]:
            actual = dig(data, path)
            got = round(actual, places) if places is not None else actual
            ok = got == quoted
            print(f"  {entry['repo']}  {path:<44} page {quoted}  repo {got}  {'ok' if ok else 'MISMATCH'}")
            if not ok:
                failures.append(f"{entry['repo']}.{path}: page says {quoted}, repository says {got}")
    if failures:
        print("\n" + "\n".join(failures))
        return 1
    print("every quoted number matches the repository it came from")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
