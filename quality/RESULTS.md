# Benchmark results

All runs use Codex CLI 0.166.0 with `gpt-6.1-sol`. Each case ran once in each
arm, and a blind Codex session graded each answer three times. One run for each
case gives a coarse signal: do not report a difference of one case as an
improvement.

## v1.0 without web search (main result, 2026-11-09)

Web search was off and the shell sandbox had no network, so the arm without the
skill used only the model's own knowledge. See
[task summary](results/v1.0-task/SUMMARY.md) and
[trigger summary](results/v1.0-trigger/SUMMARY.md).

| 15 task cases | With skill | Without skill |
|---|---:|---:|
| Mean score | 0.93 | 0.83 |
| Median input tokens for each run | 97,469 | 12,935 |

- The skill was better in 4 cases (h12, h13, t04, t08) and worse in 1 (h14).
- Every "findings" grader passed in both arms. All failures were in the
  "nuance" graders, and most were about completeness: no acceptance checks, no
  subscription name, or no tap destination. So the skill mostly made answers
  more complete; the model already knew the main HIG rules, also for 2026 pages.
- h14 (Mac touch display): v1.0 does not have the 2026-10-28 touch rules, and
  the answer with the skill missed one of them.
- Triggers: 10 of 10 requests started the skill, and 2 of 10 near misses also
  started it (Fastlane and iOS binary size).

## v1.0 with web search (2026-11-09)

Codex has web search on by default. In these runs, both arms searched the web
and opened Apple's live HIG pages, so the arm without the skill also had the
current guidance. See [task](results/v1.0-web-task/SUMMARY.md),
[hard cases](results/v1.0-web-hard/SUMMARY.md) and
[triggers](results/v1.0-web-trigger/SUMMARY.md).

| | With skill | Without skill |
|---|---:|---:|
| Mean score of 10 task cases | 1.00 | 0.95 |
| Mean score of 5 hard cases | 0.90 | 0.70 |
| Median input tokens (10 task cases) | 164,112 | 69,451 |

Triggers with web search on: 10 of 10 started the skill, and 0 of 10 near misses
started it.

## What this means for v1.1

- Make the route cheaper. The skill used about 7.5 times the input tokens of a
  run without it, for a gain of 0.10 in the mean score.
- Keep the parts that make answers complete: the request modes, the acceptance
  checks and the evidence limits.
- Make the description narrower, so that build and tooling questions about iOS
  do not start the skill.
- Add the 2026-10-28 HIG changes (touch on a Mac).
