# Changelog

All notable changes to the `apple-hig` skill are listed here. Each release
names the Apple HIG source snapshot that it uses.

## [Unreleased]

### Added

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
