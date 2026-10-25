# Revision outcome

Patched interface.md in place from a one-paragraph prototype description into a concrete iOS/iPadOS camera AR contract. The patch replaces immediate camera launch, arbitrary floating scale, backward-walking exit and stale placement claims with explicit entry, permission handling, surface-gated actual-size placement, stationary controls and an honest recovery state.

## Decisions and rationale

AR remains optional because product selection and dimensions provide value without scanning. Unsupported hardware hides the optional entry; denied access leaves product details usable. The existing stack is preserved because no source code or framework choice was supplied.

The state table defines Finding floor → Ready → Placed, with Recovery on uncertainty or interruption. Estimated placement avoids waiting for exact floor edges; old geometry is hidden until its anchor is resolved. Exit AR and Restart Scan prevent indefinite recovery. Actual-size furniture and floor-constrained adjustment preserve the purpose of judging a product in a room. These decisions apply [AR placement, interactions and interruptions guidance](https://developer.apple.com/design/human-interface-guidelines/augmented-reality).

Context appears in product details, with the system permission request following explicit AR invocation; no extra custom permission pre-alert is introduced. Camera/spatial data stays transient and on-device as a specified policy, requiring implementation verification. This follows [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission).

Visible movement/rotation controls supplement gestures, and exit never requires bodily movement. System buttons, 44 × 44 pt product targets, text/symbol status, text enlargement and assistive-input checks apply [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons), [Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures) and [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility). The 5 cm/5 degree increments, 15-second reminder, specific copy and data retention contract are design choices, not HIG mandates. iPhone and iPad arrangements preserve selection and draft through resizing and interruption, following [iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios) and [iPadOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados).

## Worked before/after

Before: A person opens the prototype in a small living room. Camera use begins without explanation, a chair floats at arbitrary scale, and a call interrupts the session. On return the frozen chair still says “placed”. Exiting requires walking backward toward unseen obstacles.

After: The same person sees the chair and its catalog dimensions in details, reads room-preview context, then chooses View in Your Room and responds to the system camera prompt. Coaching finds a usable floor estimate; a footprint and Place Chair become available. Placement uses verified real dimensions. The person rotates it twice with Rotate Right (10 degrees total) without walking. A call makes the placement unverified. On return the chair is hidden, status explains recovery, and edits are unavailable. If the anchor resolves, actual-size placement returns; otherwise Restart Scan preserves the chosen product, or Exit AR returns immediately to its details and releases the session. This is a specified scenario, not a device test.

## Acceptance checks and status

Static document checks passed: the revised artifact explicitly covers all four supplied defects; every session state has an exit; placement requires a usable estimate and dimensions; recovery cannot present stale placement as valid; denial, unavailable hardware and failed recovery retain useful product context. The state/action and data contracts are present. These passes establish specification coverage only.

No failed static checks were identified in the final document review. The original four behaviors are confirmed defects of the supplied brief; their runtime correction remains unverified.

The following implementation acceptance scenarios were **not executed**:

| Check | Required observable result |
| --- | --- |
| Fresh launch, first AR invocation, denial, restriction, Settings return | No early camera use; prompt uses specified purpose; details remain usable; no repeated prompt loop or automatic restart. |
| Unsupported device; missing model units | Optional unavailable AR is hidden; invalid assets never enter placement or receive arbitrary scaling. |
| No floor, poor light, low texture, excessive movement | No floating chair or enabled placement without usable estimates; relevant coaching, restart and exit remain available; reminder does not gate actions. |
| Place on an estimated floor, then refine | Prompt placement; verified dimensions; plausible lighting, perspective and contact; no visible jump, detachment or false fit guarantee. Validate model units against a known physical reference. |
| Small room and seated/stationary use | Complete entry, placement, adjustment, reposition/cancel and exit without walking backward or reaching distant virtual geometry. Check offscreen cue and selection proximity. |
| Limited/lost tracking, call, app switch, camera interruption | Remove placed claim and geometry, disable edits, preserve unverified draft; restore only after resolved anchor; restart and exit work even if recovery never succeeds. |
| Rotate/drag versus buttons | Gestures and controls give corresponding results, fixed scale holds, invalid moves are rejected, feedback is immediate, system-edge gestures remain available. |
| iPhone/iPad, portrait/landscape, narrow/wide windows, enlarged text | Preserve selected product/draft; keep exit and status accessible; no clipping, target overlap or hidden essential actions at 200% text. |
| Accessibility Inspector and assistive input | Verify names, states, reading order and state announcements; complete commands with VoiceOver, Switch Control and Full Keyboard Access. Measure targets and contrast against actual camera backgrounds in light/dark appearances. |
| Data and lifecycle inspection | Camera stops and spatial draft is released on exit; frames/maps are neither recorded nor uploaded; temporary interruption preserves only intended session state. |

## Evidence and routing limits

Read the installed apple-hig root SKILL.md from `.agents/skills/apple-hig`, then searched its topic index. Read the Getting started, Technologies, Foundations, Menus and actions, and Inputs family routes; read the iOS, iPadOS, Augmented reality, Privacy, Accessibility, Buttons and Gestures topic procedures before their respective source guides. Each instruction/source read used a separate single-file command. The installed source guides identify a 2026-10-25 snapshot and are derived guidance rather than SDK references. Official links above identify supporting articles; no web browsing was performed.

Only the supplied brief and local installed instructions support this work. No app implementation, assets, screenshots, telemetry, device, SDK, GUI or accessibility execution was available. Capability detection, permission strings, coaching integration, anchor stability thresholds, performance and platform/window support need SDK and device validation during implementation. Physical safety, actual scale accuracy, surface quality, comfort, rendering, privacy behavior and accessibility cannot be established by this specification. No current API availability or independent source/media review is claimed.
