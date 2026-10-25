---
name: apple-hig-gestures
description: Use when designing, reviewing, or adapting touch, indirect hand, direct spatial, trackpad, or Watch gestures and their discoverable alternatives.
---

# Make gestures predictable shortcuts to visible work

Read [Gestures](../../references/gestures.md). Inspect the task, target platforms, existing system/custom gestures, physical demands, and visible alternatives. Establish design, review, or adaptation mode. Preserve the stack; use actual interaction evidence to distinguish a gesture conflict from an untested possibility.

Start with standard meanings for tap, swipe, drag, hold, zoom, and rotation. Give immediate predictive feedback showing what moves, how far, and whether movement is locked/unavailable. Keep an explicit route for essential work through controls or supported alternative input. A custom gesture needs a frequent specialized task, simple explanation, discoverability, and another way to perform the action; if teaching it is harder than the task, redesign.

Check conflicts against the platform's reserved navigation, edges, undo/redo, multitasking, and overlay gestures. Do not repurpose a familiar system action to save one button. On visionOS, prioritize indirect interaction from rest and avoid sustained raised arms, complex two-hand/finger patterns, prescribed handedness, or required body movement. Custom hand gestures need Full Space/hand-data permission and must coexist with palm/wrist system overlays. On Watch, double tap already scrolls or advances vertical containers; only assign a primary button action where the container context permits it.

**Worked transformation:** Before, a spatial editor requires a two-hand twist above shoulder height to close a panel and places tool UI directly on the wrist. Decision: dismissal must be simple and compatible with system overlays. After, a labeled Close action and familiar indirect activation cover dismissal; optional manipulation gestures supplement visible controls, and task tools move away from reserved wrist space.

Deliver a gesture-to-action/conflict map and revised interaction artifact. Fail if an essential task has only a complex gesture, standard navigation changes meaning, feedback lags behind the manipulated content, or a system overlay competes for the same movement. Ergonomics and gesture recognition require real-use/device testing; static review cannot verify reliability.

Use [Accessibility](../../../apple-hig-foundations/.topics/apple-hig-accessibility/SKILL.md) for alternatives, [Apple Pencil and Scribble](../apple-hig-apple-pencil-and-scribble/SKILL.md) for stylus gestures, or [Eyes](../apple-hig-eyes/SKILL.md) for indirect target feedback.
