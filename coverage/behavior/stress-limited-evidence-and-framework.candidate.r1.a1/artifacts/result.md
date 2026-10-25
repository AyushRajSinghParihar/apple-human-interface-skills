# iPhone React web interaction review

## Result and scope

Retain React and iPhone Safari. No native rewrite, SwiftUI migration, Apple SDK dependency, or implementation change is recommended by this review. The supplied `interface.md` contains screenshot notes only, not an actual screenshot, CSS, DOM, or executable prototype. It describes two visually small glyphs without visible labels, a dimmed backdrop, and an “Edit profile” panel.

There is insufficient evidence to confirm a runtime HIG violation. The concrete result is a set of evidence-qualified review findings and a proposed interaction contract. The specification is incomplete for interaction sign-off; this is not proof that its implementation fails.

Guidance below comes exclusively from the installed local HIG snapshot. Official links identify the underlying articles; no web pages were fetched or current SDK capabilities verified.

## Findings and decisions

| Area | Evidence and classification | Effect or risk | Concrete decision |
|---|---|---|---|
| Two glyphs beside the form | **Observed in supplied notes:** visually small, no visible text labels. Their symbols, actions, familiarity, and accessible names are unknown. **Potential discoverability issue**, not a confirmed missing accessible name. | People may have to guess the commands if the symbols are unfamiliar in context. | Inventory each glyph’s action and affected object before assigning labels. Use a short action label where the symbol is unclear; a familiar contextual symbol may remain icon-only with an action-specific accessible name. Do not invent that these are Save/Delete/Close. [Buttons — Content](https://developer.apple.com/design/human-interface-guidelines/buttons#Content). |
| Touch targets | **Not assessable:** visual glyph size does not establish activation size or spacing. | Small or overlapping activation regions could cause missed or wrong actions. | Measure the actual clickable bounds and separation. Use 44 × 44 pt as the iOS HIG starting target for buttons; preserve space between targets. Do not report the glyphs as undersized without measurements. [Buttons — Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices), [Accessibility — Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility). |
| Backdrop and editor | **Observed:** dimmed backdrop and task title. **Unknown:** background blocking, task length, exit controls, focus behavior. Dimming alone establishes neither modality nor a native sheet. | A blocking editor without a clear task benefit or exit could trap people or obscure context. | Proposed assumption: profile editing is a brief parent-related task that benefits from focused editing. Keep a single React dialog styled as a sheet if this assumption holds; otherwise use ordinary page navigation or inline editing. A web element called “panel” need not be an Apple native Panel. [Modality — Best practices](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices), [Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets). |
| Dismissal and data protection | **Specification gap:** dirty-state, save, cancel, gesture, and navigation outcomes are not supplied. No observed data loss. | Different exit routes could silently discard work. | Adopt the transition contract below. Provide a visible exit and protect edits consistently across supported exits. [Modality — Best practices](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices), [Sheets — Anatomy](https://developer.apple.com/design/human-interface-guidelines/sheets#Anatomy). |
| Accessibility and keyboard | **Not assessable:** DOM/ARIA, names, focus, contrast colors, and actual keyboard behavior are explicitly absent. | Unnamed controls, unreachable fields, background focus leakage, low contrast, or keyboard occlusion are possible, unconfirmed barriers. | Specify semantic buttons and form labels, an editor name derived from its title, coherent task order, reachable completion/cancellation, and focus restoration. Measure contrast and test enlarged text and assistive input. These are implementation/verification tasks, not passed checks. [Accessibility — Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision), [Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility), [Speech](https://developer.apple.com/design/human-interface-guidelines/accessibility#Speech). |

The local sources differ in target guidance: Buttons gives a general at-least-44 × 44 pt hit region; Accessibility lists iOS/iPadOS default 44 × 44 pt and minimum 28 × 28 pt. Conservatively use 44 × 44 pt for these form actions; 28 pt is not a blanket recommendation for compact controls. These are Apple platform points, not a measured CSS result. A React implementation can start with 44 × 44 CSS px targets as an engineering choice, then verify viewport scaling and usability on iPhone; do not claim a proven physical equivalence.

## Proposed React interaction contract

This is application advice derived from the guidance, not an observation of existing behavior or a claim that every web editor must be modal.

1. **Entry:** opening Edit profile copies committed values into a draft. Preserve the parent context and initiating control. For the proposed modal variant, background content is unavailable to pointer, keyboard, and assistive navigation while editing. Use appropriate web dialog semantics and test actual browser support and behavior.
2. **Presentation:** retain “Edit profile” as the task title. Provide leading Cancel and trailing Save; Save explicitly commits the form, serving the HIG completion role described as Done. Do not add Back to a single-step task. Keep all fields and actions reachable when the software keyboard appears and when text enlarges. Native detents, grabbers, and native swipe behavior are not inferred or required merely from the web panel’s appearance. If custom resizing or swipe dismissal is added, specify and test it separately. [Sheets — iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/sheets#iOS-iPadOS).
3. **Clean exit:** Cancel closes without changing committed values and returns focus to the initiating control, or a sensible surviving parent control.
4. **Edited exit:** Cancel opens an explicit in-editor choice to Keep Editing or Discard Changes. Keep Editing restores the draft and focus to the editing task; Discard Changes closes and leaves committed values unchanged. This choice is a proposed product policy. No automatic discard is authorized by a backdrop tap.
5. **Alternate exits:** proposed backdrop behavior is no dismissal. If Escape is supported, route it through the same clean/edited exit policy. Any added close control or dismissal gesture must share that policy. Define browser Back/navigation and reload behavior separately; no promise of interception or durable recovery can be made without browser and persistence evidence.
6. **Save:** validate, retain the draft on error, explain errors by their fields, and close only after successful commitment. If completion is asynchronous, show pending feedback in Save, prevent duplicate submissions, and preserve edits on failure. On success update the parent and restore focus. These states require implementation evidence. [Buttons — iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS).

## Acceptance checks and present status

**Passed — document inspection only:** iPhone Safari and React constraints identified and preserved; supplied evidence limitations recorded; installed root → family → topic → supporting-guide routing followed. The title identifies the editing task at specification level. None of these establish runtime success.

**Failed — specification completeness only:** the supplied specification does not define the two glyph actions or the editor’s exit/data contract. Resolve these before interaction sign-off. No runtime defect has been confirmed.

**Not executed — acceptance checks for the proposed contract:**

| Check | Passing evidence required |
|---|---|
| Each glyph is understandable and operable | Action inventory matches visible label/familiar symbol and accessible name; activating each affects the intended object. |
| Targets are selectable without ambiguity | Measured clickable bounds, spacing, viewport configuration, and iPhone tapping evidence; adjacent targets do not overlap. |
| Modal behavior matches the chosen contract | Parent cannot receive interaction while open; focus enters the editor, reaches all fields/actions, remains within the modal task, and returns appropriately on close. If a nonmodal design is chosen, revise and test that contract instead. |
| Clean and dirty exits preserve the intended data | Trace Cancel, supported Escape, close/gesture paths if added, and backdrop taps in clean and edited states; Keep Editing retains the draft, Discard leaves committed data unchanged. |
| Completion and failure are coherent | Save updates the intended profile once; invalid or failed saves retain edits and present understandable errors; reopening after success shows committed values. |
| Keyboard and enlarged text remain usable | On iPhone Safari with software keyboard and supported external keyboard, reach every field and action; no essential content clips or becomes unreachable at 200% text enlargement. |
| Contrast is sufficient in actual appearances | Supply foreground/background values, sizes/weights, state colors, and measured ratios for supported appearances; evaluate applicable web contrast criteria explicitly rather than claiming HIG alone proves conformance. |
| Assistive access completes the same task | Actual iPhone VoiceOver navigation/activation verifies names, roles, states, form errors, task order, modal boundaries, and return focus; test supported Full Keyboard Access and other relevant assistive input paths. |
| Navigation/interruption has an explicit policy | Record and test browser Back, navigation away, reload, and interrupted saving against the agreed draft persistence policy. |

## Evidence still missing

- Actual screenshot and glyph identities, intended commands, parent context, task length, and existing exit controls.
- React/DOM/ARIA source, CSS activation bounds and spacing, viewport settings, form validation, focus lifecycle, and modal background handling.
- Dirty-state detection, persistence model, save outcomes, browser navigation policy, and any gesture/resizing behavior.
- Colors, typography, supported appearances, enlarged-text layouts, and software-keyboard viewport behavior.
- Executable prototype and recorded iPhone Safari, keyboard, and assistive-technology results.

No device, browser GUI, SDK compilation, native rendering, Accessibility Inspector, VoiceOver, keyboard, contrast measurement, physical comfort, or haptic execution was performed or established.

## Local guidance audit

Each file was explicitly read with a separate `cat` command, resolving paths from `.agents/skills/apple-hig/`:

- Root: `SKILL.md`.
- Foundations: `subskills/apple-hig-foundations/SKILL.md` → `.topics/apple-hig-accessibility/SKILL.md` → `references/accessibility.md`.
- Presentation: `subskills/apple-hig-presentation/SKILL.md` → `.topics/apple-hig-sheets/SKILL.md` → `references/sheets.md`.
- Menus and actions: `subskills/apple-hig-menus-and-actions/SKILL.md` → `.topics/apple-hig-buttons/SKILL.md` → `references/buttons.md`.
- Patterns, routed for modality: `subskills/apple-hig-patterns/SKILL.md` → `.topics/apple-hig-modality/SKILL.md` → `references/modality.md`.

All topic paths above are relative to their respective family directory. Supporting articles were read after their topic procedures. No claim of independent source review or newer-release verification is made.
