# Medication reminder complication — revised interaction specification

## Scope and decisions

The watch face answers “Does a reminder need my attention?” A tap opens the corresponding dose context in the Watch app. Recording happens there. The complication contains no scrolling, task list, instructions, medication name, patient identifier, or dose-recording control.

Observed evidence is the prose in `interface.md`: full medication name and patient identifier on a shared-visible face, tiny multiline instructions, a scrolling task list, and due/recorded/overdue states. No rendered screen, implementation, schedule rules, supported OS version, or device inventory was supplied.

The following are product decisions applying the local HIG snapshot, not claims that Apple mandates this exact design:

- Use a changing, concise status rather than a miniature app. Tap goes directly to the relevant context, following [watchOS best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos#Best-practices) and [Complications](https://developer.apple.com/design/human-interface-guidelines/complications#Best-practices).
- Default to a neutral shared-visible presentation. Offer an explicit opt-in to generic status on the face, explaining that even “Overdue” can disclose a care routine. Never offer names or patient IDs on the face. Redact status in privacy-restricted and Always On states. This conservative disclosure policy applies [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices), [Complications](https://developer.apple.com/design/human-interface-guidelines/complications#Best-practices), and [Always On](https://developer.apple.com/design/human-interface-guidelines/always-on#Best-practices).
- Keep supplied care instructions and schedule intact in app detail. “Recorded” means a saved user report, not proof of ingestion or adherence. Do not invent missed-dose advice, grace periods, or clinical thresholds. [CareKit task guidance](https://developer.apple.com/design/human-interface-guidelines/carekit#Tasks) informs title/schedule/completion semantics only: its local reference marks watchOS UI unsupported and separately describes Watch notifications. No CareKit adoption is assumed.

## Face content contract

Assume a modern watchOS complication design; final OS deployment and supported face slots remain implementation inputs. Modern family vocabulary does not require an SDK here. Older ClockKit support is outside this revision, not implicitly interchangeable.

| Context | Rectangular | Inline | Circular / corner |
|---|---|---|---|
| Default private, or privacy-restricted | Neutral app glyph; “Reminders” | “Reminders” | Neutral app glyph |
| Generic-status opt-in, active: due | “Reminder” / “Due” | “Reminder due” | Clock glyph + “Due” where legible |
| Opt-in, active: overdue | “Reminder” / “Overdue” | “Reminder overdue” | Exclamation glyph + “Overdue” where legible |
| Opt-in, active: recorded | “Reminder” / “Recorded” | “Reminder recorded” | Check glyph + “Recorded” where legible |
| Opt-in, active: future scheduled dose | “Reminder” / “Next 20:00” | “Next 20:00” | Clock + local time where legible |
| Opt-in, active: stale/unknown | “Reminders” / “Open to update” | “Open reminders” | Neutral app glyph |
| No schedule / signed out / unavailable account | “Reminders” / “Open to set up” | “Open reminders” | Neutral app glyph |

Circular/corner fall back to a recognizable neutral launcher if the complete state cannot fit at the supported template size; do not shrink or use cryptic abbreviations to force it. Fall back as a whole state, retaining the app destination. Do not use percentage rings or gauges: no bounded quantity is defined. Color is supplementary; labels and distinct glyphs retain meaning in tint and grayscale.

Rectangular has at most two short text rows; inline one. Use the selected family's standard typography and spacing, with SF Compact Rounded or equivalent platform-provided complication styling when implemented. Do not apply a general app font minimum blindly to system-sized complication templates. App detail uses semantic text roles, a 16-pt watchOS body starting point, and resizing through at least 140%, with wrapping rather than shrinking. See [Typography](https://developer.apple.com/design/human-interface-guidelines/typography#watchOS) and [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision).

Supply a static, nonpatient placeholder for each supported family: neutral glyph and “Reminders” where text fits. Placeholder is never interpreted as a recorded dose. Production assets must use the chosen template's content and placeholder sizes separately. The local complication tables include a conflicting legacy 41-mm inline height and a legacy circular placeholder typo; neither is a production sizing authority for this design. Verify target template dimensions before exporting assets. The [family guidance](https://developer.apple.com/design/human-interface-guidelines/complications#Circular) is not evidence of actual slot fit.

## Selection, time, and freshness

Use stable internal dose-occurrence IDs, never patient names or medication text in public deep links. Select within the explicitly configured wearer/account context; never automatically combine patients. Multiple-patient choice occurs privately in the app before setup completes.

```text
select(snapshot, now):
  if account inaccessible or schedule absent: return SETUP
  if snapshot invalid or now >= snapshot.validUntil: return UNKNOWN
  pending = occurrences not durably recorded
  if any pending with overdueAt <= now: choose earliest scheduledAt, then ID
  else if any pending with scheduledAt <= now: choose earliest scheduledAt, then ID
  else if any occurrence recorded in current local calendar day:
    choose most recently recorded occurrence
  else if any future pending: choose earliest scheduledAt, then ID
  else: return EMPTY

state(occurrence, now):
  if durable record exists: RECORDED
  else if now >= overdueAt: OVERDUE
  else if now >= scheduledAt: DUE
  else: UPCOMING

face(model, context):
  if privateDefault or privacyRestricted or wristDown: neutralReminderContent
  else: familyLayout(model)
```

`overdueAt` must come from the established care-plan rules, strictly after `scheduledAt`; absent/invalid rules produce UNKNOWN rather than an invented overdue transition. Timestamps retain schedule timezone semantics. Recompute after timezone/daylight-saving changes, local midnight, plan changes, account changes, and records/corrections. EMPTY displays “No reminders” only with a fresh complete schedule; it does not mean “all medication taken.” Once a future dose becomes due it replaces the recorded summary. These selection rules are product policy, not clinical guidance.

Precompute useful timeline entries at due, overdue, midnight, and validity boundaries. Request refresh after durable records, corrections, schedule/account/privacy changes; tolerate deferred reloads and bounded storage. No second-by-second countdown or guaranteed immediate face update. `validUntil` is supplied by the data source's freshness contract; missing validity means UNKNOWN. Never carry “Recorded” or “No reminders” beyond validity. Opening always rereads current data before offering actions. Revoking access clears cached sensitive data and requests neutral replacement; implementation must verify system redaction because refresh requests alone cannot guarantee immediate removal. See [Complications best practices](https://developer.apple.com/design/human-interface-guidelines/complications#Best-practices).

## Tap and record interaction

1. The entire complication is one activation target. Tap opens the selected occurrence's detail, not generic home. Neutral content opens the current reminder context after access checks. SETUP opens setup; UNKNOWN opens reminders with “Information needs updating.”
2. Revalidate account, access, ID, schedule revision, and record on entry. If the occurrence was removed, show “Reminder changed” with a labeled “View reminders” action. Never silently record a replacement occurrence.
3. Detail shows the full supplied medication/task title, scheduled date/time, current state, and supplied instructions. Patient context is shown only where needed to disambiguate privately. Primary action is “Record dose”; instructions remain available in full, without tiny compressed text. This action reports the user's event and never instructs taking an overdue dose.
4. Activation starts one idempotent save for that occurrence. Disable duplicate submission and show “Saving…”. Show “Recorded at [time]” only after durable success. On failure retain Due/Overdue and show “Couldn’t save” with Retry. Uncertain outcomes are reconciled by occurrence/event ID before retrying.
5. A recorded detail exposes “Correct record”; activating it opens the record for explicit correction, without modifying the schedule. Persist the correction before changing status. No timed-only undo. No face tap, wrist raise, scrolling, or elapsed time records a dose.
6. Preserve the selected occurrence and pending save across interruptions. Wrist down redacts health details and patient/title/instructions in place, dims controls to unavailable appearances, and keeps layout stable; wrist raise restores context after access checks. Face wrist-down content stays neutral. Device support and exact dimming behavior require implementation verification.

The Watch app remains useful without requiring the phone for each record when valid local data and durable local storage are available. If those prerequisites are absent, show unavailable state; do not falsely claim a successful record.

## Accessibility contract

One complication element has a name matching the currently permitted visible content, a current value when disclosure allows, and an activation action opening reminders. Its accessibility content must not leak redacted names, state, or patient identity. Detail order is title/context, schedule, state, instructions, record/correction, secondary navigation. This specifies semantics, not a verified VoiceOver order.

App actions start with 44 × 44 pt activation areas and comfortable separation, following the watchOS default in [Accessibility mobility guidance](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility); do not enlarge a system-owned face slot by inventing its geometry. No essential gesture-only action, sound-only confirmation, flashing alert, marquee, or automatic scrolling. Use persistent visible save/error feedback. At larger text sizes, detail wraps and grows vertically; all content and actions remain reachable. Measure actual contrast in tint, dimmed, dark, and Increase Contrast contexts. Font metrics, native rendering, and assistive behavior remain untested.

## Worked before/after

Illustrative fixture, not a supplied clinical schedule: occurrence D17, title “[full medication name]”, patient “[patient identifier]”, scheduled 08:00, plan-provided overdue boundary 08:30, valid snapshot through 09:00.

**Before:** the face exposes both identifying strings, tiny instructions, and a scrolling list. The brief does not establish how tapping or recording works.

**After:** at 08:10 the default rectangular face reads “Reminders”; with generic-status opt-in while active it reads “Reminder / Due.” Neither exposes the fixture strings. Tap opens D17's private detail with the full title, 08:00 schedule, Due, supplied instructions, and Record dose. Tap Record dose at 08:12: Saving → durable success → Recorded at 08:12. The next permitted face refresh shows Recorded. Without a record, the precomputed 08:30 entry shows Overdue. At 09:00 without renewed validity, show Open to update rather than asserting a current state. Wrist down always returns the face to neutral content, without losing D17 or an in-progress save.

## Acceptance checks and evidence limits

**Passed — specification inspection only:** the revised contract removes face identifiers/instructions/scrolling; defines all three supplied dose states, family fallbacks, destinations, privacy states, static placeholders, and bounded-update behavior; distinguishes a saved report from ingestion. Installed root, owning families, selected topic procedures, and supporting references were explicitly read locally. No web was used. Official links above identify source provenance, not live verification.

**Failed — supplied proposal against this contract:** shared-visible identifiers, tiny multiline instructions, and scrolling task-list behavior are explicitly present in `interface.md`. Geometry, contrast, assistive semantics, and tap behavior are not established by that prose and are not asserted as observed failures.

**Not executed — implementation acceptance gates:**

| Scenario | Pass condition |
|---|---|
| Time fixtures | Due at 08:00, overdue at 08:30 only if unrecorded, recorded wins after saved event, unknown at expired validity; timezone/midnight and multiple pending selection follow the stated rules. |
| Record/save | Face activation never records; repeated taps/retries create one record; failed/uncertain saves never falsely show Recorded; corrections restore truthful state. |
| Routing races | D17 tap opens D17 after revalidation; deleted/reassigned records show changed/access state, never another patient's action. |
| Privacy | All families, placeholders, previews, semantics, cached states, and wrist-down views omit prohibited values; sign-out/revocation and opt-out do not leave disclosed status. |
| Rendering matrix | Each advertised slot/device fits complete permitted labels in full color, tint, grayscale, dimmed mode and long localized strings; fallbacks activate when needed; assets match verified templates. |
| Reading and access | Detail works at default and at least 140% text, Bold Text and relevant accessibility preferences; labels/actions remain reachable; measured contrast and target geometry pass the chosen platform checks. |
| Assistive completion | On supported Apple environments, assistive navigation reaches the complication, opens the right detail, reads only permitted content, records and corrects without sight, speech, or complex gestures. |
| Updates/interruption | Deferred reloads, offline data, expired validity, wrist lowering, and app interruption preserve truthful state and pending work; physical readability and energy/update behavior are verified on supported watches. |

Only a design artifact was produced on the headless Linux workspace. No device, SDK build, GUI, accessibility tool, authorization flow, synchronization, clinical validation, or physical wrist test was executed. The installed references are dated application guidance, not SDK documentation or independently verified current Apple behavior. Deployment version, exact supported devices/templates, care-plan timing policy, data-source freshness guarantees, persistence/security mechanisms, and notification delivery remain implementation inputs. This specification does not add a notification flow or claim health-framework access.
