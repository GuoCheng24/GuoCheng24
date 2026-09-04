## Guo Cheng

Medical-imaging AI, and the measurement discipline that decides whether a result is real.
Most of what I publish here is a harness: something that tries to prove its own headline
number wrong, and says so in the README when it succeeds.

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
| [scholarcheck](https://pypi.org/project/scholarcheck/) [![](https://img.shields.io/pypi/dm/scholarcheck?label=&color=555)](https://pypistats.org/packages/scholarcheck) · [sciglyph](https://pypi.org/project/sciglyph/) [![](https://img.shields.io/pypi/dm/sciglyph?label=&color=555)](https://pypistats.org/packages/sciglyph) · [docxaudit](https://pypi.org/project/docxaudit/) [![](https://img.shields.io/pypi/dm/docxaudit?label=&color=555)](https://pypistats.org/packages/docxaudit) | On PyPI, and installed by people I have never met. Verify citations before a reviewer does; publication figures that check their own layout; find what a converter silently dropped. |
| [worldmodel-from-scratch](https://github.com/GuoCheng24/worldmodel-from-scratch) | Build a world model in an afternoon, then measure where it breaks. The README separates claims that hold on any machine from those that do not, and CI checks only the first kind. |

### How I work

Numbers go to disk before sentences are written about them. Every guard is run against a
deliberately broken input and has to fail for the right reason before it counts. When a
result does not survive that, the repository says so — the honest number is more useful
than the flattering one.
