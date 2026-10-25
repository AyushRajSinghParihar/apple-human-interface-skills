# Revised iPad inventory interaction specification

## Scope and evidence

`interface.md` is the entire supplied product description: iPadOS, fixed 1024×768 positioning, clipped names, controls underneath system bars, selection discarded when a second window opens, and counts ranging from zero to five digits. These are reported defects, not independently observed runtime results. No implementation, screenshot, action inventory, minimum window size, or font measurements were supplied.

Design assumption: the core task is scanning inventory and selecting one item. This revision supplies a single inventory list and a nondestructive **Open in New Window** action for inspecting the selected item in a separate inventory window. Existing business actions must retain their outcomes and follow the same placement and reflow rules; their labels, permissions, and write behavior require a later product contract. This specification introduces no stock editing, deletion, sorting, or reorder operations.

## Decisions

1. **Use available window space.** Replace absolute coordinates with a flow layout inside the host-provided unobscured content region. Recompute on resize, rotation, system inset changes, and text preference changes. Backgrounds may extend beneath bars; names, counts, and hit regions may not. Respect window-control exclusion regions as well as safe-area insets. Do not hard-code bar heights or infer width from the iPad model. This applies [Layout — Adaptability and safe areas](https://developer.apple.com/design/human-interface-guidelines/layout#Adaptability) and [Windows — iPadOS](https://developer.apple.com/design/human-interface-guidelines/windows#iPadOS).

2. **Keep one list at all widths.** Reading order is Inventory heading, selected-item summary and actions, then inventory records. Each row contains the full item name and a labeled count. Wide rows place name leading and count trailing; narrow or enlarged-text rows stack count below name. No fixed row height, maximum line count, ellipsis, horizontal scrolling, or text shrinking. Very long unbroken names may wrap between grapheme clusters as a last resort. All records remain reachable through vertical scrolling. Text rows suit scanning; a detail pane is unnecessary for the two supplied fields. See [Lists and tables — Content](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables#Content) and [Typography — Supporting Dynamic Type](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type).

3. **Measure fit instead of choosing an orientation breakpoint.** Product spacing tokens are 16 pt content margins, 12 pt row padding, and 12 pt between peer fields. These are proposed values, not Apple mandates. Let C be usable content width after margins and row padding; let Q be the measured width of the widest localized stock label for the current data, including a five-digit fixture; let N be 12 em at the current item-name style. Use side-by-side fields only when C ≥ N + 12 pt + Q and the text category is not an accessibility category. Otherwise stack. Name text can still wrap in wide mode. If a stock label alone cannot fit, wrap its label above the unabridged number. Never split a number across lines. Measure with the current font, weight, locale, and text scale. No guessed pixel-to-point equivalence is required.

4. **Preserve readable text.** Heading uses a title role; names use emphasized body; counts and action labels use body. Prefer the platform's semantic font service when available. A non-Apple implementation must provide equivalent preference-driven sizing and Bold Text behavior through its host adapter; it must not assume Apple font APIs are present. Default body reference is 17 pt. Support at least 200% enlargement and every supported iPad larger accessibility category, including the largest; 200% is not a cap. Grow rows and buttons with their text. See [Typography — Ensuring legibility](https://developer.apple.com/design/human-interface-guidelines/typography#Ensuring-legibility) and [Accessibility — Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision).

5. **Treat count as data, including zero.** Render zero as “Stock: 0 — Out of stock”; five digits as a full locale-formatted value, for example “Stock: 99,999” in en-US. Never replace zero with a blank, dash, or false-like absence. Missing counts are a distinct “Stock unavailable” value. Do not abbreviate counts to “100K.” Out-of-stock meaning is conveyed in words, independent of color. Reserve/measure count width using actual localized strings, not five character cells.

6. **Make selection and actions explicit.** Activating a row selects its stable item ID in that window without changing stock. Show a selected indicator plus a distinguishable outline/background and expose selected state programmatically. Repeated activation is idempotent. The summary reads “Selected: [full name]” or “Select an item.” **Open in New Window** is a normal, lower-emphasis text button below the heading/summary, enabled only with a valid selection; the empty summary explains the disabled state. Activation requests one new inventory window initialized with that selected ID. There is no implicit Return default. Press/focus feedback must be perceivable. Touch, pointer, and keyboard activation reach the same outcome; hover is unnecessary. Use activation regions at least 44×44 pt, growing with labels, with 12 pt separation between peer buttons. Buttons wrap their labels and stack when their measured widths do not fit. The 44 pt target follows [Buttons — Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices); the local accessibility guide also lists a smaller minimum, which this design does not use as its default.

7. **Keep controls reachable in short windows.** Heading, summary, actions, and rows share one primary vertical scroll owner, so oversized headers cannot consume the entire usable viewport. No pinned overlay or same-axis nested scroller. Preserve the top visible item ID and within-item offset during reflow, clamping as needed. Reveal focused content only enough to make its activation region visible. A row taller than the viewport remains readable by scrolling. See [Scroll views — Best practices](https://developer.apple.com/design/human-interface-guidelines/scroll-views#Best-practices).

## State and transition contract

```text
shared inventory: records keyed by stable item ID
per window: windowID, selectedID?, topVisibleID?, withinItemOffset,
            focusedControlID?, lastKnownTextPreferences

on environmentChange(bounds, exclusions, textPreferences):
    capture scroll anchor and focused control
    recompute unobscured region and measured field/button fit
    reflow without changing selectedID or record order
    restore anchor; minimally reveal focused control if needed

on select(itemID):
    set only this window.selectedID = itemID
    persist this window's restoration state

on openInNewWindow:
    request new window with selectedID copied by value
    leave source selection, focus, and scroll anchor unchanged
    while request pending, prevent duplicate request from this activation
    on failure, keep source context and expose persistent inline error + Retry
    on success, new window reveals selected row; source scroll stays unchanged

on windowClose:
    retain restoration state under that window's identity
    never clear another window's selection

on restoreWindow:
    restore selection and anchor if their IDs still exist
    if selected item was removed, clear selection and show “Item no longer available”
    preserve surviving scroll anchor; otherwise use nearest surviving successor,
    then predecessor, then list start
```

Windows share inventory data but own navigation state. Selecting B in window 2 must leave A selected in window 1. Repeated deliberate opens may create separate windows with independent IDs; resize never opens a window. Restoring a closed window restores its own context; an unrelated fresh launch starts unselected. If the dataset is empty, show “No inventory items,” preserve the heading, and disable the selection-dependent action. No automatic selection of another item after deletion by an external source. These ownership choices are product decisions applying [Windows — Best practices](https://developer.apple.com/design/human-interface-guidelines/windows#Best-practices) and [Designing for iPadOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados#Best-practices).

## Worked before → after

Fixture: item A is “Stainless steel hex bolts — M8 × 120 mm — warehouse replenishment pack,” stock 0. Item B has stock 99,999. A is selected.

**Before (reported):** the 1024×768 layout clips A's name, leaves absolute-positioned actions vulnerable to system bars, and discards A when another window opens. Exact clipping and coordinates are unknown.

**After (specified):** at a 1024×768 window, safe-region subtraction occurs first; if measured fit succeeds, A's wrapped name sits beside “Stock: 0 — Out of stock.” B displays all of “Stock: 99,999.” On resizing to a 375×600 pt test window with 200% body text, both rows stack name over count, row heights grow, and actions flow onto their own lines. At the largest accessibility category, stacked layout applies even in a wide window. A remains selected and the scroll anchor survives. Opening window 2 copies A; selecting B there leaves A selected in window 1. Returning to the original size changes arrangement without resetting either window. These dimensions are test fixtures, not verified supported OS bounds or measured font-fit outcomes.

## Acceptance checks and status

**Passed — document inspection:** supplied defects are mapped to revised behavior; the specification includes zero/five-digit data, reflow rules, action reachability, and independent window state. Installed root → family → topic procedures were explicitly read before their supporting guides. Only local sources were used.

**Failed — supplied baseline contract:** the brief reports clipping, unsafe placement, and lost selection. This records the brief's failures; no runtime reproduction occurred.

**Not executed — implementation acceptance:**

| Scenario | Required observable result |
|---|---|
| Smallest/largest host-supported windows; 375×600, 600×375, 768×1024, 1024×768 pt where allowed; continuous intermediate resizing | No overlap or inaccessible action; layout follows usable width and measured text; selection and anchor persist |
| Default, 200%, every supported text category through largest accessibility size; Bold Text | Full names, counts, and button labels remain readable; no forced shrinking, fixed-height clipping, or target overlap |
| Insets/window controls change; onscreen keyboard if present | Content and hit regions remain in unobscured region; focus can scroll into view |
| Zero, 1, 99,999, missing count; long/unbroken names; empty and long datasets | Exact values and all records accessible; zero differs from missing; no silent omissions |
| Two windows, resize either, select independently, close/restore either, repeated opens and failed open | Stable per-window selection/anchor; correct item identity; failure does not clear source state |
| Touch, pointer, keyboard, Full Keyboard Access, Switch Control, VoiceOver | Every row/action reachable and activatable; names/roles/selected states identify the same item; focus order follows visual task order; no gesture-only command |
| Light/dark and Increase Contrast, long localization, RTL | Meaning independent of color; measured text/state contrast appropriate to actual colors; localized counts remain intact and peers do not collide |

Check activation regions independently of glyph size. Use the source's 44×44 pt iPad default, verify separation and actual hit geometry, and test assistive navigation on a supported Apple environment. Detailed spoken grouping/rotor behavior requires a later VoiceOver-specific design and validation pass.

## Evidence limits

This is a framework-agnostic design artifact, not an implemented screen. No device, Apple SDK, GUI, accessibility service, font measurement, contrast calculation, or window lifecycle was executed. Numerical spacing and fit thresholds are proposed product choices requiring measurement. Apple links identify the official sections represented by the installed local snapshot (dated 2026-10-25); no web verification or independent media review was performed. Physical comfort, native safe-area delivery, actual Dynamic Type mapping, focus restoration, and multiwindow persistence remain unverified until implementation and supported-environment testing.
