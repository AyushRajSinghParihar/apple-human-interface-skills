# Revised Mac specimen archive browser

## Basis and decisions

The supplied `interface.md` describes three arbitrary columns for search results, status, and size; selecting a child loses parent context. Deep paths, long folder names, and empty folders are explicit requirements. No implementation, screenshot, specimen dataset, or runtime was supplied.

Replace those three columns with a horizontally scrollable, root-first hierarchy browser. Each column represents one level, not one attribute. Preserve selected ancestors when revealing children. Status and size become labeled metadata for the selected item. This fits the documented use of columns for deep, frequently traversed hierarchies where attribute sorting is unnecessary. Apple also recommends resizable columns and suggests meaningful leaf previews. [Column views — Best practices](https://developer.apple.com/design/human-interface-guidelines/column-views#Best-practices)

Product assumption: traversal is the primary task; status/size comparison and sorting are secondary. The brief does not establish sorting requirements. If cross-folder attribute sorting proves central, reassess a table/outline rather than overloading these navigation columns. This is a browsing specification, not an Open/Save replacement, and assumes no SDK.

The exact state rules, dimensions, search matching, and keys below are product decisions applying the guidance; they are not claimed as Apple mandates.

## Layout and identity

- Column 0 is headed “Archive root” and contains the configured root folder. It is always the first logical column. Selecting it reveals its immediate children in column 1. There is no fixed three-column limit.
- Every subsequent column is headed with its parent folder's name and contains only that parent's immediate children. Each row has a folder/file indicator and name. Folders have a trailing disclosure triangle, including empty folders; the marker communicates navigability, not a guarantee of contents. Files do not.
- Single selection per column. Highlight the selected ancestor chain persistently; distinguish keyboard focus from selection. Use immutable item IDs and parent IDs, never display names or row indices, as identity. Duplicate names in different branches remain distinct.
- Sort children by name using locale-aware natural ordering with a stable ID tie-breaker. Status and size are not navigation columns or sort controls. Unknown size reads “Not available”; folder size reads “Not calculated” unless a verified aggregate exists. Do not report unknown size as zero.
- For a selected file, use the next area for a detail panel: full wrapping name, type, complete path, status text, size if known, and available modification date. Provide a preview only when supported; otherwise say “Preview unavailable” while keeping metadata. Selecting a folder shows its full name and available metadata above its child list, including an empty child list.
- Add a noneditable segmented path in the window body above the browser. It shows root through selected item; activating a folder segment selects that folder and shows its children. The final file segment identifies the selection without launching another app. No destination chooser or path-drop editing is implied. Placement and compact ancestry follow [Path controls](https://developer.apple.com/design/human-interface-guidelines/path-controls#Best-practices).

## Selection and asynchronous transitions

State consists of `rootID`, `selectedChain`, `focusedRegion`, `columnWidths`, per-column vertical offsets, horizontal offset, and `mode = browse | search`. `selectedChain` starts with the root; every adjacent pair must be a verified parent/child relation. On initial load, select the root and request its children.

```text
select(itemID, columnIndex):
    verify item belongs to columnIndex's parent (or is root in column 0)
    invalidate outstanding descendant requests
    selectedChain = prefix before columnIndex + itemID
    remove all columns and details after columnIndex
    update path from selectedChain immediately
    if folder:
        append child area labeled with this folder, state = loading
        request children(itemID, newGeneration)
    else:
        append details bound to itemID; request available metadata/preview

receive(request, payload):
    accept only if generation, target ID, and current branch still match
    replace loading with children, empty, or error for that target
    never insert results from a previous branch
```

Selecting a different ancestor removes all former descendants and previews synchronously, before loading. Selecting the same item retains its child state and scroll position. Returning to an ancestor retains that column's vertical offset, but does not silently reselect a previously visited descendant. No child is auto-selected on load.

An empty folder yields a next-column message, “This folder is empty,” with its parent's name and zero items. It remains selected and navigable back to its ancestors. Loading is labeled “Loading contents…”; failure is “Couldn't load contents” with a Retry action. Neither is represented as an empty folder. An unavailable/deleted selection clears invalid descendants, keeps the deepest verified ancestor, and shows a persistent explanatory message. Retry cannot restore an obsolete branch.

## Deep paths, resizing, and long names

Start hierarchy columns at 260 logical layout units wide, with a 180-unit minimum; these are provisional product values to validate, not HIG measurements. Allow widening up to the viewport width by dragging a separator and through a keyboard-accessible “Column width” setting. Store widths per depth for the current window. Never shrink all columns to fit a deep path.

Use horizontal scrolling when widths exceed the viewport. Reveal a newly created child area while retaining its parent onscreen when space permits. At narrower widths, prioritize the active area, retain the logical ancestor columns, and expose them through scrolling and the path control. Root remains reachable through its path segment even when its column is offscreen. Resizing changes presentation only; it never clears selection, changes branch, or exits search.

Rows may truncate long names at the tail with an ellipsis. Resizing, a hover tooltip, and the wrapping full-name area for the selected item expose the original name. Hover is supplementary: keyboard selection also exposes the complete name, and accessible names never contain the visual truncation. Path overflow preserves the root and selected item where possible; an explicitly labeled ancestor overflow menu lists every hidden segment in order, using full wrapping names. For extremely narrow space, a selected-item path pop-up exposes the entire hierarchy. No ancestor becomes unreachable.

## Search contract

Keep one trailing toolbar search field labeled “Search archive names,” with placeholder “Search all archive names.” Scope is the configured root and all descendants, independent of the current selected folder. Use explicit scope labeling and preserve result identity across resizing, following [Search fields — macOS](https://developer.apple.com/design/human-interface-guidelines/search-fields#iPadOS-macOS) and [Searching — Best practices](https://developer.apple.com/design/human-interface-guidelines/searching#Best-practices).

Entering a nonempty query saves the browse chain and scroll state once, then displays a separate result list; search results must not masquerade as hierarchy levels. Product baseline matching is case-insensitive name substring matching, including folders and files. Each result carries ID, kind, full name, and ancestor path to disambiguate duplicates. No relevance, content search, or complete indexing claim is implied. Show the actual search coverage and any unavailable portions; never label an incomplete scan as exhaustive.

Update during typing when feasible. Each query has a generation token: old results clear or become explicitly noncurrent when a new query starts and cannot be activated as current matches. Distinguish “Searching…”, “No matching names”, partial coverage, and failure with Retry. Result selection shows item details; activating “Reveal in archive” or pressing Return reconstructs and verifies its complete root-to-item chain, exits search, and selects the exact item. A folder reveals children; a file reveals details. On resolution failure, retain the query and identify the unavailable result; do not navigate to a different item with the same name.

Clearing search or Escape from the search field restores the saved browse chain and offsets, revalidating missing ancestors as above. Clear leaves focus in the field; Escape returns focus to the previous browser row. Reveal commits a new browse location, so clearing afterwards cannot restore an older branch. No search history, predictive suggestions, or external Spotlight integration is specified in this version; these need corpus and privacy evidence before design. The supplied brief does not establish their availability.

## Input and access contract

Within a hierarchy column, Up/Down selects the previous/next row and applies the selection transition. Right enters the child list and selects its first row if any; at an empty folder or file it leaves selection unchanged. Left focuses the selected parent row and selects that parent, clearing its descendants. At root it does nothing. Pointer row selection has the same branch semantics. Path segments provide a visible alternative to backward traversal.

Tab/Shift-Tab follow the configured keyboard access behavior through search, path, browser, details, and actions; arrow handling applies only while the browser owns focus. Option-Command-F focuses search; Escape cancels search as specified. Keep text editing and system accessibility shortcuts intact. Show command names and bindings in the app's command presentation. Do not derive unrelated commands from reserved shortcuts. These proposed mappings require verification in the implementation and on supported Mac keyboard layouts. [Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards#Best-practices)

Specify each row's full name, file/folder kind, selection state, and child relationship as accessible information. Label each child list by its parent, each path segment by its full name, and width controls by the affected column. Status uses text rather than color alone. Loading, empty, failure, and completed result counts must be available as state information without transferring focus unexpectedly. Reading order follows the current path from root through children to details, excluding removed descendants.

At 200% text enlargement, allow taller rows, wrapping headings/details, and scrolling without removing essential actions. Use platform-equivalent readable text and visible focus; measure actual contrast and activation areas during implementation. No automatic animated scrolling is required. These access requirements apply [Accessibility — Vision, Mobility, Speech](https://developer.apple.com/design/human-interface-guidelines/accessibility); they do not establish runtime accessibility support.

## Worked before/after

Synthetic fixture, not a supplied archive: `Specimen Archive / Marine / Expedition 2024 — North Atlantic voucher specimens / Lot 0007 / image-001.tif`; sibling `Lot 0008` is empty. A separate root branch is `Botany`.

**Before, as described by the brief:** the three columns contain results, status, and size. Choosing a nested folder loses its parent context. The brief supplies no exact screen sequence, truncation behavior, or empty-state behavior, so those are unknown rather than observed defects.

**After:** select the root, Marine, the long expedition folder, then Lot 0007. The columns are successive hierarchy levels and retain those selected rows. Selecting `image-001.tif` produces a path ending in that ID and details for that file. Widen the expedition column or inspect its wrapping selected name to read the full name.

Select sibling Lot 0008 in the lot column. The former image column and preview disappear immediately; the next column reads “This folder is empty.” The root, Marine, expedition, and Lot 0008 remain in the path. Select Botany in the root's children: the entire Marine suffix disappears. A late Lot 0007 preview response is rejected. Activate the root path segment to return to the beginning. Search for `image-001`, then reveal its exact result to reconstruct the original chain without treating results/status/size as parents.

## Acceptance checks and current evidence

**Passed — document inspection only:** the revised contract defines root-first columns, folder/file selection, descendant invalidation, empty folders, complete-name access, resizing, leaf details, search restoration, and a route to root. The synthetic scenario is traceable through these rules. Installed root, selected family routes, topic procedures, and their local source guides were explicitly read in that order before applying guidance.

**Failed — supplied design description:** retaining parent context fails according to `interface.md`; the three attributes do not implement the expected parent-to-child hierarchy. These are brief-level findings, not observed runtime test failures.

**Not executed — implementation acceptance:**

| Check | Required observable result |
|---|---|
| Root → deep folder → file | Each column contains only the selected parent's children; correct file details and full path |
| Switch to sibling and then another root branch during loading | Old descendants disappear immediately; late data never repopulates them |
| Select empty folder; simulate access failure | Empty state differs from loading/error; ancestor navigation and Retry work |
| Return to root from depth 12 | Root segment works; column order stays root-first; no detached selection |
| Resize a long-name column; narrow and expand window | Full name remains obtainable without hover; identity and offsets remain coherent |
| Select duplicate-name search result | Reveal reaches the selected ID's actual ancestry, not another namesake |
| Change query rapidly; clear; no results; delete a result | No stale activatable matches; browse restoration works; missing result explains failure |
| Keyboard-only completion and width adjustment | Root-to-file, sibling traversal, search/reveal/clear, Retry, and resizing need no pointer |
| 200% text; light/dark and Increase Contrast | Essential names/actions remain usable; measured contrast and geometry meet chosen criteria |
| VoiceOver, Full Keyboard Access, Switch Control on Mac | Names, relationships, states, reading order, focus, and activation support the complete task |

## Evidence limits

This is a framework-agnostic specification written on a headless Linux server. No SDK compilation, GUI, device, keyboard, filesystem permission, accessibility, contrast measurement, search latency/relevance, or native rendering test was run. No code or archive was provided to execute. Dimensions and example data are proposals requiring validation with representative archives and Mac users.

Guidance came exclusively from the installed package's dated local snapshots. Official links above identify the source articles; they were not fetched. The local references report a 2026-10-25 snapshot/retrieval date and are independent application guidance, not SDK documentation or proof of independent source review. No claim is made about newer guidance, API availability, or native behavior in an unspecified framework.
