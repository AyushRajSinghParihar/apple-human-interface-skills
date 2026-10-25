---
name: apple-hig-image-wells
description: Use when creating, reviewing, or adapting macOS editable image containers with copy, paste, drop, and deletion.
---

# Make image editing use familiar commands

Read [the image-well guide](../../references/image-wells.md). The workflow is application advice; image wells are Mac-specific.

Inspect image role, required/default status, editable container, accepted content, platform, and create/review/adapt goal. Determine whether the image is merely displayed, activates an action, or can be replaced/cleared. Record paste/drop/delete handlers and command availability from evidence.

Choose an image well when editing is intended. Allow dropping an image without requiring prior well selection; when selected, support applicable Copy/Paste/Delete and standard Edit-menu shortcuts. Define accepted image data and rejection behavior so an invalid drop cannot destroy the current image. If the product requires a picture, clearing restores an appropriate default. Distinguish “remove custom image” from deleting the underlying source file; that distinction is an application contract, not implied by the component. Adapt other platforms using their supported media-editing UI.

Implement the editing operations, provide a command/drop/default specification, or review concrete blocked-work and loss defects. Preserve standard menu access rather than creating an unexplained gesture-only replacement.

**Worked transformation:** Before: a Mac profile image accepts drops only after selection, Delete blanks a required avatar, and Paste exists only in a context menu. Decision: editing should be standard and required-image state preserved. After: enable direct drops, expose Edit-menu Paste/Copy/Delete with normal shortcuts, and restore the default avatar after clearing.

Deliver the artifact and selected/unselected/drop/clear behavior. Verify unselected drop, compatible/incompatible paste, Copy, Delete, required/default restoration, and keyboard routes. Fail for lost original after rejected input, absent standard command access, or a missing required image. Mark native pasteboard/drag execution separately from source inspection.

Load [image-views](../../../apple-hig-content/.topics/apple-hig-image-views/SKILL.md) for display-only content or [edit-menus](../../../apple-hig-menus-and-actions/.topics/apple-hig-edit-menus/SKILL.md) for command semantics.
