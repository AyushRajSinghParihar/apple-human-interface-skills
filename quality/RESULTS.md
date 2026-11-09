# Benchmark results

## v1.0, before the v1.1 changes (2026-11-09)

Codex CLI 0.166.0 with `gpt-6.1-sol` ran each case once and graded each
answer three times in a blind Codex session. See
[task summary](results/v1.0-before-task/SUMMARY.md) and
[trigger summary](results/v1.0-before-trigger/SUMMARY.md).

### Task quality: at the ceiling

| | With skill | Without skill |
|---|---:|---:|
| Mean score of 10 cases | 1.00 | 0.95 |

Only one case (t04, Mac alerts) had a difference, and that difference was a
missing list of acceptance checks, not missing HIG knowledge. The judge reasons
for the runs without the skill are correct: this model already knows these HIG
rules. So these cases cannot show what the skill adds for this model.

### Cost: the skill made each run larger

| Median for each task run | With skill | Without skill |
|---|---:|---:|
| Input tokens | 164,112 | 69,451 |
| Input tokens not from cache | 35,790 | 21,789 |
| Output tokens | 1,548 | 908 |
| Skill files read | 9.5 | 0 |

### Triggers: correct in this run

- 10 of 10 requests that must start the skill started it.
- 0 of 10 near misses started it.

An earlier smoke run of the same binary-size question did start the skill, so
the trigger result varies between runs.

### What this means

- For a strong model, the value of the skill is not shown by these cases. Its
  cost is clear: about 2.4 times the input tokens.
- The next changes must make the route cheaper, and the next cases must test
  what a model cannot know without the skill: rules newer than its training,
  exact numbers and platform-specific limits.
- One run for each case gives a coarse signal. Do not report a difference of
  one case as an improvement.
