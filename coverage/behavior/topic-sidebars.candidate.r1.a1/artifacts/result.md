# Responsive reading navigation specification

## Scope and decisions

The supplied `interface.md` names iPadOS/macOS and reports mixed library destinations, chapters and Delete Account, excessive narrow-window sidebar width, and loss of the book on collapse. These are reported problems, not independently observed runtime defects. This specification prioritizes iPad reading and includes explicit Mac differences. No framework or Apple SDK is required by this contract.

1. **Separate app navigation from book navigation.** Keep a shallow leading sidebar for the existing library destinations only; retain their actual names and IDs, which the brief does not supply. Do not invent new destinations. Opening a book enters its reading workspace. Its Contents list is a separate contextual pane, with the book title as heading and chapter rows below. Do not nest library → book → part → chapter inside the app sidebar. Deeper book structure belongs in Contents, with part headings and chapter rows, not extra sidebar levels. This applies the generally two-level sidebar guidance and coordinated pane model. [Sidebars, Best practices](https://developer.apple.com/design/human-interface-guidelines/sidebars#Best-practices), [Split views](https://developer.apple.com/design/human-interface-guidelines/split-views).
2. **Protect reading space.** Evaluate tabs first: the brief supplies neither destination count nor frequency, so a tab set cannot be justified. Choose a hideable sidebar without tab conversion for this revision; revisit tabs when those data exist. While reading, show at most Contents beside the reader; app navigation replaces Contents temporarily rather than creating three competing narrow columns. [Sidebars, iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/sidebars#iOS-iPadOS).
3. **Move Delete Account to in-app Settings → Account → Delete Account.** It is an account command, never a navigation peer of chapters. On iPad expose Settings at the top of app navigation, visually separated from destination rows; on Mac use App menu → Settings (Command-Comma), not the main toolbar. The deletion entry opens an explanation/review flow, never immediately deletes. Retain a discoverable real deletion route; disclose actual timing, retained data and subscription implications before commitment. Backend details are unavailable and must be supplied before implementing that flow. Returning without deletion restores the book. [Settings](https://developer.apple.com/design/human-interface-guidelines/settings#General-settings), [Managing accounts, Deleting accounts](https://developer.apple.com/design/human-interface-guidelines/managing-accounts#Deleting-accounts).

## Hierarchy and controls

- Library destination → book list → reader. Contents navigates only within the current book.
- Reader header: leading app-navigation button, book title, Contents button. Accessible names are “Show Library Navigation” and “Show Contents”; change Show to Hide when the corresponding pane is visible. Keep these controls reachable in all reader layouts. Shorten the visible title before removing navigation; a wrapping book heading in Contents always exposes its full title.
- Selecting a library destination shows that destination's book list and retains the current book as a resumable session. A “Resume [book title]” row above that list returns to its exact reading anchor. Only opening a different book replaces the active reader identity.
- Contents has a persistent heading and explicit return/hide control. In a narrow layout label it “Back to Reading”; it returns to the unchanged reader, rather than closing the book. Selecting a chapter navigates to its start and returns to the reader in compact layout; beside-reader Contents stays open.
- Selecting the already-current chapter is an explicit jump to its start. Merely opening Contents, focusing a row, collapsing or resizing never jumps there.

Use recognizable scalable symbols with text alternatives, semantic title/body roles and platform-appropriate selected styling. Navigation essentials cannot be removed by customization. On Mac mirror reader toolbar actions in menus: View → Show/Hide Library Navigation, View → Show/Hide Contents; Library → Resume Reading. A suggested Command-Shift-L binding toggles app navigation, subject to collision and international-layout verification. [Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars#Item-groupings), [Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards#Custom-keyboard-shortcuts).

## Responsive layout contract

Measure safe available window width W, excluding obstructions, in logical layout units corresponding to points on Apple platforms. Widths below are **initial product choices**, not Apple breakpoints. Recompute with text size and localized control measurements; never use orientation or device name as the switch. Let N be pane width: initially 280, increasing to 360 for enlarged text. Let R be the minimum reader width: initially 440, increased if actual reader controls cannot fit. G = 1 divider unit. Contents and app navigation share N and never appear simultaneously.

| Environment | Arrangement and transition |
|---|---|
| Expanded, W ≥ 1000 and N + G + R fits | Reader plus requested leading pane. First reading session defaults to Contents visible. User may hide it for full-width reading. |
| Intermediate, 721 ≤ W < 1000 and N + G + R fits | Reader plus requested leading pane. Initial Contents remains visible, but never grows by taking the reader below R. |
| Compact, W < 721, or fit test fails at any width | One surface at a time. Reader is the default reading surface. Opening Contents or app navigation replaces the reader with a full-width navigation surface, retaining reader state. Do not leave a sliver of reader behind a mostly full-width sidebar. |

Expanded and intermediate share a two-pane structure deliberately: this brief gives no reason for a third pane. In a library destination, the companion surface is its book list rather than the reader. Pane replacement does not mutate session state.

On shrink, visible navigation becomes its full-width counterpart if it has keyboard/assistive focus or was explicitly opened; otherwise show the reader. On expansion retain the foreground route and restore the requested pane beside the reader. An explicit user Hide overrides automatic reopening until Show is invoked. Never auto-open navigation just because width increased after the user hid it. Resize must not steal focus; preserve focused control identity across equivalent representations. If it must disappear, expose its equivalent restoration control and preserve the logical focus return target.

On iPad, a leading-edge inward swipe opens app navigation; visible buttons supply the same operation without a gesture. Opening navigation does not change the current destination. Do not intercept system gestures. On Mac provide visible, operable resizable dividers, initially constrain pane width to 240–400 units, and collapse the pane if reader fit fails. Larger sidebar sizing/text accommodations can raise these bounds and trigger compact layout. Restore through the header and View menu. Essential controls remain at the top, independent of an offscreen window bottom. [iPad design](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados#Best-practices), [Layout](https://developer.apple.com/design/human-interface-guidelines/layout#Adaptability), [Split views, macOS](https://developer.apple.com/design/human-interface-guidelines/split-views#macOS).

## State and long-content behavior

Store navigation identity separately from presentation:

```text
session = {libraryDestinationID, bookID, chapterID, readingAnchor}
perBook[bookID] = {chapterID, readingAnchor, contentsScrollAnchor}
presentation = {requestedPane: contents | appNavigation | none,
                foreground: reader | navigation | bookList,
                explicitlyHidden, focusReturnTarget}

resize(environment):
    save reader semantic anchor before repagination
    choose layout using available space and text/control fit
    project session and presentation into layout
    restore same book, chapter and semantic anchor after reflow
    // never clear bookID or open chapter 1 as a layout side effect

activateChapter(id):
    save old readingAnchor
    set chapterID = id; set readingAnchor = chapterStart(id)
    if compact: foreground = reader
```

A reading anchor identifies a text location, not a pixel offset or page number. Persist it per book on progress changes and before navigation/backgrounding; restore on reopening. Save Contents scroll by stable chapter ID plus within-row offset, not row index. Resize and app deactivation preserve the same session per window. No cross-device sync is implied.

Contents is one vertically scrolling list, in book order, with no silent limit on chapter count. Virtualization is allowed if all rows remain accessible. First opening reveals the current chapter; later openings restore browsing position, with a top “Current Chapter” action to reveal it. Highlight the current chapter persistently and add a non-color “Current” indicator; keyboard focus has a separate appearance and does not activate chapters.

Chapter rows show chapter number and full title, wrap without a fixed line limit, grow vertically and use normal readable leading. Break otherwise unbreakable strings to prevent horizontal overflow. This trades density for distinguishable long titles; do not shorten publisher titles to fit. Use body text roles, meaningful glyph scaling and Bold Text support. On iPad follow Dynamic Type; where unavailable offer equivalent text enlargement to at least 200%. On Mac use standard control typography and explicit app text sizing, without claiming macOS Dynamic Type. [Lists, Content](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables#Content), [Typography](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type).

With no book, omit Contents and show the library. With no chapter metadata, show “Contents unavailable” and Back to Reading; keep the book readable. A failed chapter load retains the previous reading anchor and offers Retry/Back to Reading; only commit the new chapter after successful load.

## Input and accessibility contract

Touch, pointer click and keyboard activation invoke identical actions; hover is never required. Use iPad activation areas of at least 44 × 44 pt as the default, expanding row height as needed. Mac starts from 28 × 28 pt default controls while respecting sidebar sizing preferences. These are platform defaults adopted for this design, not universal minima. Keep neighboring targets separate. [Accessibility, Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility).

Expose pane headings, named buttons, full chapter titles, navigation roles and selected/current state. Reading order follows header → active navigation list → reader when both are visible. Hidden surfaces are absent from traversal. Tab moves between logical content groups; arrows move within lists; Return activates a focused row. Full Keyboard Access must reach every header control as well as content. Escape cancels a temporary navigation visit without losing the reader. Explicit close/back returns to its opener; chapter activation takes the reader to the chosen chapter heading. [Focus and selection](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#iPadOS), [Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards#Best-practices).

## Worked before/after

Fixture (invented for verification): book B, 180 chapters; chapter 73 is “The Observatory Beyond the Northern Ridge — Second Expedition”; reader anchor is paragraph 12, character 80. Window narrows from W=1100 to W=600.

**Before, as reported:** library destinations, chapter 73 and Delete Account share one hierarchy. The sidebar consumes most of the narrow window; collapsing loses B. The brief does not say what replacement screen appears.

**After:** at 1100, Contents occupies 280 units and B occupies the remaining reader space. Chapter 73 is marked Current and its full title wraps. Shrinking to 600 while reading produces a full-width reader at the same semantic anchor after repagination. Show Contents opens the full-width chapter list; Back to Reading restores paragraph 12, character 80. Choosing chapter 74 instead opens its start. Show Library Navigation exposes only library destinations and separated Settings access. Settings → Account reaches deletion review without changing the reading anchor. Widening restores the requested Contents pane and selected chapter 74; explicit Hide keeps it hidden through later resizing.

## Acceptance checks and evidence limits

Static specification checks **passed**: all three reported problems have explicit corrections; hierarchy, compact/intermediate/expanded transitions, restoration paths, long lists, long titles, state identity, Mac differences and keyboard alternatives are specified. The worked fixture has determinate expected transitions. These passes assess this document only.

Reported baseline checks **failed according to the brief**: hierarchy separation, narrow reading-space protection and book preservation. No baseline execution was available to corroborate them.

Implementation acceptance checks — **not executed**:

| Check | Required observable result |
|---|---|
| Resize 1100 → 800 → 600 → 800 → 1100; test around 720/721 and 999/1000 | Same book, chapter and semantic anchor; no clipped required controls; focused navigation remains reachable. |
| Hide, resize, then restore; iPad edge swipe and button; Mac View command and header | Explicit Hide persists; every restoration path returns the same navigation identity. |
| 180 chapters; duplicate title prefixes; very long title/string; final row | Full titles distinguishable, all chapters reachable, current and focus visually distinct. |
| Default, 200% and largest supported text; Bold Text; short window | Rows grow, controls remain reachable, fit failure selects one surface; no essential clipping. |
| Browse Contents, dismiss, reopen; select a different library destination then Resume | Contents scroll restores; reader anchor survives; only deliberate chapter/book activation changes it. |
| Keyboard only, ordinary content focus and Full Keyboard Access separately | Can open navigation, reach chapter 180, activate, return, hide and restore without pointer; shortcuts do not conflict. |
| Assistive traversal, Switch Control and Voice Control | Correct full labels, roles, selected state, hidden-surface exclusion and complete task access. |
| Missing chapters or failed load; background/reactivate and reopen | Reader remains recoverable; failure does not commit incorrect chapter; saved anchor restores. |
| Light/dark, increased contrast, sidebar size preferences | Selected/current state remains understandable without color; measured contrast and target geometry meet the chosen design criteria. |
| Mac partly offscreen bottom and app activation changes | Essential commands remain reachable at top/menu; commands target the active window's preserved session. |

Only local supplied files and installed guidance were used; official links above identify source articles and were not fetched. The installed references describe a 2026-10-25 snapshot and are derived guidance, not SDK documentation or proof of independent source review. No source conflict material to these decisions was found in the passages used. Breakpoints, pane widths, chapter fixtures and command naming are product proposals needing measurement. No device, browser GUI, SDK compilation, native gesture, accessibility, font, contrast, geometry or physical-comfort execution occurred. Account retention, billing and backend behavior remain unknown; this sidebar specification does not establish legal compliance or a completed deletion implementation.
