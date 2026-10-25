---
name: apple-hig-designing-for-ipados
description: Use when creating, reviewing, or adapting an iPad experience for resizable multitasking, a larger canvas, mixed input, or prolonged creative work.
---

# Use the iPad canvas without assuming exclusive space

Read [Designing for iPadOS](../../references/designing-for-ipados.md). Inspect the task, related content, current navigation, window assumptions, and supported touch/Pencil/keyboard/pointer paths. Identify whether people hold the iPad or work at a stand/table. Establish design, review, or adaptation mode and revise only the authorized surface using the existing stack.

Decide which relationships benefit from simultaneous visibility. Keep a list beside detail or tools beside a canvas when that reduces navigation; leave unrelated information out. Replace repeated full-screen transitions or modal panels with persistent contextual structure when space permits. At compact multitasking widths, collapse that structure while retaining selection, draft, and the route back to context.

Map each meaningful operation to the inputs the task supports. Touch remains usable without attached accessories. Precise pointer selection and keyboard commands can accelerate work; Pencil may create or annotate content without becoming a required substitute for ordinary controls. Let input methods change during the same task without discarding state or hiding essential commands behind hover.

For cross-app work, specify what can be dragged out/in and where imported content lands. Treat resizing, orientation, larger text, and another app's presence as normal operating conditions. If the iPad experience runs on Mac, identify the Mac adaptation work rather than claiming identical behavior is already native.

**Worked transformation:** Before, a sheet-music editor copies its phone flow: choose score, open full-screen tools, then return to the page after each change. Decision: editing needs score and tools together, but multitasking may narrow the window. After, a contextual tool column accompanies the score at regular width and becomes a dismissible panel at compact width, preserving page, selection, and undo history. Touch editing and keyboard commands reach the same operations.

Deliver a wide/narrow task flow and input mapping or corresponding implementation. Fail if shrinking loses a selected object, a pointer-only control blocks touch, or imported content silently replaces work. Use supplied evidence for findings; physical reach, Pencil response, and inter-app drag/drop remain unverified until exercised on supported devices.

Continue with [Layout](../../../apple-hig-foundations/.topics/apple-hig-layout/SKILL.md) for resizing, [Apple Pencil and Scribble](../../../apple-hig-inputs/.topics/apple-hig-apple-pencil-and-scribble/SKILL.md) for drawing/writing, or [Pointing devices](../../../apple-hig-inputs/.topics/apple-hig-pointing-devices/SKILL.md) for precision input.
