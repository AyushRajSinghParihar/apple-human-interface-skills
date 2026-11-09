# Daily treatment tasks — revised interaction specification

## Scope and evidence

Target: iOS, brief daily checks on an iPhone with touch as the baseline. This is a framework-agnostic design contract; an Apple SDK is not required. The only product evidence is `interface.md`: a dense spreadsheet of clinician terminology, missed tasks labeled “Failure,” symptoms automatically shared with every contact, and a requirement to record prescribed care without inventing or altering treatment. No screen, code, actual prescription, backend, or permission implementation was supplied. Examples below are illustrative fixtures, not treatment recommendations.

## Decisions and source support

| Decision | Reason and guidance |
| --- | --- |
| Replace the spreadsheet with a dated, grouped task list and task details. | Daily scanning takes priority over multicolumn comparison. Rows open details; opening a row never records completion. [Lists and tables — Content](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables#Content), [Designing for iOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices). |
| Select presentation by the prescribed task's completion meaning. | One action uses simple completion; necessary instructions appear before recording; individually described steps use a checklist; symptoms/events use timestamped logs. Every task has a short title and schedule. [CareKit — Tasks](https://developer.apple.com/design/human-interface-guidelines/carekit#Tasks). These are experience patterns, not a requirement to adopt CareKit. |
| Use familiar patient-facing titles, with authoritative clinical content preserved. | Show clinician-approved plain-language labels where available; otherwise retain the source title and offer clarification through the care team. Do not automatically paraphrase dosage, timing, warnings, or instructions. [CareKit — Tasks](https://developer.apple.com/design/human-interface-guidelines/carekit#Tasks), [Writing — Best practices](https://developer.apple.com/design/human-interface-guidelines/writing#Best-practices). Clinical approval of alternate wording is a product safeguard. |
| Replace “Failure” with factual recording states. | An absent record does not prove that care was not performed. Use “Not recorded” and offer a correction path; use “Not done” only when the patient explicitly records it. Avoid blame and explain remedies. [Writing — Best practices](https://developer.apple.com/design/human-interface-guidelines/writing#Best-practices). Exact states below are product decisions. |
| Stop automatic contact-wide disclosure. | Recording and sharing are independent. No recipient or data is preselected. Require a preview and an explicit send for each copy. Minimize access and explain use. [Privacy — Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices), [Collaboration and sharing — Best practices](https://developer.apple.com/design/human-interface-guidelines/collaboration-and-sharing#Best-practices). The one-time model is this specification's scope choice. |
| Show durable, truthful feedback beside the affected record. | Distinguish stored locally, sending, confirmed delivery, and failure. Avoid routine modal success alerts. [Feedback — Best practices](https://developer.apple.com/design/human-interface-guidelines/feedback#Best-practices), [Buttons — iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS). |

## Screens and actions

### Today

Header: “Today” and the full local date. Secondary labeled actions: “Previous day,” “Next day,” “Care team,” and “Share records.” Changing the viewed day never changes the prescribed schedule. Initial view uses today's date; preserve a manually selected date during navigation and interruption.

Show all scheduled occurrences for the viewed date in groups “To record” and “Recorded,” ordered by prescribed time within each group, with source order breaking ties. Keep the current row in place while interacting; regroup after returning from detail so focus does not jump during activation. Each row shows the approved short title, exact schedule, textual record state, and an “Open [title]” navigation action. A checkmark plus “Recorded done” identifies completion; color is supplementary. No score, streak, ranking, or adherence ring.

“No tasks scheduled for this day” is distinct from unavailable data. When loading fails, show “Tasks could not be loaded. Try again.” with “Retry”; never substitute an empty plan. A missing schedule is “Schedule unavailable” with access to source instructions and care-team clarification, not a guessed due time. All occurrences remain accessible, including long lists and past days.

### Task detail

Show title, prescribed date/time, plan source/version, original instructions and warnings, and record history. Essential warnings remain visible before the recording action. Long supplementary explanations can follow below. “Back” returns to the same day and row; preserve system swipe-back behavior. No custom gesture is required.

| Source task semantics | Presentation and action contract |
| --- | --- |
| One prescribed action | Instructions if supplied; prominent “Record as Done” stores a report for this occurrence only. Secondary “Record as Not Done” records an explicit report without rescheduling treatment. |
| Several prescribed, individually described steps | Checklist with full step descriptions and separate “Record Step as Done” actions. Overall “Recorded done” only when every required source step is recorded done; partial completion says “2 of 3 steps recorded done,” for example. No bulk completion that hides required steps. |
| Symptom or event | “Add Symptom Record” opens a labeled draft with observed time and the source-defined fields/units, plus optional note. Show the current time as editable; do not invent symptom scales or assume no symptoms from an empty field. “Save Record” commits; no binary done flag replaces an event log. |

For explicit done/not-done reports, show the reported time, editable before saving if needed. “Not done” may include an optional reason; no mandatory justification. Detail always offers “Correct Record,” which creates a new revision and preserves the prior report in history. Corrections change reports, never prescriptions. Back from an unsaved draft preserves it privately with “Draft — not saved as a record”; reopening restores it, and “Discard Draft” removes only that draft. Save returns focus to the persisted record and its status. Drafts are excluded from sharing.

Each screen has one prominent likely action; secondary actions are labeled and less emphasized. All controls have meaningful names, button roles, press/focus feedback, and disjoint activation areas of at least 44 × 44 iOS points. This uses the Buttons guide's general target recommendation; the Accessibility guide's smaller 28-point minimum is not the design target here. During a delayed save, the initiating button reads “Saving…” with an inline activity indication; duplicate activation is suppressed. [Buttons — Style and Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Style).

### State and persistence contract

```text
Occurrence = source task ID + plan version + source scheduled occurrence ID
Report = occurrence ID + report revision + reported state/time + recordedAt
         + optional reason + per-step reports
Event = stable event ID + source task ID + observedAt + supplied fields + recordedAt

record state: unrecorded | partial | done | explicitly_not_done
save state: draft | saving | saved_local | save_failed
share state: unsent | sending | delivered | failed | delivery_unknown

on source schedule passes:
    keep unrecorded; display "Not recorded" (never infer not done)
on Record as Done:
    commit report atomically with stable operation ID
    display "Recorded done" only after successful persistence
on save failure:
    retain prior report and draft
    display "Record not saved. Try again." + Retry
on late report:
    retain original occurrence and actual reported time; do not move next occurrence
on plan update:
    retain historical plan version and reports; apply only supplied new schedule
```

If network synchronization exists, show “Saved on this device — sync pending” separately from any remote acknowledgement. A local save never means clinician receipt. Retry uses the same operation ID to avoid duplicates. On restart restore day, occurrence, scroll/focus context, and persisted drafts; display save failures again. If a plan changes while a draft is open, retain the draft with its source version and explain the update before committing; never silently attach it to a different prescription. Store scheduled instants/time zones from the source; display local dates with zone context where conversion changes the day. If source time-zone semantics are absent, flag them for clarification rather than rescheduling.

No completion button recommends taking a missed dose, repeating a task, changing intensity, or making up care. “Questions about a missed task? Contact the care team.” opens the supplied care-team directory with named roles and labeled call/message destinations. Contacting someone does not attach symptoms automatically. No symptom triage or emergency thresholds are invented; display supplied clinical escalation instructions verbatim when available.

## Privacy and sharing contract

Default: recording sends nothing to personal contacts. “Not shared with contacts” describes only that boundary; never use “Only on this device” if a backend receives data. The product must disclose its actual storage, synchronization, retention, and deletion behavior before release; those facts are absent from the brief.

| Data | Minimum purpose/access | Transfer rule |
| --- | --- | --- |
| Prescribed plan and occurrence IDs | Display and attach reports to the correct care instructions | No contact disclosure; any plan-service access must be documented. |
| Task reports and symptoms | Private care recording | Share only selected saved revisions after explicit review. |
| Recipient identity/address | Send the reviewed copy | Manually choose a verified destination; no address-book-wide collection or launch-time Contacts prompt. |
| Device health, motion, photos, research data | No dependency established | Do not collect or request access for this experience. |

“Share records” opens a dedicated flow: choose saved records and date range → choose named recipient(s) with full destination and care role if known → review exact payload, dates, notes and recipients → “Send Copy.” Selections start empty on each new share. “Cancel” exits without sending and leaves source records intact. The final review says “This sends a copy of these records. It does not give ongoing access. A delivered copy cannot be recalled.” No public link or editing/invite permission is created. If the product has no sending capability, explain “Sharing is unavailable” and preserve recording; do not pretend to send.

Bind Send Copy to an immutable reviewed payload and recipient list. Any change requires renewed review. Do not queue new sends offline for automatic later delivery: retain an unsent draft and require review when online. Confirm “Delivered to [destination]” only from a receipt that establishes that outcome; otherwise use the actual supported status, such as “Submitted — delivery not confirmed.” On failure retain the selection, show a reason and Retry; check operation status before retry after an ambiguous timeout. A share history identifies recipients, payload revisions, time, and truthful delivery state. Corrections do not automatically send updates. No ongoing app sharing means there is no access grant to revoke; cancellation cannot recall a delivered copy. If existing releases created ongoing grants, release migration must disable new automatic transfers and expose accurate grant management before rollout; prior disclosure cannot be undone by this UI.

If Apple Health integration is later introduced, request only relevant types at feature invocation, recheck authorization as needed, and keep its sharing management in system privacy settings. The app's one-time copy flow must not claim to control Apple Health permissions. Core recording remains usable after optional access is denied. [HealthKit — Privacy protection](https://developer.apple.com/design/human-interface-guidelines/healthkit#Privacy-protection), [CareKit — Data and privacy](https://developer.apple.com/design/human-interface-guidelines/carekit#Data-and-privacy). No SDK integration or authorization is specified as already available.

## Readability and alternative access

Use semantic title, heading, body, and action-label roles; default iOS body text is 17 pt with Regular or stronger weight. Prefer system text styles when available; otherwise provide equivalent scaling and Bold Text behavior. Permit wrapping and growing rows, stack schedule/status beneath titles, and keep instructions/actions reachable by vertical scrolling in portrait and landscape. Support at least 200% enlargement and test all supported sizes including the largest accessibility size. Preserve the selected day, task, and draft on reflow. [Typography — Supporting Dynamic Type](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type).

Every state has text as well as any icon/color. Save and send outcomes remain visible until the person moves on; no essential timed toast, sound, haptic, or animation. Provide reading order as heading → schedule → instructions/warnings → record status → actions → history. Each repeated action's accessible name includes its task/step context. All actions must be reachable and activatable through supported assistive and keyboard input, with visible focus. Text entry does not require speech. Use static transitions under Reduce Motion; no celebratory animation is needed. Measure actual contrast in light, dark, and Increase Contrast appearances; no palette measurements are available here. [Accessibility — Vision, Mobility, Speech, Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility).

## Worked before/after

Illustrative fixture: a clinician-supplied occurrence titled “Prescribed exercise,” with supplied instructions and two separately described steps, scheduled yesterday at 09:00; the patient performed only one step and wants to log a symptom.

**Before (brief-supported pattern):** The patient scans clinical terminology across a dense spreadsheet, sees the missed entry marked “Failure,” and their symptom is sent to every contact. The brief does not establish the exact controls or literal clinical terms.

**After:** The patient opens yesterday via “Previous day.” The row reads “Prescribed exercise · Yesterday, 09:00 · Not recorded.” Opening it displays the original instructions and both complete step descriptions. They record the first step done; the row becomes “1 of 2 steps recorded done,” without marking the second step done or changing today's schedule. They choose “Add Symptom Record,” enter a note with the observed time, and save. Detail shows “Saved on this device” once persistence succeeds and “Not shared with contacts.” A care-team destination remains available for questions without promising monitoring.

To share, they choose that symptom record, select one named care-team recipient, inspect the exact note/time/destination, and activate “Send Copy.” Other contacts receive nothing. If sending fails, the record remains saved, the flow reports “Copy not sent. Try again,” and the patient can leave without losing the record. No care advice is generated from the partial completion or symptom.

## Acceptance checks and audit status

**Passed — static specification review only:** The artifact includes a title/schedule contract, task-type mapping, separate recording/sharing, factual missed-task states, preserved prescribed content, cancellation/recovery, data-purpose mapping, and explicit alternative-access requirements. Source routing was read from the installed root through owning families and topic procedures before their supporting references, including Privacy's CareKit/HealthKit handoff. No web access was used.

**Failed — supplied design description:** Contact-wide automatic symptom disclosure fails the revised recipient-scope requirement. “Failure” fails the revised factual, blame-free state requirement. The described spreadsheet fails the revised daily-list requirement. These are comparisons against this design contract, not runtime tests or proof of every possible HIG violation.

**Not executed — implementation acceptance scenarios:**

| Scenario | Required observable outcome |
| --- | --- |
| Open, scroll, and return from a task in a long day; empty day; unavailable plan | Correct identity and position restored; all tasks accessible; genuine empty and error states distinct. |
| Complete a simple action; partially complete detailed steps; add two symptom events | Correct per-occurrence/per-step semantics; two timestamped events; no inferred completion or treatment change. |
| Let scheduled time pass; enter a late report; cross midnight/time-zone display boundary | Unrecorded stays unrecorded; original occurrence retained; no extra dose/task or silent schedule mutation. |
| Background/terminate during a draft, save, and ambiguous send; reopen | Draft/context restored, truthfully resolved persistence/delivery, no duplicate report or send. |
| Reject a save; deny network or optional permission; change a source plan | Recoverable retained work, no false success, core logging available, historical version intact. |
| Cancel sharing at every pre-send stage; share one symptom to one recipient | Zero pre-send transfers; final payload exactly matches review; zero other contacts; no continuing access. |
| Change a review selection; retry after uncertain delivery; correct a previously shared record | Renewed review, operation-status check/deduplication, no silent correction resend. |
| 200% and largest supported accessibility text; Bold Text; portrait/landscape | Full titles, warnings, recipients, and actions remain readable and reachable; no overlapping targets. |
| Measure targets and contrast in light/dark/Increase Contrast | Disjoint targets at least 44 × 44 iOS pt; measure actual color pairs. Use the local Accessibility guide's scoped contrast table; do not treat it alone as conformance certification. |
| VoiceOver, Switch Control, Full Keyboard Access, AssistiveTouch; muted sound; Reduce Motion | Entire recording/sharing path reachable, meaningfully named and ordered, focus retained, status perceivable without sound/color/motion. |
| Optional Apple Health access denied/revoked, if later implemented | No misleading current-access claims; system privacy settings remain authoritative; manual recording works. |

## Evidence limits and handoff

This is a revised interaction specification, not an implemented or clinically validated product. No device, SDK, GUI, accessibility, touch-comfort, storage, transmission, security, or authorization execution occurred. Contrast, target geometry, localization, native rendering, and assistive order remain unmeasured. Acceptance rows are future tests, not passes.

Guidance came only from the installed local HIG-derived snapshot (references dated 2026-10-25); official links identify provenance and were not visited. Local file presence does not establish independent source review. CareKit's reference describes Watch notifications while its general platform summary excludes watchOS UI; this specification stays within iOS and makes no Watch-support claim. Engineering must confirm persistence/sending capabilities and actual privacy disclosures; clinicians must supply schedules, instructions, and any approved terminology or escalation content. No legal compliance, medical efficacy, Apple API availability, or current-source verification is claimed.
