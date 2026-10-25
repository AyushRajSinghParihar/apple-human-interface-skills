# iPhone React prototype review

Review result: the supplied specification is insufficient to establish interaction or accessibility compliance. No runtime defect is confirmed. Keep the React web prototype; no SwiftUI, UIKit, SDK migration, or automatic native rewrite is recommended or authorized.

Evidence inspected: `interface.md` contains screenshot notes, not an actual screenshot, implementation, or running prototype. It describes two visually small unlabeled glyphs beside a form, a dimmed backdrop, and a panel titled “Edit profile.” All conclusions below are limited to those notes.

## Findings and decisions

| Evidence/classification | Effect or risk | Concrete decision and source |
| --- | --- | --- |
| Observed in notes: two small glyphs without visible labels. Their shapes, meaning, and actions are unspecified. This is a discoverability concern, not proof that icon-only controls violate HIG. | People may not predict what activation does; familiarity cannot be assessed. | Inventory each glyph's action and affected field/object. Use a short action label when the symbol's meaning is unclear; a familiar contextual symbol can remain. Give each actionable icon a meaningful accessible name. Do not invent names such as Delete or Save before identifying the action. [Buttons — Content](https://developer.apple.com/design/human-interface-guidelines/buttons#Content), [Accessibility — Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility). |
| Unknown: actual activation areas and separation. Small visible glyphs do not establish small hit regions. | Missed or accidental taps are possible but unproven. | Measure both selectable rectangles and their separation. Use the general 44 × 44 pt hit-region guidance as the iPhone design baseline, allowing small artwork within larger targets. The accessibility guide separately lists iOS/iPadOS default controls at 44 × 44 pt and minimum controls at 28 × 28 pt; that smaller minimum is not a blanket recommendation. These local passages differ in scope; conservatively target 44 × 44 pt rather than declaring every smaller control a confirmed violation. [Buttons — Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices), [Accessibility — Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility). |
| Observed: “Edit profile” identifies a task; dimming suggests presentation emphasis. Unknown: whether the parent is blocked, task length, or actual surface type. | Dimming alone cannot prove modality, a native sheet, or an inappropriate presentation. | Provisionally use one scoped editor for a short profile edit. Make it modal only if focusing on this task benefits the person; otherwise use in-context editing or ordinary navigation in React. A long editor needs reassessment. The word “panel” in the notes does not establish Apple's platform-specific Panel component. [Modality — Best practices](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices), [Sheets — Best practices](https://developer.apple.com/design/human-interface-guidelines/sheets#Best-practices). |
| Unknown: visible completion/cancellation controls, dirty-state policy, outside-tap, swipe, browser navigation, and keyboard exits. | Silent edit loss or an unclear exit would be a serious issue if reproduced. No such failure is established here. | Adopt the proposed exit contract below. HIG calls for an obvious exit and protection of created work across button and gesture exits. [Modality — Best practices](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices), [Sheets — Anatomy and iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/sheets#iOS-iPadOS). |
| Unknown: DOM/ARIA, focus, colors, and keyboard behavior. “Unlabeled” in the notes establishes no visible text labels, not absent accessible names. | Screen-reader, keyboard, or contrast barriers remain possible, unverified concerns. | Inspect semantics and actual color pairs; then execute the complete edit task with supported input methods. No accessibility failure or pass can be assigned from these notes. [Accessibility — Vision, Mobility, Speech](https://developer.apple.com/design/human-interface-guidelines/accessibility). |

## Proposed React interaction contract

These are review recommendations and explicit product assumptions, not descriptions of existing behavior or new universal Apple requirements.

- Entry: activating the identified profile-edit command opens “Edit profile” with current values copied into a draft. Preserve the parent context. For a modal implementation, make the background unavailable to interaction and assistive navigation while open; move focus into the named editor and restore it to the invoker on exit, or a logical replacement if it no longer exists.
- First view: show visible Cancel at the leading top edge and Done at the trailing edge, following iPhone sheet conventions. Done commits; Cancel exits without committing. Do not use Back for whole-task dismissal. This does not assert that either of the two unknown glyphs currently represents these actions. [Sheets — iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/sheets#iOS-iPadOS).
- Clean cancellation: close and leave stored profile data unchanged. Dirty cancellation: retain the draft while offering explicit Keep Editing and Discard Changes outcomes. Discard closes without committing; Keep Editing returns to the draft. This recovery choice applies consistently to every app-controlled dismissal path.
- Completion: validate, commit once, and return to the parent with updated profile values. If saving is asynchronous, prevent duplicate commits, show progress in the activating control, and retain the draft with an actionable error on failure. [Buttons — iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS).
- Outside tap, swipe, supported Escape, and browser Back/navigation: document which are supported. Any app-controlled exit that is offered follows the same dirty-state policy; do not promise interception of browser termination or all browser navigation without evidence. Do not claim native swipe, detents, grabber behavior, or draft persistence across reloads. If resizable sheet behavior is deliberately implemented, specify its sizes and accessible resizing; otherwise do not add a decorative grabber implying unavailable interaction.
- Use semantic web controls and intentional button types in React; associate form labels and errors with fields, provide action names and perceivable press/focus states, and ensure Enter cannot trigger an unintended command. These are implementation recommendations applying the interaction/accessibility goals, not verified API guidance or a native requirement.

Apple dimensions above remain in pt and scoped to iOS/iPadOS guidance. For the web prototype, document the CSS-pixel target policy and viewport configuration and measure on iPhone Safari; do not claim a verified pt-to-CSS-pixel equivalence from these notes.

## Acceptance checks and current status

**Passed — static review only:** identified the supplied iPhone Safari platform and profile-edit context; preserved the React constraint; read the installed root, selected family routes, routed procedures, and supporting local guides. The notes supply a task-specific title. None of these passes establishes runtime usability.

**Failed — confirmed behavior:** none established by the supplied evidence. The specification is incomplete for acceptance because the following checks cannot be evaluated.

| Check to execute | Acceptance condition | Current status / evidence needed |
| --- | --- | --- |
| Both glyph actions | Each action, scope, name, role, and outcome are identifiable; familiar symbols or visible labels explain them. | Not executed; need actual screenshot, action inventory, DOM/accessibility names. |
| Touch targets | Measure actual regions against the documented iPhone baseline; adjacent activation regions do not overlap and each activates only its intended action. | Not executed; need CSS/layout measurements and iPhone Safari touch testing. |
| Exit matrix | Clean and edited Cancel, supported outside tap/swipe/Escape/navigation exits follow the contract; no silent draft loss; reopening shows current committed values. | Not executed; need implemented event/state policy and flow execution. Unsupported paths must be explicitly recorded. |
| Commit and recovery | Done updates the intended profile once; invalid fields remain editable; asynchronous failure retains work and supports retry. | Not executed; need save/validation implementation and controlled success/failure runs. |
| Modal boundaries and focus | If modal, background cannot be operated; entry, field order, error access, completion, and focus restoration work without trapping users. If nonmodal, parent availability matches its declared contract. | Not executed; need DOM/focus code and Safari keyboard/assistive execution. |
| Assistive access | Names, roles, states, values, and task order identify both glyphs and every form action; the whole task is operable. | Not executed; need actual iPhone VoiceOver and relevant supported alternative-input checks. Static ARIA inspection alone cannot pass this. |
| Enlarged content and keyboard | At least 200% text enlargement preserves essential fields/actions without clipping or overlap; the on-screen keyboard does not prevent reaching validation or completion. | Not executed; need rendered layout and iPhone Safari keyboard/reflow checks. [Accessibility — Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). |
| Contrast and feedback | Actual text/control states remain distinguishable against their backgrounds, including the backdrop context and supported appearances; custom buttons show press feedback. | Not executed; need foreground/background values, rendered states, contrast measurements, and interaction evidence. No numerical contrast failure can be inferred. |

## Evidence boundary and instruction audit

Local-only review; no web browsing, device, SDK, build, GUI, keyboard, contrast-tool, or accessibility execution was performed. Official links identify the source articles referenced by the installed snapshot; they were not fetched. The supplied notes cannot establish native rendering, physical comfort, haptics, accessibility conformance, or runtime correctness.

Installed package root: `.agents/skills/apple-hig/`. Read the root `SKILL.md` explicitly. Then read each selected family `SKILL.md`, its topic procedure, and the supporting article, with one file per shell command:

- Presentation → `.topics/apple-hig-sheets/SKILL.md` → `references/sheets.md`.
- Menus and actions → `.topics/apple-hig-buttons/SKILL.md` → `references/buttons.md`.
- Foundations → `.topics/apple-hig-accessibility/SKILL.md` → `references/accessibility.md`.
- Patterns → `.topics/apple-hig-modality/SKILL.md` → `references/modality.md`, following the presentation/sheets modality handoff.

All family paths resolve under `subskills/apple-hig-<family>/` in that installed package. These are framework-agnostic procedures. An absent platform subsection is not evidence of support, nonapplicability, or identical platform behavior.
