# Revised Mac specimen archive browser

This is a framework-agnostic interaction contract, based on `interface.md`. It specifies a resizable macOS workspace for traversing deep specimen folders. It requires no Apple SDK. The brief establishes three unrelated columns (search results, status, size), loss of parent context, long folder names, and frequent empty folders; it supplies no running interface or representative archive. Examples below are synthetic.

## Decisions

Replace the three fixed-purpose columns with a root-first hierarchy browser. Each vertical column represents one hierarchy level, never an attribute. Root column contains the named archive root; selecting it reveals its immediate children. Selecting a folder reveals its children immediately to the right and leaves every selected ancestor visible when space permits. Folder rows have a trailing navigation triangle, including empty folders; files do not. Single selection per level defines one unambiguous branch.

This follows [Column views — Best practices](https://developer.apple.com/design/human-interface-guidelines/column-views#Best-practices): columns suit deep, frequently traversed hierarchies when table-style sorting is unnecessary. The brief supplies no requirement to sort or compare status/size. Default to name ordering; status and size remain available for the selected item. If attribute comparison becomes the primary task, reconsider a table or outline rather than turning hierarchy columns back into attributes.

Use the next area after a selected file for a detail summary: full name, full archive-relative location, type, status, and size with units. Show “Unknown” for unavailable metadata; never substitute zero. A file preview is optional and appears only if its format is supported; the summary always works without it. Folder status and size can appear in a summary below the browser, identified by the selected folder's full name. Folder size is “Not calculated” unless supplied; browsing must not require recursive size calculation. Metadata placement and these strings are product decisions; HIG suggests considering useful leaf previews and metadata, rather than requiring a particular preview implementation.

Do not retain search results as a hierarchy level. Any existing search surface remains separate. Its result-to-browser handoff must resolve the selected result's ancestor IDs from the archive root, then select and reveal that branch. If resolution fails, keep the current branch and report the unavailable result; never invent a parent relationship. Search query, ranking, and search UI redesign are outside this brief.

## Selection and state contract

Store stable item IDs, parent IDs, node kind, per-column width and vertical scroll position. Names are labels, not identity. The archive root is the navigation boundary.

```text
state = { rootId, selectedChain, columns, focusedColumn, requestGeneration }

selectRow(level, itemId):
    require itemId belongs to columns[level]
    increment requestGeneration
    selectedChain = selectedChain before level + itemId
    discard columns after level and all previous preview/metadata
    mark item selected; make level the focused column
    if item is file:
        show summary bound to itemId
    else:
        append child column bound to itemId, initially loading
        request children(itemId, requestGeneration)

receiveChildren(parentId, generation, result):
    ignore unless generation is current and parentId is selectedChain.last
    replace loading area with rows, empty state, or error
    do not automatically select a child
```

The root is selected on first entry, revealing its contents. Selecting a sibling ancestor immediately clears the former descendants, even while new data loads. Every metadata response uses the same selected-ID/generation guard. A late response cannot reintroduce another branch or preview.

An empty folder remains a folder: keep its row selected and show “This folder is empty” in its child column. Provide “Go to Parent”; at the archive root this action is unavailable. A pending request says “Loading folder…”; an unsuccessful request says “Couldn’t load this folder” with “Retry.” Never interpret failure or pending work as emptiness. These are proposed states for potentially asynchronous archives, not observed implementation defects. Clear, actionable empty/error copy follows [Writing — Best practices](https://developer.apple.com/design/human-interface-guidelines/writing#Best-practices).

Go to Parent truncates the chain by one item, retains the parent selection and its children column, and focuses that parent's row. At a file, this selects its containing folder. Go to Archive Root selects root, removes deeper selections, reveals root children, and scrolls the browser to its beginning. Neither command leaves old detail content visible. Switching to another app and back preserves the branch, widths, scroll positions, and command target.

## Width, depth, and input

Allow independently resizable columns. Starting values are product defaults, not HIG measurements: 240 logical points wide, minimum 160. Do not impose a name-length-based maximum. A divider drag changes only that column and preserves selection. Offer View > Fit Selected Column to Name as a keyboard alternative; it measures the longest loaded label in that column plus row adornments. Overflow uses horizontal scrolling rather than shrinking every column into illegibility.

Names use one row with middle truncation when necessary. The selected-item summary always exposes the complete, selectable, wrapping name and location, including for folders. Resizing therefore is not the only way to read a name. Do not rely on hover alone. Names with identical visible fragments remain distinguishable by selecting them and reading their full names.

On descent, scroll horizontally only enough to reveal the new child column and its selected parent where feasible. At narrow widths, earlier columns can move offscreen; retain them in the scrollable strip. Go to Parent and Go to Archive Root remain available through the menu regardless of horizontal position. Resizing a window never changes the branch or converts columns into attributes. These overflow policies are product choices applying HIG's root-first and resizable-column guidance.

Use one resizable workspace; support ordinary window and full-screen arrangements without requiring full screen. Put navigation commands in a Go menu and sizing in View. Menu and any visible control invoke the same state transitions and enabled states. This applies [Designing for macOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos#Best-practices).

Proposed keyboard contract while the browser owns focus:

| Action | Input and outcome |
|---|---|
| Select sibling | Up/Down selects adjacent row and applies the same selection transition as a click; stops at list boundaries. |
| Enter folder | Right moves to its child column and selects its first row, if loaded and nonempty; otherwise stays on the parent. |
| Return | Left invokes Go to Parent; no change at root. |
| Reach all commands | Menu navigation exposes Go to Parent, Go to Archive Root, Retry when applicable, and Fit Selected Column to Name. |
| Move between controls | Tab/Shift-Tab follows the host's keyboard navigation policy; no keyboard trap. |

Do not intercept browser arrows when a text field or selectable summary text owns focus. Distinguish focused target from persistent ancestor selection visually. No custom global shortcut is required. Preserve system and text-editing shortcuts; actual menu reachability and Full Keyboard Access require later Mac testing. These requirements apply [Keyboards — Best practices](https://developer.apple.com/design/human-interface-guidelines/keyboards#Best-practices); the exact browser arrow mapping is a product decision.

## Worked before/after

Synthetic branch:

```text
Specimen Archive / Marine Invertebrates /
North Atlantic Expedition 1902 — Station 014 — Preserved Reference Specimens /
Tray A / specimen-0042.tif
```

Before, as described by the brief: the three columns mean Search Results, Status, and File Size. Choosing Tray A loses its parent context; the brief does not establish how that loss is rendered or what resizing does.

After selecting through Tray A:

```text
[Specimen Archive ▸] | [Marine Invertebrates ▸] | [North Atlantic…Specimens ▸] | [Tray A ▸] | specimen-0042.tif
```

Each bracketed row is a persistent ancestor selection in its own level. Widen the expedition column or read its full name in the selected-folder summary. Select the file: its parent chain remains and the following area shows its summary, including its full location. Change the expedition selection to sibling “Pacific Expedition 1903”: Tray A, the file column, and the file summary disappear immediately; only the Pacific children can populate the next column. If Pacific contains an empty “Uncatalogued” folder, selecting it retains the Pacific path and shows the empty-folder message with Go to Parent. Returning to root reveals the archive's children without any stale specimen preview.

## Acceptance checks and evidence limits

Static specification checks passed: the contract assigns one hierarchy level per column; retains ancestor IDs; defines descendant invalidation, root return, leaf summary, long-name access, empty-folder behavior, width/overflow policy, and keyboard actions. These are document checks, not execution results.

The supplied design fails the stated task at the brief level: its three columns represent unrelated information and choosing a child loses parent context. No additional runtime defects were observed.

All implementation checks below are **not executed**. Each is a required acceptance scenario for a future implementation:

| Check | Pass condition |
|---|---|
| Deep traversal | Traverse six levels; each selected child has the selected parent immediately to its left in the model. Horizontal scrolling recovers every ancestor. |
| Sibling change and races | Switch an ancestor while old child/metadata requests are pending. Former descendants clear immediately; delayed responses never appear in the new branch. |
| Root return | From a leaf and from a horizontally scrolled narrow window, Go to Archive Root reveals root children and clears stale detail. |
| Long names | Use two 200-character names with matching prefixes. Resize and fit the column; select each and read/copy its complete name from the summary without hover. |
| Empty folder | Empty folder stays selected; child area reports emptiness and Go to Parent returns correctly. Loading and error are distinguishable from empty. |
| Leaf identity | Select two different files; each summary's name, location and metadata match only the current file. Unknown size is never displayed as zero. |
| Narrow/expanded window | Resize while deep in a branch. IDs, selection and widths survive; scroll and menu routes remain usable. |
| Keyboard task | Without a pointer, reach a deep file, inspect its name, visit an empty sibling folder, fit a column, retry a failure, and return to root. Text editing retains its normal keys. |
| Activation and command consistency | Switch apps and return; selection survives. Menu and visible actions target the same selected ID. |
| Mac access verification | Exercise Full Keyboard Access and assistive-technology traversal on a Mac; verify focus visibility, full names, hierarchy relationships, and empty/error announcements. |

Only local `interface.md` and installed skill instructions/references were used; no web browsing occurred. Official links identify the sources recorded in the local snapshots, dated 2026-10-25; they were not fetched or independently verified. Root skill, relevant family routes, topic procedures, and their guides were explicitly read from the installed package; the topic index was searched for matching concepts. No device, SDK, GUI, build, performance, keyboard, localization, or accessibility execution occurred. No archive samples establish real depth, latency, name distributions, metadata semantics, or sorting needs. Defaults and synthetic examples therefore require validation with representative specimen archives.
