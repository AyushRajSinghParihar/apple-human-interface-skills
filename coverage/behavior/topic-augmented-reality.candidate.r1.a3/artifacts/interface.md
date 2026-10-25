# Furniture placement: revised session specification

Platform: iOS/iPadOS handheld camera AR. Preserve furniture selection and dimension data in the existing prototype; no framework replacement is specified. AR is an optional way to preview the selected product. Product details and dimensions remain useful without camera access. This document specifies intended behavior, not an implemented or tested app.

## Entry and environment

Open product details without starting the camera. Show the selected chair, verified width/depth/height and a “View in Your Room” action on capable devices. Hide that optional action on unsupported devices; keep product details available. If model units or real dimensions are unknown, withhold AR placement and explain “Room preview unavailable for this item.” Never substitute an arbitrary scale.

Beside the AR action, explain: “Preview this chair at actual size using your camera. Choose a clear, well-lit floor area. Stay aware of people and obstacles; you can place and adjust it without walking.” This is ordinary product context, not a separate permission pre-alert. Do not promise obstacle detection or exact fit.

On activation, request camera access through the system prompt if needed. Purpose string: “Use your camera to preview furniture at actual size in your room.” Do not add a custom consent imitation or request microphone, location, or photos access. On denial or restriction, return to details with “Camera access is needed for room preview”; offer product details and, when permission can be changed, “Open Settings”. Never repeatedly prompt. Recheck access on return from Settings; start AR only after a fresh explicit invocation.

## Session states and transitions

Keep a labeled, screen-fixed “Exit AR” button available in every camera state, including coaching and recovery. It stops camera/session use and returns to the same product details. No distance, gesture, placement, or recovery success gates exit. Keep system navigation and reserved edge gestures intact.

| State | Scene and status | Available transition |
| --- | --- | --- |
| Finding floor | Live camera; no chair. Prefer system coaching for horizontal-surface discovery. Hide unrelated product/edit controls while coaching. Say “Aim at a clear floor area. Move your device slowly if comfortable.” | Usable horizontal floor estimate and usable tracking → Ready. Exit AR → Details. “Restart Scan” restarts discovery. |
| Ready | A surface-aligned footprint at the current estimate, with “Ready to place”. Chair remains absent. A horizontal estimate must correspond to a floor the person intends to use; do not require exact floor boundaries or unsupported semantic classification. | “Place Chair” commits the indicated estimate → Placed. If estimate or tracking becomes unusable, remove indicator, disable placement with an explanation → Finding floor or Recovery. |
| Placed | Render the chair attached to the chosen surface at verified real scale; status “Placed · actual size” and product dimensions. Use plausible perspective, environmental lighting and diffuse contact shadow. | Adjust or reposition within the usable floor estimate. Loss/limited tracking or interruption → Recovery. Exit AR → Details. |
| Recovery | Immediately remove the “Placed” claim, hide chair and placement indicator, and disable spatial edits. Show “Placement unavailable — finding your room again.” Prefer system relocalization coaching. Retain selected product and last transform as an unverified draft. | Restore only after usable tracking and a resolved prior anchor → Placed. Otherwise remain unverified. “Restart Scan” → Finding floor, discarding the old anchor but retaining product/dimensions. Exit AR → Details at any time. |

Place promptly from the current usable estimate; do not wait for perfect edges. Refine surface attachment gently as estimates improve. If refinement would visibly jump the chair or the old anchor cannot be resolved, enter Recovery rather than silently relocating it. An interruption (call, app switch, unavailable camera, backgrounding) suspends camera use; returning enters Recovery, never an immediate trustworthy frozen scene. Resizing/orientation retains product and draft; if it interrupts spatial continuity, use the same recovery path.

During discovery/recovery, expose Restart Scan and Exit AR from the start. Provide contextual remedies only when supported by the session condition: “Try more light or a floor with visible detail” or “Move your device more slowly.” If no usable result after 15 seconds, add “You can restart or return to product details.” This is a product reminder threshold, not an Apple tracking timeout. Never require waiting for that reminder or continuing movement.

## Placement and stationary adjustment

Use a fixed 1:1 model-to-meter conversion validated against catalog dimensions. Disable pinch scaling; do not enlarge a distant chair to make it reachable. Dimensions are product data, and the AR preview is an estimate rather than a clearance or fit guarantee. Keep “Preview only — check dimensions and clearances” available with the dimensions.

Tap the chair to select it. Optional one-finger drag moves it along the usable floor; optional two-finger rotation changes yaw. Give immediate predictive feedback, keep contact with the surface, and reject moves outside the current usable estimate instead of floating or losing the chair. Give thin/distant parts a reasonable larger selection proximity without overlapping the fixed controls.

Stationary, labeled controls provide the same essential work: “Move Left”, “Move Right”, “Move Nearer”, “Move Farther” move 5 cm per activation along the floor in the current view direction; “Rotate Left” and “Rotate Right” change yaw by 5 degrees. These increments are product choices. Disable a move that lacks a usable destination and explain why. “Reposition” retains the existing placement as a draft, opens floor targeting, and offers “Place Here” or “Cancel Reposition”; cancellation restores the prior verified placement only if its anchor is still usable, otherwise Recovery. If the chair is offscreen, show a directional cue and Reposition; never instruct backward walking. Exit AR stays visible throughout.

## Controls and inclusive use

Use system buttons and their enabled, disabled and pressed feedback. Place frequent actions in reachable screen-fixed space, outside reserved system edges and separate from scene hit testing. Use at least 44 × 44 pt activation regions for this product, with separated, nonoverlapping targets. Place Chair/Place Here is prominent only when eligible; Restart Scan and Exit AR remain distinct secondary actions. Reset affects only the spatial draft and cannot remove catalog data. No purchase, saved room map, or destructive account action exists in this session.

Keep camera content dominant. On iPhone use a compact lower action area; on wider iPad windows expose adjustment controls alongside the scene. Compact iPad windows use the same reachable action area as iPhone. Preserve selection/draft across these arrangements; touch works without Pencil, pointer, or keyboard accessories. Scrolling the adjustment controls must not hide Exit AR or essential status.

Status is screen-space text plus a symbol, never color or sound alone. Controls expose names matching their labels, button roles, and enabled states; dimension content identifies units. Reading/task order is Exit AR, session status, product/dimensions, placement or recovery action, then adjustments. Announce meaningful state changes once, avoiding per-frame announcements. Support Dynamic Type enlargement to at least 200% with reflow and scrolling instead of clipped essential text. Back controls and all essential commands must be reachable with assistive navigation and Full Keyboard Access. Offer product details for people unable to scan safely; do not claim that nonvisual room placement is solved by labels alone.

## Data contract

| Data | Purpose and access | Retention/transfer requirement |
| --- | --- | --- |
| Camera frames and transient spatial estimates | On-device room preview after camera permission | No recording, upload, or analytics payload containing frames/maps. Release on exit. |
| Product ID, dimensions and session draft | Preserve chosen furniture and adjustments through temporary interruption | Keep draft in session memory only; no persistent room map. On exit discard spatial draft and retain product selection in details. |

These are new implementation requirements, not observations about existing collection. Review disclosures against actual shipping behavior before release.

## Guidance basis

The installed local HIG snapshot informs this specification; links identify official articles without claiming online verification. Prefer system coaching, estimated-surface placement with refinement, real product scale, stationary manipulation and cancellable recovery: [Augmented reality](https://developer.apple.com/design/human-interface-guidelines/augmented-reality#Providing-coaching), especially placement, interactions and interruptions. Permission timing and purpose copy: [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission). Labeled alternatives and preserved system gestures: [Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures#Best-practices). System controls and targets: [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices). Text, semantics and alternative input: [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility). Interruption and device context: [iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios) and [iPadOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados). Specific labels, increments, retention policy, recovery gating and reminder timing are product decisions applying that guidance.
