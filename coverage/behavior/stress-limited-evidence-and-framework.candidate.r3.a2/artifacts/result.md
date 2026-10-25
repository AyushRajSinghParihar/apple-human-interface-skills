# iPhone Safari prototype review

The React web framework stays. The supplied specification does not establish a confirmed runtime HIG violation. It establishes two visually small glyphs without visible labels, plus a dimmed backdrop and an “Edit profile” panel. These warrant inspection and a clearer interaction contract; they do not justify a native rewrite.

## Evidence and classification

Reviewed `interface.md`, which contains screenshot notes only. No actual screenshot, implementation, measurements, interaction recording, or device results were supplied. “Observed” below means documented by those notes, not independently inspected pixels.

| Item and candidate topic | Evidence-backed result | Concrete decision and remaining question |
| --- | --- | --- |
| Glyph 1 beside form → Buttons | Visually small, no visible label. Its symbol, purpose, role and outcome are unknown. Potential discoverability problem, not a proven inaccessible button. | Inventory its outcome, affected object and reversibility. Use a familiar symbol only if its context explains the action; otherwise add a short visible verb label. Supply a matching accessible name if it is an action. |
| Glyph 2 beside form → Buttons | Same evidence limits; do not assume it is Save, Cancel, Clear or Delete. | Review independently using the same contract. If either glyph represents a persistent setting or opens choices, route to the corresponding selection/menu procedure before choosing behavior. |
| Both glyphs → Buttons, Accessibility | Small artwork does not establish small hit regions. CSS regions, separation, accessible names and press states are absent. | Measure actual activation regions and overlap. Provide meaningful semantics and perceivable press feedback for custom buttons. Target failure and missing names remain unverified. |
| Form → Text fields | No field inventory, labels, formats or validation supplied. | Treat text fields as a candidate, not proof of field types. Inspect each actual field’s persistent purpose, input type, validation timing, corrective feedback, overflow and Tab order. Do not invent a password, email or validation defect. |
| “Edit profile” panel → Sheets, Modality | Title identifies the task. A short parent-related edit is a plausible sheet-like task. Duration, entry, exits and parent interactivity are unknown. | Provisionally retain a single scoped editor. Establish whether focused editing benefits from blocking the parent. Dimming alone proves neither modality nor correct blocking. |
| Dismissal → Sheets, Modality | No dirty-state or dismissal behavior supplied. | Specify consistent data protection across supported exits. Silent loss is a risk to investigate, not an observed defect. |
| Focus and keyboard → Accessibility, Keyboards; scope-check Focus and selection | No DOM/ARIA, focus sequence or actual keyboard behavior supplied. | Inspect browser semantics and test the whole task. Missing evidence proves neither a focus trap nor complete accessibility. |
| Contrast → Color, Accessibility | No foreground/background colors or compositing data supplied. | Measure rendered pairs in supported appearances and states. A dim backdrop is not evidence of low panel contrast. No ratio or contrast failure can be reported. |

HIG support: [Buttons — best practices, content and roles](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices), [Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields#Best-practices), [Sheets — anatomy and iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/sheets), [Modality](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices), [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility), and [Color](https://developer.apple.com/design/human-interface-guidelines/color#Inclusive-color). These links identify official sources underlying the installed local snapshot; no online verification was performed.

## Proposed interaction contract

The following is review advice for the next prototype revision, not a description of existing behavior or an Apple-mandated web implementation.

1. Entry opens “Edit profile” with the current saved values and an isolated draft. Keep the parent context. Provisionally make this a modal web editor only if the product confirms a short, focused editing task; prevent background activation while it is modal. If parallel interaction is useful, explicitly choose nonmodal behavior instead.
2. Provide visible Cancel at the leading top edge and Done at the trailing edge for a single-view sheet-like editor. Done is the likely nondestructive completion action; Cancel exits without committing. Do not relabel the unidentified glyphs until their purposes are known. Back, if steps are later added, returns within the editor and preserves the draft.
3. Done validates and commits to the intended profile, then returns to its parent. Invalid input stays editable with clear correction guidance. If saving is asynchronous, indicate progress in the activating button, prevent duplicate submission, and retain the draft on failure. Close only after successful completion.
4. For clean Cancel, close directly. Proposed reversible policy for dirty Cancel: close without changing the saved profile but retain a recoverable draft; reopening explicitly offers to resume it. This avoids silently throwing work away. Persistence scope and expiry require a product decision. Any supported backdrop dismissal, custom gesture or Escape follows the same policy. Browser navigation and interruption need a separately verified recovery policy; do not promise interception of every Safari exit.
5. For the provisional modal implementation, expose the editor’s name and modal semantics, move DOM focus inside on entry, keep keyboard interaction within the active task, and restore focus to its opener on exit. Associate form labels and errors with their fields. These are proposed web engineering measures supporting accessibility; adding ARIA alone does not prove they work.
6. Keep necessary fields and completion actions reachable with the onscreen keyboard visible, in portrait/landscape and with text enlarged. Use normal browser inputs/buttons where suitable and preserve browser/system navigation and editing commands. Do not add a decorative grabber or promise native detents and swipe behavior unless those web interactions are deliberately implemented and tested.

The scoped task, exit naming and unfinished-work protection follow [Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets#iOS-iPadOS) and [Modality](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices). Draft retention and the specific DOM strategy are reviewer choices. Handheld reach, interruption and orientation checks follow [Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices). Keyboard access follows [Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards#Best-practices) and [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Speech).

## Acceptance checks and status

**Passed — document review only:** target platform and React constraint identified; all described controls mapped to candidate procedures; editor title names its task. None of these establishes runtime compliance.

**Failed — specification completeness:** action identities, exit/data policy and measurable interaction evidence are absent. This is a review-readiness gap, not proof that the implementation fails.

**Not executed — implementation/device acceptance:**

| Check | Acceptance criterion and required evidence |
| --- | --- |
| Action meaning | Record each glyph’s visible content, accessible name, role, outcome, object, availability and reversibility. Activate each and confirm the named result. Use visible text when an unfamiliar symbol would hide meaning. |
| Target geometry | Inspect computed layout and hit testing, including edges and spacing; targets must not overlap. The Buttons guide recommends general hit regions of at least 44 × 44 pt. Accessibility lists 44 × 44 pt as the iOS default and 28 × 28 pt as its minimum: use 44 pt as the conservative design baseline, not 28 pt as a density goal. These are Apple point dimensions, not a verified CSS-pixel equivalence. Establish the browser viewport/zoom mapping and validate physical selection on iPhone. |
| Completion and exits | Trace clean and edited Done/Cancel, supported Escape/backdrop/gesture paths, navigation away and reopening. Saved values change only on successful commit; draft recovery works as specified; Back never abandons the task. Exercise delayed save and failure if applicable. |
| Modal boundary | If modal, pointer and keyboard cannot activate the parent. Focus enters the editor and returns to its opener; no unreachable control or inescapable task. If nonmodal, document and verify the intended parent interaction. |
| Assistive access | On iPhone Safari, verify meaningful names, roles, values, task order, field/error associations and all exits with VoiceOver; verify supported keyboard and Switch Control task completion. Record actual device/OS/browser/settings and results. |
| Form and viewport | With actual fields, test empty, partial, invalid, valid and long input, plus applicable locale rules. At 200% text enlargement, portrait/landscape and keyboard-open sizes, essential content and actions remain reachable without loss of draft or clipped labels. |
| Contrast | Obtain computed rendered foreground/background colors, opacity/backdrop composition, font sizes/weights and states. Record calculator inputs/results for supported light/dark and increased-contrast treatments. Apply the relevant source criteria with their scope; do not equate a single ratio with overall accessibility conformance. |

The size guidance differs in general recommendation versus platform default/minimum; the conservative baseline above preserves both statements. See [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices) and [Accessibility — vision and mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility). The Focus and selection article marks iOS unsupported in its component-focus sense; this does **not** establish that Safari DOM focus, VoiceOver or keyboard access is inapplicable. Its iPad focus-group model is not prescribed here. See [Focus and selection](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Platform-considerations).

## Missing evidence and audit trail

Next review needs the actual screenshot, glyph/action inventory, React markup and handlers, CSS/computed hit geometry, form schema, save/draft policy, parent and exit behavior, rendered colors, viewport assumptions, and recorded iPhone Safari interaction/accessibility results. These can change the provisional decisions above.

Read the installed root `apple-hig/SKILL.md` first, then `interface.md`; searched `references/topic-index.md` for platform, web, buttons, sheets, modality, accessibility, fields, keyboard and contrast concepts. Read the owning family SKILL.md, then each routed topic SKILL.md before its supporting reference, for Designing for iOS, Buttons, Sheets, Modality, Accessibility, Text fields, Keyboards, Color, and Focus and selection. All paths were resolved inside `.agents/skills/apple-hig/`, with one file per shell command. Safari is the browser host, not evidence of an embedded Web view, so no native Web-view migration was inferred.

Only local file review and report creation were performed. No web browsing, SDK compilation, GUI, device, touch-comfort, keyboard, assistive-technology or accessibility execution was performed. Native rendering, haptics and API support are not claimed.
