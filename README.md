## Guo Cheng

Medical imaging, inverse problems, and the evaluation of AI systems. I work at both ends — the
applied mathematics and the code that checks whether it survived contact with data. Most of what is public here is a
harness: something built to prove its own headline number wrong, which says so in the README
when it succeeds. The methods work sits mainly in unreleased repositories; what you can read
below is the part I can show.

Recent examples of that working: on TopCoW a *random* assignment of fragments cut the break rate as much
as the repairs I had built, so [topocheck](https://github.com/GuoCheng24/topocheck) ships that baseline as
one of its five checks — if your repair does not beat random, it prints `beats random: False`;
and a reproduction of an official CT pipeline needed seven undocumented layers before its number
matched, each one written down in
[DEBUGGING.md](https://github.com/GuoCheng24/ct-reconstruction-harness/blob/main/DEBUGGING.md).

### Contributions to other people's projects

Found by reading someone else's source, each submitted with a reproduction and a before/after
table. Four of the pull requests are merged; the two entries in vLLM are a question and a
measurement, and they have so far produced two fix pull requests written by other people.

Most of them are one defect. A system keeps running while a number inside it quietly stops
meaning what it says: a leakage guard that compares floats with `==`, so the 117 lines behind it
never execute; an aborted request whose tokens land in one family of counters and not the other,
so two billing gateways disagree by exactly the prefill a client abandoned; a regression gate
whose tolerance sits 8.9 standard errors below its own baseline, so a five-point accuracy drop
passes it 99.5% of the time. Nothing raises, nothing is red, and the number is wrong. That is
also what the repositories below are built to catch, which is why I keep finding it.

| Where | What | Status |
|---|---|---|
| [vllm-project/vllm](https://github.com/vllm-project/vllm) — the inference engine most open LLM serving runs on, 91k stars | [#55634](https://github.com/vllm-project/vllm/issues/55634) an aborted request adds its prefill to `vllm:prompt_tokens_total` — +3010 across five client-side aborts — while every per-request histogram and the success counter stay at exactly zero, so a gateway billing from one family and a gateway billing from the other disagree by the whole prefill of every abandoned request. Traced to `OutputProcessor.abort_requests()` never reaching `_update_stats_from_finished()`; reproduced twice three days apart, then again on v0.28.0 · [#34333](https://github.com/vllm-project/vllm/issues/34333) measured what vLLM's own GSM8K regression gate can detect. Across the 53 shipped configs the one-sided tolerance sits **8.9 binomial standard errors** below its own baseline: median power against a true five-point regression is **0.54%**, and 43 of the 53 are under 5%. A paired McNemar test against a pinned reference reaches ~97% at three points on the same GPU time, and `_score_gsm8k` already computes the per-item vector before discarding it — [script and per-config output](https://gist.github.com/GuoCheng24/c31d9c5c98794dc69415f0b160ba41e1) | **two contributors opened fixes the next day** ([#55837](https://github.com/vllm-project/vllm/pull/55837), [#55940](https://github.com/vllm-project/vllm/pull/55940) +209/−50 across six files, open); the RFC is open |
| [odlgroup/odl](https://github.com/odlgroup/odl) — operator discretization library, 433 stars, shipping 1.0 | [#1730](https://github.com/odlgroup/odl/pull/1730) ASTRA's non-vector `parallel` geometry has no slot for a detector position, so in 2d parallel beam a shifted detector was silently discarded — [issue #359](https://github.com/odlgroup/odl/issues/359), open since 2016, and by now the CUDA and CPU backends disagreed on the same geometry with no warning. Found by a guard that requires every mismatch axis to change the sinogram; it changed it by exactly 0.0. Regression test fails on the unpatched code with the two sinograms bit-identical | open, maintainer review addressed |
| [InternScience/MLEvolve](https://github.com/InternScience/MLEvolve) — the agent that competes on MLE-bench | [#8](https://github.com/InternScience/MLEvolve/pull/8) a data-leakage guard, on by default, compared floats with `==` — so the 117 lines behind it had never once run · [#9](https://github.com/InternScience/MLEvolve/pull/9) the memory block sorted minimise-metrics backwards, so the model was shown the worst sibling and told it was the best | **both merged**, and now [third contributor](https://github.com/InternScience/MLEvolve/graphs/contributors) |
| [github/awesome-copilot](https://github.com/github/awesome-copilot) — GitHub's own collection | [#2854](https://github.com/github/awesome-copilot/pull/2854) [`research-harness-engineer`](https://github.com/github/awesome-copilot/blob/main/agents/research-harness-engineer.agent.md), an agent definition for running research as a falsification loop · [#2938](https://github.com/github/awesome-copilot/pull/2938) one row of their contributor table carried eight cells at `width="14.28%"` each, so the last avatar overflowed the table and rendered narrower than the rest | **both merged**, and on the [contributor wall](https://github.com/github/awesome-copilot#contributors-) |
| [InternScience/InternAgent](https://github.com/InternScience/InternAgent) | [#27](https://github.com/InternScience/InternAgent/pull/27) a task was configured to *maximise* test-set MSE, so a worse error scored as progress and was rewarded. One character | open |
| [ResearAI/DeepScientist](https://github.com/ResearAI/DeepScientist) | [#110](https://github.com/ResearAI/DeepScientist/pull/110) `pytest` aborted collection on a clean checkout — 56 test files lost to one undeclared optional import, in a repository whose CONTRIBUTING tells you to run exactly that | open |


### Things I maintain

| Project | What it does, and the number it stands on |
|---|---|
| [breakthrough-harness](https://github.com/GuoCheng24/breakthrough-harness) | Make a research agent hard to fool. Adapters for nine stacks; every claim in the README is asserted by a test. Works with DeepSeek Harness with nothing to copy — its skill provider scans `.agents/skills`, which this repo already has. |
| [ct-reconstruction-harness](https://github.com/GuoCheng24/ct-reconstruction-harness) | Reproduce the LoDoPaB-CT baselines from scratch, then beat one with a paired test: the matched TV recipe is 33.00 ± 0.33 against a published 33.36, and a generate-and-select loop finds TGV ratio 0.3 at +0.70 ± 0.04 dB over it, paired on the same 128 held-out images, winning 125 of them. Its first table quoted the first 16 images, which run 0.9 dB easy for the iterative methods; the README now says so and withdraws the claim that rested on them. Every guard is run against a deliberately broken operator, and one of them found the ODL bug above. |
| [ifeval-reproduction](https://github.com/GuoCheng24/ifeval-reproduction) | Reproducing a published IFEval score on one shared GPU. Three arms and a pre-registration chain that CI re-hashes on every push. The third arm looked like an 11-point gain from thinking mode until the paired test showed the first arm scores the same on those same prompts — the subsample was easier. |
| [topocheck](https://github.com/GuoCheng24/topocheck) [![](https://img.shields.io/pypi/v/topocheck?label=PyPI&color=0b6e4f)](https://pypi.org/project/topocheck/) | Five checks for topology-aware segmentation claims — including the random-repair baseline that beat every learned repair I tried. |
| [scholarcheck](https://pypi.org/project/scholarcheck/) [![](https://img.shields.io/pypi/v/scholarcheck?label=PyPI&color=0b6e4f)](https://pypi.org/project/scholarcheck/) · [sciglyph](https://pypi.org/project/sciglyph/) [![](https://img.shields.io/pypi/v/sciglyph?label=PyPI&color=0b6e4f)](https://pypi.org/project/sciglyph/) · [docxaudit](https://pypi.org/project/docxaudit/) [![](https://img.shields.io/pypi/v/docxaudit?label=PyPI&color=0b6e4f)](https://pypi.org/project/docxaudit/) | On PyPI, and installed by people I have never met. Verify citations before a reviewer does; publication figures that check their own layout; find what a converter silently dropped. |
| [worldmodel-from-scratch](https://github.com/GuoCheng24/worldmodel-from-scratch) | Build a world model in an afternoon, then measure where it breaks. The README separates claims that hold on any machine from those that do not, and CI checks only the first kind. |
| [world-model-map](https://github.com/GuoCheng24/world-model-map) | A researcher's map of open-source world models — what each one actually claims, what its authors say it cannot do, and an evidence grade per entry. CI re-resolves every citation. |
| [kakeya-conjecture-lab](https://github.com/GuoCheng24/kakeya-conjecture-lab) | An interactive lab for the Kakeya conjecture. The dimension meter recomputes its own numbers in the test suite, so the page cannot drift from the mathematics. |

### Who actually uses this

Stars are a poor signal at this size. The number that does not depend on trusting me is on
PyPI: four packages, **about 2,200 installs a month between them**, and
[pypistats](https://pypistats.org/packages/scholarcheck) is public — go and look. Clone traffic
is below it because it needs a caveat first.

**A correction I had to make to my own table.** GitHub counts every Actions checkout as a clone,
and my CI runs on push. In the first version of this section, between 13% and 56% of each
repository's "clones" were my own workflows. On the day I caught it, `worldmodel-from-scratch`
showed 250 clones by 64 people, of which about 140 were CI; excluding them took that repository
from 64 people to **5**, and reordered the table completely. Those two numbers are from the first
snapshot and stay there — the table below moves as traffic accumulates, which is the point of
keeping every snapshot rather than a current figure. The first column now counts only days on
which **no workflow ran in that repository at all**, and the raw totals sit beside it so the size
of the correction is visible instead of asserted.

**You cannot re-run these yourself**, because the traffic endpoint is visible only to a repository's
owner. So the raw API response — every day, with that day's CI-run count — is committed to
[`data/traffic.json`](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json). Each badge is a live shields.io query against that file, not
a picture of a number, and [its history](https://github.com/GuoCheng24/GuoCheng24/commits/main/data/traffic.json)
shows the figures accumulating over time. The PyPI badges link to
[pypistats.org](https://pypistats.org/packages/scholarcheck), which is public: **those four numbers
you can check without me.**

| Repository | People who cloned it, CI excluded (2026-09-08) | Raw total | PyPI / month |
|---|---|---|---|
| [docxaudit](https://github.com/GuoCheng24/docxaudit) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.docxaudit.ci_free.uniques&label=people&color=1f6feb)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.docxaudit.uniques&label=incl.%20CI&color=555)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.pypi.docxaudit.last_month&label=PyPI/month&color=0b6e4f)](https://pypistats.org/packages/docxaudit) |
| [scholarcheck](https://github.com/GuoCheng24/scholarcheck) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.scholarcheck.ci_free.uniques&label=people&color=1f6feb)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.scholarcheck.uniques&label=incl.%20CI&color=555)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.pypi.scholarcheck.last_month&label=PyPI/month&color=0b6e4f)](https://pypistats.org/packages/scholarcheck) |
| [kakeya-conjecture-lab](https://github.com/GuoCheng24/kakeya-conjecture-lab) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.kakeya-conjecture-lab.ci_free.uniques&label=people&color=1f6feb)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.kakeya-conjecture-lab.uniques&label=incl.%20CI&color=555)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | — |
| [sciglyph](https://github.com/GuoCheng24/sciglyph) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.sciglyph.ci_free.uniques&label=people&color=1f6feb)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.sciglyph.uniques&label=incl.%20CI&color=555)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.pypi.sciglyph.last_month&label=PyPI/month&color=0b6e4f)](https://pypistats.org/packages/sciglyph) |
| [topocheck](https://github.com/GuoCheng24/topocheck) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.topocheck.ci_free.uniques&label=people&color=1f6feb)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.topocheck.uniques&label=incl.%20CI&color=555)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.pypi.topocheck.last_month&label=PyPI/month&color=0b6e4f)](https://pypistats.org/packages/topocheck) |
| [worldmodel-from-scratch](https://github.com/GuoCheng24/worldmodel-from-scratch) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.worldmodel-from-scratch.ci_free.uniques&label=people&color=1f6feb)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.worldmodel-from-scratch.uniques&label=incl.%20CI&color=555)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | — |
| [world-model-map](https://github.com/GuoCheng24/world-model-map) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.world-model-map.ci_free.uniques&label=people&color=1f6feb)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.world-model-map.uniques&label=incl.%20CI&color=555)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | — |
| [breakthrough-harness](https://github.com/GuoCheng24/breakthrough-harness) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.breakthrough-harness.ci_free.uniques&label=people&color=1f6feb)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.breakthrough-harness.uniques&label=incl.%20CI&color=555)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | — |
| [ifeval-reproduction](https://github.com/GuoCheng24/ifeval-reproduction) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.ifeval-reproduction.ci_free.uniques&label=people&color=1f6feb)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.ifeval-reproduction.uniques&label=incl.%20CI&color=555)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | — |
| [ct-reconstruction-harness](https://github.com/GuoCheng24/ct-reconstruction-harness) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.ct-reconstruction-harness.ci_free.uniques&label=people&color=1f6feb)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.ct-reconstruction-harness.uniques&label=incl.%20CI&color=555)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | — |

### Work that is not public yet

Most of the methods work is in unreleased repositories, because a paper or a filing is still open.
It is described only in outline: an idea in submission is easy to take and hard to get back. This
section exists so the public half of the page is not mistaken for the whole of it.

Four lines are open at the moment. Between them they cover guarantees for medical image
segmentation, what a pre-treatment image can and cannot establish about a treatment decision, image
synthesis for adaptive radiotherapy, and prognostic markers in functional imaging. One has a patent
filed against it; two are with reviewers; one is written and held.

What they have in common is the part I would rather be judged on than the individual results: each
began with a measured ceiling and a random baseline before any method was built, each carries a
shuffled or permuted control wherever one is definable, and each has a written record of the
attempts that did not survive those checks. Several lines were closed on exactly that basis, which
is why there are four here rather than a dozen.

Happy to go into any of it properly in a conversation.



### How I work

Numbers go to disk before sentences are written about them. Every guard is run against a
deliberately broken input and has to fail for the right reason before it counts. When a
result does not survive that, the repository says so — the honest number is more useful
than the flattering one.
