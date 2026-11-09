# AR adaptation result

Patched `interface.md` in place from a one-paragraph problem statement into an implementable iOS/iPadOS furniture-preview contract. No app source, rendering, device session or test harness was supplied.

## Decisions and changes

| Supplied behavior | Revised contract and reason |
|---|---|
| Camera opens immediately without explanation | Chair detail explains the task and surroundings; explicit View in your room requests system camera permission at the point of use. Denial keeps dimensions useful. |
| Arbitrary-scale floating chair before surface discovery | No chair until a usable floor estimate and explicit placement; floor-aligned indicator, verified model dimensions, fixed real size and gentle estimate refinement. |
| Walk backward to exit | Stationary End AR in every active state, including coaching/recovery; no movement prerequisite. Offscreen recovery offers Place again. |
| Tracking loss freezes a chair labelled placed | Remove placed status and hide unstable content; disable edits, explain recovery, retain useful selection, and allow immediate restart or exit. Restore only after establishing trustworthy correspondence. |

Additional product decisions make those fixes usable: optional AR with a dimensions fallback, on-device ephemeral spatial data, interruption recovery, familiar drag/rotation plus visible controls, undo, safe invalid-drop behavior, reachable controls and text reflow. The 5 cm movement and 15 degree rotation steps are proposed product increments, not Apple requirements. Fixed furniture scale serves purchasing evaluation; it does not establish accurate clearance or collision detection.

The source recommends system coaching and considers hiding old objects during recovery; this specification deliberately adopts both. It does not promote every recommendation into a universal Apple rule. A usable estimate permits prompt placement; inability to establish a floor does not permit an arbitrary placement. No face-tracking or image-recognition timing guidance is applied to furniture tracking.

## Worked before/after

Before: A person opens the prototype in a small room. The camera activates without explanation, a chair floats at an arbitrary size, and a call interrupts the session. Returning leaves a frozen chair marked placed. Exiting requires walking backward toward unseen obstacles.

After: The person selects the same chair and variant, reads its dimensions and room-preview explanation, and explicitly starts AR. After authorization, coaching finds a floor. A floor-aligned footprint becomes ready; Place chair renders the validated real-size model. The person rotates it with stationary controls. After a call, the chair is hidden and “Preview paused — finding your floor again” replaces “Placed.” The selection and previous transform remain available for recovery but are not treated as verified. If relocalization fails, Restart returns to discovery with the same chair, or End AR stops the camera and returns to its dimensions without moving. This is a specified scenario, not an executed device trial.

## Acceptance checks and status

Static specification checks passed: the patched document explicitly covers each of the four supplied defects, a six-stage entry-to-exit/recovery flow, permission denial/revocation, reset state retention, model-scale validation, invalid placement and nonmovement alternatives. Both requested files exist. These checks establish document coverage only.

Failed: none in the document coverage checks. Runtime pass/fail is unknown.

Not executed — implementation acceptance gates:

1. Fresh authorization, authorized, denied and restricted camera states: no camera frames before consent; explicit entry; truthful purpose text; denial retains dimensions without repeated prompts. Audit that no frames/maps reach storage, network or analytics; End AR stops capture and discards spatial data.
2. Unsupported device and missing/mismatched model dimensions: hide optional unavailable AR, preserve product information, and never claim arbitrary-scale content is actual size.
3. In well-lit/textured and dim/featureless rooms: no pre-surface chair; aligned footprint; place from a usable estimate without waiting for exact edges; gentle attachment refinement without jumping, drifting or false floor classification. Measure actual model dimensions and performance, including the HIG target of 60 scene updates/second; no achieved rate is claimed.
4. Interrupt via a call/app switch, lose tracking and invalidate an anchor: placed status disappears, unstable chair hides and editing disables. Verify restoration only with reliable old-anchor correspondence. Exercise prolonged recovery, Restart, camera failure and End AR without requiring movement or waiting for recovery.
5. Place near view limits, drag onto an invalid target, rotate and undo: maintain scale/attachment; invalid drop returns to valid state; direct and stationary controls agree. Verify system navigation/gesture coexistence and offscreen cues without requiring backward walking.
6. iPhone/iPad portrait, landscape and narrow/wide windows: preserve chair/variant/edit context, recover if camera continuity breaks, keep End AR reachable above coaching, and retain every action through text enlargement of at least 200%.
7. On supported Apple environments, measure 44 × 44 pt activation areas/separation and actual text contrast over changing camera content, in light/dark and Increase Contrast. Exercise VoiceOver, Switch Control, Full Keyboard Access and touch through entry, placement, recovery and exit; confirm names, roles, states and values. No accessibility execution is claimed.
8. In supervised physical-use sessions, check short sessions, seated/stationary use, reach, fatigue, obstruction awareness and offscreen recovery. Confirm useful dimensions fallback where AR cannot be performed. Static prose cannot establish safety, comfort, spatial accuracy or accessibility equivalence.

## Local evidence and routing audit

Read the installed root `.agents/skills/apple-hig/SKILL.md` explicitly before routing. Each file was read by a separate `cat` command, with topic procedures read before their supporting guides:

- Technologies family → `.topics/apple-hig-augmented-reality/SKILL.md` → `references/augmented-reality.md`.
- Inputs family → `.topics/apple-hig-gestures/SKILL.md` → `references/gestures.md`.
- Foundations family → Privacy procedure → `references/privacy.md`; Accessibility procedure → `references/accessibility.md`.
- Getting started family → Designing for iOS and Designing for iPadOS procedures → their respective reference guides, for platform and capability/fallback decisions.

All paths above resolve beneath the installed root; references belong to the corresponding family. The AR procedure routed gestures and privacy; gestures routed accessibility. Guidance was applied only after reading the owning procedure and local source guide. No web browsing or external lookup occurred.

Official links identify the source of the local guidance; they were not fetched: [AR](https://developer.apple.com/design/human-interface-guidelines/augmented-reality), [privacy](https://developer.apple.com/design/human-interface-guidelines/privacy), [gestures](https://developer.apple.com/design/human-interface-guidelines/gestures), [accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility), [iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios), [iPadOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados). The local articles report retrieval on 2026-10-25 and describe themselves as original application guidance, not verbatim manuals. Their existence does not establish independent review or current SDK availability.

Evidence limits: the supplied artifact documents behavior but provides no runtime proof. No SDK/API names, capability matrix, compilation, camera permissions, frame rate, rendering, physical safety, GUI, device or assistive-technology behavior was executed or verified. No current-release claim or legal/security certification is made. The next implementation must validate framework APIs and hardware support against its SDK; this local-only task cannot do so.
