# iPhone React prototype interaction review

## Result and scope

Retain React and iPhone Safari. The supplied `interface.md` contains screenshot notes, not a screenshot, implementation, or runnable build. This review identifies one visible-label concern and several unresolved interaction questions; it does **not** establish runtime accessibility or interaction failures. No native rewrite, SwiftUI migration, or Apple SDK integration is warranted by this evidence.

The task is editing a profile. “Edit profile” is an appropriate task title. A short editor related to its parent can reasonably use a sheet-like web presentation, but the notes do not establish task length, actual modality, or whether blocking the parent is beneficial. “Panel” is descriptive here, not evidence of a native Apple panel component. A dimmed backdrop alone proves neither background blocking nor a correct focus boundary.

## Findings and decisions

| Priority / classification | Supplied evidence and consequence | Concrete decision and source |
|---|---|---|
| P1: visible affordance concern, supported by notes | Two visually small glyphs beside the form have no visible labels. Their purposes are not supplied, so their meaning and discoverability cannot be assessed. This is not proof that they lack accessible names. | Identify both actions. Prefer visible action text for unfamiliar or ambiguous glyphs; retain icon-only treatment only when its meaning is clear in context, with an accessible name. Use actionable names matching the actual operations; do not guess that these are Save/Delete. [Accessibility — Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility) supports labeled, comfortably operable controls. The visible-text preference is this review’s proposed improvement. |
| P1: measurement missing, not a confirmed target-size defect | “Visually small” describes artwork, not CSS activation regions or separation. | Inspect and measure full hit regions and spacing. The local HIG snapshot gives iOS/iPadOS **44 × 44 pt default**, **28 × 28 pt minimum**; the minimum is not a recommended dense-layout target. For this web prototype, propose 44 × 44 CSS px activation regions as an implementation starting point, then validate viewport scale, spacing and real-device usability. CSS px are not a claim of measured native points. [Accessibility — Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility). |
| P1: dismissal/data policy unspecified, not observed data loss | No dirty-state or dismissal behavior is supplied. Losing edits is a risk to investigate, not an established defect. | Adopt the exit contract below. Keep completion distinct from cancellation, and protect unfinished work consistently across supported exits. [Sheets — Anatomy and iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/sheets), [Modality — Best practices](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices). |
| P1: semantics and input behavior unverified | DOM/ARIA, focus and keyboard evidence are absent. A dimmed backdrop and title cannot establish an accessible dialog. | If the editor is modal, implement a named dialog with matching background interaction blocking, focus entry, reachable actions and focus restoration. Use semantic HTML controls and form labels. These are proposed web implementation decisions serving the HIG’s complete keyboard/assistive navigation goal, not verified behavior or an Apple API requirement. [Accessibility — Speech and Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility), [Modality](https://developer.apple.com/design/human-interface-guidelines/modality). |
| P2: contrast and reflow unmeasured | No colors, text sizes or viewport behavior are supplied. | Measure actual foreground/background pairs and test text enlargement to at least 200% without losing fields or actions. Do not infer low contrast from the intentional backdrop dimming. [Accessibility — Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). |

## Proposed React interaction contract

These decisions fill specification gaps; they are not descriptions of existing behavior.

- **Entry:** An explicit Edit profile action opens a draft initialized from the saved profile. For a short task needing focused completion, use one modal web editor titled “Edit profile”; retain parent context. If editing requires ongoing comparison with the parent, reassess blocking and use ordinary navigation or an inline editor instead.
- **Presentation:** For a single-step editor, place visible Cancel at the leading top edge and Done at the trailing edge, following the [iPhone sheet convention](https://developer.apple.com/design/human-interface-guidelines/sheets#iOS-iPadOS). Keep fields and completion reachable as the Safari keyboard changes the viewport. Allow scrolling when needed. Do not prescribe native detents, a grabber, or swipe behavior merely because this is sheet-like; these require an intentional web capability decision and testing.
- **Completion:** Done validates and saves. Keep the draft open on validation or save failure with an understandable error; close only after successful persistence, update the parent, and restore focus to the opener or a logical surviving control. This save/error policy is an engineering proposal.
- **Clean cancellation:** Cancel closes without changing the saved profile and restores focus. No Back control is needed in this single-step contract; if steps are later added, Back returns within the task and preserves edits.
- **Dirty cancellation:** Cancel and every enabled close route use one policy: retain the draft while asking whether to keep editing or discard changes. Keep editing returns to the intact draft; deliberate discard closes without saving. Do not silently discard from backdrop taps, a close glyph, Escape, or custom swipe. An explicit Save option may be added only if it uses the same validation and persistence path as Done. This implements [Modality’s content-protection guidance](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices).
- **Other exits:** Backdrop dismissal and custom swipe are optional, not established features; disabling them is a reasonable web choice when Cancel is visible. If Escape is supported, route it through the same dirty-state policy. Define browser Back separately and verify its history behavior. Reload, tab closure and process interruption require a draft-persistence decision; do not promise prevention of these events from a custom dialog.
- **Focus and semantics:** For the proposed modal, move focus into the named editor, keep navigation within it while open, prevent interaction with the background, expose each field/control’s name, role and state, and restore focus on exit. Keep the focus boundary and data policy coherent when a discard decision is shown. Avoid stacking editors. Verify actual Safari and assistive behavior rather than assuming ARIA makes it work.

## Acceptance checks and current outcomes

“Failed” below refers only to a supplied specification gap or visible concern, not a runtime test failure.

| Check | Current outcome | Acceptance evidence required |
|---|---|---|
| Preserve React web and iPhone Safari scope | **Passed — review decision** | No framework migration prescribed. |
| Identify the editing task | **Passed — notes only** | Title is reported as “Edit profile”; rendered title and accessible dialog name remain unverified. |
| Make both glyph actions understandable | **Failed — visible-label concern in notes** | Supply action meanings and rendered controls. Visible labels or demonstrably clear contextual symbols; verify accessible names separately. |
| Define completion and every dismissal’s data outcome | **Failed — original specification incomplete** | Proposed contract above is available for implementation; implementation must demonstrate each transition. |
| Measure hit regions and separation | **Not executed** | DOM/CSS dimensions, viewport scale, nonoverlapping activation areas, and physical iPhone checks. Small artwork alone must not fail this check. |
| Clean and dirty exit matrix | **Not executed** | Exercise Cancel, Done, each enabled backdrop/gesture/Escape/Back route; verify clean close, intact draft on keep-editing, deliberate discard, successful save, and retained draft after save failure. Mark intentionally disabled routes as such. |
| Background blocking and focus lifecycle | **Not executed** | Verify actual modal boundary, focus entry/order/restoration, keyboard activation and no trapped or unreachable action. |
| VoiceOver and other supported assistive input | **Not executed** | On iPhone Safari, complete entry → edit → save and cancel; check spoken names, roles/states, task order and background exclusion. Exercise supported external keyboard and assistive input paths. |
| Contrast and 200% text enlargement | **Not executed** | Actual color/typography measurements in supported appearances and enlarged-text reflow with all content/actions usable. Preserve the source’s contrast-table scope; do not claim conformance from assumed colors. |
| Keyboard, scrolling and screen fit | **Not executed** | Actual iPhone Safari runs with software keyboard open, supported viewport sizes/orientations, and reachable fields/Cancel/Done without obscured focus. |

## Evidence still missing

Needed next: the actual screenshot; meanings of both glyphs; DOM/ARIA and CSS including hit regions, spacing, viewport configuration and colors; form complexity; opening control; state/persistence code; supported exits and browser-history behavior; save/validation/error states; and supported iPhone/Safari versions. Device recordings or test results are needed for touch comfort, software/external keyboard behavior, VoiceOver and focus handling. Native rendering, haptics, SDK compilation and Accessibility Inspector execution have no evidence and are not prerequisites to retaining this web framework.

Only local file reading and specification review were performed on the headless Linux server. No browser, device, GUI, SDK or accessibility execution occurred. Runtime checks above remain pending; reading a guide does not pass them.

## Local guidance audit

Read the installed root `.agents/skills/apple-hig/SKILL.md` first, then selected routes with each topic procedure read before its source guide:

1. `subskills/apple-hig-foundations/SKILL.md` → `.topics/apple-hig-accessibility/SKILL.md` → `references/accessibility.md`.
2. `subskills/apple-hig-presentation/SKILL.md` → `.topics/apple-hig-sheets/SKILL.md` → `references/sheets.md`.
3. `subskills/apple-hig-patterns/SKILL.md` → `.topics/apple-hig-modality/SKILL.md` → `references/modality.md` (routed to resolve blocking and unfinished-work policy).

All paths above resolve within the installed apple-hig package; each file was read in a separate `cat` command. Official links identify the source articles for the local guidance; they were not browsed. The installed references are dated snapshots and derived guidance, not proof of current SDK capabilities or independently verified source coverage.
