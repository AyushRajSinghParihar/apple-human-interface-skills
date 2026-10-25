---
name: apple-hig-file-management
description: Use when creating, reviewing, or adapting document creation, opening, saving, file browsing, previews, or provider integration.
---

# Preserve the document beyond the current screen

Read [the file-management guide](../../references/file-management.md). This workflow is application advice; browser/provider/launcher behavior has platform and version qualifications.

Inspect document identity/type, storage/sync, create/open/save routes, autosave policy, platform, and create/review/adapt mode. Establish what must survive close/background and whether autosave is disabled. Record actual persistence and extension visibility, not just an Edited label.

Prefer standard filesystem/browser integration with discoverable New/Open/Add and relevant keyboard/menu commands. A custom browser can prioritize a location but must retain wider browsing. Autosave periodically and on leaving/closing where applicable, honoring explicit cancel/delete. On Mac with autosave off identify unsaved work and request saving at consequential exits; apply dirty/Edited cues according to the source rather than all at once. Let people choose name/format/location and preserve extension preferences. Use Quick Look for useful previews rather than forcing app switches. Provider UI filters accepted types, exposes local/remote metadata and destinations, and avoids a duplicate host toolbar. New document launchers should preserve quiet branding and accessible actions across sizes.

Implement authorized persistence/browser behavior, produce a document lifecycle specification, or review exact loss and access defects. tvOS/watchOS do not normally offer document browsing; do not promise identical file UI there.

**Worked transformation:** Before: a Mac sketch app keeps edits only in memory, clears Edited after any button press, and exports to a hidden fixed folder. Decision: visual cues misrepresent durability and file choice. After: bind saved cues to actual save completion, preserve drafts across exits, and expose standard name/format/location selection while retaining the original document.

Deliver the artifact and new/open/save/close/sync/preview contract. Verify unsaved exits, failed save, reopen, extension preference, unsupported attachment preview, and provider type filtering. Fail for lost work, false saved state, or trapped filesystem scope. Actual storage durability/provider behavior requires execution evidence.

Load [the-menu-bar](../../../apple-hig-menus-and-actions/.topics/apple-hig-the-menu-bar/SKILL.md), [path-controls](../../../apple-hig-navigation-and-search/.topics/apple-hig-path-controls/SKILL.md), or [printing](../apple-hig-printing/SKILL.md) when those define the document workflow.
