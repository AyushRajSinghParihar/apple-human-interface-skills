# Claude Code benchmark

This suite measures two things with `claude plugin eval`:

1. **Task quality** (`evals/task/`, tag `task`): 10 realistic requests. Each case
   has two `llm` graders with specific required findings, plus a `skill-fired`
   indicator. Two cases are for apps outside Apple platforms (a React web app
   and a WinUI 3 app).
2. **Triggers** (`evals/trigger/`, tag `trigger`): 10 requests that must start the
   skill and 10 near misses that must not start it.

The prompts never name the skill. The task cases adapt cases from `evals/cases`
(the older Codex suite) and add sharper required findings.

## Run

The script copies the skill and these cases into a temporary plugin folder, so
the eval cases do not ship with the installed skill.

```bash
# Task quality: each case runs once with the skill and once without it (20 runs).
scripts/claude-eval.sh LABEL-task --tag task --ablation with-without --runs 1 \
  --model sonnet --max-cost-usd <cap>

# Triggers: each case runs once with the skill (20 runs).
scripts/claude-eval.sh LABEL-trigger --tag trigger --ablation none --runs 1 \
  --model sonnet --max-cost-usd <cap>
```

Results go to `quality/results/LABEL-*/`. Commit `aggregate-result.json` and a
short `SUMMARY.md`. The HTML report stays local.

## Limits

One run for each case gives a coarse signal. A difference of one case can come
from chance, so do not report small differences as an improvement.
