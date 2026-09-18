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
        # The two figures this page quotes from TRL #6789 come from one run that rescored the same
        # 3,916 tokens under each setting. It lived only on the machine that produced it until an
        # audit of this page asked where it was; the repository commits it now, so this can check it.
        "repo": "batch-logprob-gap",
        "path": "results/kernel_arms.json",
        "checks": [],
        "derived": [
            ("vLLM logprobs against the bf16 trainer",
             lambda d: 100 * d["arms"]["gen vs bf16 b8"]["out"] / d["n_tokens"], 7.5, 1),
            ("the trainer's own chunking, no engine",
             lambda d: 100 * d["arms"]["bf16 b1 vs b8"]["out"] / d["n_tokens"], 8.0, 1),
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
