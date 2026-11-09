# iPad field-report export controls: correction plan

## Scope and evidence

This is a specification review of `interface.md`, not an inspection of a running app. Its statements are the evidence for current behavior: four equally prominent filled buttons; Delete is primary/default; Preview is glyph-only with no accessible name; actual hit regions are 20 × 20 pt with 2 pt gaps; Publish takes eight seconds without feedback and repeat activation creates duplicate uploads. All four functions must remain available. No framework or Apple SDK is assumed.

## Ranked verified findings

Ranking is a product-risk judgment, not an Apple severity scale. “Verified” below means explicitly established by the supplied brief.

| Rank | Finding and effect | Correction and source |
|---|---|---|
| 1 — High | Publish gives no feedback for eight seconds and repeat taps create duplicate uploads. People cannot tell whether publishing started and can publish repeatedly. | Immediately show activity inside Publish, label it “Publishing…”, and atomically guard all activation paths. Add request deduplication and explicit completion/failure states. The activity treatment follows [Buttons — iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS); deduplication is engineering advice to meet this product's outcome. |
| 2 — High | Delete is the editor's primary/default action. Accidental default activation can select data loss. Actual deletion scope and reversibility are unknown. | Make Publish the likely primary command; remove Delete's default mapping and prominent fill. Give Delete destructive semantics and a separate position. Generally primary should be a likely nondestructive action: [Buttons — Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Role). Resolve recovery as specified below before implementation. |
| 3 — High | Every actual target is 20 × 20 pt, with only 2 pt gaps. This increases selection difficulty and risk of choosing a neighbor, especially Delete. | Use at least 44 × 44 pt activation regions, sufficient width for labels, and clear separation. Proposed layout uses 12 pt between target boundaries and 24 pt before Delete. These gaps are product choices, not a universal HIG spacing requirement. [Buttons — Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices) recommends at least 44 × 44 pt general targets. |
| 4 — High | Glyph-only Preview has no accessible name, so its action is not identified to assistive input. | Show “Preview” and expose button role/name “Preview”. A retained decorative glyph must not create a second spoken label. [Accessibility — Vision and Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility) supports meaningful descriptions and labeled controls. |
| 5 — Medium | Four equally prominent filled buttons conceal priority and give destructive Delete the same visual emphasis as routine actions. | Keep one filled primary, Publish. Use lower-emphasis Preview and Save Draft, and a spatially separate destructive Delete. Keep peer target heights consistent; use style rather than unequal sizes for hierarchy. [Buttons — Style](https://developer.apple.com/design/human-interface-guidelines/buttons#Style) advises one or two prominent likely actions per view. |

The local guides differ in their numerical framing: Buttons gives general targets of at least 44 × 44 pt; Accessibility lists iPadOS 44 × 44 pt default and 28 × 28 pt minimum. This plan conservatively chooses 44 × 44 pt or larger. The supplied 20 × 20 pt fails both. The smaller accessibility minimum is not a reason to retain dense controls.

## Decisions and corrected action contract

All four are commands, so buttons remain appropriate; none represents persistent selection. The footer is retained. Proposed order: a separate leading Delete, then Save Draft, Preview, and trailing Publish. At narrow editor widths or enlarged text, wrap into stable rows with full labels and nonoverlapping targets; never shrink targets to fit. All custom buttons need visible press feedback, focus indication, and exposed enabled/busy states. Do not rely on red alone to identify Delete.

| Control | Outcome and scope | Role, availability and recovery |
|---|---|---|
| Publish | Publish a captured revision of the current report, including its attachments. This scope is a proposed contract, to validate against the service. | Sole primary, filled; enabled when publishable and no unresolved publish operation exists. It never deletes or dismisses unfinished work. Focused activation works; any editor-level default mapping must be Publish, never Delete, and must not intercept Return in text editing. |
| Preview | Open a read-only preview of the current report revision. | Normal, lower emphasis; visible and accessible label “Preview”. Closing returns to the editor and initiating control without losing edits. Remains usable during upload. |
| Save Draft | Persist the current editable report without publishing. | Normal, lower emphasis. Report actual save success/failure and preserve unsaved edits on failure. Remains usable during upload if draft persistence is independent; serialize it safely if the existing service shares mutable state. Never silently discard it. |
| Delete | Remove the current report, with exact local/remote scope disclosed before committing. | Destructive, lower emphasis, never the editor default. Block while Publish is unresolved, with nearby explanation “Available after publishing finishes.” |

Deletion recovery is not established by the brief. Conservative proposed behavior until its scope is resolved: activating Delete opens a confirmation identifying the report and exact loss, with Delete and Cancel and no default action. Cancel and supported keyboard cancellation leave the report intact and restore focus. Do not claim that confirmation already exists or is universally required. If investigation establishes routine, fully undoable deletion, prefer immediate deletion with a reliable Undo path instead of routine confirmation. If Assistive Access is supported, separately implement its documented two-confirmation treatment for difficult-to-reverse actions. [Alerts — Best practices and Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons) permits a default confirmation for deliberately requested destruction; the editor's unsafe default does not justify a blanket ban on that exception.

## Slow-upload state model

The eight seconds are observed duration in the brief, not a timer for declaring success. Show an indeterminate activity indicator **inside the activating Publish button**, replacing any image while retaining its label context and stable geometry. Use “Publishing…” and expose busy/unavailable semantics with a concise status announcement. Do not move focus or announce every animation frame. A spinner alone must not be the only accessible state.

Use measured progress only if the service can describe meaningful whole-operation completion; never invent percentages from elapsed time. If bytes reach 100% before server commit, say “Finishing publication…” rather than “Published”. Keep status in a stable location. Persistent success/error text should remain readable without a forced short timeout. [Progress indicators — Best practices](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#Best-practices) supports honest progress, stall explanation and safe cancellation.

```text
states = idle, publishing, reconciling, failed, published

activatePublish():                     // same handler for touch, keyboard, assistive input
  atomically:
    if state in {publishing, reconciling}: return
    if currentRevision already has acknowledged publication: show existing result; return
    capture immutable reportRevision and attachments
    obtain stable operationKey for this publication intent
    state = publishing                 // guard before starting asynchronous work
  render busy Publish("Publishing…"), status("Publishing report…")
  submit captured revision with operationKey

onAcknowledgedCommit(operationKey, publicationId):
  ignore callbacks for other operations
  record publicationId and captured revision durably
  state = published
  clear activity; show persistent "Published" and result link when available
  if editor has newer edits: show "Published revision; newer changes are unpublished"
  restore Publish only for a new publishable intent/revision

onDefinitiveFailure(operationKey):
  state = failed
  clear activity; show actionable reason and explicit Retry
  retain editor contents and captured operation context
  Retry reuses the key for the same intent

onTransportTimeoutOrLostResponse(operationKey):
  state = reconciling
  show "Publication not yet confirmed. Checking status…"
  query operation status; do not issue a new publication intent
  committed -> onAcknowledgedCommit
  definitively failed -> onDefinitiveFailure
  unknown -> retain guarded state with Check Status recovery
```

Server-side operation keys must return the same publication result for duplicate requests; a UI guard alone cannot cover retries or lost responses. Persist pending operation identity if navigation/reload can occur. These are proposed engineering requirements, not claims that the existing backend supports them. If no deduplication/status service exists, build that capability or expose an unresolved state that prevents unsafe retries; do not label uncertain publication as failed and start a fresh upload.

Keep editing, Preview and independent Save Draft usable; publish the captured revision rather than racing with later edits. Do not offer Cancel Upload until the service can guarantee what cancellation means. If safe cancellation is implemented, distinguish “request cancellation” from confirmed cancellation, preserve the draft, and resolve any concurrent server commit. No modal alert is needed for routine waiting.

## Worked before/after

**Before:** A field worker taps Publish at t=0. Nothing changes. At t=2 they tap again. The supplied behavior creates another upload. At approximately t=8 there is still no specified completion feedback. Delete remains equally prominent and the default.

**After (proposed):** At t=0 the first activation synchronously enters publishing and captures revision R17. Publish contains an activity indicator and reads “Publishing…”. At t=2 touch or keyboard reactivation creates no additional operation. Preview still opens R17/current content according to its clearly identified revision; later edits can be saved as R18. At t=8, **if** the server acknowledges R17, activity ends and the editor says “Published revision; newer changes are unpublished” when R18 exists. If the response is lost, the editor says publication is unconfirmed and checks the same operation key. It never asserts success from the elapsed eight seconds. Delete is separated, has no editor default mapping, and is unavailable with an explanation until publication is resolved.

## Acceptance checks and current status

**Passed — document inspection only:** All four original functions are retained in this contract; each has a label, role, scope and availability rule. The proposed state model covers pending, success, definite failure and uncertain completion. Local root, family routes, Buttons and Accessibility procedures and their guides were read. No implementation pass is implied.

**Failed — supplied design evidence:** Four prominent fills; destructive editor default; all 20 × 20 pt targets; unnamed Preview; absent upload feedback and duplicate suppression. These are specification failures, not executed device tests.

**Not executed — acceptance gates for implementation:**

1. Measure actual target regions: every action at least 44 × 44 pt, no overlap; verify proposed gaps and layout at narrow iPad editor widths and at least 200% text enlargement. Labels remain readable and all four functions reachable.
2. Inspect visual hierarchy in light/dark and increased contrast: only Publish has primary fill; Delete is recognizable without color. Measure actual contrast once colors/fonts exist.
3. Activate every command with supported touch, keyboard and assistive input. Confirm meaningful names, roles, focus, press feedback and busy states. Return in report text must not publish or delete. Closing Preview restores editor state; cancelling Delete changes nothing.
4. Inject an eight-second upload and bursts of activation through every input route: activity appears on initiation, one intent is submitted, and the server produces one publication. Verify unchanged button geometry and continued access to Preview/draft work.
5. Simulate definitive rejection, offline submission, lost acknowledgment after commit, repeated callbacks and navigation/reload. Preserve draft and operation identity; Retry cannot duplicate a committed report; stale callbacks cannot overwrite a newer operation.
6. Verify success only after acknowledged commit; newer edits stay unpublished. Test status announcement without focus theft or repeated chatter using VoiceOver and supported alternative input on an appropriate Apple environment.
7. Establish Delete's real scope and undo guarantees. Test either complete restoration through Undo or explicit confirmation/cancellation, including all documented exits. Verify upload/Delete races cannot remove a report during unresolved publication.

## Evidence and routing limits

Only local files and installed instructions were used; no web request was made. Official links above identify the articles behind the local snapshot, not newly verified online guidance. The installed root is `.agents/skills/apple-hig/SKILL.md`; routes were read under `subskills/apple-hig-menus-and-actions`, `apple-hig-foundations`, `apple-hig-status`, and `apple-hig-presentation`. The Buttons and Accessibility `.topics/.../SKILL.md` procedures were successfully read before their `references/buttons.md` and `references/accessibility.md` guides.

The Status and Presentation routes link to `.topics/apple-hig-progress-indicators/SKILL.md` and `.topics/apple-hig-alerts/SKILL.md`, respectively, but reads found those files missing from this installed package. Their local `references/progress-indicators.md` and `references/alerts.md` guides were used as a limited fallback after the failed procedure reads. Full procedure compliance for those two topics cannot be claimed.

There is no rendered screen, source implementation, network service, deletion contract, SDK or runtime evidence. Contrast, actual focus order, native rendering, physical target comfort, accessibility execution and device behavior remain unverified. This deliverable corrects the written interaction contract; it does not implement or demonstrate it.
