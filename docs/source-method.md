# Source and review method

## Reproducible discovery

The source corpus is current English Apple HIG. The primary navigator is
`https://developer.apple.com/tutorials/data/index/design--human-interface-guidelines`
(without a `.json` suffix). Pages expose structured DocC data under
`https://developer.apple.com/tutorials/data/design/human-interface-guidelines`.
Article JSON URLs append `/<slug>.json`; the root appends `.json` directly.
Public pages also advertise `.md` alternates.

These are observed first-party representations, not a guaranteed API contract.
The utility follows all in-HIG topic references and separately checks update
history for historical routes. Newly discovered unowned articles remain errors
until assigned; source failures cannot silently shrink the inventory.

The initial 2026-10-25 inventory contained 173 routes: 158 articles and 15
organizational pages. The navigator's modification date can lag individual article
changes, so freshness uses canonical content hashes for every page.

## Accounting is separate from review

`coverage/manifest.json` records source identity, retrieval state, family,
destination, canonical source hash, nested source units, headings, media uses,
external dependencies, and review status. Every guidance unit maps to its
containing source heading's same-named local HTML anchor; `overview` maps to the
article introduction. Repeated source anchors can consolidate equivalent summary
and detailed treatment in one local section.

Resource sections, related links, developer documentation, videos listed as
resources, and source change histories are metadata rather than substantive
article requirements. Their links remain inventoried. Embedded media within
guidance is accounted for independently of resource thumbnails.

The extractor walks tables, list items, notes, rows, columns, and tabs. Container
scope prevents a heading in one column or tab from misattributing its siblings.
Unknown typed content raises an extraction error.

An article approval binds the canonical source-document hash and the local
destination byte hash. A valid approval identifies the independent reviewer and
review evidence. A heading mapping or file count is not an approval. Media review
additionally records actual inspection method, fetched binary identity,
explanatory evidence, source occurrence IDs, and supporting-file hashes. Frozen
source representations identify appearance alternatives; approval must account
for those appearances as well as the primary asset. Reference metadata hashes
are explicitly distinct from media binary hashes.

## Maintenance commands

- `discover` fetches the navigator, current source graph, and update history,
  then writes a snapshot manifest. Raw data is cached under ignored `.cache/`.
  `--offline` rebuilds accounting from a previously fetched cache.
- `check` validates source accounting, package structure, local links and anchors,
  reachability from the root, and current independent approvals.
- `check --live` writes its comparison snapshot under `.cache/` and fails on
  additions, removals, failed retrievals, or content changes. It does not rewrite
  the tracked manifest or authored guidance.
- `check --allow-pending` permits explicitly pending semantic/media review during
  development; structural and source failures still fail. It is not a release gate.
- `report` regenerates `coverage/REPORT.md` from the recorded evidence, explicitly
  showing incomplete review.

The skill is file-only. Maintenance dependencies and source caches are never
required to consume a copied package. Live source retrieval should use bounded
concurrency and retry transient access failures without removing failed entries.

## Publication boundary

Publish original text, code, source citations, inventory metadata, and actual
review/evaluation evidence. Keep raw Apple source representations, media, tooling
environments, and analysis contact sheets ignored. Check both tracked files and
release archives before publication. MIT applies to original project material;
it does not relicense Apple documentation or assets.
