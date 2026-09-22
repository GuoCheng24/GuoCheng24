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
        # This page once quoted taichu's "82.0% [73.3, 88.3] contains 84.50" as a reproduction,
        # then over-corrected and quoted one adjusted estimate as if it were the estimate. The
        # subsample is a uniform random draw, so several estimators of the full-set accuracy are
        # legitimate and they disagree by five points; the row quotes the span and the tightest.
        "repo": "taichu-eval-reproduction",
        "path": "results/representativeness.json",
        "checks": [
            ("cvbench.estimators.difference.value", 88.45, 2),
            ("cvbench.estimators.direct.value", 89.33, 2),
            ("mathvista.estimators.difference.value", 77.20, 2),
            ("mathvista.estimators.direct.value", 82.00, 2),
            ("mathvista.estimators.regression.value", 79.75, 2),
            ("mathvista.estimators.regression.ci", [73.6, 85.9], None),
        ],
        "derived": [],
    },
    {
        # doubleblind's row quotes counts over its own ledger, and a ledger grows
        # while the prose about it does not. Both files live in that repository,
        # so this checks across the boundary the way the rows above do.
        "repo": "doubleblind",
        "path": "ledger/findings.json",
        "checks": [
            ("context.fresh_eyes_run_1.guard_checks_before", 37, None,
             "already passed **{}** mechanical checks"),
            ("context.fresh_eyes_run_1.findings_verified", 5, None,
             "of the **{}** that survived verification"),
        ],
        "derived": [
            ("defects recorded in the ledger",
             lambda d: len(d["findings"]), 20, None, "ledger of **{}** real defects"),
            ("verified fresh-eyes findings that were correct numbers in false sentences",
             lambda d: sum(1 for f in d["findings"]
                           if f.get("source") == "fresh-eyes-run-1"
                           and f["category"] == "correct-number-false-sentence"), 4, None,
             "findings; **{}** of the"),
        ],
    },
    {
        # groundwork's row quotes counts over its own archive and skill tree; both
        # grow while the prose about them does not.
        "repo": "groundwork",
        "path": "archive/causes-of-death.json",
        "checks": [],
        "derived": [
            ("ways a direction dies", lambda d: len(d["causes"]), 10, None,
             "archive of **{}** ways a"),
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


README = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "README.md")


def _pad(t, n):
    """A check may end with an optional phrase the number must sit in; pad when it does not.

    `checks` rows are (path, quoted, places[, near]) and `derived` rows are
    (label, fn, quoted, places[, near]), so the target length differs and is
    passed in rather than guessed from what happens to be there.
    """
    if len(t) == n:
        return t
    if len(t) == n - 1:
        return (*t, None)
    raise ValueError(f"check row has {len(t)} fields, expected {n - 1} or {n}: {t!r}")


def on_page(quoted, readme, places=None, near=None):
    """Is the figure, as this table writes it, actually on the page?

    Until this existed the loop compared the table above against the repository and never
    opened README.md, so the page could say 88.40 while the table said 88.45 and both the
    repository and the check agreed with the table. A number is matched with digit boundaries
    ("5.33" must not be satisfied by "15.33"); a list is matched as the page writes it.
    """
    import re
    if isinstance(quoted, list):
        return f"[{', '.join(str(x) for x in quoted)}]" in readme
    # written at the precision the table declares: 77.20 is "77.20" on the page, not "77.2"
    text = f"{quoted:.{places}f}" if places is not None and isinstance(quoted, float) else str(quoted)
    # A small whole number is on almost every page somewhere. Deleting "a ledger
    # of 19 real defects" left on_page(19) true, because 19 appears elsewhere -
    # so a check may name the phrase the number has to sit in, and then only
    # that occurrence counts.
    if near is not None:
        return re.search(re.escape(near).replace(re.escape("{}"), re.escape(text)),
                         readme) is not None
    return re.search(r"(?<![\d.])" + re.escape(text) + r"(?![\d])", readme) is not None


def main() -> int:
    failures = []
    with open(README, encoding="utf-8") as fh:
        readme = fh.read()
    for entry in QUOTED:
        url = RAW.format(repo=entry["repo"], path=entry["path"])
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                data = json.load(r)
        except Exception as exc:                       # noqa: BLE001
            print(f"  {entry['repo']}: could not fetch {entry['path']}: {exc}")
            return 0 if os.environ.get("ALLOW_OFFLINE") else 1
        for path, quoted, places, near in (_pad(t, 4) for t in entry["checks"]):
            actual = dig(data, path)
            got = round(actual, places) if places is not None else actual
            ok = got == quoted and on_page(quoted, readme, places, near)
            state = "ok" if ok else ("MISMATCH" if got != quoted else "NOT ON PAGE")
            print(f"  {entry['repo']}  {path:<44} page {quoted}  repo {got}  {state}")
            if not ok:
                failures.append(f"{entry['repo']}.{path}: table says {quoted}, repository says {got}, "
                                f"on page: {on_page(quoted, readme, places, near)}")
        for label, fn, quoted, places, near in (_pad(t, 5) for t in entry.get("derived", [])):
            got = round(fn(data), places)
            ok = got == quoted and on_page(quoted, readme, places, near)
            state = "ok" if ok else ("MISMATCH" if got != quoted else "NOT ON PAGE")
            print(f"  {entry['repo']}  {label:<44} page {quoted}  repo {got}  {state}")
            if not ok:
                failures.append(f"{entry['repo']}: {label}: table says {quoted}, repository says {got}, "
                                f"on page: {on_page(quoted, readme, places, near)}")
    if failures:
        print("\n" + "\n".join(failures))
        return 1
    print("every quoted number matches the repository it came from")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
