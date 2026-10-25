# Independent coverage audit

Status: accepted for the dated current English HIG snapshot. All 158 article reviews and embedded media uses have current hash bindings. Independent strict verification has zero errors or pending items; 34 maintenance tests pass. The full live source/media comparison and installed-package trials are verified. No author mapping is an independent approval.

The audit target is the dated current English Human Interface Guidelines (HIG),
including substantive media guidance. Historical routes and external dependencies
are separate inventories. Completeness is assessed against the reproducible source
snapshot, rather than every page Apple may have published or left unlinked.

## Independent discovery baseline

On 2026-10-25 an independent read-only traversal of Apple's root, structural
children, and all in-HIG topic references fetched 173 canonical routes: 15 indexes
and 158 articles. All fetched successfully. The six top-level families contained
9 getting-started articles, 18 foundations, 25 patterns, 13 inputs, 29 technologies,
and eight component subgroup indexes containing 64 articles.

Sources:

- [HIG root](https://developer.apple.com/design/human-interface-guidelines)
- [Structured root](https://developer.apple.com/tutorials/data/design/human-interface-guidelines.json)
- [Markdown root](https://developer.apple.com/design/human-interface-guidelines.md)
- [Design update history](https://developer.apple.com/design/whats-new/)

The update history independently exposed four historical paths absent from the
173-route navigation closure. The public `/in-app-purchase` route redirects to
`/apple-in-app-purchase`; `/navigation-bars` redirects to `/toolbars`. The old JSON
routes return 404. `/messages-for-business` and `/touch-bar` returned 404 for both
public HTML and JSON. Resolve public redirects before constructing a data URL;
preserve unavailable historical entries without synthesizing their content.

The initial traversal counted 3,744 image reference records and 61 video references.
Resource thumbnails and unused references are not the embedded-content denominator.
The frozen article extraction accounts for 1,472 image occurrences (1,280 distinct
primary asset IDs), 933 image appearance alternatives, 61 distinct embedded video
sequences, and 20 video appearance alternatives. Decorative topic/section artwork
remains accounted for with a reasoned classification.

The 158 articles contain 1,740 heading entries, including resource/change-history
headings; 13,623 nested guidance units; and 178 guidance tables. Another 1,627
metadata units include 115 metadata tables. Nested container and child units overlap:
these figures measure extraction coverage, not independent design lessons.

## Review requirements

1. Freeze the source route, section, table, note, platform, and substantive-media
   unit inventory before reviewing guidance. Preserve source hierarchy and anchors.
   Unknown structured-content node types are extraction errors until classified.
2. Give every article one primary module owner. Secondary mappings do not increase
   the covered-source count. Account for indexes without treating their link cards
   as substantive article coverage.
3. Read each article against its local reference. For every substantive section,
   verify that the guidance preserves the source's decisions, conditions, important
   exceptions, and platform distinctions. A title, abstract, generic paragraph, or
   source link is insufficient. An author mapping only identifies a review target.
4. Check every specification table for preserved decision-relevant values, units,
   labels, exceptions, and platform scope. Verify quantitative claims against the
   corresponding source unit; do not infer platform support from missing headings.
5. Distinguish shared guidance, explicit platform differences, explicit
   nonapplicability, and unspecified applicability. Preserve all six platform entry
   articles and substantive platform sections elsewhere.
6. Classify media used by substantive content separately from navigation images
   and resource thumbnails. Inspect distinct guidance-bearing examples and
   materially different platform variants. Determine whether original prose fully
   explains the demonstrated rule. An available caption or alt text is evidence,
   not automatic proof that a visual example adds no guidance.
7. Bind approvals to both source-content and destination-content hashes, reviewer,
   and review time. If either content changes, the prior approval is stale. Source
   retrieval success and author assertions cannot grant semantic approval.
8. Maintain explicit pending, approved, needs-fix, and blocked states. A blocked
   source or meaningful media example remains in the denominator. Last-known-good
   content is distinguishable from a current successful fetch.
9. Reconcile a final live discovery/source check with the release snapshot. Additions,
   removals, redirects, changed text/tables/media, and failed fetches require review.
   Offline CI proves snapshot consistency, not live freshness.
10. Verify that an installed package can reach every local reference through the
    router and its explicitly loaded modules, without authoring caches or Python.
    Inspect publication artifacts for raw Apple sources and media.

## Media review record

Each distinct substantive example needs its source article/section, source asset
URL, asset identity/hash where available, use context, classification, review
method, original local explanation, destination identity/hash, and independent
verdict. Multiple uses may share one asset review only when their guidance and
context are equivalent. Decorative, navigation, resource-thumbnail, and redundant
examples need a reasoned disposition, not an unexplained exclusion.

Still images can be reviewed through available image inspection tools. Video
review must inspect the actual visual sequence, not only its poster. Use headless
frame extraction and relevant audio/transcripts when needed; mark unreviewed
motion, timing, or audio meaning explicitly. Raw sources and media stay in the
ignored cache. Their absence from the public package does not excuse omitted
guidance.

The independent auditor has inspected all 61 primary embedded video sequences and
their 20 available light/dark alternatives, using chronological extracted frames
and source context, with a native-resolution detail crop where needed. Original
explanations are retained in the package's supplementary media references. These
reviews do not assert exact playback-timing reproduction or a device comfort test.

Audio input is unsupported by the reviewing model. Audio was therefore assessed
through actual decoded PCM waveforms/envelopes and frequency analysis, without a
claim of auditory listening. Fourteen non-haptic tracks are exact digital silence;
two contain only a few brief, low-level interaction transients. The 18 haptic
recordings provide illustrative proxies for predefined patterns whose meanings
are documented in source prose and whose relative envelopes were visually
inspected. No additional spoken instruction was identified by this signal-based assessment;
the local pattern guidance does not depend on audition of these illustrative proxies. Eight alternate haptic tracks decode identically to their primary;
the ninth differs only by silent padding. No physical tactile evaluation is
claimed. Audio-only instructions or speech in a future source revision require
transcription or another suitable review method before approval.

## Cross-cutting audit cases

- Accessibility includes vision, hearing, mobility, speech, and cognitive needs.
  Its source changelog moves Dynamic Type guidance to Typography and VoiceOver to
  its own article. Verify these relationships locally.
- Liquid Glass guidance includes materials, color, component behavior, platform
  differences, and supporting implementation dependencies.
- Games connect controls, display adaptation, onboarding, accessibility, audio,
  haptics, Game Center, and purchases.
- Localization design includes right-to-left behavior, writing, inclusion, and
  text/layout adaptation. English-source completeness does not imply translated
  source parity or multilingual-package coverage.
- Spatial guidance includes layout, immersion, eyes, gestures, ornaments, and
  accessibility; macOS, tvOS, and watchOS distinctions must remain discoverable.

## Findings resolved during review

- Independent traversal matched the implementation's 173 current routes; historical
  redirects and unavailable pages remained separate from the article denominator.
- Row/column heading scope originally leaked into sibling content. The extractor
  was corrected and the regression now checks lexical section association.
- Absolute in-HIG links were originally misclassified as external dependencies.
  Normalization was corrected without discarding genuinely external resources.
- The iPhone Duo reference needed a precise description of vertical system bars;
  the author corrected it. The original visual supplement retains equal-pane Notes
  behavior and Calculator keypad adaptation in different poses.
- Source games guidance has conflicting touch-target prose/table values. The local
  reference preserves the conflict and applies a conservative interpretation.
- Actual [Game Center artwork diagrams](https://developer.apple.com/design/human-interface-guidelines/game-center)
  label challenge/multiplayer crops 1465 × 1080 pt, while their adjacent tables say
  1465 × 767 pt. The [original visual explanation](../skills/apple-hig/references/media/game-center-images.md)
  preserves both values and the unresolved discrepancy rather than approving a
  table-only account of the visual source.
- All 72 ordinary/increased-contrast light/dark RGB swatch labels were visually
  inspected and independently compared with the dated original local tables.
- Root routing, all 13 nested skill entry points, the platform/task map, and media
  routing were read independently. The paths resolve relative to the installed
  package, nested reads are explicit, and platform/SDK/history boundaries are clear.

## Final gate acceptance

The independent auditor read the final gate implementation and ran both the full
maintenance suite and strict corpus check after reconciliation: **34 tests passed**,
**173 pages / 158 articles**, **zero errors**, and **zero pending items**.

The corrected media gate freezes source representation URLs/traits, requires an
actual inspected URL and valid binary fingerprint, a nonempty inspection method,
reviewer/evidence, occurrence IDs, and nonempty reachable hash-bound supporting
files. It groups resolution-only variants while requiring independent appearance
provenance; deleting the appearance list no longer hides meaningful alternatives.
Decorative redundancy needs an explicit reasoned classification. Actual inspection
has now covered all 1,280 distinct primary image IDs, all 933 distinct alternate image
representations, all 61 primary video sequences, and all 20 video alternatives.

The final 54 secondary image attestations were reconciled independently against
current source, primary binary and supporting-file hashes. The publication guard
also rejects vector/print/TIFF assets outside ignored cache directories. Static
checks validate recorded bindings; they cannot replace the human/agent source-to-
guidance judgment or prove that someone actually inspected an asset.

Ten decorative alternates were upgraded from reasoned dispositions to actual
paired inspection during final reconciliation. Their supplemental live-byte check
matched all 10 expected hashes with no failures. The full live run finished at
2026-10-25T13:53:27+00:00 with zero errors or pending items, covering the 173 current
pages and 2,284 previously recorded asset URLs. Together the runs verified all
**2,294 distinct inspected media URLs**, including all 61 primary and 20 alternate
videos. The auditor read the actual live output, checked the additional hashes
against the current records, and verified the recorded manifest/script hashes in
[release verification](release-verification.json). This establishes freshness at
that verification time; later upstream revisions still require drift checking.

## Verdict ledger

| Review area | State | Evidence |
| --- | --- | --- |
| Independent current-route discovery baseline | Reconciled | Independent 173-route baseline agrees with final 173-route live inventory; historical outcomes unchanged |
| Article and section semantic review | Recorded, hash-valid | 158/158 independent article records: auditor 24, reviewer A 75, reviewer B 59; all guidance units have source-bound evidence |
| Platform differences and specification tables | Recorded | Explicit section/unit/table judgments in article records; substantive image diagrams reviewed separately |
| Distinct embedded image/video inventory | Inventoried | 1,472 image occurrences, 1,280 distinct primary image IDs, 933 image appearance alternatives, 61 videos and 20 video alternatives |
| Media semantic review | Reviewed, hash-valid | All 1,472 image occurrences and 61 video occurrences approved; all 1,280 primary images, 933 image alternatives, 61 videos and 20 video alternatives actually inspected |
| Source/destination review hashes | Recorded per approval | Canonical source, guidance, supplementary explanation, reference metadata and actual binary hashes are separately bound |
| Router/module/source boundaries | Independently reviewed | Root and 13 module entry points, platform/task routing, topic/media graph and limitations inspected |
| Maintenance boundary checks | 34 tests observed passing | Includes provenance/appearance deletion, wrong assets, occurrence removal, supporting files, source failures, relocation, publication and live drift; reported media-field deletion gap corrected |
| Installed-package retrieval/application | Executed, independently assessed | Seven repeated prompts plus two enabled application/media cases; 52 actual file reads, 51 unchanged in final roster plus one additive media-index expansion; see evaluations.md for limits |
| Final live source drift | Verified | Live source/result: zero errors and pending; 2,284 base plus 10 supplemental media URLs matched, totaling 2,294; dated evidence in release-verification.json |

This ledger reflects observed evidence. Passing route or file checks alone cannot
approve semantic units. The final strict and live checks pass for this recorded
snapshot. Source or local changes after this verification require renewed
validation and review.
