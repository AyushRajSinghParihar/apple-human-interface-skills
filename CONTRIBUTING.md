# Contributing

Keep one primary topic procedure for each current English HIG article. A source
reference supplies facts; a procedure teaches an agent how to perform useful work.
The complete bundle is the installation unit.

## Change a topic

1. Read the affected source reference, platform qualifications, important tables
   and relevant visual explanation. Use current official implementation documents
   when code depends on an API rather than an experience decision.
2. Inspect the topic's frozen artifact case and the failure you intend to address.
   A new capability needs a concrete fixture, expected work product and
   source-specific acceptance criteria before extensive instruction authoring.
3. Update the procedure with a consequential decision, a usable output contract,
   a worked transformation, observable failure checks and conditional handoffs.
   Preserve the user's stack. Avoid generic checklists that fit unrelated topics.
4. Have an independent reviewer assess the seven instruction-quality gates:
   decision, artifact, transformation, verification, applicability, handoffs and
   distinctiveness. Record real judgments against current source/instruction/
   reference hashes. Do not approve your own authored instructions.
5. For behavior claims or consequential workflow changes, run relevant artifact
   cases through the installed client and independently assess their outputs.
   Preserve failures and reruns.
   Changing evidence bytes invalidates the old result; never refresh hashes just
   to turn a gate green.

Do not edit an article reference unnecessarily. If its source-backed guidance
changes, its article and affected media/supporting approvals need renewed review.
Changing a topic invalidates its behavioral result; changing routing or shared
inputs requires the corresponding routing and dependent-case checks again.

## Verify the change

```bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/hig.py check
.venv/bin/python scripts/hig.py check-skills --instructions-only
```

The first release gate checks source accounting and article/media provenance.
The second checks operational ownership, source-backed procedure review and
routing. Both run in CI. The optional `check-skills` command without
`--instructions-only` additionally requires independently graded behavioral
evidence; the extended study is incomplete. Neither deterministic gate judges
design quality by keyword matches. `--allow-pending` permits incomplete review
and is a development aid, not the publication check.

Use the evaluation runner's help for scoped or resumable executions. Cases run
from temporary installed copies, not the authoring checkout. Keep unrelated
personal skills and plugins disabled per process, retain session/file-read
provenance, and never publish authentication material. CI needs no model account;
it validates committed evidence identities and meaningful deterministic contracts.

Published command captures may redact unrelated personal `skills.config` paths.
Retain the original capture hash and identify the redaction; do not present the
public argument list as a verbatim executable replay. Recreate local paths and
process overrides when repeating a run. See the [publication method](docs/source-method.md#publication-boundary).

## Boundaries

Publish original guidance/code, source citations, inventories and actual review/
evaluation records. Keep raw Apple Markdown/DocC, downloaded assets, contact
sheets, environments and private caches ignored. Check the actual release archive.

Git clones and source archives distribute committed files, including required
hidden `.topics` directories. Untracked procedures and evidence do not ship merely
because local checks can read them. Stage intended package, tooling, documentation
and evidence files selectively; inspect the staged tree, then inspect an archive
of the candidate commit. Preserve the baseline commit in repository history for
the matched-control checks. Publish after source, instruction, archive and CI checks pass. Claim behavioral
acceptance only when its separate execution and grading checks pass.

Resource links and histories are reference-only; substantive coverage cannot be
replaced by links. Preserve inaccessible or ambiguous source records rather than
lowering the denominator. Historical sources, complete SDK/WWDC libraries, and
translated editions stay outside the current-English article denominator.

Report inspected code/specifications, client execution and actual device checks
separately. Do not infer native rendering, VoiceOver behavior, physical comfort or
haptics from a Linux artifact evaluation. An unexecuted check stays unexecuted.
