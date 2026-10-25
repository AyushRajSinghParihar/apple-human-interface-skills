---
name: apple-hig-path-controls
description: Use when creating, reviewing, or adapting a macOS filesystem path display or editable path selector.
---

# Represent location without confusing selection

Read [the path-control guide](../../references/path-controls.md). The following is application advice; this component is macOS-only.

Inspect the actual file/folder location, display-versus-edit purpose, available width, platform, and create/review/adapt request. Determine whether activating a segment navigates or chooses a location and whether dropped items should change selection. Do not infer editable behavior merely from a displayed path.

Choose standard segments when visible ancestry matters; choose the pop-up form when compact display can reveal ancestry on demand. Place the control in the window body, not toolbar/status bar. In editable mode, accept supported dropped locations; a pop-up additionally needs Choose. Preserve the actual selected item's identity even when intermediate segment names hide under width pressure. Define what nonfolder or unavailable drops mean according to product requirements rather than implying arbitrary paths are valid.

Implement the control/location handling, provide a location/segment/drop specification, or review concrete ambiguity and placement defects. For another platform choose a supported navigation or file-location presentation; do not claim native path-control parity.

**Worked transformation:** Before: an export window shows a toolbar breadcrumb that appears editable but rejects drops and offers no chooser. Decision: location selection needs explicit editable behavior and body placement. After: use an editable body pop-up showing the selected folder, full hierarchy on opening, Choose, and valid folder-drop handling.

Deliver the artifact with displayed path, editability, navigation/selection, and validation contract. Verify root/deep paths, narrow width, selection by Choose/drop, and stale locations. Fail for displayed versus actual location disagreement, inaccessible hidden ancestry, or silent acceptance of an invalid destination. Native filesystem permissions and drag behavior need runtime evidence.

Load [file-management](../../../apple-hig-patterns/.topics/apple-hig-file-management/SKILL.md) for broader location/persistence work or [drag-and-drop](../../../apple-hig-patterns/.topics/apple-hig-drag-and-drop/SKILL.md) for transfer semantics.
