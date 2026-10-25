# iPhone expense entry: revised interaction specification

## Evidence and decisions

The supplied interface.md reports that all 28 fields block saving, validation clears entered data, generic keyboards serve currency/email/date, and optional receipt details interrupt required amount/vendor entry. No code, screenshots, schema, or business rules were supplied.

Design decision: use one short core form with optional enrichment below it. This specification is framework agnostic; use platform controls where available or equivalent behavior. No Apple SDK is assumed.

Product assumptions: a saved expense needs amount, vendor, currency, and expense date. Amount and vendor normally require typing; currency and date can have visible defaults. Saving records an expense without submitting it for reimbursement. If submission has additional requirements, collect those at that later explicit action. These are proposed product rules, not facts established by the brief. The storage contract must accept absent optional details.

Before implementation, inventory all 28 fields and map each to core, optional receipt details, other optional details, or a documented later submission requirement. Preserve every field's identity and existing values; the incomplete inventory does not authorize deleting fields or inventing their purposes.

| Decision | Concrete change | Guidance |
|---|---|---|
| Reduce entry | Core fields first; optional groups initially collapsed; neither group must be opened to save | [Entering data — Best practices](https://developer.apple.com/design/human-interface-guidelines/entering-data#Best-practices) recommends appropriate defaults, meaningful choices, and understandable gating |
| Preserve work | Errors change error state, never reset the form | Product recovery decision following the installed Entering data procedure |
| Match inputs | Decimal amount input, email input, and date selection replace generic entry | [Virtual keyboards — Best practices](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards#Best-practices) |
| Explain corrections | Persistent labels and specific inline messages | [Text fields — Best practices](https://developer.apple.com/design/human-interface-guidelines/text-fields#Best-practices) |
| Explicit completion | One prominent Save Expense action with pending/failure/success behavior | [Buttons — Role and iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#Role) |

## Screen contract

Open a dedicated New Expense screen from the expense list. Order: title; instruction “Amount and vendor required. Review currency and date.”; Amount; Vendor; Currency; Expense Date; Show Receipt Details (Optional); Show Other Details (Optional); Save Expense.

Optional buttons expand their sections in place after the core fields and become Hide Receipt Details / Hide Other Details. Hiding retains values. Collapsed summaries report the number of entered fields. No wizard or mandatory review screen is added.

Provide a secondary Save Draft & Close button. It preserves incomplete and invalid input, then returns to a labeled Draft row in the list. System back uses the same policy. If draft persistence fails, stay on the form and show “Couldn't keep draft. Try again.” Reopening restores values and expanded sections. Ordinary touch entry initially focuses Amount; assistive entry starts at the screen title without a forced jump into input.

## Field and input contract

| Field | Default / representation | Entry, validation, and feedback |
|---|---|---|
| Amount (Required) | Empty. Keep raw text separately from exact decimal value and currency code; avoid binary floating point | Locale-aware decimal keyboard, paste, and hardware input. Allow intermediate empty text, separator, and trailing separator while typing. On leaving, require a finite positive amount and currency-appropriate precision. Show a specific error, such as “Enter an amount greater than zero.” Never silently strip punctuation, round, or reinterpret ambiguous pasted text |
| Vendor (Required) | Empty; retain Unicode text | Ordinary text keyboard with appropriate capitalization and correction; allow paste. Require non-whitespace on leaving: “Enter a vendor.” No forced suggestion or invented vendor database |
| Currency (Required) | Existing expense currency preference when available; otherwise Choose Currency | Ordered localized currency picker beside the value, showing name and ISO code. Locale alone does not establish transaction currency. Selection commits to the draft. Changing currency retains amount text and revalidates precision without conversion |
| Expense Date (Required) | Today at draft creation, visibly editable | Inline date-only calendar near the row; locale/calendar-aware display. Selection updates draft directly; collapsing hides the editor without reverting. Store date-only semantics, not midnight UTC. Resumption across midnight retains the selected date; time-zone changes must not shift it. No invented past/future restrictions |
| Email (Optional, in its existing appropriate detail group) | Empty unless an existing explicitly applicable value is known | Email keyboard and email semantics, no automatic capitalization/correction; permit paste. Validate nonempty syntax on leaving; empty passes. Explain format errors without claiming deliverability |
| Remaining existing fields | Preserve identities and values | Inventory is missing: define each value type, constraints, sensitivity, input, default, and validation before implementation. Do not assign every field the same keyboard |

Persistent labels remain visible after entry. Short text fields have trailing Clear controls named for their field; Clear affects only that value. No password prefill, new camera/upload workflow, contact access, or permission flow is introduced. Extended notes, if present in the missing inventory, need a separate multiline input decision.

The date choice follows [Pickers — iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/pickers#iOS-iPadOS); exact host-control availability remains unverified. Formatting and email timing follow [Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields#Best-practices).

## Validation, saving, and recovery

Save Expense is unavailable while required values are missing/invalid, nonempty optional values are invalid, or saving is pending. A nearby textual reason names the blocker, initially “Add amount and vendor to save.” Missing requirements are identified immediately without premature red errors. Validate touched fields on leaving, tolerate intermediate typing, and remove resolved errors promptly when validity is certain. Every alternative save entry point uses the same guard.

An invalid optional value must be corrected or explicitly cleared; never silently omit it. Expand sections containing errors. Multiple errors produce a linked summary and inline messages. On attempted commit, reveal the first invalid field for correction, retaining every other value. Text accompanies any error color.

Framework-agnostic state model:

1. Editing: each change updates raw draft values and persists a draft snapshot, including incomplete input. Validation never initializes a new draft.
2. Close/back: acknowledge draft persistence before returning to the list. Failure retains the screen and values.
3. Save: validate all applicable fields. If invalid, reveal errors and remain Editing. If valid, freeze a submitted snapshot and enter Saving.
4. Saving: show activity inside the initiating button with “Saving…”; prevent duplicate activation and simultaneous editing/closing while resolving the commit. Commit using a stable draft identity with idempotent retry.
5. Failure: return to editable state with persistent “Couldn't save expense. Try again.” Retain raw values, position, and expanded sections. Field-specific storage rejections also appear inline. Retry keeps the same identity. Unknown-outcome timeouts reconcile or retry idempotently before creating another record.
6. Success: only after durable acknowledgement, replace the draft with the saved expense and return to its persistent list row. Saved does not imply remote synchronization unless it completed.
7. Interruption: retain draft state through backgrounding; after restart restore the last acknowledged snapshot. If a commit was interrupted, reconcile by draft identity before retrying. Do not claim unsaved keystrokes survived a failed persistence operation.

Persistence, storage acknowledgement, and reconciliation are requirements for implementation, not demonstrated existing capabilities.

## Layout and access

Use a scrollable form that responds to actual keyboard bounds/insets. Keep the active field, correction, and Save Expense reachable and unobscured as the keyboard moves; do not hardcode keyboard height. Supply a labeled Next action from Amount to Vendor when the decimal pad has no Return. Text Return advances in logical visible order; Done dismisses input without saving. Save Expense explicitly commits. Hardware Tab follows visual order.

Buttons, including section and Clear actions, have at least 44 × 44 pt activation regions and clear separation. Custom buttons need perceivable press feedback. This adopts the [Buttons target recommendation](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices) and iOS default in [Accessibility — Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility). The accessibility guide's smaller 28 × 28 pt minimum is not the target chosen here.

Use title, section heading, body, and supporting-error text roles. Start body text from the iOS 17 pt default; support at least 200% enlargement, Bold Text, wrapping labels/errors, and growing rows. Prefer semantic platform text styles where available, otherwise equivalent scaling. Preserve essential content at the largest supported accessibility size. See [Typography — Supporting Dynamic Type](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type) and [Accessibility — Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision).

Controls expose names, roles, values, required status, expanded state, and associated errors. All commands support keyboard and assistive activation. Saving/failure have textual status; success remains discoverable in the list rather than only a timed toast. No essential gesture, sound, or color-only cue is required.

## Worked before/after

Illustrative scenario, not a recorded test: record coffee at Café North for EUR 12.50, with an existing EUR preference and today's date.

**Before:** The person encounters 28 requested fields with receipt details interrupting amount/vendor entry. Generic input serves different value types. A validation failure clears their entries, forcing re-entry. Exact original taps and error wording are unknown.

**After:** Open New Expense, type 12,50 in a comma-decimal locale, advance to Vendor, and type Café North. Review visible EUR and today's date; leave optional groups closed; tap Save Expense. Parse exact decimal 12.50 with code EUR. With the stated default, only two fields require typing; no email or receipt detail is required. This is a proposed reduction in required entry, not a measured speed improvement.

**Correction variant:** Paste 12,5x. On leaving Amount, show “Enter a valid amount for EUR, for example 12,50.” Preserve that text, Café North, date, currency, and optional data. Save's reason identifies the invalid amount. Correcting it to 12,50 resolves the error. If storage fails next, retain everything and offer retry. Retry uses the same identity and success creates one expense.

## Acceptance checks and status

**Passed — document inspection only:** All four supplied friction points have concrete replacements. This specification defines requested versus reused data, input/validation/gating, optional grouping, close/resume/save/failure states, and a worked correction path. The installed root, relevant families, topic procedures, and supporting passages were read. No web browsing was used.

**Failed — existing behavior reported by the brief:** Clearing values on validation failure; optional details interrupting core fields; all 28 fields blocking saving despite optional details; generic currency/email/date input. These are supplied observations, not reproduced runtime failures.

**Not executed — implementation acceptance:**

| Check | Pass condition |
|---|---|
| Minimal capture | Amount/vendor plus valid visible defaults save with both optional groups closed; absent currency preference requires explicit selection with an explained blocker |
| Value edges | Empty, separator-only, trailing separator, invalid suffix, zero/negative, over-precision, and large amounts preserve raw input and get appropriate commit validation; supported currency limits are documented |
| Locale/paste | Comma/period decimals, grouping, Unicode vendors, and ambiguous pasted amounts retain meaning or get correction; changing currency never silently converts or rounds |
| Email | Empty passes; malformed nonempty value gets inline feedback on leaving; clearing it unblocks save; @ and period remain available without unwanted correction |
| Date | Leap day, month/year boundaries, calendar/locale changes, midnight/resume, editor collapse, and time-zone changes preserve the intended date-only meaning |
| Retention | Validation, hide/show, background/resume, restart after acknowledged persistence, and close/reopen retain all fields including invalid raw input; persistence failure never falsely claims retention |
| Commit | Double activation creates one record; failure retains data; unknown timeout and retry reconcile by identity; success waits for acknowledgement |
| Keyboard/access | Decimal Next works without Return; Tab is logical; active field/error/action stay visible; names, values, required states, and errors are available to assistive navigation |
| Visual access | At 200%, largest supported accessibility size, and Bold Text, long labels/errors wrap without essential clipping or target overlap; measured targets meet 44 × 44 pt |
| Device checks | Exercise the same complete path using touch, VoiceOver, Switch Control, and Full Keyboard Access on a supported iPhone environment; measure contrast in light/dark and Increase Contrast; verify native input and rendering |

## Evidence limits and routing audit

Only interface.md and installed local guidance informed this document. Consulted references identify a 2026-10-25 snapshot. Official links identify source articles/sections but were not fetched. Local references are derived guidance, not SDK documentation or proof of independent review. No material conflict was found in consulted passages; target-size qualifications are retained above.

Installed package: .agents/skills/apple-hig/. Explicitly read its root SKILL.md, searched references/topic-index.md, then followed these family → topic → source routes. Topic and reference paths below are relative to the named family directory:

- subskills/apple-hig-patterns/SKILL.md → .topics/apple-hig-entering-data/SKILL.md → references/entering-data.md.
- subskills/apple-hig-selection-and-input/SKILL.md → .topics/apple-hig-text-fields/SKILL.md, .topics/apple-hig-virtual-keyboards/SKILL.md, .topics/apple-hig-pickers/SKILL.md → each corresponding reference.
- subskills/apple-hig-menus-and-actions/SKILL.md → .topics/apple-hig-buttons/SKILL.md → references/buttons.md.
- subskills/apple-hig-foundations/SKILL.md → .topics/apple-hig-accessibility/SKILL.md and .topics/apple-hig-typography/SKILL.md → corresponding references; typography decisions use its introductory legibility, hierarchy, and scaling sections.

Each read command targeted one file. No application, device, SDK, GUI, accessibility tool, persistence service, or usability session was executed. No native behavior, physical comfort, accessibility conformance, or measured efficiency is established. The missing field inventory, business rules, supported OS versions, currency catalog/precision limits, and persistence architecture remain implementation dependencies.
