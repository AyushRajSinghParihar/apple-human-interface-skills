# Independent artifact grading

Each opaque directory contains a fresh ephemeral Codex grading session, its exact
prompt, client command, raw events and the grades it produced. A grading record
maps opaque submission IDs back to execution records **after** grading.

Public command captures may redact unrelated personal `skills.config` paths while
retaining the original capture hash. They document the launch configuration rather
than provide a verbatim executable argument list; a repeat needs local paths and
process overrides. See the [publication method](../../docs/source-method.md#publication-boundary).

The grader receives the task, fixture, rubric, actual artifacts and relevant
source guides in a temporary project. Candidate/control labels, run directory
names, topic procedures and execution traces are withheld. Artifact style can
still suggest its origin; this is label blinding, not a guarantee of complete
anonymity. Unrelated skills and plugins are disabled for that process.

Five axes score 0–2: task completion, HIG correctness, artifact usefulness,
conditions/accessibility, and evidence honesty. Candidate acceptance requires
at least8/10, no critical unsupported advice, no invented observations/high-severity
findings, and the case's required findings. Controls use the same rubric but
remain observations even when they fail.

Before a grade is attached, orchestration checks the grader's actual captured
reads of each supplied file, its reported artifact hashes, completed session,
and unchanged execution record. The attached grade binds that record and case
and links its grading transcript. Runtime routing is checked independently from
the original execution trace; a polished artifact cannot establish a missing read.

Development grading trials and pilot grades remain in the history. The final
suite inventory identifies which executions count toward release coverage;
grading sessions do not count as additional topic/stress/control executions.

To repeat a review, assemble an anonymous temporary project with `task.json`,
`artifacts/` and `source-guidance/` per submission, use the retained prompt and
recorded Codex version/model, and retain a new session and grade rather than
overwriting a result. Scores are agent judgments about artifacts, not native
Apple runtime or hardware certification.
