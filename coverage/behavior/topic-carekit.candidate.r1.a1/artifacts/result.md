# Daily prescribed-care record — revised interaction specification

Target: iOS, primarily a patient using an iPhone. Framework agnostic; no Apple SDK dependency is assumed. This is a proposed interaction contract, not an implemented app.

## Decisions and boundaries

The supplied `interface.md` describes a dense spreadsheet of clinician terminology, missed tasks labeled “Failure,” and symptoms automatically sent to every contact. It supplies no screens, implementation, care plan, or sharing infrastructure. These are the observed requirements and problems; geometry and runtime behavior remain unknown.

1. Replace the spreadsheet with a single-column **Today** list. Patients need to find and record an individual prescribed task, rather than compare clinical columns. Each row opens that task; tapping a row never records completion. Use date and plan-provided time groups, with all tasks retained, including completed tasks. This applies [Lists and tables — Content and Style](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables#Content).
2. Use familiar patient-facing titles only when supplied or approved by the care team. Preserve the full original instruction, quantities, timing, precautions, author, and plan version in task details. Define specialist terms using approved definitions; do not generate translations of medical meaning. When no approved title exists, show the original and offer “Ask care team about this instruction.” This follows [Inclusion — Welcoming language](https://developer.apple.com/design/human-interface-guidelines/inclusion#Welcoming-language); clinical approval is a product safeguard, not a HIG rule.
3. Replace “Failure” with factual recording states. Absence of a record means **Not recorded**, never proof that care was not performed. Explicit patient reports can say **Recorded as not done**. No streak loss, score, blame, or celebratory pressure. Clear, blame-free copy follows [Writing — Best practices](https://developer.apple.com/design/human-interface-guidelines/writing#Best-practices); these exact states are product decisions.
4. Stop automatic symptom sharing to contacts. Saving a symptom and sending it are separate actions. Default to no external recipients and require an explicit review and send for each disclosure. OS contact permission is not consent to disclose health information. Apply data minimization and purpose-specific access from [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices).
5. The app records prescribed care. It never creates a treatment, adjusts a dose or schedule, recommends catching up, or infers treatment from symptoms. Editing a record changes the patient's report only. Plan updates require an authenticated clinician-originated version through an existing, validated plan process; that process is outside this brief.

## Screens and navigation

**Today** begins with the localized full date, followed by “Record care from your prescribed plan.” A secondary “View care plan” action exposes the original plan. “Previous day,” “Next day,” and “Return to today” provide date navigation without a required swipe. Future occurrences can be inspected but cannot be recorded as already performed.

Rows show approved task title (or original title), prescribed time exactly as supplied, and a textual status. Sort by plan-provided time, with stable plan order for ties; put untimed tasks under “No time specified.” Do not invent “morning” or a due window. Completed rows remain in place to avoid losing the patient's position. A row's disclosure navigates to details; no checkbox or nested completion target appears in the row. Back returns to the same date, row, and scroll position. Past days remain reachable without silently dropping records. No task reordering, prescription addition, or removal is offered in this patient workflow.

**Task details** shows title, scheduled date/time, complete original instructions, plan source/version, and status. Essential instructions are visible before recording, rather than hidden behind terminology help. Available actions:

| Label | Contract | Emphasis and recovery |
|---|---|---|
| Record as Done | Opens a draft report for this occurrence; does not save yet | Primary when no report exists |
| Record as Not Done | Opens a draft report with an optional reason | Secondary, neutral; never changes the plan |
| Edit Record | Opens the saved report for correction | Primary when a report exists; history retained |
| Ask Care Team | Shows supplied contact details and existing approved contact route | Secondary; never claims a message was sent merely by opening it |
| Back | Returns to the list | Preserves selection and scroll |

**Report draft** identifies the task and scheduled occurrence, then displays the selected report (“Done” or “Not done”). For Done, allow a labeled “When performed” field initialized to now, with explicit review; reject future actual times with “Choose a time that has already occurred.” Do not infer a clinical compliance judgment if actual and scheduled times differ. “Reason (optional)” accepts patient text for Not done. “Save Record” commits; “Cancel” abandons draft changes and preserves the saved report. Correction uses the same flow and appends a revision instead of silently rewriting history.

Use ordinary navigable screens for these steps. No swipe-only actions, timed undo, destructive deletion, or additional confirmation alert is required for a reversible report correction. Outcome-specific labels, a single prominent likely action, press feedback, and in-button activity feedback for delayed operations apply [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Style).

Empty date: “No prescribed tasks scheduled for this date,” with “View Care Plan.” Loading: “Loading prescribed tasks.” Load failure: “Tasks could not be loaded. Try again,” with “Try Again”; never render this as an empty plan. No plan: “No care plan is available,” with the supplied care-team contact route. Completed date: keep the list and say “All tasks have a record,” which does not imply clinical recovery or that every task was done.

## State and persistence contract

Clinical schedule and patient report are separate data:

```text
Occurrence = {id, planVersion, originalInstruction, approvedTitle?, scheduledAt?, planDate}
Report = {occurrenceId, revision, outcome: done | not_done,
          performedAt? only for done, optionalReason?, recordedAt}
recordState = none | saved(report)
writeState = idle | saving | error
```

- Time passing or crossing midnight changes neither report nor prescription. An unrecorded past occurrence reads “Not recorded”; it remains available to record later. Preserve schedule timezone/offset and plan date; display actual timestamps with enough date/zone context to distinguish them. If schedule timezone is missing, flag it for clarification rather than converting treatment times by guesswork.
- Save uses a stable operation ID and expected revision. During saving, show “Saving…” in the activating button and suppress duplicate commits. Show “Saved” only after the persistence layer acknowledges a durable write. Keep it visible until the next action.
- Failed save leaves the draft intact: “Record could not be saved. Try again.” Offer Try Again and Cancel. Retry the same operation ID. On an uncertain response, resolve its status before creating a new operation. A conflicting newer report must be shown for review; do not silently overwrite it.
- Successful correction retains old and new report revisions. A changed plan never silently reassigns an old report to a new instruction; historical reports retain their original occurrence/version. This is a recording model, not permission to edit prescribed treatment.
- No offline guarantees are assumed. If durable saving is unavailable, show an explicit unsaved draft state and keep the draft while this view remains open; do not show Saved or promise cross-session recovery without an implemented persistence guarantee.

## Symptom recording and sharing

“Record a Symptom” opens a labeled free-text draft with an occurrence timestamp and optional link to a task. Saving records the patient's words without diagnosis, severity inference, or treatment advice. On successful private save, show “Symptom saved. Not shared with contacts.” This claim requires the no-recipient storage policy below; do not use it if an implementation has undisclosed external readers.

| Data | Purpose and minimum access | Disclosure rule |
|---|---|---|
| Plan and task reports | Display prescription and keep patient's record | No contact delivery; account/backend access must be inventoried before implementation |
| Symptom text and time | Patient's symptom journal | Patient-only access by default, including no automatic care-team access |
| Recipient name and destination | Send a particular reviewed symptom | Select one verified destination at a time; no address-book-wide collection |
| Sharing receipt | Explain what was sent, when, and to whom | Retain minimum delivery metadata with the patient's record |

After saving, secondary **Review Sharing** opens a screen with the exact symptom content, timestamp, and initially no recipient. A separate recipient list offers “Choose [name]” for a verified destination; selection returns to the review. Do not preselect relatives or assume that any contact is trusted. Prefer existing verified destinations/manual entry; this specification does not require address-book permission. If a future implementation adds protected contact access, request it only when choosing from contacts and explain its precise purpose; recording remains available after denial.

Final action label: **Send to [name]**. It is unavailable until a destination is selected and verified, with the nearby reason “Choose a recipient to send this symptom.” Copy above it: “Send this symptom and its recorded time to [name, destination]. They may keep a copy.” Cancel returns to the saved symptom without sending. This review is an application disclosure decision, not an imitation OS permission prompt.

At send, freeze the displayed payload and recipient into an authorized send operation. Show “Sending…” and prevent duplicate sends. Delivery states distinguish “Sent to [name]” after service acknowledgment, “Could not send. Try again,” and “Delivery status unknown. Check status.” Do not blindly retry an unknown delivery. Editing the symptom afterwards neither changes the sent copy nor sends a new one. Show sharing history alongside the symptom; explain “Already sent copies cannot be recalled here.” Each additional recipient requires a new review and send.

For existing installations, disable the old automatic contact broadcast and queued unsent broadcasts before enabling this experience. Do not treat old blanket access or OS permission as a new send authorization. Explain that future contact sharing requires explicit send; do not claim old recipients' copies were removed. Backend authorization and existing care-team access must be reconciled with this contract before release. These are product privacy decisions derived from the HIG principle, not proof of security or legal compliance.

## Reading and access contract

Use semantic title, headline, body, and supporting-text roles; use a readable regular-weight body with the iOS 17 pt default as the baseline, rather than shrinking to the 11 pt source minimum. Prefer platform text styles where the stack supports them; otherwise provide equivalent resizing and Bold Text behavior. At every supported size, including largest accessibility sizes and at least 200% enlargement, grow rows, wrap titles and instructions, and stack timestamps/actions. No horizontal spreadsheet scrolling or clipped essential instruction. See [Typography — Supporting Dynamic Type](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type).

Use at least 44 × 44 pt nonoverlapping activation regions for this iOS design, with clear separation. The accessibility reference lists a smaller 28 × 28 pt minimum, while the buttons reference recommends general regions of at least 44 × 44 pt; choose the comfortable 44 pt default here. Use text plus optional symbols for all states, never red/green alone. No essential sound or animation. Specify static state changes so Reduce Motion loses no information. Test measured colors in light, dark, and Increase Contrast appearances; no supplied palette permits a measured contrast claim. Apply [Accessibility — Vision, Mobility, and Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision).

Every action has a programmatic button role, visible matching name, enabled/busy state, and press feedback. Rows expose title, time, and status as one navigable item with an open-details action; completion is a separate button in details. Reading order: screen title/date, guidance, group heading, rows in visual order; details: task identity, schedule, instructions, status, actions. Focus enters the new screen at its heading and returns to its initiating row on Back. Save status is available as text and announced once without stealing focus. Provide keyboard and assistive navigation through the full path. These are required implementation semantics and tests, not claims of VoiceOver execution.

## Worked before / after

Illustrative fixture only: the supplied brief contains no actual patient task or clinical wording. Assume a clinician-authored task T1 has an approved display title “Prescribed care task” and an original instruction available verbatim; use that fixture rather than inventing a treatment or dose.

**Before:** T1 appears among spreadsheet columns under specialist terminology. Its past scheduled occurrence says “Failure.” Recording a symptom sends it to every contact.

**After:** Today shows “Prescribed care task · 9:00 AM · Not recorded” (9:00 AM is a fixture schedule). The patient opens T1, reads the unchanged original instruction, chooses Record as Not Done, leaves the optional reason blank, and saves. The list returns to the same row with “Recorded as not done.” Nothing reschedules T1 or suggests making it up. A mistaken report can be corrected with Edit Record, retaining history.

The patient records “I felt uncomfortable” as symptom text. Save produces “Symptom saved. Not shared with contacts.” Review Sharing shows no selected recipient. Choosing verified recipient Alex shows exactly that text and time plus Alex's destination. Cancel sends nothing; Send to Alex sends only the reviewed payload to Alex. Other contacts receive nothing. A send failure does not erase the symptom or change T1's report.

## Acceptance checks and evidence limits

**Passed — specification inspection only:** The revised artifact defines list identity/order, full instruction access, neutral missing-record semantics, reversible report corrections, explicit recipient/payload review, failure states, and preservation of clinician-authored treatment. The worked example exercises Not done, symptom save, cancel, and explicit send on paper. Root → family → topic procedure → supporting reference was read from the installed package; no web lookup was used.

**Failed — supplied baseline description:** The brief's terminology-heavy spreadsheet does not provide the proposed patient task hierarchy; “Failure” conflates record absence with judgment; automatic delivery to every contact conflicts with precise, intentional disclosure. These are brief-level findings. No visual density, hit-region, contrast, or assistive-technology defect was measured.

**Not executed — implementation acceptance gates:**

| Scenario | Required observable result |
|---|---|
| Open any row, Back, navigate dates | Correct occurrence/version opens; date and scroll return; no row tap records completion |
| Empty, loading, failed load, long list | Distinct states; all expected tasks remain reachable; long titles retain full-text access |
| Save Done / Not done; edit; cancel | Exact chosen report persists only on Save; Cancel preserves prior report; correction history survives reload |
| Double activation, failed write, uncertain write, conflict | One operation; draft retained on error; status resolved before retry; newer revision never silently overwritten |
| Midnight, timezone change, late recording, future occurrence | No inferred adherence, schedule mutation, catch-up advice, or premature completion; identity remains stable |
| Symptom save; denied optional contact access | No recipient transfer; recording still works; private-save copy matches actual access policy |
| Review, Cancel, Send, edit after send | Cancel transfers nothing; only reviewed recipient/payload sent; edits do not automatically resend |
| Send failure/unknown result; old queues | No duplicate delivery on retry; unknown outcome checked; legacy broadcasts blocked |
| Narrow width, 200% and largest supported text, Bold Text | Full instructions and actions remain usable without clipping, overlap, or required horizontal scrolling |
| Light/dark/Increase Contrast; measured targets | Text/status understandable without color; measured contrast documented; targets at least 44 × 44 pt and separate |
| VoiceOver, Switch Control, Full Keyboard Access, AssistiveTouch | Complete entry-to-record-and-share path reachable and activatable; names, order, focus return, and save announcement verified |
| Patient and clinician review; localization | Titles/definitions preserve clinical meaning; neutral copy understood; dates/times and long translations remain clear |

Only local text evidence was available. No app was built or run; no device, SDK, GUI, accessibility tool, font measurement, contrast measurement, backend authorization, encryption, persistence, or delivery execution occurred. The installed references identify themselves as derived guidance with snapshot/retrieval date 2026-10-25; links above are attribution, not evidence of live verification or independent source review. Clinical validity, patient comprehension, current SDK availability, security, legal compliance, and release readiness remain unestablished. Implementation must resolve actual storage/access, verified recipient delivery, plan provenance, and timezone data before making the specified claims.
