---
name: apple-hig-photo-editing
description: Use when designing or reviewing a Photos editing extension, its system toolbar, preview, changed versus unchanged cancellation, and non-destructive save behavior.
---

# Keep extension edits previewable and recoverable

Read [Photo editing](../../references/photo-editing.md). Inspect the extension's entry from Photos edit mode, current controls, edit state, preview/save/cancel paths, and requested design/review/adaptation. Preserve the existing editing pipeline. The source covers iOS/iPadOS/macOS and excludes TV/visionOS/Watch.

Use the supplied modal/system top toolbar rather than adding a second conflicting toolbar. Keep the containing app's icon so the extension's origin is recognizable. Determine which controls affect the edit and ensure the result can be previewed before the extension dismisses; an unexplained immediate return is not a preview.

Track whether edits exist. Cancel without changes should leave without a needless confirmation. Cancel after changes should explain that those edits will be lost and allow the person to retain them. Save produces a new file while preserving the original; do not promise non-destructive behavior if the actual pipeline overwrites the source. The precise dirty-state tracking and output checks are application engineering choices that implement the guide's interaction contract.

**Before → decision → after:** A filter extension adds its own Done bar below the system toolbar, asks “Are you sure?” on every cancel, and dismisses as soon as a filter is tapped. Decision: selection, preview, and completion need distinct meanings. After, the supplied toolbar handles completion, filter choice remains previewable, unchanged Cancel exits directly, and changed Cancel explains edit loss while Save retains the original and writes the result.

Deliver corrected modal/edit-state transitions or implementation, including unchanged/changed cancellation and saved output identity. Fail if preview is impossible, duplicate toolbars conflict, unchanged exit prompts unnecessarily, or the original is modified. Code/file inspection can verify output handling when executable; actual Photos hosting, toolbar integration, and visual results require supported runtime checks.

Use [Live Photos](../apple-hig-live-photos/SKILL.md) if edits must preserve all live frames and [Images](../../../apple-hig-foundations/.topics/apple-hig-images/SKILL.md) for export fidelity.
