# iPhone React prototype interaction review

## Result and evidence boundary

Keep the React web prototype in iPhone Safari. No native rewrite, SwiftUI migration, Apple SDK integration, or native sheet behavior is required by this review. Apply the interaction principles through web controls and verify browser behavior separately.

The only product evidence is `interface.md`: screenshot notes describing two visually small unlabeled glyphs beside a form, a dimmed backdrop, and a panel titled “Edit profile.” No image, implementation, measurements, or executable flow was supplied. These notes establish visual descriptions, not runtime behavior. No confirmed interaction or accessibility failure can be established from this evidence. The specification does leave important action and exit contracts unresolved.

## Findings and concrete decisions

| Priority / classification | Evidence and effect | Correction or decision | Acceptance evidence needed |
| --- | --- | --- | --- |
| P1 — unresolved action meaning; visual discoverability risk | Both glyphs lack visible text in the notes. Their shapes, familiarity, outcomes, and affected objects are unknown. Users may have to guess their purposes. This is not proof that icon-only controls violate HIG or lack accessible names. | Inventory glyph A and glyph B separately. Record each symbol, outcome, affected field/object, role, reversibility, and availability. If the symbol is not familiar and unambiguous in context, use a short visible action label. Every icon-only action needs a meaningful accessible name. Do not invent “save,” “delete,” or “clear” as their existing functions. | Inspect rendered controls and DOM; confirm the visible meaning and accessible name match the actual outcome; activate each independently. |
| P1 — unknown activation geometry | “Visually small” describes glyph artwork only. CSS hit regions and separation are absent; undersized targets and overlap are unproven. | Measure the full selectable region, including padding, separately from glyph dimensions. Use the HIG general 44 × 44 pt hit-region recommendation as the iPhone design baseline with adequate separation. For this web prototype, propose at least 44 × 44 CSS px targets as an implementation starting point, then verify viewport scaling and device usability; CSS px are not asserted to be native pt. | Inspect computed layout and hit testing at supported viewport/zoom settings. Confirm neighboring targets do not overlap and each activates reliably on iPhone. |
| P1 — unresolved presentation and data contract | A dimmed backdrop and “Edit profile” title suggest a scoped editor, but do not establish whether the parent is blocked, whether an exit exists, or whether changes are lost. | Candidate: one sheet-like web editor for a short profile task, provided focusing the edit justifies blocking the parent. Explicitly choose modal or nonmodal behavior. For the proposed modal contract below, make parent content unavailable while editing. If parallel reference to the parent is necessary, evaluate inline/nonmodal editing instead. | Trace entry, parent availability, completion, cancellation, each supported dismissal, and reopening using clean and edited data. |
| P1 — unknown focus and alternative input | DOM/ARIA, focus handling, and keyboard behavior are explicitly absent. A focus trap, background exposure, or inaccessible exit is not an observed defect. | For the proposed modal editor, give it a programmatic name from “Edit profile,” move focus meaningfully into it, keep keyboard navigation within the active modal, and return focus to its opener on exit. Use semantic HTML buttons and labeled inputs; inspect browser support before selecting a dialog implementation. | Inspect semantics and handlers, then exercise keyboard traversal/activation, dismissal, focus restoration, and VoiceOver on an Apple environment. |
| P2 — unknown contrast | No foreground/background colors, opacity values, or rendered compositions are supplied. Dimming the parent alone is not a contrast failure. | Define roles for panel surface, text, interactive controls, backdrop, and focus indication. Measure actual composited foreground/background pairs and test supported appearances and increased-contrast treatment. Do not copy native semantic-color API values into CSS as proof of adaptation. | Capture colors, font sizes/weights, appearance, calculator inputs and ratios; evaluate applicable contrast criteria. No ratios can be reported now. |
| P2 — form inspection pending | The form's fields, labels, types, formats, and validation are unspecified. No particular field defect can be established. | Map short-value inputs to Text fields guidance. Once the field inventory exists, specify persistent labels where purpose would otherwise disappear, input/keyboard type, validation moment, corrective feedback, and logical traversal. Inspect whether either glyph is a field accessory before assigning its component behavior. | Test each actual field with empty, partial, invalid, valid, and long input; verify focus order and the actual Safari keyboard. |

Source support: familiar symbols or clear action phrases, spacing and press feedback come from [Buttons — Best practices, Content and Role](https://developer.apple.com/design/human-interface-guidelines/buttons). Meaningful descriptions, alternative input, text enlargement, and actual contrast measurement come from [Accessibility — Vision, Mobility and Speech](https://developer.apple.com/design/human-interface-guidelines/accessibility). The 44 × 44 pt button recommendation and Accessibility's iOS default of 44 × 44 pt coexist with its smaller 28 × 28 pt minimum; the smaller value is not a general recommendation for dense targets. Use the conservative 44 pt baseline here without claiming an unseen failure.

Presentation decisions follow [Modality — Best practices](https://developer.apple.com/design/human-interface-guidelines/modality) and [Sheets — Anatomy and iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/sheets). A sheet can be nonmodal on iOS; the word “panel” in the notes does not establish an AppKit panel. Native detents, grabbers, and swipe dismissal are not automatically supplied by a React overlay and are not mandatory web imitations. Palette decisions follow [Color — Best practices and Inclusive color](https://developer.apple.com/design/human-interface-guidelines/color); input inspection follows [Text fields — Best practices](https://developer.apple.com/design/human-interface-guidelines/text-fields).

## Proposed editor contract

These are review decisions for completing the specification, not claims about the current implementation.

- Entry opens one “Edit profile” editor with current values and a separate draft. Preserve the parent route and context. A short, parent-related task is a reasonable sheet-like candidate; task length and the opener remain to be confirmed.
- Provide visible Cancel at the leading top edge and Done at the trailing edge. Done validates and commits the draft, then returns to the updated parent. Invalid submission retains the draft and explains correction. If saving is asynchronous, keep pending feedback and prevent duplicate submission; failure retains edits for retry.
- Cancel on an unchanged draft closes without saving. On a changed draft, retain the draft and offer an explicit choice to keep editing or discard changes before loss. Apply the same policy to every supported close path. The exact confirmation surface remains a design choice requiring its own component review; no additional stacked sheet is prescribed here.
- Do not add a custom swipe merely to resemble native UI. If backdrop dismissal, Escape, swipe, or in-app navigation away is supported, route it through the same dirty-state decision. A backdrop tap may instead leave the editor open. Document browser Back and interruption behavior explicitly; do not promise that every Safari navigation or process termination can be intercepted. For exits that cannot be reliably guarded, define draft recovery.
- Keep one main editor active. Reopen after commit with committed values, after discard with original values, and after an interrupted session according to the documented draft-recovery policy. Back within a multistep editor changes steps and retains edits; do not label whole-task cancellation “Back.”
- With the onscreen keyboard visible, retain access to the active field, feedback, and completion/cancellation controls through usable scrolling. Preserve draft and context across orientation changes and ordinary interruptions. Test text enlargement to at least 200% without losing essential labels or actions. These web adaptations implement the intent of [Designing for iOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios) and Accessibility; they do not assert native Dynamic Type support.

## Acceptance checks and current status

| Status | Check / required outcome |
| --- | --- |
| Passed — document inspection only | Target and framework are identified as iPhone Safari and React web; the review preserves both. The notes explicitly identify missing runtime evidence. “Edit profile” identifies the intended task in the supplied text. |
| Failed — specification completeness only | Neither glyph has an action contract; parent availability, field inventory, exit/data policy, and accessible interaction contract are unspecified. This does not establish an implemented UI failure. |
| Not executed | Activate glyph A and B independently; verify correct outcomes, press feedback, disabled states where applicable, meaningful names, and no unintended form submission. |
| Not executed | Measure hit regions and spacing independently of glyph artwork. Validate comfortable selection on an actual iPhone. |
| Not executed | Open the editor, traverse all fields/actions using keyboard and assistive input, confirm parent availability matches the chosen model, and verify focus restoration. |
| Not executed | For every supported exit, exercise unchanged and changed drafts. Confirm no silent loss, consistent protection, correct parent update after Done, and correct data on reopening. Exercise save failure if saving is asynchronous. |
| Not executed | Show/hide Safari's onscreen keyboard, rotate, enlarge text to 200%, and interrupt/resume. Essential content/actions remain available and useful work survives according to the recovery contract. |
| Not executed | Measure text/icon contrast against actual backgrounds in supported appearances; verify state meaning does not rely only on color. |
| Not executed | VoiceOver, Voice Control, Switch Control, Full Keyboard Access and other applicable assistive input checks on supported Apple hardware/software. No device, GUI, accessibility execution, native rendering, haptic, or SDK build result is claimed. |

## Missing evidence to close the review

Supply the actual screenshot or rendered view; the two glyph assets and intended actions; React/HTML, CSS and viewport configuration; computed target geometry; DOM/accessibility-tree names, roles and states; focus and event handlers; form field/value/validation inventory; presentation and opener context; persistence/save behavior; all supported dismissal/navigation routes; rendered color/font/appearance data; and iPhone Safari keyboard, enlargement, interruption and assistive-technology results. Missing evidence is an inspection request, not proof of failure or grounds to remove a control from scope.

## Local guidance audit

Read the installed root `/tmp/hig-eval-9w388h4y/.agents/skills/apple-hig/SKILL.md` explicitly, then searched its `references/topic-index.md` for platform, button, modality, sheet, accessibility, color, field and web concepts. Each file read used its own shell command. Paths were resolved inside that installed package.

Selected families → topic procedures → supporting references, all explicitly read in that order before making source-backed recommendations:

- `apple-hig-getting-started` → `designing-for-ios`
- `apple-hig-patterns` → `modality`
- `apple-hig-presentation` → `sheets`
- `apple-hig-menus-and-actions` → `buttons`
- `apple-hig-foundations` → `accessibility`, `color`
- `apple-hig-selection-and-input` → `text-fields`

Within each family, procedures are `.topics/apple-hig-<topic>/SKILL.md`; supporting guides are `references/<topic>.md`. Both glyphs were mapped individually to candidate Buttons procedures, the editor to Modality/Sheets, and unspecified short form inputs to Text fields. Reclassify a glyph if later evidence establishes selection or menu behavior. Safari is the host browser, not evidence of an embedded Web view, so that topic was not applied. No actual screenshot/animation was supplied for visual-example matching. Official links above identify the sources recorded in local guides; no web browsing or independent verification of those live pages occurred. The installed guides are dated application guidance derived from Apple sources, not an SDK reference or proof of current API availability.
