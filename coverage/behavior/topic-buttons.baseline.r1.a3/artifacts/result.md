# iPad field-report export controls: correction plan

Review basis: `interface.md`, a textual interface description. All findings below are verified against that description, not an executing application. Preserve Publish, Preview, Save Draft, and Delete. This specification is framework agnostic.

## Ranked findings

Priority reflects likely impact and recovery cost; it is an audit judgment, not an Apple severity scale.

| Rank | Verified observation and effect | Correction and source |
| --- | --- | --- |
| 1 — High | Repeated Publish taps create duplicate uploads during the 8-second operation. This can create unintended repeated publications. | Atomically admit one publish operation, suppress repeat activation, and deduplicate requests across retries. The concurrency mechanism is an engineering decision supporting reliable immediate actions; HIG supplies the feedback guidance in rank 4. |
| 2 — High | Delete is the primary/default action. Routine default activation can select data loss. All four buttons are equally prominent filled buttons, obscuring priority. | Make Publish the single prominent, nondestructive primary action; Preview and Save Draft secondary; Delete a separated destructive action with an explicit text label. HIG generally assigns primary to a likely nondestructive action and recommends one or two prominent buttons per view: [Buttons — Style and Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Style). Publish priority is a proposed product decision based on the export task, not verified usage research. |
| 3 — High | Every hit region is 20 × 20 pt with 2 pt gaps. Small, crowded targets increase mistaps, especially beside Delete. | Use at least 44 × 44 pt hit regions, nonoverlapping, with clear separation. Use 12 pt between filled/bordered controls as an initial layout choice, then validate. [Buttons — Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices) recommends general hit regions of at least 44 × 44 pt. [Accessibility — Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility) lists iPadOS default 44 × 44 pt and minimum 28 × 28 pt, with around 12 pt padding for bezelled elements. These source formulations differ; 20 × 20 fails both, and this plan conservatively adopts 44 × 44. Neither source establishes a universal 12 pt interbutton gap. |
| 4 — High | Nothing changes during the 8-second Publish upload. People cannot tell whether activation registered or work is continuing. | Immediately show press feedback, then an activity indicator inside Publish and the label “Publishing…”. Keep its position and context stable. Use honest measurable progress only when available. [Buttons — iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS), [Progress indicators — Best practices](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#Best-practices). |
| 5 — High | Glyph-only Preview has no accessible name. Assistive interaction cannot identify its purpose reliably. | Show “Preview” text, optionally with the familiar glyph; expose the accessible name “Preview”, button role, enabled state, and activation. Provide equivalent semantics for every action. [Accessibility — Vision and Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision), [Buttons — Content](https://developer.apple.com/design/human-interface-guidelines/buttons#Content). |

## Decisions and corrected behavior

- Keep four direct action buttons in the footer. Use equal target heights; communicate priority through style rather than size. Put Delete apart from the routine workflow. Reflow into additional rows when narrow iPad windows, enlarged text, or localization require it; do not shrink targets or truncate action names to retain one row.
- Publish activates immediately without a routine confirmation. Set its busy state synchronously before starting network work. While busy, its repeat activation does nothing; expose its busy/unavailable state and announce “Publishing report” once without moving focus. Keep visible status in a consistent place. Success means server-confirmed publication, not merely bytes sent.
- Keep Preview available for the captured report version and Save Draft available for local edits. Publish captures an immutable version; edits or subsequent saves do not silently change the upload. Temporarily disable Delete while publication outcome is unresolved, with nearby explanation “Publishing; deletion unavailable.” These are product concurrency decisions; all four functions remain available in their applicable states.
- At success, show persistent inline “Published” status with the report version or timestamp, stop the indicator, and announce completion. Prevent accidental publication of the same unchanged version again; a changed version can be published as a new intentional operation.
- On a known failure, retain the report and show a specific inline explanation plus Retry. Retry uses the same operation identity. If delivery is uncertain, show “Checking publication status…” and reconcile before offering another publication. Never claim failure merely because the client timed out. Explain a genuine stall with a recovery route. These recovery details are product decisions supported by [Progress indicators — Best practices](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#Best-practices).
- Do not fabricate percentages from elapsed time or assume every upload lasts eight seconds. Keep the in-button activity indicator; if trustworthy whole-operation progress exists, add a consistently placed progress bar without replacing the spinner with a different shape midtask. If upload reaches 100% before server processing ends, label that phase explicitly and continue activity feedback.
- Offer cancellation only if the transport and server can honor it safely. Confirm cancellation outcome before showing “Canceled”; an uncertain outcome still needs reconciliation. Do not require cancellation merely because an upload takes eight seconds. HIG says to allow cancellation where safe and to consider pause when cancellation loses useful partial work.
- Delete reversibility is unspecified. Prefer recoverable deletion with Undo if the data model supports it; common undoable deletion generally needs no confirmation. For uncommon irreversible deletion, explain the affected report and consequence in a confirmation with Delete and Cancel. Choose no default there to encourage deliberate reading. Do not claim the missing confirmation is a verified defect. The alert-specific exception permits a normal default confirming deliberately requested destruction; it does not justify the editor's Delete default. [Alerts — Best practices and Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons). If Assistive Access is supported, the local accessibility guidance calls for two confirmations for difficult-to-reverse actions in that mode; do not impose that rule on ordinary iPadOS use.

## Framework-agnostic operation contract

```text
state = idle | publishing | reconciling | failed | published
operation = { id, reportId, immutableVersion, payload }

on Publish activation:
  atomically:
    if state in {publishing, reconciling}: return
    if immutable current version already confirmed published: return
    capture current report as operation with unique durable id
    persist operation before dispatch
    state = publishing
  render busy button and accessible status immediately
  send operation with idempotency key = operation.id

on response for current operation.id:
  confirmed success -> persist receipt; state = published
  confirmed failure with no publication -> state = failed
  timeout / ambiguous delivery -> state = reconciling
  render status; announce meaningful transition once

on Retry after known failure:
  atomically admit one retry; reuse operation.id and immutable payload
  state = publishing; send operation

on reconciliation:
  query outcome by operation.id
  success -> published
  confirmed absent -> permit retry with same operation.id
  unknown -> remain reconciling; preserve payload and status/recovery path
```

The backend must enforce uniqueness atomically for an operation ID and return its existing result on replay; client disabling alone cannot guarantee this. Persist and reconcile pending operations after reconnection or restart. Ignore stale callbacks for other operation IDs. A changed payload needs a new operation ID after the previous operation is resolved. This is a required service contract for the proposed duplicate prevention, not evidence that such a service already exists.

## Worked before/after

**Before (supplied):** Four equally filled 20 × 20 pt targets, 2 pt apart; Delete is default; Preview is an unnamed glyph. At t=0 the person taps Publish. Nothing changes. At t=2 they tap again; another upload starts. The first upload takes eight seconds, with no feedback during that interval.

**After (specified):** Publish alone is prominent; Preview and Save Draft are secondary, and Delete is separated and destructive. All targets are at least 44 × 44 pt. Preview has a visible and accessible name. At t=0, Publish captures version 7 under operation A, immediately shows its indicator and “Publishing…”, and announces the status. A second tap at t=2 is ignored before dispatch. Preview can show version 7; local edits can still be saved. At t=8, a server-confirmed receipt marks version 7 Published, stops activity, and announces completion. Exactly one publication exists for A. If the response is lost instead, the UI enters reconciliation and retrieves A's outcome; it does not create operation B. This is an illustrative expected trace, not a measured run.

## Acceptance checks

These are proposed checks; none has been executed on an implementation.

1. Inspect hierarchy and keyboard activation: Publish is the only primary editor action; Delete never receives the editor's default activation. Each function remains reachable. All actions have press, focus, and unavailable feedback as applicable.
2. Measure all four effective hit regions at ≥44 × 44 pt with no overlap. Check separation and accidental activation risk in narrow windows and with enlarged/localized labels. At 200% text enlargement, labels, status, and actions remain usable without target shrinkage.
3. Inspect semantic output: each action has a meaningful name and button role. Preview is announced as Preview. Busy state, completion, and errors are perceivable without relying on animation or color. Verify focus remains predictable and status is not repeatedly announced on every progress tick.
4. With an eight-second delayed response, observe immediate press/busy feedback and continuous activity until confirmed outcome. Send rapid touch, keyboard, and assistive activations: one admitted operation and one publication result. Check client and server evidence, not just disabled styling.
5. Simulate timeout after server success, offline recovery, restart, duplicate request replay, and late callbacks. The same operation ID reconciles to one receipt; uncertain delivery never starts a new publication automatically. Failed uploads retain report content and offer a safe retry.
6. Feed real progress, unknown progress, and delayed finalization: no invented percentage, premature Published state, unexplained frozen indicator, or disruptive spinner-to-bar replacement. Confirm any cancellation claim against actual server outcome.
7. Check Preview and Save Draft during publishing, immutable uploaded-version behavior, and Delete availability after resolution. Validate the selected reversible/irreversible deletion branch and confirmation focus behavior. Test a changed version as a separate intentional publication.
8. On an actual iPad implementation, test VoiceOver, Voice Control, Full Keyboard Access, Switch Control, pointer/touch use, enlarged text, light/dark appearance and contrast. Use available accessibility inspection tools when feasible. These require later runtime evidence.

## Evidence limits and instruction trail

Only `interface.md` and the installed local apple-hig instructions/references were used. No web browsing, rendered interface, source implementation, SDK, device, GUI, accessibility execution, network service, or measured upload trace was available. Colors, actual contrast, focus order, persistence, deletion reversibility, cancellation support, and server idempotency remain unverified. Official links above are attribution from the local snapshot, not independently fetched current pages. The package identifies its articles as derived guidance; local existence does not establish independent source review.

Read from installed package `.agents/skills/apple-hig/`, using one file per read command:

1. Root `SKILL.md` explicitly read before routing.
2. `subskills/apple-hig-menus-and-actions/SKILL.md` → `references/buttons.md` within that family.
3. `subskills/apple-hig-status/SKILL.md` → `references/progress-indicators.md` within that family.
4. Root `references/topic-index.md` searched for exact component routes.
5. `subskills/apple-hig-foundations/SKILL.md` → `references/accessibility.md` within that family.
6. `subskills/apple-hig-presentation/SKILL.md` → `references/alerts.md` within that family, as explicitly routed by Buttons' destructive-role advice.

Each selected family's procedure was consumed before its source guide. No further topic procedure was routed by those family instructions. No screenshot or animation was supplied, so no visual-example reference was required.
