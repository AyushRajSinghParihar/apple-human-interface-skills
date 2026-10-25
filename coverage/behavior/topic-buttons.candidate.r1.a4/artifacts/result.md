# iPad field-report export controls: correction plan

## Scope and evidence

This is a specification review of `interface.md`, not an executed app audit. The supplied description establishes the current behavior: four equally prominent filled footer buttons; Delete is primary/default; Preview is glyph-only without an accessible name; every hit region is 20 × 20 pt with 2 pt gaps; an eight-second Publish upload has no feedback and repeated taps create duplicate uploads. Preserve Publish, Preview, Save Draft, and Delete. All four are immediate commands and map to the Buttons procedure, including Preview, whose result is opening a preview rather than publishing.

Read the installed apple-hig root, then the Menus and actions → Buttons, Status → Progress indicators, Foundations → Accessibility, and Presentation → Alerts family/topic/source routes. Paths resolve under `.agents/skills/apple-hig/`; each file was read separately. Official links below identify the articles represented by the local snapshot; no web retrieval occurred.

## Ranked verified findings

Ranks are product risk judgments; evidence is the supplied description rather than runtime reproduction.

| Rank | Observed problem and effect | Correction and source |
| --- | --- | --- |
| 1 — High | Publish remains unchanged for eight seconds and repeated taps create duplicate uploads. People cannot distinguish an accepted request from a missed tap and can publish repeatedly. | Immediately show activity **inside Publish**, retain its context, and guard the operation before starting asynchronous work. Define completion and recovery explicitly. In-button activity is iPadOS guidance; request locking and idempotency are engineering decisions. [Buttons: iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS), [Progress indicators: Best practices](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#Best-practices). |
| 2 — High | Delete is primary/default in a report editor. Default activation favors data loss rather than the likely editing/export task. Actual deletion reversibility is unknown. | Remove Delete's primary/default role. Choose Publish as the single prominent nondestructive editor action; this assumes publishing is the main footer task. Keep Delete separate and lower emphasis with destructive meaning. This is the editor, not an explicit destruction-confirmation alert; the alert exception does not justify this editor default. [Buttons: Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Role). |
| 3 — High | Preview has no accessible name. Its action cannot be identified by name through accessibility semantics. | Prefer visible “Preview” and an accessible button name “Preview”; an optional glyph is decorative. Do not rely on a tooltip or glyph recognition. [Accessibility: Vision and Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). |
| 4 — High | Actual hit regions are 20 × 20 pt with only 2 pt separation, making adjacent actions difficult to target, particularly beside Delete. | Use at least 44 × 44 pt nonoverlapping activation regions, with generous separation. Adopt 12 pt clear gaps between these bezelled targets as a project layout choice, increasing separation around Delete where room permits. Reflow instead of shrinking. [Buttons: Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices), [Accessibility: Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility). |
| 5 — Medium | Four equally prominent filled buttons obscure the preferred action. | Give Publish the sole prominent fill; use lower-emphasis Preview and Save Draft, and a clearly labeled, lower-emphasis Delete. Keep peer target heights equal; rank through style rather than unequal sizes. HIG recommends one or two prominent likely actions; choosing one here is a product decision. [Buttons: Style](https://developer.apple.com/design/human-interface-guidelines/buttons#Style). |

Geometry qualification: the local Buttons guide gives a general minimum of 44 × 44 pt. Accessibility lists iPadOS default 44 × 44 pt and minimum 28 × 28 pt. Use the conservative 44 × 44 pt target for this footer; 20 × 20 pt fails both. The Accessibility source suggests around 12 pt padding for bezelled elements; it does not establish a universal 12 pt inter-button gap. No exact universal gap violation is claimed solely from the supplied 2 pt value.

## Corrected action contract

Use ordinary semantic buttons in the available framework, with visible press, focus, and disabled states. A native component is preferred when available, but no Apple SDK is required. Maintain text labels, button roles, accessible names matching the labels, and state semantics in a custom implementation. Labels and status must survive at least 200% text enlargement; wrap/reflow the footer into rows rather than clip labels or overlap targets. [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons), [Accessibility: Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision).

| Control | Outcome / role / placement | Availability and behavior |
| --- | --- | --- |
| Publish | Publish an immutable snapshot of the current report revision. Primary emphasis, trailing in the main action group. | Enabled when valid and no publish operation is unresolved. Default activation may invoke it only in an appropriate command context; Return inside a report text field still edits text. While busy, retain its bounds and show spinner plus “Publishing”; if it has an image, replace that image with the spinner. Expose accessible name “Publish” and busy/disabled state with status “Publishing report.” |
| Preview | Open a preview of current content; normal role and lower emphasis. | Remains available during upload. Returning preserves the editor and upload status. Preview never starts an upload. |
| Save Draft | Persist current edits as a draft; normal role and lower emphasis. | Remains available during upload. It saves the current revision without changing the frozen publishing snapshot. Show success only after the relevant persistence confirms; on failure retain edits and offer retry. Storage location is not established by the brief. |
| Delete | Delete the current report; destructive meaning, separated from the main group, never editor default. | Temporarily unavailable during unresolved publishing, with adjacent explanation “Publishing must finish before this report can be deleted.” Recovery/confirmation depends on actual deletion semantics, below. |

These concurrency choices are proposed product behavior. If editing continues during upload, label the result “Published revision [identifier]; newer edits are not published” when appropriate. Do not let an older completion overwrite current edits or claim all current content is published.

### Delete decision gate

The brief does not establish irreversible loss, undo, or an existing confirmation; absence of confirmation is **not** a verified finding. Before shipping, establish the actual consequence and recovery guarantee. If destruction is uncommon and irreversible, present “Delete Report?” with a truthful message naming what is lost, “Cancel” and “Delete Report.” Use no default to require deliberate reading; Cancel does not become the default. Cancel or supported Escape/Command-Period leaves the report intact and restores focus to Delete. Confirm commits only the named deletion. For routine undoable deletion, prefer reliable recovery over an unnecessary alert; specify and verify restoration before choosing that branch. Do not claim Undo already exists.

The alert guide allows a normal default for confirmation of explicitly requested destruction; choosing no default here is a conservative product choice, not a universal prohibition. Assistive Access, if supported, needs its separate difficult-to-reverse-action confirmation treatment. [Alerts: Best practices and Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons), [Accessibility: Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility#Cognitive).

## Slow-upload state model (framework-agnostic)

```text
state = idle | publishing | checkingOutcome | failed | succeeded
operation = {id, reportId, frozenRevision, payload}

on Publish activation:
  atomically:
    if state in {publishing, checkingOutcome}: return
    if current revision already confirmed published: show that result; return
    validate current report; if invalid: explain and focus error; return
    create and persist operation with stable unique id and frozen payload
    state = publishing
  render busy Publish immediately, before awaiting network work
  send operation using id as server idempotency key

on confirmed publication(operation.id, receipt):
  ignore stale/mismatched callbacks
  persist receipt and published revision
  state = succeeded; remove activity; show persistent “Published” status
  allow Publish again only for a new eligible revision

on definitive failure with no publication:
  state = failed; remove activity
  retain report and operation; show actionable inline error and Retry

on timeout / lost connection / ambiguous response:
  state = checkingOutcome
  keep operation locked; show “Publication status unknown. Checking…”
  reconcile by operation id; do not create a new publication blindly

on Retry:
  atomically guard repeated activation
  reuse the same operation id and frozen payload
  resume sending or reconciliation; restore in-button activity
```

The server must deduplicate the operation ID and return its original result, including across retries/restarts. A UI lock alone prevents local repeated taps but cannot guarantee uniqueness after a network ambiguity. Backend support is not evidenced; this is an implementation dependency and acceptance gate.

Use indeterminate activity because no whole-operation progress measurement is supplied. Eight seconds is the supplied scenario, not a promised duration or a reason for a fabricated percentage. Keep indicator shape/location stable. Announce meaningful state changes accessibly without repeatedly moving focus or announcing spinner frames. Success requires a publication receipt, not merely request acceptance or uploaded bytes. Errors and success stay in context; ordinary waiting should not trigger an alert. [Progress indicators](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#Best-practices), [Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts#Best-practices).

Cancellation support is unknown. Do not expose a Cancel action that falsely promises to retract an already committed publication. If safe cancellation is implemented, retain the draft and confirm cancellation with the service before unlocking the operation; if partial work would be lost, explain that consequence and allow resuming. The initial correction must tolerate an eight-second wait and uncertain outcomes without requiring cancellation.

## Worked before/after

**Before:** A person taps Publish at t=0. Nothing changes. They tap again at t=2 and t=4; the supplied behavior creates duplicate uploads. The nearby primary/default Delete also makes accidental default activation consequential.

**After:** At t=0 the first activation atomically registers operation `R42-rev7-op1`, freezes revision 7, and changes Publish to an in-place spinner with “Publishing.” At t=2 and t=4 further tap, keyboard, or assistive activations are ignored by the same guard. Preview and Save Draft remain usable; Delete explains its temporary unavailability. At t=8 a confirmed receipt produces “Published revision 7” and removes the spinner. If revision 8 was edited meanwhile, those edits remain and can be published as a new operation. If the response is lost instead, show the unknown-status state and reconcile `op1`; a retry reuses `op1`, preventing a second publication when the server supports the specified contract.

## Acceptance checks and current status

**Passed — specification inspection only:** all four required functions are retained; every supplied control maps to Buttons; the proposed contract covers roles, labels, geometry, pending/resolved behavior, and recovery. The local reading route and source qualifications are documented.

**Failed — current interface, as explicitly described:** single-operation Publish behavior; visible upload feedback; safe editor default; named Preview; adequate target size; restrained primary emphasis. These are verified brief-level failures, not reproduced runtime failures.

**Not executed — implementation acceptance gates:**

1. Hold the publication response for eight seconds. First activation immediately shows in-button activity; rapid taps and mixed input activation create one operation and one publication. Repeat with concurrent callbacks, retry, restart, and a lost success response; verify server records by operation ID.
2. Exercise success, definitive failure, ambiguous timeout, prolonged stall, and reconciliation. No fake percent, premature “Published,” permanent spinner after resolution, lost draft, or stale callback changes current content. Retry is actionable and uses the same operation.
3. Measure actual targets at ≥44 × 44 pt, nonoverlapping, including the glyph/label edges and reflowed layouts. Check 200% text, narrow iPad windows, and long localized labels; preserve all four actions and status.
4. Inspect semantic names, roles, disabled/busy states and status announcements; run VoiceOver, Switch Control, Full Keyboard Access and pointer paths on a supported iPad environment. Preview is named and each action is reachable. Text-field Return does not publish or delete. Busy feedback retains focus/context.
5. Verify Preview and Save Draft during upload preserve report content and operation identity. Test saving newer edits, then receipt of an older publication; status accurately names the published revision.
6. Establish deletion reversibility and implement the matching recovery branch. Test confirmation, cancellation, keyboard exits, focus restoration and repeated activation; no unintended deletion or stacked confirmations. Test supported Assistive Access behavior separately.
7. Inspect press/focus/disabled styling, contrast in actual light/dark appearances, and non-color destructive identification. Verify physical targeting comfort on device; numeric layout checks alone do not prove it.

## Evidence limits

Only `interface.md` and installed local instructions/guides were used. No rendered app, source implementation, backend, measurements beyond the brief, or test harness was supplied. No device, GUI, accessibility technology, SDK compilation, network upload, contrast calculation, or backend test was executed. The corrected behavior is a reviewable specification, not a claim of an implemented fix. Publication semantics, persistence, deletion recovery, cancellation, and idempotency support require implementation evidence. Local guidance is a dated derived snapshot, not independently verified current Apple documentation; the linked official articles were not browsed.
