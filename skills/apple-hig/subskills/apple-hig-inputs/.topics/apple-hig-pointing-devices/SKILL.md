---
name: apple-hig-pointing-devices
description: Use when designing or reviewing mouse and trackpad selection, pointer effects, hover-revealed controls, cursor roles, hit regions, or mixed pointer/touch/eye input.
---

# Show what precision input can do without changing the task

Read [Pointing devices](../../references/pointing-devices.md). Inspect the target platform, pointer actions, touch/keyboard equivalents, custom hit regions, and requested design/review/adaptation. Preserve user gesture mappings and the existing stack. This guide marks tvOS/watchOS unsupported; do not impose iPad pointer behavior on Mac or visionOS.

Map selection, dragging, text insertion, links, invalid drops, and resizing to their semantic cursor/effect roles. Keep systemwide gestures and modifier-drag meanings. Hover can reveal minimized bars/playback controls, but essential work must remain coherent when switching to another input. Distinguish a pointer from a finger only for a useful precision benefit, such as click-to-seek.

On iPad, use highlight for a group of controls in a Liquid Glass container, lift for a standalone Liquid Glass control or a small element with an opaque background, and hover for large elements. Check target padding, contiguous adjacent bar hit areas, and how easily a person can leave a target. Limit scaling where neighbors would collide; tint alone can suit tight rows. Keep pointer accessories simple and meaningful.

On Mac, use appropriate cursor roles and respect configurable primary/secondary clicks and trackpad gestures. On a Mac with a touch display, give essential hover-only controls a touch path: reveal them with a tap at their location while keeping the selection, hide them after use or a few seconds, offer them in a short context menu, and follow the guide's sidebar and tab close-button rules. Do not keep them permanently visible or add touch for tooltips. On visionOS, preserve system transfer among gaze, pointer, and window context; do not recreate gaze-based pointer relocation or assume private gaze data is available.

**Worked transformation:** Before, an iPad asset grid lifts every dense row until neighbors overlap and displays a custom pointer instruction paragraph. Decision: feedback should communicate target/action without moving the layout into conflict. After, dense rows use restrained tint/hover, resize affordances use simple accessories where applicable, and ordinary controls retain standard effects with touch-accessible actions.

Deliver corrected cursor/effect/hit-region assignments or implementation. Fail if an effect hides a neighbor, a target traps the pointer, input switching loses selection, a system gesture is overridden, or an essential hover-only control has no touch path on a touch-capable Mac. Native pointer effects, configurable gestures, and spatial pointer transfer require actual supported execution; static review cannot establish their feel.

Use [Focus and selection](../apple-hig-focus-and-selection/SKILL.md) for keyboard target movement and [Gestures](../apple-hig-gestures/SKILL.md) for shared manipulation meanings.
