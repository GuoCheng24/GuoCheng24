#!/usr/bin/env python3
"""Numbers this page quotes about a repository must match that repository's results.

This page once advertised "FBP 31.05 ... TGV at 34.51 held out, against a published
34.41" for ct-reconstruction-harness on the same day that repository's README
withdrew those numbers: they were means over the first 16 of 3553 test images,
which run 0.9 dB easy for the iterative methods. A reader clicking through found the
repo disowning what the page claimed. Nothing checked across the boundary, so it
survived.

Every entry below names a repository, the raw URL of a results file it commits, and
what this page quotes from it: either a json path and its value, or -- for a number
the page states but the results file only implies -- a small function of the file.
The second kind is how "0.9 dB easy" is checked, and it is the kind that drifts
unnoticed, because nothing about it looks like a number that came from anywhere.
A quoted number that no longer matches, to the precision it is written at, fails.

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
        # the sentence "vLLM's batch-invariant kernels shrink it (8.0% -> 7.1%, while changing
        # trainer precision goes to 3.7% in one step)" rested for days on a measurement that
        # lived only on the machine that ran it; it is committed now, so this page can check it.
        "repo": "batch-logprob-gap",
        "path": "results/kernel_arms.json",
        "checks": [],
        "derived": [
            ("batch-invariant off, against the bf16 trainer", lambda d: 100 * d["arms"]["BI0 vs bf16 b8"]["out"] / d["n_tokens"], 8.0, 1),
            ("batch-invariant on, against the bf16 trainer", lambda d: 100 * d["arms"]["BI1 vs bf16 b8"]["out"] / d["n_tokens"], 7.1, 1),
            ("batch-invariant off, against the fp32 trainer", lambda d: 100 * d["arms"]["BI0 vs fp32 b8"]["out"] / d["n_tokens"], 3.7, 1),
        ],
    },
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
        "derived": [
            # "the first 16 images run 0.9 dB easy" -- against the other 112 that
            # were evaluated, for each iterative method the page's sentence covers.
            (f"first sixteen easier than the rest, {m}", lambda d, m=m: (
                d[m]["first16_mean"]
                - (d[m]["n"] * d[m]["psnr_mean"] - 16 * d[m]["first16_mean"]) / (d[m]["n"] - 16)
            ), 0.9, 1)
            for m in ("tv_aniso_official_recipe", "tgv2_ratio0.3_gamma28")
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
        for label, fn, quoted, places in entry.get("derived", []):
            got = round(fn(data), places)
            ok = got == quoted
            print(f"  {entry['repo']}  {label:<44} page {quoted}  repo {got}  {'ok' if ok else 'MISMATCH'}")
            if not ok:
                failures.append(f"{entry['repo']}: {label}: page says {quoted}, repository says {got}")
    if failures:
        print("\n" + "\n".join(failures))
        return 1
    print("every quoted number matches the repository it came from")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
