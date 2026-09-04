## Guo Cheng

Medical imaging, inverse problems, and the evaluation of AI systems. I work at both ends —
the applied mathematics (topology, distribution-free uncertainty, optimal transport) and the
code that checks whether it survived contact with data. Most of what is public here is a
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

### Who actually uses this

Stars are a poor signal at this size, so here is the traffic instead — unique cloners over
the fourteen days to 2026-09-04, straight from GitHub's traffic API:

| Repository | Clones (unique people) | PyPI installs / month |
|---|---|---|
| [worldmodel-from-scratch](https://github.com/GuoCheng24/worldmodel-from-scratch) | 250 (64) | — |
| [topocheck](https://github.com/GuoCheng24/topocheck) | 116 (41) | — |
| [sciglyph](https://github.com/GuoCheng24/sciglyph) | 106 (35) | [on PyPI](https://pypistats.org/packages/sciglyph) |
| [scholarcheck](https://github.com/GuoCheng24/scholarcheck) | 93 (29) | 568 |
| [docxaudit](https://github.com/GuoCheng24/docxaudit) | 88 (33) | [on PyPI](https://pypistats.org/packages/docxaudit) |
| [breakthrough-harness](https://github.com/GuoCheng24/breakthrough-harness) | 64 (35) | — |

Counted, not estimated. The numbers move, so treat the date as part of the claim.

### How I work

Numbers go to disk before sentences are written about them. Every guard is run against a
deliberately broken input and has to fail for the right reason before it counts. When a
result does not survive that, the repository says so — the honest number is more useful
than the flattering one.
