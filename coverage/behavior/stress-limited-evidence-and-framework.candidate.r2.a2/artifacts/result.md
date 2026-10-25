# iPhone React prototype interaction review

Decision: keep the React web prototype in iPhone Safari. The supplied notes are insufficient to establish an interaction or accessibility failure. They identify risks to investigate, not grounds for a native rewrite. This review proposes a concrete contract below; it does not claim the prototype already implements it.

## Evidence and scope

Reviewed `interface.md`: two visually small unlabeled glyphs beside a form, a dimmed backdrop, and a panel titled “Edit profile.” No screenshot pixels, code, CSS hit regions, DOM/ARIA, focus handling, dirty-state dismissal behavior, colors, or keyboard execution were supplied. “Unlabeled” here describes visible text, not an established absence of accessible names. The glyph shapes, familiarity, purposes, and action outcomes are unknown.

Only installed local guidance was consulted. Official links below identify the sources behind the local snapshot; no web pages were fetched. Native HIG conventions inform the web interaction, but native APIs, detents, grabbers, keyboard layout guides, and system rendering are not browser capabilities established by this review.

## Control inventory and findings

| Supplied element | Candidate topic | Evidence classification and effect | Concrete decision / correction if confirmed |
| --- | --- | --- | --- |
| First small glyph beside form | Buttons | Visible icon-only presentation reported; small activation region and absent accessible name are **unverified**. Unknown symbol/outcome prevents judging whether its meaning is familiar. Ambiguity could prevent choosing the intended action. | Identify its outcome and affected field/object. Use a short action label if the symbol is unfamiliar in context; give any icon-only button a meaningful accessible name. Measure its actual activation region separately from its artwork. |
| Second small glyph beside form | Buttons | Same independent evidence gap as the first; do not assume the two glyphs are Save/Cancel, or even immediate commands. | Record its own outcome, reversibility, semantic role, enabled state, and target. If it represents a persistent setting or selection, reclassify and review the corresponding control before choosing behavior. |
| Form controls, unspecified | Text fields; Virtual keyboards | Candidate mapping only: actual field types, labels, formats, validation, and input behavior are missing. No field defect can be established. | Inventory each field. For short text values use semantic HTML inputs with associated labels, appropriate content/input hints, and clear corrective feedback. Preserve partial and valid input. Route other field types when known. |
| “Edit profile” panel and dimmed backdrop | Modality; Sheets | Title identifies the task at specification level. Dimming does **not** prove background blocking, focus confinement, a native sheet, or data loss on dismissal. A short parent-related editor is a plausible sheet-like task, not a confirmed classification. | Adopt the proposed scoped editing contract below if profile editing is brief. Confirm task length and entry/return context first. A complex editor may warrant ordinary page navigation within React. |

Button recommendations follow [Buttons: content, roles, and best practices](https://developer.apple.com/design/human-interface-guidelines/buttons) and [Accessibility: mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility). Familiar symbols are allowed; visible text is not universally mandatory. Native guidance gives a general button target of at least **44 × 44 pt**, while the accessibility table lists **44 × 44 pt default** and **28 × 28 pt minimum** for iOS/iPadOS. Use the more conservative 44-point target for these buttons; do not treat the smaller minimum as a density goal. For this web prototype, adopt at least **44 × 44 CSS px** nonoverlapping hit boxes as a project implementation target, then verify viewport scaling and touch usability. CSS px and Apple pt are not asserted to be interchangeable measurements.

Field recommendations follow [Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields) and [Virtual keyboards](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards): retain understandable purpose during entry, logical traversal, suitable keyboard semantics, and visibility of both the active field and its action. HTML input hints are proposed web mechanisms; actual Safari behavior remains untested.

## Proposed interaction contract

These are review decisions to make the underspecified flow implementable, not observed repairs or additional universal Apple requirements.

1. **Entry and scope:** the profile edit entry opens one brief editor titled “Edit profile,” containing a working draft of current values. Preserve the originating page and scroll context. Keep unrelated navigation outside the editor. Confirm that a focused temporary task benefits the product before retaining a blocking presentation.
2. **Parent availability:** for this proposed modal variant, prevent background interaction and background keyboard/assistive navigation while open. Tie dialog semantics to the visible title; move focus to a sensible initial element and restore it to the opener or a logical fallback on exit. These DOM/focus details are web implementation decisions requiring runtime verification.
3. **Actions:** provide visible Cancel at the leading top edge and Save at the trailing top edge. Save is the explicit commit action; Cancel exits without committing. “Save” is an outcome-specific web label; the sheet guide describes Done as the finish/save action. Do not rename the existing glyphs until their actual functions are known. Back, if later needed for an internal step, returns within the editor and retains edits.
4. **Draft protection:** clean Cancel closes. Dirty Cancel retains an uncommitted draft and closes; reopening restores it with a clear “Unsaved draft” indication. This reversible draft-retention policy is a proposed product choice. It avoids silently discarding created work without inventing an unobserved confirmation dialog. Save success updates the profile, clears the retained draft, and returns to the parent. Invalid input or save failure keeps the editor and entered values available with corrective feedback. If saving is asynchronous, show pending state and prevent duplicate commits.
5. **Other exits:** backdrop taps do not dismiss in this proposed version. Do not add a custom swipe gesture merely to imitate a native sheet. Any implemented Escape or other controlled dismissal uses the same draft policy as Cancel. Browser navigation, reload, and app interruption require an explicit persistence design and tests; do not claim React can intercept every browser/system exit. Preserve the draft across the agreed interruption scope before release.
6. **Available space:** let content scroll so the active field and Save remain reachable when Safari chrome or the software keyboard changes the viewport. Accommodate portrait, landscape, and at least 200% text enlargement without losing labels or actions. Do not disable browser zoom.

The task scope, clear exit, and draft protection are grounded in [Modality: best practices](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices). A short related editor and leading/trailing action placement follow [Sheets: iOS and iPadOS](https://developer.apple.com/design/human-interface-guidelines/sheets#iOS-iPadOS). Native sheet resizing/swipe conventions are not automatic requirements to simulate in Safari. Keyboard clearance follows [Virtual keyboards](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards); enlargement follows [Accessibility: vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). Context retention and orientation checks follow [Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios).

## Acceptance checks and current status

**Passed — static review only:** platform and React constraint identified; supplied title names the editing task; both glyphs, form, and presentation mapped to candidate topics; missing evidence separated from confirmed defects. The title check establishes only the documented wording, not rendering or announcement.

**Failed — confirmed prototype behavior:** none established from the supplied evidence. This is not a finding of conformance.

**Not executed — implementation acceptance:**

| Check | Acceptance result required | Missing evidence / execution |
| --- | --- | --- |
| Each glyph | Outcome and accessible name match; any unfamiliar symbol has explanatory visible text; activation produces that outcome and press feedback. | Action inventory, DOM, rendered controls, activation tests. |
| Touch access | Hit boxes meet the adopted web target, do not overlap, and can be selected independently. | Computed geometry, viewport configuration, iPhone touch checks; artwork size alone is insufficient. |
| Entry and modal boundary | Title is announced appropriately; focus enters sensibly; background cannot be activated in this modal variant; closing restores a useful focus position. | DOM/ARIA and actual Safari keyboard/VoiceOver navigation. |
| Clean and dirty exit | Clean exit closes; every implemented dirty dismissal preserves the same draft; reopen restores it; Back retains it; success clears obsolete drafts. | State logic, persistence scope, executable clean/dirty transition tests. |
| Save | Invalid/partial values are retained with useful feedback; valid Save updates once; pending/failure leaves a usable recovery path. | Field schema, validation rules, save behavior and failure execution. |
| Text entry and traversal | Every field retains its purpose during entry; required characters are available; logical keyboard order reaches fields and actions. | Field markup, keyboard/content hints, Safari software and hardware keyboard tests. |
| Viewport and enlargement | At 200% text size and supported orientations, labels remain legible and both active input and completion action remain reachable with keyboard open. | Rendered layout, supported device/OS matrix, actual resizing and keyboard tests. |
| Contrast | Measure actual foreground/background pairs, including states and supported appearances, against applicable contrast criteria. | Color values, composited backgrounds, text sizes/weights, measurements. Dimming proves neither adequate nor inadequate contrast. |
| Interruption and navigation | Agreed draft persistence survives app switching and controlled navigation; reload/browser Back behavior is documented and verified without breaking normal navigation. | Persistence requirements, implementation, iPhone Safari execution. |
| Alternative access | Complete entry, editing, save, and cancellation using supported keyboard and assistive paths without a required complex gesture. | VoiceOver, Switch Control and other relevant Apple-device testing; no accessibility execution supplied. |

No device, browser GUI, SDK build, native rendering, physical comfort, or accessibility execution was performed. Proposed checks are not passes. No implementation files were supplied or changed.

## Guidance audit trail

Installed package root: `.agents/skills/apple-hig/`. Explicitly read root `SKILL.md`, then searched `references/topic-index.md` for the supplied concepts and component/framework terms. Read these family → topic procedure → supporting guide routes, each file in its own `cat` or `rg` command:

- `subskills/apple-hig-getting-started/SKILL.md` → `.topics/apple-hig-designing-for-ios/SKILL.md` → `references/designing-for-ios.md` (platform procedure and guide before component procedures).
- `subskills/apple-hig-foundations/SKILL.md` → `.topics/apple-hig-accessibility/SKILL.md` → `references/accessibility.md`.
- `subskills/apple-hig-menus-and-actions/SKILL.md` → `.topics/apple-hig-buttons/SKILL.md` → `references/buttons.md`.
- `subskills/apple-hig-patterns/SKILL.md` → `.topics/apple-hig-modality/SKILL.md` → `references/modality.md`.
- `subskills/apple-hig-presentation/SKILL.md` → `.topics/apple-hig-sheets/SKILL.md` → `references/sheets.md`.
- `subskills/apple-hig-selection-and-input/SKILL.md` → `.topics/apple-hig-text-fields/SKILL.md` and `.topics/apple-hig-virtual-keyboards/SKILL.md` → their respective `references/text-fields.md` and `references/virtual-keyboards.md`.

Topic and reference paths in each route are relative to the named family directory. The index's Web views route concerns embedded in-app web content; the supplied target is a website in Safari, so React alone does not justify applying that route or prescribing an embedding/native architecture. No actual screenshot or animation was supplied, so no visual-media-specific claims were made. Local guides identify their snapshot as 2026-10-25; independent source/media review and current online verification are not implied.
