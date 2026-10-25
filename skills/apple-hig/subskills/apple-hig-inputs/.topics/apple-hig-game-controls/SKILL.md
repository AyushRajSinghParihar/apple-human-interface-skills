---
name: apple-hig-game-controls
description: Use when designing, reviewing, or porting game touch controls, physical-controller mappings, active-device glyphs, keyboard bindings, or input alternatives.
---

# Preserve the playable action across input devices

Read [Game controls](../../references/game-controls.md). Inspect the core action set, target platforms, active controller profiles, touch regions, and requested design/review/adaptation scope. Preserve the engine and separate gameplay bindings from menu navigation. watchOS is unsupported here; controller requirements on tvOS/visionOS need the appropriate store badge and graceful absence handling.

Map the loop to the platform's built-in input first, with controller enhancement where useful. On touch, prefer direct manipulation for objects and virtual controls for movement/many actions. Keep frequent actions near thumbs, outside camera/movement regions and hardware safe areas; use the guide's frequent/secondary size requirements. Show pressed feedback that remains visible around a finger. Label actual actions rather than borrowing arbitrary physical button letters. Combine related actions and avoid complex simultaneous combinations.

Detect active controller/profile and player, updating glyphs accordingly. Outside gameplay, preserve familiar activation, cancel/back, section, selection, and pause mappings; Home/logo stays system-owned. If connection drops or no required controller exists, explain connection and retain a usable state. On keyboards, favor reachable related bindings and customization, while preserving system commands. For visionOS spatial controllers, retain look/trigger indirect and reach/trigger direct semantics.

**Before → decision → after:** A climbing game puts tiny A/X buttons beside the Home indicator and keeps Xbox labels after a different controller connects. Decision: actions need reachable touch controls and labels matching active hardware. After, “Grab” and “Jump” touch regions sit in safe thumb areas with clear pressed states, while connected-controller prompts use that player's actual glyphs; menus retain conventional Back/Pause behavior.

Deliver an action-to-input/player mapping and corrected control layout or implementation. Fail if the advertised platform cannot complete the loop, input changes produce wrong prompts, or a control conflicts with system gestures. Hardware mapping, ergonomics, and multiplayer identity need actual device/controller tests; list unperformed checks.

Use [Designing for games](../../../apple-hig-getting-started/.topics/apple-hig-designing-for-games/SKILL.md) for first-play/platform scope and [Gestures](../apple-hig-gestures/SKILL.md) for supplementary touch interaction.
