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

[![Contributor to github/awesome-copilot](https://img.shields.io/badge/contributor-github%2Fawesome--copilot-1f6feb?logo=github&logoColor=white)](https://github.com/github/awesome-copilot#contributors-)
[![agent definition](https://img.shields.io/badge/agent-research--harness--engineer-0b6e4f?logo=githubcopilot&logoColor=white)](https://github.com/github/awesome-copilot/blob/main/agents/research-harness-engineer.agent.md)


| Where | What | Status |
|---|---|---|
| [github/awesome-copilot](https://github.com/github/awesome-copilot) — GitHub's own collection, 38.6k stars | [`research-harness-engineer`](https://github.com/github/awesome-copilot/blob/main/agents/research-harness-engineer.agent.md), an agent definition for running research as a falsification loop | **merged**, and on the [contributor wall](https://github.com/github/awesome-copilot#contributors-) |
| [InternScience/MLEvolve](https://github.com/InternScience/MLEvolve) | [#8](https://github.com/InternScience/MLEvolve/pull/8) the data-leakage trigger compared floats with `==`, so a default-on guard never fired · [#9](https://github.com/InternScience/MLEvolve/pull/9) the memory block sorted minimise-metrics backwards, showing the model the worst sibling as the best | open |
| [ResearAI/DeepScientist](https://github.com/ResearAI/DeepScientist) | [#110](https://github.com/ResearAI/DeepScientist/pull/110) `pytest` aborted collection on a clean checkout — 56 test files lost to one undeclared optional import | open |
| [InternScience/InternAgent](https://github.com/InternScience/InternAgent) | [#27](https://github.com/InternScience/InternAgent/pull/27) a task was configured to *maximise* test-set MSE, so a worse error scored as progress | open |

Each of those came with a reproduction and a before/after table, not a hunch.

### Things I maintain

| Project | What it does, and the number it stands on |
|---|---|
| [breakthrough-harness](https://github.com/GuoCheng24/breakthrough-harness) | Make a research agent hard to fool. Adapters for nine stacks; every claim in the README is asserted by a test. Works with DeepSeek Harness with nothing to copy — its skill provider scans `.agents/skills`, which this repo already has. |
| [ct-reconstruction-harness](https://github.com/GuoCheng24/ct-reconstruction-harness) | Reproduce the LoDoPaB-CT baselines from scratch (FBP 31.05 vs official 30.19; TV-Adam 33.83 vs 33.36), then a generate-and-select loop finds TGV at 34.51 held out, against a published 34.41. Every guard is run against a deliberately broken operator. |
| [topocheck](https://github.com/GuoCheng24/topocheck) | Five checks for topology-aware segmentation claims — including the random-repair baseline that beat every learned repair I tried. |
| [scholarcheck](https://pypi.org/project/scholarcheck/) · [sciglyph](https://pypi.org/project/sciglyph/) · [docxaudit](https://pypi.org/project/docxaudit/) | On PyPI, and installed by people I have never met. Verify citations before a reviewer does; publication figures that check their own layout; find what a converter silently dropped. |
| [worldmodel-from-scratch](https://github.com/GuoCheng24/worldmodel-from-scratch) | Build a world model in an afternoon, then measure where it breaks. The README separates claims that hold on any machine from those that do not, and CI checks only the first kind. |
| [world-model-map](https://github.com/GuoCheng24/world-model-map) | A researcher's map of open-source world models — what each one actually claims, what its authors say it cannot do, and an evidence grade per entry. CI re-resolves every citation. |
| [kakeya-conjecture-lab](https://github.com/GuoCheng24/kakeya-conjecture-lab) | An interactive lab for the Kakeya conjecture. The dimension meter recomputes its own numbers in the test suite, so the page cannot drift from the mathematics. |

### Who actually uses this

Stars are a poor signal at this size, so here is clone traffic instead.

**A correction I had to make to my own table.** GitHub counts every Actions checkout as a clone, and
my CI runs on push. In the first version of this section, between 13% and 56% of each repository's
"clones" were my own workflows — `worldmodel-from-scratch` showed 250 clones by 64 people, of which
about 140 were CI. The first column now counts only days on which **no workflow ran in that
repository at all**. That reorders the table completely and cuts the largest figure from 64 people
to 5. The raw totals sit beside it so you can see the size of the correction instead of taking my
word for it.

**You cannot re-run these yourself**, because the traffic endpoint is visible only to a repository's
owner. So the raw API response — every day, with that day's CI-run count — is committed to
[`data/traffic.json`](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json). Each badge is a live shields.io query against that file, not
a picture of a number, and [its history](https://github.com/GuoCheng24/GuoCheng24/commits/main/data/traffic.json)
shows the figures accumulating over time. The PyPI badges link to
[pypistats.org](https://pypistats.org/packages/scholarcheck), which is public: **those three numbers
you can check without me.**

| Repository | People who cloned it, CI excluded (2026-09-04) | Raw total | PyPI / month |
|---|---|---|---|
| [docxaudit](https://github.com/GuoCheng24/docxaudit) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.docxaudit.ci_free.uniques&label=people&color=1f6feb)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.docxaudit.uniques&label=incl.%20CI&color=555)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.pypi.docxaudit.last_month&label=PyPI/month&color=0b6e4f)](https://pypistats.org/packages/docxaudit) |
| [scholarcheck](https://github.com/GuoCheng24/scholarcheck) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.scholarcheck.ci_free.uniques&label=people&color=1f6feb)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.scholarcheck.uniques&label=incl.%20CI&color=555)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.pypi.scholarcheck.last_month&label=PyPI/month&color=0b6e4f)](https://pypistats.org/packages/scholarcheck) |
| [kakeya-conjecture-lab](https://github.com/GuoCheng24/kakeya-conjecture-lab) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.kakeya-conjecture-lab.ci_free.uniques&label=people&color=1f6feb)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.kakeya-conjecture-lab.uniques&label=incl.%20CI&color=555)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | — |
| [sciglyph](https://github.com/GuoCheng24/sciglyph) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.sciglyph.ci_free.uniques&label=people&color=1f6feb)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.sciglyph.uniques&label=incl.%20CI&color=555)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.pypi.sciglyph.last_month&label=PyPI/month&color=0b6e4f)](https://pypistats.org/packages/sciglyph) |
| [world-model-map](https://github.com/GuoCheng24/world-model-map) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.world-model-map.ci_free.uniques&label=people&color=1f6feb)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.world-model-map.uniques&label=incl.%20CI&color=555)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | — |
| [topocheck](https://github.com/GuoCheng24/topocheck) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.topocheck.ci_free.uniques&label=people&color=1f6feb)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.topocheck.uniques&label=incl.%20CI&color=555)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | — |
| [worldmodel-from-scratch](https://github.com/GuoCheng24/worldmodel-from-scratch) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.worldmodel-from-scratch.ci_free.uniques&label=people&color=1f6feb)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.worldmodel-from-scratch.uniques&label=incl.%20CI&color=555)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | — |
| [breakthrough-harness](https://github.com/GuoCheng24/breakthrough-harness) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.breakthrough-harness.ci_free.uniques&label=people&color=1f6feb)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | [![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FGuoCheng24%2FGuoCheng24%2Fmain%2Fdata%2Ftraffic.json&query=%24%5B-1%3A%5D.repos.breakthrough-harness.uniques&label=incl.%20CI&color=555)](https://github.com/GuoCheng24/GuoCheng24/blob/main/data/traffic.json) | — |
| [ct-reconstruction-harness](https://github.com/GuoCheng24/ct-reconstruction-harness) | *too new to have traffic* | — | — |

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
