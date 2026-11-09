# Revised iPhone event-creation interaction specification

## Scope and decisions

The supplied `interface.md` describes a brief iOS event task attached to a calendar, requiring title, date and invitees. It reports Cancel, Back and Done together on every step, enabled Done with an empty title, and swipe dismissal that discards partial work. No implementation or rendered prototype was supplied.

Keep one modal creation sheet: temporarily blocking calendar edits gives this short task a clear boundary. Retain the underlying calendar's selected day, scroll position and initiating control. Use three internal steps, rather than additional sheets or unrelated navigation. A future substantial editor would require reconsidering this scope. This follows [Modality — Best practices](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices) and [Sheets — Best practices](https://developer.apple.com/design/human-interface-guidelines/sheets#Best-practices).

Use a large-only sheet, with scrollable content when necessary. Composition benefits from room for entry and the keyboard; medium-only confinement adds no value here. There is no resize control or grabber because there are no alternate detents. Retain vertical swipe dismissal with unfinished-work protection. These are product choices applying [Sheets — iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/sheets#iOS-iPadOS), whose medium-detent guidance is optional, not a requirement for every iPhone sheet.

Product assumptions, rather than HIG requirements: title and date are required; invitees is a required *step* with zero invitees allowed. The brief does not establish a minimum invitee count. This version creates a date-only event, defaults to the calendar's selected date, and stores a calendar-qualified date rather than a midnight instant. Time, duration, contact discovery and invitation delivery are outside this specification. Selected invitees become event metadata; Done does not promise that invitations have been delivered. No contact permission or Apple SDK is assumed.

## Step and control contract

Every step has the task title “New Event” and a separate “Step N of 3” indicator. Values belong to one shared draft. Back never rolls them back. Navigation labels below are visible text, not unlabeled icons.

| Step | Leading top control | Trailing top control | Content and continuation |
| --- | --- | --- | --- |
| 1: Details | Cancel | Done, disabled | Persistent “Title (required)” label, title field, trailing Clear, “Enter a title to continue.” when empty; primary body Next advances to Date only with a nonblank title. |
| 2: Date | Back | Done, disabled | Persistent “Date (required)” label and inline date calendar; primary body Next advances to Invitees only with a valid date. Explain “Complete Invitees to finish.” near continuation. |
| 3: Invitees | Back | Done, enabled only when the entire draft is valid | “Invitees (optional)” email entry, Add button and removable selected addresses. Summary of title/date and “No invitees” or selected count. No body Next. |

Cancel and Done form the first-step pair; Back and Done form subsequent pairs. Never show Cancel, Back and Done together. From later steps, Back leads to step 1 for explicit Cancel, and the downward swipe remains an exit on every step. Disabled Done on earlier steps communicates that the flow is unfinished; the step indicator and Next provide the route forward. This applies the documented multistep example in [Sheets — iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/sheets#iOS-iPadOS); the exact three-step structure and body Next are application decisions.

Done is the final primary nondestructive action; Next is primary on the earlier steps. Back and Cancel have lower visual emphasis. Related buttons keep comparable target sizes, with nonoverlapping selectable regions at least 44 × 44 pt on iPhone and perceivable press/disabled feedback. Use platform controls where available; a framework implementation must preserve these behaviors. See [Buttons — Best practices, Style and Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices).

## Field and validation contract

- Title: accept typing and paste, including non-Latin text. Preserve entered text while editing; use a whitespace-trimmed copy to test emptiness and trim outer whitespace on final save. Do not invent a character limit. A long title remains editable through field scrolling and wraps in the final summary. Clear updates the draft and immediately disables Next. Missing title is visible guidance, not a repeated alert.
- Date: prefill the selected calendar date and accept past dates. Use localized calendar labels and ordering, with inline selection near the Date label. Preserve date meaning across locale changes; retain its calendar identifier with year/month/day. Invalid imported or unavailable dates show “Choose a valid date” and disable Next; never silently replace a user selection. No time or minute interval applies. See [Pickers — Best practices and iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/pickers#iOS-iPadOS).
- Invitees: enter one email address at a time using an email-appropriate input mode with paste allowed. Add validates on activation; leaving an invalid nonempty field shows “Enter a complete email address.” Preserve the text for correction. The address validator must be Unicode-capable and must not claim mailbox existence. Add commits a valid address to the draft and clears the entry; duplicate exact addresses are not added twice. Each selected address has a text-named Remove action. Pending nonempty entry disables Done with “Add or clear this address to finish,” preventing silent omission. Zero selected addresses with empty entry is valid. Do not show suggestions or request contacts in this version.

Required-data gating, persistent labels, useful defaults and contextual correction follow [Entering data — Best practices](https://developer.apple.com/design/human-interface-guidelines/entering-data#Best-practices) and [Text fields — Best practices and iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/text-fields#Best-practices). The exact validation messages and invitee rules are product decisions.

## State, exits and data outcomes

Define `initialDraft` after defaults are applied. Dirty means draft values or pending invitee text differ from that baseline; changing a value back to its original value clears that difference. Step changes and focus alone are not edits. Nothing creates an event until successful Done.

| Trigger | Result |
| --- | --- |
| Open from calendar | Capture calendar context, initialize draft, show step 1; calendar remains visible but noninteractive. |
| Next / Back | Validate Next's current step; move internally and preserve all values. Back performs no save or discard. |
| Cancel at step 1, downward swipe at any step, or supported keyboard escape | Route through the same exit request. Clean draft closes immediately. Dirty draft remains retained while the discard choice is presented. |
| Dirty exit choice | Short action sheet titled “Discard this event?” with destructive “Discard Event” first and safe “Keep Editing” cancellation at the bottom. Discard destroys only this draft and returns to calendar. Keep Editing, outside dismissal or system cancellation returns to the same step with every value and pending entry intact. |
| Done on final step | Revalidate the complete draft; if invalid, keep the sheet open and return to the first relevant field/step with corrective text. Otherwise start one save operation. |
| Save pending | Show activity in the Done button, labeled “Saving…”. Prevent duplicate saves, edits, Back and destructive dismissal while the result is unresolved. Explain the wait; retain the draft. |
| Save succeeds | Close creation flow, clear its draft, insert exactly one event in the intended calendar and reveal that event. A later New Event starts fresh. |
| Save fails | Restore editable final step and Done, retain all input, show “Couldn’t save the event. Try again.” No event is claimed created. Retry uses the same operation identity to prevent duplication after an ambiguous response. |
| App interrupted | Retain draft, pending text and step locally for restoration. Resume at that step. Resolve any pending operation before allowing another save; interruption is never an implicit discard. |

The discard choice follows [Action sheets — Best practices and iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/action-sheets#Best-practices). It resolves an intentional exit, rather than presenting an urgent alert. It is a single temporary decision surface, not a second event-creation sheet. Suspend the composer presentation if the framework requires replacement, retaining its complete state; restore it on cancellation. Ignore repeated exit requests while the choice is open. No nested composer or stacked confirmations are permitted. Preserve only one active decision and one draft identity.

Delayed feedback follows [Buttons — iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS). Idempotent save identity and interruption recovery are application reliability requirements, not asserted HIG API behavior.

Framework-agnostic exit handler:

```text
requestExit(origin):
    if saving or exitDecisionOpen: return
    if draft == initialDraft and pendingInvitee == "": closeToCalendar()
    else:
        retain(draft, pendingInvitee, step, focusedControl)
        showDiscardDecision(boundTo = draft.id)

resolveExit(choice):
    if choice == DISCARD: deleteRetainedDraft(); closeToCalendar()
    else: restoreComposerAndRetainedState()
```

On step entry, bring the step heading into view and use a predictable input order matching visual order. Returning from the discard choice restores the invoking control; final dismissal restores the calendar initiator, or focuses the newly created event after success. Content must scroll above the keyboard with navigation reachable. These are specified behaviors requiring runtime verification, not observed accessibility results.

## Worked before/after

Before, as reported: every step exposes Cancel, Back and Done. Done is enabled even with no title. After entering “Design review,” a downward swipe discards the partial event. The brief does not establish what activating empty-title Done actually saves.

After: opening from November 4, 2026 shows Details with Cancel, disabled Done and disabled Next. Typing “Design review” enables Next. Date starts at November 4; change it to November 6 and select Next. On Invitees, enter `sam@` then swipe down. “Discard this event?” appears; Keep Editing returns to Invitees with `sam@`, the title and November 6 preserved. Correct to `sam@example.com`, tap Add, then Back: Date still shows November 6. Next returns with Sam selected. Done saves one event, closes the flow and reveals it on November 6. No invitation-delivery success is implied.

## Acceptance checks and evidence status

**Passed — static specification trace:** each step has at most two top navigation actions; Back is distinct from exit; all available dismissal paths share dirty protection; the worked example preserves title, date and pending text; save success/failure have explicit outcomes. These are checks of this written contract only.

**Failed — supplied design against revised requirements:** the reported simultaneous Cancel/Back/Done, enabled empty-title completion, and destructive edited swipe do not meet this contract. This finding rests on the text brief, not executed prototype behavior.

**Not executed — implementation acceptance:**

1. Empty and whitespace-only title disable Next; pasted valid Unicode title enables it; Clear disables it again. Early Done cannot commit through touch or hardware keyboard.
2. Next/Back round trips preserve title, date, selected invitees and pending entry. Back at step 2 returns to step 1 without closing.
3. Clean Cancel/swipe/escape close with zero events; edited versions show the same choice. Keep Editing, outside cancellation and repeated invocation lose no data. Explicit Discard returns to the original calendar context.
4. Invalid invitee stays editable; pending text blocks Done with a reason; valid Add and Remove work; zero invitees is accepted. No duplicate exact address is added.
5. Locale/calendar changes preserve the selected date meaning. Past dates and boundary dates remain selectable; invalid incoming values require correction.
6. A rapid double Done or retry after ambiguous failure creates at most one event. Definite failure retains all data. Background/resume restores the draft or reconciles an in-flight save without duplication.
7. Large text, long titles/addresses, keyboard visibility and small iPhone layouts leave fields and exits reachable without overlap. Measure button targets in points. Confirm there is only a large detent and no inert resize affordance.
8. On an actual iPhone, exercise vertical gestures, focus restoration, hardware keyboard order and assistive technology traversal/names/disabled-state announcements. Verify calendar blocking, native presentation and the discard decision's safe dismissal behavior.

## Evidence limits and local routing audit

Only `interface.md` and installed local instructions/references were used. No web browsing, SDK compilation, GUI, device, native gesture, keyboard, VoiceOver or accessibility execution occurred. No implementation exists here to establish runtime persistence, backend idempotency or email-validation behavior. The checks above are acceptance requirements, not test pass claims. Official links identify the local snapshot's source articles; they were not fetched or independently verified.

Installed package root: `.agents/skills/apple-hig/`. Explicitly read root `SKILL.md`; searched `references/topic-index.md`; read each owning family and topic procedure before the corresponding source guide:

- Presentation → Sheets, Action sheets → `references/sheets.md`, `references/action-sheets.md`.
- Patterns → Modality, Entering data → `references/modality.md`, `references/entering-data.md`.
- Menus and actions → Buttons → `references/buttons.md`.
- Selection and input → Text fields, Pickers → `references/text-fields.md`, `references/pickers.md`.

Each instruction/reference read used a separate single-file command. The sources identify a 2026-10-25 snapshot. Recommendations retain their platform scope; no SDK availability or newer-release claim is made. No conflicting passages were identified in the selected local guidance.
