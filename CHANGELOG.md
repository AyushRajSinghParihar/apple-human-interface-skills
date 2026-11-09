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
