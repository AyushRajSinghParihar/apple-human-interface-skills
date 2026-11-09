# Mac inventory table audit

## Scope and evidence

This is a specification audit of [interface.md](interface.md), the only supplied interface evidence. Its statements verify what the brief reports, not observed application behavior. There is no dataset, implementation, screenshot, runtime, or declared framework. No web browsing, SDK, device, GUI, keyboard, or accessibility execution was performed.

The installed apple-hig root SKILL.md was explicitly read from `.agents/skills/apple-hig/`. Routing followed the topic-index search and these family → topic → local source paths:

- Layout and organization → Lists and tables → `references/lists-and-tables.md`.
- Inputs → Focus and selection; Keyboards → their respective references.
- Menus and actions → Buttons → `references/buttons.md`.
- Foundations → Writing → `references/writing.md`.
- Presentation → Alerts → `references/alerts.md`, for conditional deletion confirmation.

All paths above are within the installed package's `subskills/apple-hig-<family>/` directories; topic procedures are under `.topics/apple-hig-<topic>/SKILL.md`. Each file was read separately, with family and topic procedures preceding their supporting guide. These local guides are derived snapshots, not SDK documentation or proof of independent source review. Official links below identify supporting guidance; they were not fetched.

## Ranked verified findings

Priority reflects potential harm and task impact, not measured frequency. All five findings are verified against the brief only.

| Rank | Reported problem and effect | Decision and source support |
|---|---|---|
| 1 — High | “Selecting a row activates Delete immediately.” Selecting an item can invoke a destructive command when the person is only targeting it. Actual record loss and reversibility are unknown. | Selection changes the selected record only. Delete requires a separate explicit command. Keep focus, selection, and activation distinct: [Focus and selection, Best practices](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Best-practices); clarify command outcome and role: [Buttons, Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Role). |
| 2 — Medium | Column headers are missing. People cannot reliably identify the attributes being compared. | Add descriptive noun headings such as Item, Identifier, and Quantity, subject to the actual schema. Use title case without punctuation: [Lists and tables, Content](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables#Content). |
| 3 — Medium | Quantity alignment is inconsistent and comparisons fail. Inventory comparisons become harder and potentially misleading. | Use one right-aligned numeric column with consistent formatting and an explicit unit when needed. This exact alignment/formatting choice is an audit recommendation serving the table's comparison task; the loaded table guide does not explicitly mandate right alignment. |
| 4 — Medium | Sorting is indicated nowhere. People cannot determine the current ordering. This does not establish that sorting is absent or incorrect. | Show the active sort column and direction in its heading, including a textual equivalent. Support useful heading sorting and reversal, as advised for [macOS tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables#macOS). The specific indicator and stable tie-break rule below are product decisions. |
| 5 — Medium | An empty filtered list is an unexplained blank screen. People cannot distinguish no matches from missing inventory or a failed load. | Show “No Matching Items” with “Try changing or clearing the filters.” Offer Clear Filters. Empty states should provide a useful next action: [Writing, Best practices](https://developer.apple.com/design/human-interface-guidelines/writing#Best-practices). |

## Corrected behavior and decisions

Retain a flat multicolumn table for attribute comparison. No evidence justifies a hierarchy or image collection. Proposed Item/Identifier fields and integer quantities are illustrative; confirm schema, unit, precision, and missing-value semantics before implementation. Never replace a missing quantity with zero.

Keep headers visible in the zero-results state. Allow column resizing on Mac. Preserve the recognizability of long identifiers, using middle truncation where useful and a route to the complete value. In narrow windows, preserve useful minimum widths and allow horizontal scrolling; in expanded windows, allocate extra width primarily to identifying text. These sizing choices are product decisions, while resizing and recognizable content follow the table guidance above. Long lists must retain access to every matching record; virtualization must not change record identity or truncate the dataset.

Use stable record IDs rather than row positions for selection and commands. For this correction, choose single selection; batch selection is outside the supplied requirements. Clicking a row selects it and shows a persistent row highlight. Moving focus to another control does not clear selection. Distinguish active and inactive selection from keyboard focus and a pressed button. No row selection, hover, focus entry, or arrow navigation dispatches Delete.

The input contract is pointer click or Up/Down within the table to select a visible row. Sorting is available from the heading using pointer or keyboard activation. Under Full Keyboard Access, the logical route includes sortable headings, table rows, Delete, and Clear Filters when present, with a route out of the table. This is a proposed route, not a claim about tested Mac focus behavior. Preserve text-editing keys in editable controls and system shortcuts; no custom delete shortcut is introduced. See [Keyboards, Best practices](https://developer.apple.com/design/human-interface-guidelines/keyboards#Best-practices).

Place a text-labeled Delete command beside the table in the view body. It is enabled only for a valid visible selection and is not the window's default Return action. With no selection, “Select an item to delete” explains its unavailable state. Button activation targets the selected ID, never the current row index. Provide distinct press, focus, and disabled feedback; actual geometry is unmeasured.

Deletion recovery is not supplied. Before shipping, establish whether deletion is reversible. Do not invent Undo support or claim all deletion requires confirmation. Common undoable deletion generally needs no confirmation; uncommon irreversible destruction warrants one ([Alerts, Best practices](https://developer.apple.com/design/human-interface-guidelines/alerts#Best-practices)). For an irreversible implementation, the proposed continuation command is Delete… and opens:

- Title: Delete Inventory Item
- Message: “Permanently delete Cable (INV-002)? This cannot be undone.” Substitute the actual target and use this wording only if permanent deletion is true.
- Leading action: Cancel. Trailing action: Delete. No default action; Return alone does not confirm. Escape or Command-Period cancels. This no-default choice is a conservative product decision, not a universal prohibition on destructive defaults; the guide allows a normal default for explicitly requested destruction ([Alerts, Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons)).

Capture the target ID when the explicit command begins. Cancellation changes no data or selection. A successful deletion clears selection and disables Delete; do not silently select another deletion target. If focus was on the disappearing row, remove its indicator rather than guessing another record for this explicit-command flow. A failed deletion preserves the record and selection, shows a useful failure message, and re-enables retry. Pending operations reject duplicate activation. A changed or missing target must be revalidated before commit.

## Framework-agnostic state contract

```text
state: recordsById, filter, sort = (Item, ascending), selectedId = none
       focusedControl, pendingDeleteId = none, deleting = false
visibleRows = stableSort(filter(recordsById), typedSortValue, recordId)

select(id):
  require id in visibleRows
  selectedId = id                         // no mutation, no command dispatch

activateHeading(column):
  sort = (column, reverse(direction)) if already active
         else (column, ascending)
  // selectedId remains stable even if its row position changes

changeFilter(value):
  filter = value
  if selectedId not in visibleRows: selectedId = none
  // never leave an invisible record eligible for Delete

requestDelete():
  require selectedId in visibleRows and not deleting
  pendingDeleteId = selectedId            // fixed identity, not row index
  apply established recovery policy       // irreversible: confirmation above

commitExplicitDeletion():
  require deliberate activation and revalidated pendingDeleteId
  deleting = true
  on success: remove that ID; selectedId = none; pendingDeleteId = none
  on failure: retain data/selection; explain failure; allow retry
  deleting = false

render:
  show headers and current sort key/direction
  align quantities consistently; compare typed numbers, not formatted strings
  if records exist and visibleRows is empty:
    show No Matching Items + remedy + Clear Filters
  else if records are empty:
    show No Inventory Items; do not claim filtering caused it
```

Clear Filters resets all active filters, preserves the chosen sort, and restores all inventory records. It does not restore a hidden selection automatically. Loading and errors must not be represented as successful empty results; their actual data lifecycle remains unspecified.

## Worked before/after

Illustrative fixture, not supplied inventory:

| Stable ID | Item | Quantity |
|---|---|---:|
| INV-001 | Adapter | 12 |
| INV-002 | Cable | 2 |
| INV-003 | Dock | 100 |

Before, as reported: no headers, inconsistent quantity placement, no ordering cue; selecting Cable immediately activates Delete. Applying a filter with no matches produces a blank screen.

After: headers read Item, Identifier, Quantity. Item initially indicates ascending order. Selecting Cable highlights INV-002 and enables Delete; all three records remain. Activating Quantity yields Cable (2), Adapter (12), Dock (100), with Quantity ascending indicated. A second activation yields Dock (100), Adapter (12), Cable (2), with descending indicated; INV-002 remains selected despite moving. Numeric sorting avoids the string order 100, 12, 2.

Filtering to “Printer” clears the now-hidden selection, disables Delete, and displays No Matching Items with Clear Filters. Clearing filters restores all three rows in Quantity descending order, with no selected record. Selecting Cable again and explicitly choosing Delete starts only the established deletion flow. In the irreversible branch, Cancel preserves Cable; explicit confirmation deletes only INV-002 and clears selection.

## Acceptance checks and status

**Passed — static audit:** Read the supplied brief and routed local guidance; mapped the five supplied issues to concrete corrections; specified selection, sort, filter, deletion identity, and empty-state transitions. A manual specification walkthrough using 2, 12, and 100 produces the ascending/reversed orders shown above. This is reasoning over the contract, not executed application testing.

**Failed — supplied specification:** The five reported behaviors fail the intended contracts: labeled columns, comparable quantities, visible ordering, non-destructive selection, and explained empty results. These are brief-level failures, not runtime test results.

**Not executed — implementation acceptance:**

| Check | Required observable result |
|---|---|
| Select, focus, and arrow through rows | Correct stable ID is highlighted; no delete invocation or data mutation. Moving focus away retains selection. |
| Activate each useful sort heading twice | Correct typed order and reverse, matching visible/textual direction; ties deterministic; selected ID retained. |
| Filter out selected item; then clear filters | Hidden selection cleared, Delete disabled, useful no-results content shown; all records recover without restoring an unintended target. |
| Explicit deletion, cancellation, failure, duplicate press | Correct captured ID only; cancellation preserves data; failure supports retry; no duplicate deletion or stale-target commit. |
| Delete last row | No stale selection; Delete unavailable; true empty-inventory message replaces filtered-no-results copy. |
| Resize narrow/wide; use long IDs and long lists | Usable resizable columns, full-value access, consistent quantities, all matching items reachable. |
| Pointer and complete keyboard task | Reach sort, selection, deletion/cancel, and Clear Filters; exit each control; preserve text editing and system commands. |
| Native rendering and assistive access | Verify focus/selection distinctions, header/value associations, sort state and command names, disabled states, and traversal with supported Mac tooling. |

No implementation, native appearance, hit region, Full Keyboard Access behavior, VoiceOver result, SDK compilation, or live data integrity is established. Actual schema, initial ordering, deletion persistence/recovery, input bindings, layout limits, and filtering UI remain unknown. Resolve those during implementation; missing evidence is not an additional verified defect.
