---
name: apple-hig-icloud
description: Use when designing or reviewing cloud-backed continuity, offline synchronization, large document downloads, conflicts, cross-device settings, or deletion across iCloud devices.
---

# Make continuity visible only when a decision is needed

Read [iCloud](../../references/icloud.md). Inspect user-created content, continuation state, storage/sync choices, offline behavior, deletion, and requested design/review/adaptation. Preserve the existing sync architecture where it can meet the task. The source supplies no separate platform rules; verify specific APIs and service availability when implementing.

Decide what should travel: meaningful created content and appropriate continuation state, such as reading position, differ from regenerable resources or device-specific settings. Use iCloud automatically when enabled; if the app needs a choice, prefer one clear all-data-or-none first-use decision rather than repeated per-document storage prompts. Remember that Documents-folder content can enter backups even without explicit integration.

Keep disabled/offline states unobtrusive and preserve local work. Explain deferred synchronization when useful instead of alarming people. Large documents can justify user-controlled download, an indication of a newer version, and subtle progress after a wait; do not turn normal background sync into mandatory management work. Include cloud content in search.

Resolve conflicts automatically where meaning can be preserved. Otherwise show differentiated versions promptly with an understandable choice rather than technical revision IDs alone. Before deletion, explain its effect across iCloud and every device and obtain confirmation. For game saves, choose supported GameSave/offline/conflict handling appropriate to the progression model.

**Worked transformation:** Before, a journal asks “Local or Cloud?” for every entry, reports offline use as a fatal error, and labels deletion “Remove here” although it deletes everywhere. Decision: continuity should be automatic and destructive scope explicit. After, entries save locally while offline with quiet later-sync status, one clear global choice governs cloud use, and deletion explains the cross-device effect before confirmation.

Deliver a continuity/offline/conflict/deletion state contract or corrected implementation. Fail if offline edits disappear, a conflict choice cannot distinguish versions, or deletion scope is misleading. File-level tests cannot establish real iCloud propagation, account changes, or multi-device conflicts; report actual service/device evidence separately.

Use [Writing](../../../apple-hig-foundations/.topics/apple-hig-writing/SKILL.md) for conflict/deletion language and [Game Center](../apple-hig-game-center/SKILL.md) when system game activity also affects continuation.
