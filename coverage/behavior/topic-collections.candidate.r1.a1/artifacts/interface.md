# Adaptive photo collection specification

Platform: iOS/iPadOS, iPhone and iPad, including rotation and resizable iPad windows. Task: browse an album, identify a photo, open its full image, and select multiple photos. No framework is prescribed by the supplied brief. The rules below replace fixed six-column layout, rotation-cleared selection, thumbnail-only meaning, and blank empty albums.

## Layout and cell contract

Use a familiar vertically scrolling collection in stable album order. Default order is capture date descending, with stable photo ID as tie-breaker; missing dates follow dated items. Keep existing order until a deliberate reload after external changes; never reorder while scrolling, selecting, or resizing. Item count does not change density or interaction.

Let W be safe-area content width after 16 pt leading/trailing margins. Use 8 pt gaps. At ordinary Dynamic Type sizes, columns C = max(1, floor((W + 8) / 112)); image side S = (W - 8 × (C - 1)) / C. Thus 104 pt is the target minimum image width, an app choice, not an Apple minimum. At accessibility text sizes use one column with a 104 pt thumbnail and a wrapping text region alongside it; stack thumbnail above text when W < 260 pt. Grow row height to fit all text. No horizontal scrolling. Short windows retain vertical scrolling and reachable controls.

Examples (all widths in points, after device safe-area exclusion but before margins):

| Available width | W | Columns | Image side |
| --- | ---: | ---: | ---: |
| 320 | 288 | 2 | 140 |
| 390 | 358 | 3 | 114 |
| 768 | 736 | 6 | 116 |
| 1024 | 992 | 8 | 117 |

Do not force six columns on narrow iPad windows or phones. The same available width produces the same grid rules on both devices. Respect system safe regions for all content and actions. Recompute on resize, orientation, text-size, or Display Zoom changes; these environmental changes may reflow immediately, but must preserve identity and location.

Each cell contains an undistorted square thumbnail, then a wrapping caption on a solid system background: supplied photo title (fallback filename), and localized capture date (fallback “Date unknown”). Use system body style for title, secondary text style for date, supporting Dynamic Type and Bold Text. No essential caption truncation. Deliberate aspect-fill cropping is a browse preview only; detail presents the entire image with aspect-fit, including panoramas and document edges. A neutral unavailable-image placeholder keeps the same geometry and text.

Provide meaningful existing photo descriptions as text alternatives. If none exists, announce title/filename and date and explicitly use “No description available”; do not infer a subject or imply metadata describes the image. Detail exposes any supplied description in readable text too. This makes identification available without thumbnail recognition, while acknowledging absent descriptions limit access to visual content.

## Interaction and state

Use system collection selection and named button activation rather than gesture-only image actions. In browse mode activating a cell opens detail by stable ID; its accessible name combines title, date and description if available, with a button role. Detail includes a labeled Back action returning to the originating cell and scroll position.

A visible “Select” button enters selection mode. Cell activation then toggles selection; expose selected state programmatically and with a checkmark plus outline, independent of color. Show “N selected” and “Done”; Done exits selection mode and clears selection deliberately. Select is unavailable for a genuinely empty album. All controls have at least 44 × 44 pt activation regions, separated without overlapping adjacent targets. Standard pressed, disabled, focus and pointer feedback remain visible within cell bounds. Scrolling must not activate cells. No required long press, pinch, drag or custom multifinger gesture; manual reorder and drag transfer are outside this revision.

Persist selectedIDs, selection mode, detailID, and scroll anchor (first visible stable ID plus its offset below the content top) across rotation, iPad resizing, background restoration and return from detail. Restore the anchor after reflow, clamping only at the content end. Keep keyboard/assistive focus on the same item when it survives. Never use row index as identity. New external items are held behind a visible “Show updates” button; activation applies the new snapshot while retaining surviving IDs and anchor. If an item is removed externally, remove only its ID from selection and report “1 selected photo is no longer available” when applicable. If the anchor/detail item disappears, return to its next surviving neighbor, otherwise previous, otherwise the empty state. No deletion command is added here.

Logical accessibility and keyboard traversal follows the displayed item order, with controls before content and each cell encountered once. Support activation and selection via Full Keyboard Access, VoiceOver and Switch Control without touch-only steps. Offscreen items must remain reachable through standard collection scrolling. Enlarged text, focus and hover must not overlap neighbors or hide actions. Use semantic system colors; check light/dark and Increase Contrast against actual rendered backgrounds. Required state information never relies on color alone.

## Scale and availability

Use the same collection for 20 and 20,000 items. Virtualize/reuse cells; load ordered metadata in pages of 200, with total count and an indexed stable-ID lookup so anchor restoration can fetch the relevant page directly. Keep at most five metadata pages resident; retain selected IDs separately. Preserve a stable order snapshot across page boundaries with no duplicates or omissions. Do not require decoding earlier photos to reach a later page.

Request display-sized thumbnails for visible cells and at most one viewport ahead/behind. Cancel obsolete requests on reuse and bind completion to both stable ID and request generation so a late image cannot populate another cell. Use a bounded decoded-thumbnail cache (initial budget 64 MiB) and at most four simultaneous decodes; release offscreen decoded images under memory pressure. Full-resolution decoding occurs only for detail and is released when no longer needed. These are initial engineering budgets requiring profiling, not HIG performance guarantees. For 20 items this path can complete in one page; for 20,000 it must never eagerly decode all originals or instantiate all cells.

Initial metadata pending: show “Loading photos” until the first page resolves; never claim the album is empty before success. With known items, preserve the grid while further pages load and show a trailing “Loading more photos” status. Thumbnail loading/failure keeps cell text and selection usable. Initial failure: “Photos couldn’t be loaded” with “Retry”. Later-page failure retains existing cells and adds “More photos couldn’t be loaded” with Retry for that page; prevent duplicate retries while pending. Errors do not clear state or alter order.

Successful zero-item result: album title, “No photos in this album”, and “Photos added to this album will appear here.” Keep the existing album-back navigation available. Do not add an import flow or fabricate permission actions absent product requirements. Empty, pending and failed states are distinct. Updates that remove the final item transition to this explained empty state.

## Acceptance contract

Check 0, 1, 20, 21 and 20,000 items at the widths above, intermediate iPad resizing, both orientations, short heights, default and largest accessibility text, and 200% text enlargement. Require no clipped captions, unreachable controls, horizontal overflow or overlapping targets. Check a long title, missing date/description, panorama, portrait and bright/dark image content.

Select stable IDs A and B, open detail, rotate/resize and return: IDs, mode, anchor and focus survive. Scroll during a late thumbnail response: no accidental activation or wrong image. Apply updates with insertions, a removed selected ID, and removed anchor; require the specified survivor and status behavior. Verify final partial rows and first/last cells keep focus feedback visible. Reorder is intentionally unavailable.

For 20,000 items, trace page/cache/decoder counts while scrolling to the end and restoring a deep anchor, under slow loading, failure/retry and memory pressure; require the bounded work above and no duplicate/missing IDs. Measure responsiveness on supported iPhone/iPad hardware before accepting performance; no timing guarantee is established by this document. Exercise browse → detail → back and Select → toggle → Done with VoiceOver, Switch Control, Full Keyboard Access, touch and iPad pointer. Measure contrast and hit geometry in the implementation.

## Guidance basis

These are product rules informed by the installed local HIG snapshot, not universal Apple grid dimensions. Apple recommends familiar collections, cautious layout changes during manipulation, and enough space for focus: [Collections](https://developer.apple.com/design/human-interface-guidelines/collections). Width/environment adaptation and safe regions follow [Layout](https://developer.apple.com/design/human-interface-guidelines/layout). Text growth and wrapping follow [Typography](https://developer.apple.com/design/human-interface-guidelines/typography). Meaningful alternatives, non-color state and input access follow [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility). Actionable photos use button behavior per [Image views](https://developer.apple.com/design/human-interface-guidelines/image-views) and [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons). The layout guide’s numerical TV grids are tvOS-specific and are not applied to iPhone/iPad.
