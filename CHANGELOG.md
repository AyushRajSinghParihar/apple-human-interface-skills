# Changelog

All notable changes to the `apple-hig` skill are listed here. Each release
names the Apple HIG source snapshot that it uses.

## [Unreleased]

## [1.1.0] - 2026-11-10

Source snapshot: 2026-11-09.

- Benchmark: quality unchanged (mean 0.93 with the skill), 11% fewer input
  tokens, and no false starts for build and tooling questions. See
  `quality/RESULTS.md`.

### Added

- A shorter route: the root `SKILL.md` is 5.8 KB (was 8.2 KB) and links each
  topic procedure through a compact topic index of 31.8 KB (was 67 KB), which
  `hig.py index` makes from the topic descriptions.
- A description in the third person with the words that people use (SwiftUI,
  UIKit, AppKit, Dynamic Type, VoiceOver, Liquid Glass) and the requests that
  must not start the skill.
- `references/beyond-apple/`: how to apply Apple's guidance to web, Android and
  Windows apps, with host conventions, licence limits and host sources. This
  content is not from Apple's HIG.
- `references/key-numbers.md` and `references/implementation-map.md` (made by
  `hig.py api-map` from the guides' developer documentation links).
- Claude Code commands `/apple-hig:review` and `/apple-hig:adapt`, and the
  `hig-reviewer` subagent.
- `coverage/authored-reviews.json`: review records for files that are not
  derived from Apple sources.
- `scripts/hig.py stale` lists each review hash that no longer matches its file.
- `scripts/hig.py review-draft` writes the current hashes into a review record
  and marks it for another review. `--all` drafts every stale record.
- `scripts/hig.py review-approve --reviewer NAME` approves a draft after the
  reviewer rewrites its evidence.
- `hig.py check` fails while a draft or a `TODO(re-review)` marker exists.
- Tests for versions, README counts and the size of files on each route.

### Changed

- New source snapshot 2026-11-09. Apple's update of 2026-10-28 changed six
  articles: touch input on a Mac with a touch display (Designing for macOS,
  Gestures, Pointing devices, Drag and drop, Designing for games) and app icon
  formats (App icons). Pointing devices also lost "Pointer magnetism" and got
  Liquid Glass content effects, a new macOS pointer table and touch support for
  hidden controls. 20 other pages changed only outside their guidance.
- `hig.py review-remap`, `review-scaffold` and `review-renew` carry reviews to a
  new snapshot. Reviews of changed content stay drafts until a reviewer approves.
- PyYAML is now a stated requirement for the checks. Without it, each check
  gives one clear error.
- The marketplace entry now has a version.
- The plugin manifest is now `skills/apple-hig/.claude-plugin/plugin.json`.
  The marketplace entry keeps only listing data.
- The evidence of the stopped behavior study (51 MB) moved to the `evidence`
  branch. `coverage/behavior-archive.json` records its commit and trees.

## [1.0.0] - 2026-10-26

Source snapshot: 2026-10-25.

- First public release: a router, 13 family skills, 158 topic procedures and
  158 reviewed article references.
- Installation through the Skills CLI, the Claude Code marketplace and a
  Cursor manifest.
