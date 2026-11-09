# Revision outcome

Patched `interface.md` in place from the supplied one-paragraph brief into a concrete iOS/iPadOS session specification. It now covers deliberate AR entry, permission denial and unavailable-feature fallbacks, local transient data, true-size floor placement, stationary manipulation, interruption recovery, accessible control contracts and responsive layouts. Selection survives exit; uncertain room placement never remains trusted.

## Decisions

| Original issue | Revised contract | Source support |
|---|---|---|
| Immediate camera entry | Explain AR on product details; request camera on deliberate entry; retain useful browsing after denial. | [Privacy — Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission). Product context avoids a separate custom pre-alert. |
| Arbitrary floating chair | Verify model dimensions, align an indicator to the floor, place at 1:1 using usable estimates and refine gently. | [AR — Helping people place objects](https://developer.apple.com/design/human-interface-guidelines/augmented-reality#Helping-people-place-objects) and Designing object interactions. Fixed scale serves furniture comparison; AR scaling is not universally prohibited. |
| Backward walking required to exit | Persistent Close plus stationary move/rotate controls and familiar optional gestures. | [AR — Best practices](https://developer.apple.com/design/human-interface-guidelines/augmented-reality#Best-practices), [Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures). |
| Frozen chair falsely marked placed | Hide uncertain content and clear Placed; coach recovery; restore only a stable old anchor; immediate restart/exit. | [AR — Handling interruptions](https://developer.apple.com/design/human-interface-guidelines/augmented-reality#Handling-interruptions). Apple says consider hiding; this product chooses to require it. |
| Handheld/tablet access | Reachable native controls, explicit labels/status, gesture alternatives and state-preserving resizing. | [iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios), [iPadOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados), [Layout](https://developer.apple.com/design/human-interface-guidelines/layout), [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility), [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons). |

The 5 cm movement step, 15° rotation step, explicit confirmation, immediate hiding and no persisted maps/uploads are product decisions requiring implementation and usability validation. They are not additional Apple rules. The 44 × 44 pt button target uses the buttons guide and accessibility default; the smaller accessibility minimum is not used to justify dense controls.

## Worked before/after

Before: Beside a sofa, a person opens the prototype. The camera starts without explanation and an arbitrary-size chair floats before a floor is found. A call interrupts the session; returning leaves a frozen chair labeled placed. Exiting requires walking backward toward an unseen obstacle.

After: The same chair opens in product details with verified dimensions. View in Your Room leads to system authorization. Coaching finds a usable floor estimate and shows an aligned footprint, then Place Chair creates a true-size preview. Move/Rotate and Confirm Position work from the person's current position. A call suspends capture. Returning enters Recovering, hides the chair and says placement is paused. A recovered stable anchor restores it; otherwise Restart begins fresh discovery retaining the chair selection. Close stops capture and returns to details at any point. No backward movement or forced recovery wait is required.

## Acceptance checks

Passed — static document inspection only:

- All four supplied defects have explicit replacements in `interface.md`.
- Entry, denial, discovery, placement, adjustment, interruption, tracking loss, recovery, restart and exit have concrete outcomes.
- No chair appears before placement; uncertain tracking removes trusted placement; every camera state retains Close.
- Verified dimensions, gesture alternatives, data handling and iPhone/iPad resizing are specified.

Failed: no unresolved document-level failure identified. This does not establish a passing implementation.

Not executed — required implementation/device scenarios:

1. Fresh install: details never capture; deliberate entry uses the real system prompt. Deny/restrict and verify useful details, no prompt loop and appropriate Settings behavior. Test unsupported hardware and models lacking dimensions.
2. Place on a clear floor using current estimates. Measure catalog/model scale, surface alignment, drift, refinement, lighting, shadows, perspective and frame timing on supported devices. Fail on floating, jumping or detachment.
3. Remain stationary while placing, moving, rotating, canceling/confirming and closing. Test offscreen furniture and invalid moves. Fail if locomotion is essential; assess reach, fatigue and physical safety with users in real surroundings.
4. Induce tracking loss, call/app interruption and failed relocalization. Verify chair/Placed disappear, edits disable, and Close/Restart work immediately. Recover with and without the old anchor; never restore its location on tracking alone. Verify restart clears maps and exit stops capture.
5. Rotate iPhone/iPad, resize iPad windows, enlarge text to at least 200%, and resume. Preserve selection/draft/state; essential controls remain visible and usable inside safe areas. Test actual multitasking camera availability.
6. Measure target geometry and contrast against bright/dark camera imagery in light/dark appearances. Test VoiceOver, Switch Control, AssistiveTouch and Full Keyboard Access for names, order, status and complete command activation; check reserved gestures. Native-control intent is not execution evidence.
7. Inspect capture lifecycle, storage and network behavior for the no-recording/upload/map-persistence contract, and verify no unrelated permissions. Compare actual purpose strings and privacy disclosures with implementation.

## Evidence limits and instruction audit

Product evidence consisted only of the original `interface.md` prose. No implementation, assets, screenshots, SDK, device or metrics were supplied. No build, GUI, AR session, accessibility tool, contrast measurement or physical-comfort execution occurred. Runtime checks above remain pending; no safety, SDK availability or accessibility certification is claimed.

Explicitly read the installed `.agents/skills/apple-hig/SKILL.md`, then searched its topic index. Followed owning family → topic procedure → reference for Getting started (iOS and iPadOS), Technologies (Augmented reality), Foundations (Privacy, Accessibility, Layout), Menus and actions (Buttons), and Inputs (Gestures). Every file was consumed with a separate `cat` command using installed-package paths; index searches used `rg`. The local references identify a 2026-10-25 snapshot and are derived guidance, not SDK documentation. Official article links are attribution only. No web browsing or external verification occurred; platform/API feasibility requires the implementation's SDK evidence before shipping.
