---
name: apple-hig-apple-pencil-and-scribble
description: Use when designing or reviewing iPad Pencil drawing, hover, double tap, squeeze, barrel roll, Scribble, or mixed handwriting and control interaction.
---

# Keep drawing immediate and handwriting stable

Read [Apple Pencil and Scribble](../../references/apple-pencil-and-scribble.md). Inspect the iPad task, drawing/text areas, tools, supported Pencil features, and supplied implementation. Establish design, review, or adaptation mode. Preserve the chosen framework; feature availability depends on the Pencil/device, not merely iPadOS support.

Separate marking from text entry. Marking should begin immediately, including useful margins, and feedback should follow the touched content. Ordinary controls must remain Pencil-activatable. Map pressure/tilt/roll to continuous mark qualities where meaningful, keeping controls clear of either hand. For fixed photos/PDFs, preserve annotation visibility rather than automatically changing ink colors with appearance.

Treat hover as prediction, never activation: show a representative likely mark without distracting height-driven changes. Respect preferred double-tap tool mappings; any custom behavior should be opt-in, discoverable, nondestructive, and reversible. Squeeze is one quick action with UI near the tip, not sustained/repeated pressure. Reserve barrel roll for marks, not navigation.

For Scribble, accept writing without an extra focus tap where supported, provide enough space before entry or during a pause, hide placeholders when writing starts, and keep the field/transcription stationary mid-stroke. Password fields are an exception to automatic handwriting support. Supply undo/redo routes when a compact tool picker lacks them.

**Worked transformation:** Before, a diagram tool requires selecting Pen before every margin note, uses hover to commit dots, and moves a label field as letters appear. Decision: marking must be immediate and handwriting spatially stable. After, margin strokes draw directly, hover previews only, and label resizing waits until writing pauses; reversible tool changes respect Pencil preferences.

Deliver revised tool/input states or implementation. Fail if hover changes content, accidental squeeze deletes work, strokes lag behind detached feedback, or Scribble targets move during entry. Qualify latency, palm/hand comfort, hover, and hardware gesture claims until actual iPad/Pencil execution.

Use [Gestures](../apple-hig-gestures/SKILL.md) for shared gesture alternatives and [Typography](../../../apple-hig-foundations/.topics/apple-hig-typography/SKILL.md) for transcribed-text reflow.
