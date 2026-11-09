# Daily treatment tasks — revised interaction specification

## Scope and evidence

Design for iOS on iPhone, using framework-agnostic controls and state contracts. The task is to read prescribed care and record what happened. `interface.md` supplies only three observed behaviors: a dense spreadsheet of clinician terminology, missed tasks labeled “Failure,” and symptoms automatically shared with every contact. No screens, implementation, prescription examples, storage architecture, or permission flows were supplied. Other behavior below is a proposed product decision, not a finding about existing code.

The app must never generate, reinterpret, reschedule, or modify treatment. Recording completion does not authorize another dose or activity. Clinical content and any plain-language equivalent require clinician approval; if no approved equivalent exists, retain the original and offer a definition rather than inventing instructions.

## Decisions and source basis

| Decision | Reason and local HIG basis |
|---|---|
| Replace the spreadsheet with a grouped daily navigation list. | Patients need to find a task, not compare many clinical columns. Show identifying content first and put long instructions in detail. [Lists and tables: Content and Style](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables#Content). |
| Use a short task-to-detail-to-record path, preserving context on return. | Suits brief iPhone checks and interrupted use. [Designing for iOS: Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices). |
| Replace “Failure” with factual recording states. | Blame-free, direct language answers what happened and what can be recorded. Avoid assuming health literacy or a particular family/support structure. [Writing: Best practices](https://developer.apple.com/design/human-interface-guidelines/writing#Best-practices), [Inclusion: Welcoming language](https://developer.apple.com/design/human-interface-guidelines/inclusion#Welcoming-language). |
| End automatic contact sharing; require a deliberate, scoped send. | Minimize data transfer, explain purpose, and leave unrelated recording usable without optional access. The exact one-entry/one-recipient contract below is a product choice applying [Privacy: Best practices and Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission). |
| Use labeled actions, readable reflow, explicit states and generous targets. | Preserve meaning without color, sound, fine gestures, or small text. [Buttons: Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices), [Accessibility: Vision and Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision), [Typography: Supporting Dynamic Type](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type), [Layout: Adaptability](https://developer.apple.com/design/human-interface-guidelines/layout#Adaptability). |

These are applications of the installed HIG snapshot, not claims that Apple prescribes this treatment workflow. No HealthKit integration, Apple SDK, notification service, or system contact access is assumed.

## Screen and navigation contract

### 1. Today

Reading order: “Today,” localized date, “Record care from your prescribed plan,” task groups, then supporting destinations “Record a symptom,” “History,” and “Sharing history.”

Group all of today's task instances by their prescribed time or period, in prescribed chronological order. Preserve clinician order for ties. Put tasks without a prescribed time in “No set time.” Do not invent a time. Each row contains:

- Clinician-approved patient-facing title; otherwise the original title.
- Prescribed time/period and any essential distinguishing information, such as side or medication strength, copied faithfully.
- Text status: “Not recorded,” “Done,” or “Not done.” Where an unrecorded scheduled time has passed, add “Scheduled time passed”; this never changes the record to “Not done.”
- A navigation disclosure. Activating the row opens that exact task instance; it never records completion.

No percent score, streak, failure badge, red-only status, or bulk completion. All instances remain reachable through vertical scrolling; do not silently hide completed or older unrecorded tasks. History provides prior dates with the same detail path, not a new treatment schedule. Returning from detail restores row position and selection.

Empty day: “No tasks are listed for today.” Offer “View prescribed plan.” This is not a claim that no care is needed. Missing/unavailable plan: “Your prescribed plan isn’t available. Try again.” Offer “Try again”; show previously saved content with its version/date and a clear stale label if available. Never synthesize substitute tasks.

### 2. Task detail

Reading order: task title, record status, prescribed time, full original instructions, plan source/version, approved definitions, record actions. Keep all clinically meaningful dose, duration, route, limits and qualifiers visible in the original instructions. Definitions explain terms without replacing instructions. No generated summary may become the source of treatment directions.

“Record Done” saves a patient report for this instance. “Record Not Done” saves that report without demanding a reason. Both are commands, not on/off toggles. Show “This records what happened; it does not change your prescribed plan.” Do not say “Take now,” “Catch up,” “Double,” or suggest treatment changes when a task is late or not done.

After saving, persistently show “Recorded: Done” or “Recorded: Not done,” the reported event time and recording time, plus “Correct Record.” This opens a separate correction screen. It offers “Record Done,” “Record Not Done,” and “Clear Recorded Status”; clearing returns to unrecorded while retaining a correction history. Do not confuse changing a record with changing the prescription. Save corrections as new revisions, without silently overwriting prior reports.

Event time defaults to now and is displayed before commit. “Change Event Time” opens a labeled date/time entry screen with an explicit offset/timezone and “Use Time.” Invalid or future times receive a nearby remedy: “Choose a time at or before now.” A historical entry affects only the identified instance. Canceling time entry leaves the prior value.

### 3. Symptom recording

“Record a Symptom” opens a screen with a labeled “What did you notice?” text field, displayed event time, and “Save Symptom.” No diagnosis or automated treatment recommendation. Text: “Saving does not send this to anyone. This app does not monitor entries for urgent care.” Saving makes a private entry; sharing is a separate subsequent action. Back preserves a clearly labeled local draft; reopening restores it. A visible “Discard Draft” action can clear unsaved text. Do not require a contact to save.

## Recording and persistence model

```text
Prescription(version, source, exactInstructions) is immutable here
TaskInstance(id, prescriptionVersion, prescribedSchedule) is immutable here
RecordRevision(id, instanceId, report = done | notDone | unrecorded,
               eventTime, recordedAt, priorRevisionId)
SymptomEntry(id, text, eventTime, recordedAt, revision)

on recordCommand(instanceId, report, eventTime):
    validate instance identity and eventTime
    disable duplicate commit for this operation ID
    show Saving within activating button; preserve screen and values
    atomically persist RecordRevision
    if durable save succeeds: render recorded status and Correct Record
    otherwise: keep prior status and draft; show
      "Couldn’t save this record. Try again." plus Retry
```

A press animation is not evidence of persistence. Operation IDs make retries idempotent. Never show “Recorded” before durable save. Durable local recording may work offline; if the implementation cannot provide it, retain the draft and explicitly report that saving is unavailable. No patient-contact transfer is part of save or background synchronization. Any future account-sync design requires a separate, accurate data disclosure.

Retain selected day, task ID, scroll position, event time and draft across app interruption, rotation and restoration. On resume, label drafts “Not saved.” If the plan changed while interrupted, preserve the original task/version with its draft, identify the newer plan, and require review before recording against the old instance. Do not move a report to a different task. Midnight does not rewrite yesterday's instances; preserve their date. Retain schedule timezone/offset; do not recalculate treatment schedules from travel or clock changes.

## Sharing and data-purpose contract

| Data | Purpose | Access and transfer |
|---|---|---|
| Prescribed task/version and patient reports | Display care and preserve accurate recording | Private app storage; minimum identifiers needed to associate reports. No contact fan-out. |
| Symptom text and event time | Patient's own record | Private save; excluded from contact transfer until explicitly selected. |
| Recipient name and destination | Address one requested send | Enter explicitly; no address-book scan or launch-time Contacts request. Validate destination and show it in review. |
| Exact selected payload and delivery receipt | Send the reviewed entry and expose delivery state | Only to the chosen recipient after Send; receipt stores recipient, payload revision, time and outcome. No automatic future-entry access. |

From a saved symptom entry, “Review Sharing” opens a normal review screen. Initial recipient is empty. Show the exact payload (selected symptom text and timestamp), full recipient name/address, and “This sends this entry once. Future entries stay private.” Do not include other symptoms, treatment records or plan information implicitly. Recipient selection alone never sends. “Back” returns without transfer. “Send Entry” is enabled only with a valid destination and saved payload; explain missing requirements inline. Editing the entry or recipient invalidates the prior review and requires reviewing the updated payload.

On Send, create an idempotent transaction bound to recipient and payload revision; disable repeat activation and show “Sending” in the button. Show “Sent to [name/address]” only on confirmed delivery evidence. For a timeout with unknown outcome, show “Delivery not confirmed,” offer “Check Delivery,” and do not retry as a new send. A definite failure offers Retry using the same transaction. No automatic offline queue: “You’re offline. Nothing was sent. Review again when connected.” Leaving an unresolved send does not erase its receipt/status.

Sharing history shows what was sent, to whom and when. State: “Stopping future sharing cannot retrieve a copy already sent.” This version has no standing grants; correction or deletion of a private record does not retract recipients' copies. Existing automatic sharing rules and queued fan-out jobs must be disabled before rollout; do not grandfather blanket consent. Preserve an honest history of known past transfers. Previously sent copies cannot be promised recoverable. App Store privacy disclosures must match the implemented storage and transfer behavior.

## Controls, presentation and accessibility

Use one prominent likely action per action screen: record on task detail, save on symptom entry, send on sharing review. Keep secondary commands text-labeled and discoverable. Back follows the existing navigation path and supports the iOS back gesture; no essential action requires a swipe, long press, voice, or timed response. Correction and sharing use ordinary navigable screens, avoiding a dependency on an Apple sheet API.

Specify actual hit regions of at least 44 × 44 iOS points with nonoverlapping spacing, regardless of visible glyph size. This uses the buttons guide's general target recommendation and accessibility guide's iOS default; the latter's smaller 28 × 28 pt minimum is not the density target. Provide visible pressed, focused, disabled and waiting states. Return/keyboard activation must not send from the symptom editor or advance past sharing review.

Use semantic title, heading, body, status and button roles. Body starts at the iOS 17 pt default or equivalent framework metric, with Regular or stronger legible weights. Support system text preferences or equivalent resizing to at least 200%, Bold Text, and the largest supported accessibility size. Grow rows, wrap essential labels, stack metadata/actions and allow vertical scrolling rather than shrinking or horizontal spreadsheet scrolling. Respect safe regions in portrait and landscape. Keep action controls reachable above the keyboard.

Expose task navigation as a named action including task title, prescribed time and status; expose detail actions separately without nested competing targets. Status changes must be programmatically available and announced without stealing focus. After save, retain focus at the result/action area; after Back, return to the originating row. Provide text for every status, and persistent save/send outcomes rather than transient sound or toast alone. No celebratory animation is needed; any transition must retain meaning with Reduce Motion.

Use adaptive foreground/background colors. Measure actual combinations in light, dark and Increase Contrast appearances. As a conservative product target, require at least 4.5:1 for all task text; this is stricter than some rows of the local Accessibility Inspector contrast table and is not a claim of universal HIG or WCAG conformance.

## Worked before → after

Illustrative fixture only: the brief supplies no actual clinical task. Assume a clinician supplies “ROM exercise, 09:00” and approves “Range-of-motion exercise” plus a definition. The original instructions remain unchanged and are not invented here.

**Before:** The patient scans a spreadsheet of clinical terms. At 10:00 an unrecorded row reads “Failure.” Recording a symptom sends it to every contact automatically.

**After:** Today shows “Range-of-motion exercise · 09:00 · Not recorded · Scheduled time passed.” Opening it reveals the exact prescribed instructions and the approved definition. The app offers recording actions without advising whether to perform the exercise now. The patient chooses “Record Not Done”; after durable save, the screen reads “Recorded: Not done” with event and recording times and “Correct Record.” No prescription fields change.

The patient saves “I noticed discomfort” as a symptom. It stays private. On “Review Sharing,” the patient enters a chosen recipient and reviews the exact entry. Back sends nothing. Returning, reviewing and choosing “Send Entry” sends only that revision once to that recipient. Other contacts and later entries receive nothing. A delivery timeout remains “Delivery not confirmed,” rather than claiming success or duplicating the message.

## Acceptance checks and evaluation status

**Passed — specification inspection only:** The revised contract has an explicit iOS target, grouped row-to-detail behavior, neutral states, immutable prescribed care, private symptom save, scoped send review, correction history, save/delivery distinctions, and interruption/reflow requirements. The worked example exercises the intended task without adding treatment. These are properties of this document, not a running app.

**Failed — supplied description:** It explicitly uses dense clinical spreadsheet presentation, “Failure” labels and automatic symptom fan-out. These conflict with this revised contract. No geometric, semantic, security or runtime defect beyond that description was established.

**Not executed — implementation acceptance:**

| Scenario | Observable pass condition |
|---|---|
| Time passes without a record | Status remains Not recorded; neither a missed-care assertion nor new treatment instruction appears. |
| Save, rapid double activation, storage failure, retry | One durable revision on success; failure preserves draft and prior status; retries do not duplicate records. |
| Correct Done to Not done, then clear | Correct task/version changes; prior revisions remain; prescription and schedule are identical before/after. |
| Long/empty list and prior dates | Every expected instance is reachable; empty and unavailable states differ; Back restores the correct row; no patient reorder alters prescribed sequence. |
| Symptom save with no recipient/offline | Recording can complete privately where local persistence is available; no contact access or send occurs. |
| Sharing review, Back, recipient/payload edit | No send before explicit Send; changed payload/destination must be reviewed; only the displayed revision and recipient are transferred. |
| Delivery failure, timeout, duplicate press | Sent is shown only with evidence; unknown delivery is distinguishable; one transaction prevents duplicate transmission. |
| Existing automatic sharing migration | Old rules and queued fan-out are inactive before new flow is enabled; no implicit future grants remain. |
| Interrupt/relaunch, rotate, cross midnight, receive new plan | Task identity, drafts and times survive; unsaved state is explicit; no automatic report reassignment or schedule mutation. |
| Narrow/short landscape, portrait, keyboard, 200% and largest text, Bold Text, long translated strings | Full instructions/status/actions remain readable and reachable without overlap or horizontal table scrolling; safe regions remain clear. |
| Actual target and contrast measurement | Hit regions meet the specified 44 pt design target without overlap; text meets chosen 4.5:1 target in each appearance; measurements are recorded. |
| VoiceOver, Switch Control, Full Keyboard Access, AssistiveTouch | Same entry-to-save-to-review path completes; names, roles, states, task order and focus restoration match the contract; no speech or complex gesture is essential. |
| Sound off and Reduce Motion | All outcomes remain perceptible and persistent; no essential meaning depends on motion or sound. |
| Patient/clinician and localization review | Approved titles/definitions preserve exact clinical meaning; neutral copy is understandable and respectful; date/time formats are unambiguous. |

## Evidence limits and audit trail

Only supplied local material and installed instructions were used; no web browsing occurred. Official URLs above identify the supporting articles, not live verification. The installed references identify snapshots retrieved on 2026-10-25 and describe themselves as original application guidance derived from Apple sources. Their presence does not establish independent review or current SDK availability.

Auditable route: explicitly read installed `apple-hig/SKILL.md`, then `interface.md`; searched `references/topic-index.md` for everyday concepts and controls. Read the owning family SKILL.md files for getting-started, foundations, layout-and-organization, and menus-and-actions; read the procedures for Designing for iOS, Writing, Inclusion, Privacy, Accessibility, Typography, Lists and tables, Buttons, and the routed Layout procedure before their supporting source guides. Paths were resolved within `.agents/skills/apple-hig/`; each file read used a separate shell command. Typography consultation covered its introductory guidance through the start of its numerical tables; no claim depends on unread platform tables. No screenshot or animation was supplied, so no media explanation was required.

No code, device, SDK compilation, GUI rendering, accessibility execution, contrast calculation, hit-region measurement, physical reach testing, clinical validation, security audit or legal compliance evaluation occurred. Storage, recipient verification, transport, migration, retention periods and account behavior require implementation evidence and product review before release. The specification does not establish clinical efficacy, emergency monitoring, successful delivery, native appearance, or accessibility conformance.
