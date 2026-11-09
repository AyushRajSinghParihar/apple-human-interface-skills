# Revised claim-upload interaction specification

## Scope and evidence

Target: iPhone, iOS; framework agnostic. The supplied `interface.md` states that Submit stays unchanged for 30 seconds, then only vibrates even on failure; offline retry duplicates claims; people may leave and return; server behavior is unproven. These are the only observed product facts. No implementation, screenshots, service contract, device results, or accessibility results were supplied.

The design below is a proposed contract, including backend dependencies. Uploading bytes, submitting a claim, and approving an insurance claim are different outcomes. “Claim submitted” means the service has durably recorded this exact claim and returned its claim reference; it never means insurance approval.

## Decisions and source support

1. Acknowledge activation immediately through a visible pressed state, then an activity indicator inside the initiating button labeled “Submitting…”. Keep its position and width stable. Disable repeat submission and explain nearby: “Submission in progress.” This applies the local [Buttons, iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS) guidance. The response must not wait for the network.
2. Keep a persistent status region next to the claim action. Use honest indeterminate activity because no progress measurement is supplied. Do not invent percentages, estimates, or a countdown. Even transfer completion must not mean claim submission. Keep the same indicator form throughout active work and remove it on resolved or inactive states. See [Progress indicators, Best practices](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#Best-practices).
3. Confirm this consequential action with a durable receipt, rather than vibration alone. Keep recoverable problems inline with an explicit next step; routine progress and network errors do not need modal alerts. See [Feedback, Best practices](https://developer.apple.com/design/human-interface-guidelines/feedback#Best-practices).
4. Optional haptics supplement the visible, accessible result: one brief Success cue for newly confirmed submission, one Error cue for definitive failure, none for an unknown result. Request these semantic cues only if the host runtime supports them and settings permit them. No SDK or actuator is assumed; omission changes no functionality. Never replay cues merely on reopening. See [Playing haptics, iOS Notification](https://developer.apple.com/design/human-interface-guidelines/playing-haptics#Notification) and [Best practices](https://developer.apple.com/design/human-interface-guidelines/playing-haptics#Best-practices).
5. Preventing duplicate claims requires more than disabling a button. Durable identity, idempotent service behavior, and authoritative reconciliation below are product engineering decisions, not capabilities established by HIG or the supplied brief. Treat them as release dependencies.
6. Text and semantic status carry every essential outcome; color, animation, and vibration are supplementary. Status and receipt do not auto-dismiss. Provide labeled actions, names matching visible labels, button roles and availability, and an accessible status region exposing the current message. Notify assistive technology once per meaningful state transition, not every timer tick; do not unexpectedly move focus on asynchronous updates. Keep reading order claim summary → status → available actions. Require reflow at 200% text size and iPhone activation regions of at least 44 × 44 pt with separation. The Buttons guide gives the general 44 pt target; Accessibility lists a smaller 28 pt minimum, which this design does not adopt. See [Accessibility, Vision, Mobility, and Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility). These are requirements to verify, not measured results.

## Screen and state contract

Keep claim details and attachments available across all states. Freeze the submitted snapshot while its outcome is unresolved; explain “Submission pending; check its status before editing.” Back navigation remains available. Leaving the screen does not cancel a claim and must never imply that it does. No Cancel or Pause command is offered because safe server cancellation and resumable transfer are unproven.

Only one primary action is prominent at a time; secondary navigation remains lower emphasis. Custom controls need visible press feedback. Disabled actions expose their reason. All labels below are proposed product copy.

| State and truth source | Visible status and initiating control | Actions and transition |
| --- | --- | --- |
| Ready: valid local draft, no unresolved submission | “Ready to submit.” Primary “Submit Claim” | Submit persists identity and snapshot before any send, then enters Sending. Invalid draft shows specific field corrections instead of starting work. |
| Offline before sending: transport was never invoked | “You’re offline. Your claim hasn’t been sent. Connect to the internet, then try again.” No spinner. | Primary “Try Again” sends the same saved submission only after connectivity is available. No automatic offline queue or background-send promise. |
| Sending: request active | Button indicator + “Submitting…”. Nearby: “Sending your claim. Leaving this screen won’t cancel the request; return to check its status.” | Repeated taps, keyboard activation, and re-entry cannot create another attempt. Other navigation remains available. |
| Delayed: still active after 10 seconds without a meaningful update | Same indicator and button. “This is taking longer than usual. We haven’t confirmed submission yet.” | Continue waiting; never infer failure or success from elapsed time. Ten seconds is a proposed product threshold, not an Apple rule. |
| Unknown: connection lost after send, timeout, process interruption, or ambiguous response | Stop transfer activity when no transfer is running. “We couldn’t confirm whether your claim was submitted. Check its status before trying again.” | Primary “Check Status”; no Submit or blind Retry. A status lookup enters Checking. |
| Checking: authoritative lookup active | Indicator in “Checking…” button. “Checking whether your claim was submitted.” | One lookup at a time. Unavailable lookup returns Unknown with “Status is unavailable. Try checking again when connected.” No claim-create request. |
| Definitively not submitted: authoritative terminal result guarantees no later commit | “Your claim wasn’t submitted. [Specific safe reason and correction.] Your draft is saved.” No spinner. | “Try Again” when the reason is recoverable; “Review Claim” for validation correction. Retry keeps the identity for the unchanged snapshot. |
| Submitted: durable service acknowledgement or lookup confirms matching submission | Check symbol plus “Claim submitted”, claim reference, and server-confirmed date/time. “Submission received; this does not mean your claim is approved.” No spinner. | Primary “View Claim”; secondary “Done” returns to claims. Receipt remains reachable on return. Never offer Retry here. |

A status lookup that returns “pending” resumes the delayed/pending presentation with “Your submission is still being processed.” It does not create a new claim. A bare “not found” is insufficient to enable retry unless the service contract guarantees that no in-flight request can later commit. Without that guarantee, remain Unknown.

## Persistence, retry, and reconciliation contract

Before any create request, atomically save a durable local record containing a stable submission key, frozen payload identity, draft/attachment references, and current outcome. If persistence fails, do not send: show “Couldn’t save your submission. Try again.” Do not claim the draft is saved unless that write succeeded. Storage details and retention need implementation review.

The service must atomically deduplicate creation by an appropriately scoped submission key, reject a changed payload under an existing key, and return the same durable receipt for a repeated identical request. Its retention period must cover the supported recovery lifetime. An authoritative status operation must distinguish pending, committed, terminally not submitted, and unavailable. Races between lookup, retry, and late completion must not permit two commits.

On leaving, preserve the record. Do not promise continued transfer in the background. On return or process restart, load local state first; a nonterminal record triggers reconciliation when online, never a new create request. An offline return shows the saved state and explains that status cannot currently be checked. A stored receipt remains visible. If the local record is unavailable but a request might have been sent, do not manufacture a fresh key and silently resend; require authoritative claim-history/status recovery.

Framework-agnostic pseudocode:

```text
submit(draft):
  acquire per-draft single-flight guard
  if unresolved record exists: show/reconcile it; return
  record = persistBeforeSend(stableKey, immutableSnapshot(draft))
  if persist failed: show local-save error; return
  if offline and never sent: show OfflineBeforeSend; return
  persist sendMayHaveStarted = true BEFORE invoking transport
  show Sending immediately
  send(snapshot, key)  // only with verified service safety contract
  route response through applyAuthoritativeResult

applyAuthoritativeResult(record, result):
  ignore events for another key or snapshot
  committed receipt: persist Submitted, render receipt, optionally cue once
  terminal no-commit: persist NotSubmitted, render reason and recovery
  pending: persist Pending, show processing status
  transport error / timeout / ambiguous result: persist Unknown, offer Check Status
  never let stale pending/error overwrite a committed receipt

returnToClaim():
  render durable local record
  if unresolved and online: singleFlightLookup(key)
  if unresolved and offline: explain that status is unavailable

retry():
  allow only never-sent or authoritative terminal no-commit states
  reuse key and frozen snapshot; no new key merely because of timeout
  edited snapshot: require old attempt terminally closed before a new identity
```

If these server guarantees cannot be demonstrated, ship only truthful progress, receipt-on-confirmation, and guarded reconciliation. Keep ambiguous retries blocked with the explanation above. Provide a real claim-history or support route only after its availability is established; do not invent a contact channel. Client-side guards alone do not resolve the reported duplicate defect.

## Worked before/after

**Before (supplied):** A person taps Submit, sees no change for 30 seconds, then feels vibration even if the upload failed. Retrying offline duplicates claims. Leaving and returning has no proven recovery contract.

**After (illustrative trace, not an executed test):** Tap Submit Claim for draft D. Save key K and its snapshot, immediately show Submitting… and guard duplicate activation. At 10 seconds show the delayed explanation. At 30 seconds the connection drops after transmission: show “We couldn’t confirm whether your claim was submitted,” without a success cue. The person leaves and later returns offline: display saved pending information and Check Status with the connectivity explanation. When online, lookup K. If it returns receipt C123, persist and display Claim submitted with C123; no second creation occurs. Reopening shows that receipt without another haptic. If lookup instead guarantees terminal non-submission, offer Try Again with K. If lookup cannot determine the outcome, retain Unknown and do not resend. A verified rejection shows its reason and correction, never the success receipt.

## Acceptance checks and current disposition

**Passed — specification inspection only:** The revised contract distinguishes press, active upload, pending processing, unknown result, definitive failure, and durable submission. It defines local-save failure, offline entry, delayed response, leaving/re-entry, late replies, recovery, and an optional nonessential haptic path. It supplies no invented percentage, approval promise, or SDK dependency. Installed root → owning families → selected topic procedures → supporting guides were read from this package; the topic index was searched. No web browsing occurred.

**Failed — supplied behavior against this contract:** Unchanged feedback during the 30-second wait; tactile-only outcome that fails to distinguish failure; retry producing duplicate claims. These are brief-reported failures, not independently reproduced defects. Server persistence and re-entry safety are unknown rather than proven failures.

**Not executed — required implementation acceptance:**

| Scenario | Required observable result |
| --- | --- |
| Tap, double tap, keyboard/assistive activation | Immediate press/activity feedback; one logical submission identity and no concurrent create from repeated activation. |
| Successful response / accepted-but-pending response | Only durable matching receipt produces Claim submitted; pending never masquerades as success. |
| 30-second delay, timeout, rejection | Delayed message appears at proposed threshold; timeout becomes Unknown; authoritative rejection shows a useful correction; no false success cue. |
| Offline before send / disconnect after send | Never-sent state permits guarded retry; ambiguous state allows lookup only; exact saved-state wording is truthful. |
| Drop response after server commit, then retry/restart from multiple clients | Same identity resolves to one claim and the same receipt, backed by service logs/storage evidence. Client taps alone cannot establish this. |
| Leave, background, terminate, relaunch, late response | Recover stored identity; reconcile; no automatic fresh creation, stale overwrite of success, or repeated outcome haptic. |
| Lookup unavailable, pending, or bare not-found | Preserve uncertainty, explain next step, and avoid blind resend. |
| Persistence failure or lost local record | No send after failed initial persistence; no fresh-key resend for potentially sent work. |
| Haptics unavailable/disabled, muted audio, rapid events | Complete task using text and semantics; no cue flood; optional cues match outcomes. Validate physical timing, comfort, and camera/sensor coexistence on supported hardware if haptics are implemented. |
| Enlarged text, light/dark appearance, assistive navigation | At 200% text all status/actions reflow; measured targets meet specified geometry; contrast is measured; status and actions are reachable and understandable without color, sound, or vibration. Verify actual VoiceOver and alternative input behavior on iPhone. |

## Evidence limits and release dependencies

This deliverable is a design specification, not implemented software. No SDK compilation, backend contract test, upload, GUI session, device haptic test, contrast/geometry measurement, or accessibility execution was performed. Proposed semantic notifications do not establish actual screen-reader behavior. Service deduplication, receipt durability, authoritative terminality, recovery lifetime, attachment retention, background transport, and local storage durability remain unverified; duplicate-safe retry cannot be claimed until the relevant checks pass.

Citations are official article/section destinations supplied by the installed local guides, whose snapshots are dated 2026-10-25. They were not fetched or independently verified for currentness. No newer-release or universal hardware-support claim is made. Timing, wording, state names, persistence, and server protocol requirements are this design’s decisions; the cited HIG supports the feedback, progress, control, accessibility, and haptic principles.
