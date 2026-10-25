# iPad field-report export controls: correction plan

Review basis: `interface.md` only; it describes behavior and hit geometry, but supplies no implementation or rendered app. Findings below are verified against that brief, not reproduced at runtime. Preserve Publish, Preview, Save Draft, and Delete as immediate commands. No Apple SDK is assumed.

## Ranked findings

Ranks reflect consequence and task access, not a measured frequency of incidents.

| Rank | Verified evidence | Effect | Correction and support |
|---|---|---|---|
| 1 — High | An 8-second Publish upload changes nothing; repeated taps create duplicate uploads. | Users cannot tell whether publishing started and can publish repeatedly. | Immediately show an activity indicator inside Publish, label it “Publishing…”, and guard activation before starting work. Preserve context. Resolve to confirmed success or an actionable failure. In-button indication is iPadOS guidance; duplicate prevention and recovery are engineering decisions. [Buttons: iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS). |
| 2 — High | Delete is the primary/default action. | The editor privileges data loss and exposes accidental default activation. | Remove its default binding and primary emphasis; mark it destructive. Publish becomes the likely nondestructive primary action. The source says “generally,” not that destructive defaults are universally forbidden. [Buttons: Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Role). |
| 3 — High | All actual hit regions are 20×20 pt with 2 pt gaps. | All four commands are difficult to select; destructive adjacency increases the consequences of a miss. | Specify at least 44×44 pt actual targets, no overlap, equal peer heights and widths sufficient for labels. Increase separation and isolate Delete. [Buttons: Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices), [Accessibility: Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility). |
| 4 — High | Glyph-only Preview has no accessible name. | Assistive navigation cannot identify the command by name. | Use visible “Preview” and accessible name “Preview”, with button semantics. Hide any redundant decorative glyph from naming. [Buttons: Content](https://developer.apple.com/design/human-interface-guidelines/buttons#Content), [Accessibility: Vision and Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). |
| 5 — Medium | All four buttons are equally prominent and filled. | The likely next action is hard to distinguish from secondary and destructive commands. | Give Publish the sole prominent fill; use lower emphasis for Preview and Save Draft, and a separated destructive treatment for Delete. Rank through style, not unequal target sizes. The guide recommends one or two prominent actions; choosing one here is a product decision. [Buttons: Style](https://developer.apple.com/design/human-interface-guidelines/buttons#Style). |

The geometry sources differ: Buttons says general hit regions should be at least 44×44 pt; Accessibility lists iPadOS 44×44 pt as default and 28×28 pt as minimum. Use the conservative 44×44 pt specification here. The supplied 20×20 pt fails both. Neither source establishes a universal numerical inter-button gap. Choose 12 pt clear separation between target rectangles for this footer as a design starting point, then validate comfort; this is not an Apple-mandated gap.

## Corrected action contract

| Control / accessible name | Outcome and scope | Role and placement | Availability / recovery |
|---|---|---|---|
| Publish | Publish a captured revision of the current report. | Primary; prominent at the trailing end of the action group. No destructive default binding. | Enabled when report is valid and no publish is pending. Busy state described below. |
| Preview | Open a read-only preview of the current report. | Normal; lower emphasis, visible text. | Available while publishing; leaving preview returns to the editor without discarding edits. |
| Save Draft | Persist the current report as a draft without publishing. | Normal; lower emphasis. | Available while publishing; save feedback must refer to the saved revision. Must not alter the pending publish snapshot. |
| Delete | Remove the current report from active reports. | Destructive, lower emphasis, spatially separated from Publish; never the editor's default. | Disabled during publishing, with explanation “Available after publishing finishes.” Proposed recovery: recoverable removal with a persistent Undo route that restores report and edits. No immediate permanent purge. |

Deletion reversibility, draft storage, publish validation, and the meaning of “published” are not documented. The recoverable deletion contract is a proposed product decision, not a verified existing capability or a universal HIG requirement. Implement recovery before enabling deletion under this contract. If permanent deletion is required instead, separately resolve confirmation and recovery before release; do not silently assume Undo exists. No confirmation policy is asserted from the unavailable Alerts procedure.

Use equal target heights of at least 44 pt, widths that fit localized labels, and at least 12 pt target separation. Reflow to multiple rows in narrow editor widths or enlarged text; retain all four functions and separate Delete. Use perceivable pressed, focused, disabled, and busy states. Destructive meaning must have a text/semantic cue as well as color. Custom implementations must provide press feedback and expose name, button role, enabled state, and busy status. Do not assign Return globally: explicit focused-button activation runs that named command; any editor primary shortcut is Publish only when valid and idle. Do not add an ellipsis merely because upload takes time.

Support at least 200% text enlargement without clipping or overlapping targets, following [Accessibility: Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). Prefer system controls when available; otherwise implement equivalent behavior in the project's stack. Actual rendering, focus, contrast, and assistive access still require validation.

## Slow-upload behavior and framework-agnostic pseudocode

Product choices below extend the HIG in-button feedback requirement. A press animation alone is not completion. Use indeterminate activity because the brief supplies elapsed time, not measurable progress; never fabricate percentages or an eight-second countdown. Keep the indicator inside the activating Publish button, replacing any image while preserving its label context and target size.

```text
publishState = idle
pendingOperation = none

onPublishActivated():
  atomically:
    if pendingOperation exists or report invalid: return
    snapshot = captureImmutableRevision(report)
    operation = createOperation(snapshot, stableIdempotencyKey)
    persistPendingOperation(operation)
    pendingOperation = operation
    publishState = uploading
  renderImmediately()  // before network work: indicator + “Publishing…”
  send(operation)

while uploading:
  ignore all Publish activation paths (touch, keyboard, assistive input)
  expose Publish as busy and unavailable, named “Publishing”
  show persistent nearby text “Publishing report…”
  allow Preview and Save Draft against clearly identified revisions
  disable Delete with its reason
  retain editor content, focus context, and pending operation

onServerConfirmedPublished(operation, publishedRevision):
  ignore stale callbacks for other operations
  record publishedRevision
  clear pending operation; publishState = succeeded
  show persistent “Published” status (identify revision if editor changed)
  announce completion through the accessibility status mechanism
  allow a new publication only by a fresh deliberate activation

onDefiniteFailure(operation):
  retain report and snapshot; publishState = failed
  show “Couldn’t publish. Your report is retained.” + explicit Retry
  announce failure; restore actionable focus without an unsolicited jump
  Retry reuses the operation key; never retry automatically on render

onTimeoutOrLostConnection(operation):
  retain pending operation; publishState = uncertain
  show “Publication not confirmed. Check status.”
  Check Status reconciles that operation with the server
  do not create a second operation while outcome is unknown
```

The backend must deduplicate a stable operation key, including retries after timeout or process restart; a disabled button alone cannot guarantee one publication. Persist pending identity before sending, and reconcile on reopening. If the service lacks reconciliation/idempotency support, that is an implementation dependency: leave uncertain publication blocked from a fresh submit and expose a recovery explanation. Do not claim “failed” or “published” from elapsed time alone. Snapshot isolation and keyed requests are proposed engineering requirements, not Apple API claims.

Keep status visible until superseded or explicitly dismissed; expose meaningful start and terminal announcements without repeatedly announcing spinner frames. Upload cancellation is not promised: the brief provides no safe server cancellation contract. Preserve the draft and do not present a Cancel control that only hides the wait while publication continues.

## Worked before / after

**Before, per brief:** At t=0 the user taps Publish. At t=2 seconds nothing has changed, so they tap again. Another upload starts. At t=8 seconds the first upload completes; the interface has given no waiting indication. Delete remains the default among four equally filled 20×20 pt targets, and Preview is unnamed.

**After, specified scenario:** At t=0 the activation guard claims operation K and the current report revision R. Publish immediately displays an in-button indicator and “Publishing…”; accessible busy state and “Publishing report…” identify the wait. At t=2 another tap or keyboard activation sends no new request. Preview and Save Draft remain usable; Delete explains its temporary unavailability. At t=8 a server acknowledgment for K changes status to “Published”; the editor and draft remain intact. If acknowledgment never arrives, status becomes “Publication not confirmed” with Check Status, retaining K. A retry after a confirmed failure reuses K. The corrected footer uses readable names, targets at least 44×44 pt, separated destructive Delete, and one prominent action. This is a worked specification, not an executed trace.

## Acceptance checks and audit results

**Passed — static review only:** Read the supplied brief; identified all four functions; matched the applicable installed Buttons and Accessibility procedures to their source guides; specified each control's outcome, semantics, target geometry, and pending/resolved behavior. The proposed contract preserves all four functions.

**Failed — supplied specification:** No activity feedback or duplicate guard; destructive editor default; 20×20 pt targets; unnamed Preview; four equally prominent filled actions. These are failures established by the brief, with no runtime reproduction claimed.

**Not executed — implementation acceptance:**

- Instrument an 8-second delayed response. Immediately after first activation, verify in-button activity and busy semantics. Repeated touch, keyboard, and assistive activation must yield one operation and one publication. Test rapid concurrent input and programmatic reentry.
- Exercise success, definite failure, timeout after server commit, reconnect, reopening, retry, and stale callbacks. Assert retained edits, correct revision reporting, stable keys, server deduplication, and no premature success claim.
- Activate each named command and verify its actual outcome. Save Draft must not publish; Preview must return without data loss; Undo Delete must restore the exact report. During upload, Delete must be unavailable with a perceivable explanation.
- Measure actual target rectangles in iPadOS points: at least 44×44 pt each, at least the specified 12 pt gap, no overlapping extensions. Test narrow editor widths, portrait/landscape, localization and 200% text enlargement; all actions remain reachable and labels unclipped.
- Verify pressed/focus/disabled/busy appearance and readable contrast in light/dark and Increase Contrast settings. Test that color is not the only role or status cue.
- On a supported iPad environment, test VoiceOver names, states, task order and announcements; Full Keyboard Access, Switch Control and pointer activation; return focus from Preview; absence of unintended default deletion; usability and selection comfort. Verify Reduce Motion retains meaningful waiting status. No such execution has occurred here.

## Evidence limits and source trail

Only `interface.md` supplies product evidence. No source implementation, screenshot, device, runtime, SDK, GUI, backend contract, accessibility tree, contrast measurements, or physical interaction evidence is supplied. Missing feedback and semantics beyond the explicit brief are unknown, not additional verified defects. No build, device test, accessibility execution, or network experiment was performed.

Guidance was read locally, without browsing. Official links above identify the corresponding articles/sections; they were not fetched. The installed source guides are a dated 2026-10-25 snapshot, not proof of current SDK behavior or independent source review.

Installed paths read in order:

1. `.agents/skills/apple-hig/SKILL.md`, then `interface.md`.
2. `subskills/apple-hig-menus-and-actions/SKILL.md` → `.topics/apple-hig-buttons/SKILL.md` → `references/buttons.md` (all relative to the installed apple-hig root).
3. `subskills/apple-hig-foundations/SKILL.md` → `.topics/apple-hig-accessibility/SKILL.md` → `references/accessibility.md`.
4. Status and Presentation family procedures were read for conditional handoffs. Their routed `.topics/apple-hig-progress-indicators/SKILL.md` and `.topics/apple-hig-alerts/SKILL.md` were absent; direct reads failed and the installed topic index still points to those missing paths. Their source guides were not used as a substitute for the missing procedures. Upload recommendations use the successfully read Buttons procedure and its iPadOS section; recovery choices are explicitly product proposals. This package gap limits the alert/progress-specific audit.
