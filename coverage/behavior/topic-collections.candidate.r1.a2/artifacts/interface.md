# Adaptive photo album — iOS and iPadOS

## Scope and task

Browse, identify, open, and select photos in albums containing 0, 20, or 20,000 items. Preserve the existing product and implementation framework; no framework is supplied. A collection remains appropriate because visual recognition is the primary task. The following geometry, thresholds, loading budgets, and navigation choices are product decisions, not Apple-prescribed measurements.

## Layout contract

Use one vertical scrolling collection inside the current window's safe area. Header contains album title, localized item count, and Select. Keep controls outside photographs. Respect system navigation and Back gestures. Do not nest a second vertical scroller around the grid. Show the native scroll indicator and allow partial rows to suggest more content.

Let W be safe-area width in points. Use 16 pt leading/trailing margins and 8 pt horizontal/vertical cell gaps. Available grid width A = W − 32. At ordinary text sizes, minimum cell width M = 104 pt. Column count C = max(1, floor((A + 8)/(M + 8))); cell width S = (A − 8(C − 1))/C. Never add columns based on item count or stretch an incomplete last row. For supported widths smaller than M + 32, use one cell fitted to A. All interactive targets remain at least 44 × 44 pt, with separate nonoverlapping hit regions.

| Safe-area W | Columns | Cell width S |
|---|---:|---:|
| 320 pt | 2 | 140 pt |
| 390 pt | 3 | 114 pt |
| 768 pt | 6 | 116 pt |
| 1024 pt | 8 | 117 pt |

These are width examples, not device breakpoints: a narrow iPad window follows the narrow rule. Resize continuously on rotation, multitasking, or Display Zoom without changing album, order, selection, or open photo. Keep focus rings inside each cell's reserved space without covering neighboring content.

Use semantic system title, body, and caption styles with Dynamic Type and Bold Text. Each cell has an image and a caption below it on a semantic background: user title if available, otherwise localized capture date/time, otherwise filename. Caption may use two lines at ordinary sizes; full text is always available in photo detail. At accessibility text sizes use M = 240 pt, growing caption height with unlimited lines and stacking metadata. Reduce columns further if measured text cannot fit; never shrink text to retain density. Header controls wrap into additional rows rather than clipping. Preserve all actions through at least 200% text enlargement and the largest supported accessibility size.

## Image meaning and detail

Fit the entire photo proportionally in a square image area using neutral letterboxing; never stretch it. This conservative choice avoids hiding subjects when focal-point metadata is absent. Use an image inside a system button, with a single accessible element grouping image and caption. In browse mode activation opens that photo's detail. Detail shows the whole photo and complete caption, known description, date, and filename, and offers Back. Back restores the originating photo and scroll context.

Accessible name: title plus a known content description when it adds information, then date/time; fallback to filename and “Description unavailable.” Do not invent a visual description from a filename or present metadata as a full equivalent of photo content. Expose button role and selected state separately; do not repeat the caption as a second focus stop. Example with supplied metadata: “Maya at the beach, sunset behind Maya, October 12, 2026, 18:03.” The dataset must supply useful descriptions for meaningful visual content; missing descriptions remain a content-accessibility limitation.

## Identity, selection, and changes

Maintain immutable photo IDs, an ordered ID snapshot, selected-ID set, mode, open-photo ID, and scroll anchor (first visible photo ID plus its offset from the viewport top). Do not store selection or restoration solely by cell index. Select enters selection mode with an empty set; tapping a cell toggles its membership instead of opening detail. Show a checkmark and outline as well as selected semantics, and a persistent “N selected” count. Done leaves selection mode and explicitly clears selection. Select is unavailable for an empty album. Selection provides state only; downstream batch commands are outside this brief.

Rotation, resizing, background/resume, and return from detail preserve mode and selected IDs. Before reflow capture the anchor; after reflow restore its row to the same viewport offset, clamped at the ends. Preserve accessibility/keyboard focus on its photo ID and reveal only as far as necessary. Explicit Done or leaving the album ends selection. Persist album route, open photo, selection, and anchor for restoration where the implementation supports scene restoration; specify and test this before claiming process-relaunch restoration.

Defer background insertions/reordering while scrolling or selecting; show an “Update Album” button when a new snapshot is ready. Activation applies it while retaining surviving selected IDs and anchor. If an item is removed externally, remove its ID from selection, update the count with an accessible notification, and use the next surviving item in the old order as anchor/focus, otherwise the previous item. If none survives, enter empty state. Never substitute a new photo at the old numeric index. User reordering and deletion commands are not introduced.

## Scale and retrieval

Use the same layout and identity rules for 20 and 20,000 photos. For 20, all metadata may load together; show the incomplete final row naturally. For 20,000, virtualize/reuse cells and page ordered metadata in batches of 200 with stable cursors over the album snapshot. Fetch a lightweight month-to-first-ID index and total count independently, so reaching older photos does not require downloading preceding thumbnails.

For albums over 200 items, show a labeled “Jump to Month” button opening a dedicated month index screen with year headings, month buttons, counts, and Back. Activating a month loads its metadata page and reveals its first photo, retaining selection; cancellation returns to the unchanged anchor. Unknown capture dates form a final “Date Unknown” group. Keep order chronological newest first, with immutable ID tie-breaks; no ranking-driven reshuffles. For small albums omit this navigation. This threshold is a product choice.

Decode thumbnails off the main thread at rendered pixel size; prioritize visible cells and prefetch at most one viewport before/after. Cancel stale requests on reuse and verify returned photo ID and rendition size before display. Cap decoded thumbnail cache at 64 MiB with eviction; lower it under memory pressure. Fetch full-resolution content only for the open detail and release it on exit. Metadata pagination must not rebuild or decode the entire album. These budgets require profiling, and are not verified performance claims.

## States and controls

- Initial loading: retain title and Back; show “Loading photos…” until metadata resolves. Do not display empty copy during loading.
- Ready: show actual count and cells. Thumbnail loading reserves image/caption geometry; failure shows “Preview unavailable” and a labeled Retry Preview action in detail. Keep metadata and selection usable.
- Empty, only after successful zero count: “No Photos in This Album” and “Photos added to this album will appear here.” Keep Back available; do not invent an import capability.
- Metadata failure: “Couldn’t Load Photos” with Retry; retain already loaded cells, selection, and anchor. Further-page failure appears after the loaded content with Retry, never as a false end of album. Retry repeats only the failed request and suppresses duplicates while pending.
- Month jump failure: retain the index and offer Retry without resetting the grid's saved context.

Use system buttons with short visible labels, standard press/focus feedback, and minimum 44 × 44 pt targets. Back, Select, Done, Update Album, Jump to Month, month choices, and Retry have their stated immediate outcomes and ordinary nondestructive roles. Keep Retry context visible while its activity indication runs. Every operation is available by touch, keyboard/Full Keyboard Access, and assistive activation; pointer hover is optional feedback. Arrow navigation follows displayed rows, activation opens/toggles as appropriate, and standard system shortcuts remain intact. Scrolling must never activate a photo.

Expose album title and month/year headings for assistive navigation. Reading order follows locale order across each row then downward; captions stay with photos. Loading changes must not steal focus or announce every thumbnail. Announce relevant errors, selected-count changes, and snapshot updates. Use semantic foreground/background colors; selection must remain understandable without color. Measure contrast in light/dark and Increase Contrast. With Reduce Motion use immediate reflow and state changes without zoom/spring transitions; preserve identity and location.

## Source basis

Local installed HIG snapshot consulted; official links identify guidance, not a live web verification:

- [Collections — Best practices and iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/collections): familiar grids, selectable items, understandable layout changes; explicit updates preferred during interaction.
- [Layout — Adaptability and safe areas](https://developer.apple.com/design/human-interface-guidelines/layout), [iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios), [iPadOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados): adapt to available space and preserve task context.
- [Typography — Supporting Dynamic Type](https://developer.apple.com/design/human-interface-guidelines/typography), [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility), [VoiceOver — Descriptions and Navigation](https://developer.apple.com/design/human-interface-guidelines/voiceover): reflow, meaningful equivalents, semantics, input access, and preferences.
- [Image views](https://developer.apple.com/design/human-interface-guidelines/image-views), [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons), [Scroll views](https://developer.apple.com/design/human-interface-guidelines/scroll-views): actionable image semantics, standard controls, one scroll owner, and minimal reveal.

Acceptance matrix and evidence status are recorded in result.md.
