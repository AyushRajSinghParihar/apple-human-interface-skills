# Mac inventory table audit

## Basis and decisions

The target is macOS inventory comparison and row selection. `interface.md` is the sole interface evidence: it reports missing headers, inconsistent quantity alignment, no sort indication, selection immediately activating Delete, and an unexplained blank filtered result. “Verified” below means explicitly documented in that file, not reproduced in a running app.

Keep a flat multicolumn table. Separate selection from commands, make quantities comparable, expose the current ordering, and explain zero results without discarding the filter. This is a framework-agnostic specification; no Apple SDK is required.

## Ranked verified findings

Priority reflects likely consequence and task obstruction, not measured frequency.

| Rank | Observed problem and effect | Correction and basis |
|---|---|---|
| 1 — Critical | Selecting a row activates Delete immediately. Merely choosing an item can initiate destructive work. Whether it actually removes data or opens a confirmation is unspecified. | Selection only updates selection state and feedback. Delete requires a separate explicit command, targets the selected stable record ID, and is disabled without an eligible selection. HIG distinguishes focus/selection feedback and recommends recovery for changes; separating these events is this audit’s concrete safety decision. See [Focus and selection — Best practices](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Best-practices), [Feedback — Best practices](https://developer.apple.com/design/human-interface-guidelines/feedback#Best-practices), and [Undo and redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo). |
| 2 — High | Missing column headers obscure attribute meanings and units. | Give each column a descriptive title-case noun or noun phrase without punctuation. Proposed schema: Item, SKU, Quantity; confirm these fields against the real inventory schema. Show quantity units in a heading or nearby context if quantities are not all counts. This directly follows [Lists and tables — Content](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables#Content). |
| 3 — High | Inconsistent quantity alignment prevents comparison. | Right-align count values and their heading consistently; use a consistent numeric format. Store quantities as numbers, not display strings. If fractional quantities exist, align decimal positions with consistent precision appropriate to the unit. These are audit design decisions for comparability, not a numerical-alignment rule stated in the consulted HIG article. The table’s comparison purpose is supported by [Lists and tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables). |
| 4 — Medium | Sorting is indicated nowhere, so the ordering cannot be understood reliably. The description does not establish whether sorting currently works. | Provide sortable Item and Quantity headers; repeat activation reverses direction. Show a direction indicator on the active header plus an accessible ascending/descending description. Default to Item ascending. Click-to-sort and reversal follow [Lists and tables — macOS](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables#macOS); the indicator and default are design decisions. Sort quantity numerically, with a deterministic ID tie-breaker. |
| 5 — Medium | An empty filtered list is an unexplained blank screen. People cannot distinguish no matches from failure or know how to recover. | Retain headers and filter controls; display “No items match your filters” with “Clear Filters.” Distinguish this from an inventory with no records, loading, and failure. Exact copy and recovery action are design decisions applying contextual state feedback from [Feedback — Best practices](https://developer.apple.com/design/human-interface-guidelines/feedback#Best-practices). Preserve clear filter scope per [Searching — Best practices](https://developer.apple.com/design/human-interface-guidelines/searching#Best-practices). |

## Corrected interaction specification

Use single selection initially; multiple selection is not established as a requirement. Keep keyboard focus distinct from selected record identity. Use a full-row selection highlight and visible focus indication, retaining active/inactive context. Do not rely on color alone: expose selected state, column associations, header sort state, control names, and result count through the implementation’s accessibility mechanism. These are required implementation outcomes, not claims of accessibility testing. See [Focus and selection — Best practices](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Best-practices).

Allow column resizing, following [Lists and tables — macOS](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables#macOS). Keep item identity recognizable at narrow widths. Alternating row backgrounds are optional HIG advice, not a verified defect or acceptance prerequisite here.

```text
state:
  records: map<stableID, InventoryRecord>
  filter: Filter
  sort: (Item, ascending)
  selectedID: ID or none
  focusTarget: control or row ID or none
  undoHistory, redoHistory

visibleRows = filterRecords(records, filter)
visibleRows = stableSort(visibleRows, typedComparator(sort), tieBreak=stableID)

on SelectRow(id):                 # click or table keyboard navigation
  require id is visible
  selectedID = id
  render selection feedback       # no command dispatch; no data mutation

on ActivateHeader(column):
  if sort.column == column: reverse sort.direction
  else: sort = (column, ascending)
  recompute visibleRows
  preserve selectedID             # identity, never a row index
  expose header's current sort state

on ChangeFilter(newFilter):
  filter = newFilter
  recompute visibleRows
  if selectedID is not visible: selectedID = none
  # Keep focus in the filter when typing; do not jump to a row.

Delete.enabled = selectedID exists AND selectedID is visible AND record is deletable

on ExplicitDeleteCommand():
  require Delete.enabled
  targetID = selectedID
  if deletion cannot be restored:
    request explicit confirmation naming the target and irreversible consequence
    if cancelled: return without mutation
  delete targetID as one transaction
  if restorable: record inverse transaction; clear redo history
  selectedID = none              # never select another destructive target implicitly
  retain valid focus; if a keyboard-focused row vanished, use a nearby row
  announce updated result count and deletion outcome

on UndoDelete():
  restore exact record and ID; recompute using current filter and sort
  expose restoration outcome even if current filters hide the restored record
  # Do not silently clear filters to reveal it.

render:
  loading -> explicit loading state, not “no matches”
  failed -> explain failure with Retry; do not label it empty inventory
  records empty -> “No inventory items” and an appropriate Add action if supported
  records nonempty AND visibleRows empty -> no-match message and Clear Filters
  otherwise -> table rows
```

Restorable deletion should offer Edit > Undo Delete Item and Redo Delete Item, with Command-Z and Shift-Command-Z per [Undo and redo — macOS](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#macOS). Do not require confirmation for every ordinary undoable deletion. Warn before unexpected irreversible loss per the Feedback guidance. Persistence and deletion reversibility must be determined before implementation.

Headers, filter controls, Clear Filters, and Delete must be keyboard reachable using the host’s conventions; arrows within the table select rows without executing Delete. Preserve standard keyboard commands and test Full Keyboard Access as advised by [Keyboards — Best practices](https://developer.apple.com/design/human-interface-guidelines/keyboards#Best-practices). These interaction mappings are specified behavior, not executed observations.

## Worked before/after

The following records are invented test fixtures, not supplied inventory data: A = Bolts, quantity 2; B = Nuts, quantity 10; C = Washers, quantity 3.

**Before, as described:** values lack headings and quantity alignment varies; ordering is unexplained. Selecting B activates Delete. Applying a filter with no matches leaves a blank screen. The actual row order and deletion outcome are unknown.

**After:** the initial Item ascending view has descriptive headings and aligned counts:

```text
Item ↑       SKU    Quantity
Bolts        A             2
Nuts         B            10
Washers      C             3
```

Select B: Nuts is highlighted; all three records remain; Delete becomes available. Activate Quantity: ascending order is A (2), C (3), B (10), with Quantity’s ascending indicator. B stays selected by ID. Activate Quantity again: B (10), C (3), A (2), with descending indication. Only a separate Delete command can remove B; an undoable implementation offers Undo Delete Item, which restores B with quantity 10 under the current ordering.

Apply an Item filter of “Cable”: show “No items match your filters,” a zero result count, and Clear Filters. Clear the hidden selection and disable Delete. Clear Filters restores the rows with the current sort preserved, without restoring a hidden destructive target automatically.

## Acceptance checks

These are pending checks for a future implementation, not passing runtime test results.

1. Every data column has a descriptive heading; quantities use a consistent alignment and unit/precision policy. Resizing leaves item identities understandable.
2. Clicking or keyboard-selecting B changes selection only: record count, data, and deletion history stay unchanged. No deletion confirmation opens merely from selection.
3. With no selection, Delete is disabled and command dispatch cannot delete. With B selected, only explicit Delete affects B. Cancelled irreversible deletion changes nothing; successful restorable deletion can be undone exactly and redone.
4. With fixture quantities 2, 10, 3, Quantity ascending yields 2, 3, 10 and descending yields 10, 3, 2. Repeated header activation reverses direction. Equal values have deterministic order. Visual and accessible sort states agree with actual ordering.
5. Sorting preserves B’s selection by ID. Filtering B out clears selection and disables Delete; clearing filters does not select a replacement automatically.
6. Zero filtered results retain the filter, show the no-match explanation and working Clear Filters, and preserve the current sort. Truly empty, loading, and failed states have distinct messages and appropriate recovery.
7. Keyboard-only and Full Keyboard Access checks reach all actions; focus and selection remain perceivable. Accessibility inspection confirms header/cell relationships, named controls, selected state, sort direction, result count, and useful outcome feedback. Check active/inactive selection and narrow layouts on the actual Mac implementation.

## Evidence limits and guidance trace

No source code, screenshot, runtime, actual inventory schema, persistence model, SDK, device, GUI, or accessibility execution was supplied or performed. Alignment, contrast, target sizes, localization, rendering, numeric accuracy, actual deletion, and assistive-technology behavior cannot be independently verified. The five findings are verified only against the written interface description. Corrected behavior and examples are specifications, not a patched application.

Read the installed root `.agents/skills/apple-hig/SKILL.md` first. Routed through layout-and-organization’s `SKILL.md` to `references/lists-and-tables.md`; consulted the root topic index for the exact table and selection topics. Also read the patterns and inputs family `SKILL.md` files before their selected articles: Searching, Feedback, Undo and redo, Focus and selection, and Keyboards. Each file was consumed with a separate single-file shell command. The selected families route directly to these article references; they did not prescribe an intervening topic procedure.

All guidance came from those installed local references (dated 2026-10-25 snapshot/retrieval metadata). Official links above provide attribution only; no web pages or videos were opened, and no newer guidance or API availability was verified. Source-backed guidance is distinguished from audit-specific design decisions throughout.
