# Editable book ratings — revised macOS interaction specification

## Scope and decisions

The supplied `interface.md` is the only product evidence: empty ratings appear as zero-star failure; clicking a star deletes the review; imported read-only ratings look editable; half ratings and no rating exist; keyboard access is required. No implementation, screenshots, or data schema were supplied. This specification proposes a catalog row editor and does not require an Apple SDK.

1. **Separate missing from low.** Use `null` for no rating, displayed as **Not rated** with no failure styling. Proposed scale: 0–5 inclusive in 0.5 steps. A stored numeric zero means **0 of 5**, never missing. The brief does not establish whether zero is a valid legacy score; preserve existing numeric zeros pending data validation rather than silently converting them to null.
2. **Preserve exact values.** Display five fixed-spacing star positions for numeric ratings, plus an always-visible exact label, such as **3.5 of 5**. Whole-symbol presentation rounds with `floor(value + 0.5)`, so 3.5 shows four filled stars; the label and accessible value remain 3.5. Explain beside the rating column: “Stars round to the nearest whole star; numbers show the exact rating.” Never rewrite stored fractions merely by displaying them. This rounding tie rule is a product decision; the local guide does not specify it. [Rating indicators](https://developer.apple.com/design/human-interface-guidelines/rating-indicators)
3. **Edit directly in the row.** Editable rows show an explicit **Edit rating** entry beside the indicator. Clicking a star sets that whole-number value immediately; clicking the current star again is an idempotent set, not a toggle or deletion. The inline editor provides exact half-step choices and a separate **Clear rating** action. Do not open a separate book screen to rate. [Rating indicators — Best practices](https://developer.apple.com/design/human-interface-guidelines/rating-indicators#Best-practices)
4. **Rating and review are independent fields.** Set, clear, undo, failure recovery, and cancellation affect only the personal rating. Review text, formatting, attachments, and imported data remain intact. No rating interaction invokes review deletion. This is a product correction to the destructive behavior reported in the brief.
5. **Make imported values visibly informational.** Label them **Imported rating · Read-only**, with exact numeric value or **Not rated**. Render stars as static content, without editable bezel, hover preview, edit action, or hand cursor. Keep text readable rather than dimming it to illegibility. If personal and imported values coexist, use distinct **Your Rating** and **Imported Rating** columns/labels; do not overwrite the imported value. Read-only applies at the persistence boundary as well as the view.

## Row, input, and state contract

A row is keyed by immutable `bookId`; selection, edit target, and focus are distinct. Selecting a row never changes its rating. A rating click consumes the activation so it cannot open book details or delete anything. Multi-selection never turns a single row edit into a batch edit.

The resting editable row contains the indicator/exact label and Edit rating. The inline editing state replaces those controls with a single-choice list of **Not rated**, **0 of 5**, **0.5 of 5**, …, **5 of 5**, followed by **Apply**, **Cancel**, and **Clear rating**. All choices are in the same row area, which can expand vertically. Opening initializes the draft to the stored value. Choosing a draft does not save; Apply saves it and closes the editor. Cancel or Escape discards the draft. Clear rating immediately commits null and closes the editor; disable it when already null. Opening, hovering, tabbing, and focusing never commit a value.

Pointer star targets map positions 1–5 to integer values; half ratings are available through the inline choices without requiring precision targeting. Use fixed glyph spacing and stable hit regions; wider columns add whitespace rather than stretching stars. Target 28 × 28 pt activation regions for Mac controls, including star targets, with nonoverlapping adjacent regions; this is the local accessibility guide's default Mac control size, not a claim of measurement. At narrow widths or 200% text enlargement, expand the row to preserve the exact label, provenance, and actions. [Accessibility — Vision and Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility)

Keyboard route: focus the catalog, select a book with its normal row navigation, Tab to that row's Edit rating, then Space or Return to open. Tab/Shift-Tab traverse the choice group and actions and can leave the editor without saving. Inside the choice group, Up/Down move the draft by one choice (0.5 numerically); Not rated precedes zero. End selects 5; Home selects Not rated. Clamp at endpoints. Space selects the focused choice; Return in the group applies. Apply, Cancel, and Clear rating also activate with Space/Return. Escape cancels from anywhere inside the editor and returns focus to Edit rating for the same book. No global bare-arrow or digit handlers; keys in review text retain text-editing behavior. Preserve Command-Z/Shift-Command-Z as Undo/Redo when the rating transaction owns the undo context, and preserve text undo when the review editor owns it. Do not intercept system accessibility shortcuts. [Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards)

Show a focus ring around the active control, separately from the row selection highlight and the persistent rating value. Use platform focus effects where available; a framework implementation must provide equivalent visible focus. Successful Apply/Clear returns focus to the same book's Edit rating. A direct star click leaves the rating group focused. Defer rating-driven resort/filter removal while that group or editor owns focus; apply it when focus leaves. Preserve selected identity if the book remains visible. Do not transfer an edit to whatever row occupies the previous index. If a book is removed externally, cancel its draft and expose that fact; do not silently focus a different book. [Focus and selection](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Best-practices), [Lists and tables — macOS](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables#macOS)

Accessible contract: expose the book title, rating name, exact value, editability, and imported provenance. Example value: “Your rating for The Left Hand of Darkness, 3.5 of 5, editable”; missing: “Not rated.” Treat stars as redundant decoration when the same value is exposed by the rating group. Expose the editor as a labeled single-choice group with selected state, and actions as named buttons. Imported content has a readable value and read-only state with no set/increment actions. Provide equivalent semantic activation for every pointer edit through the choice group; announce save success/failure without sound being required. Do not claim a particular spoken order until tested. [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)

## Persistence pseudocode

```text
Book = { id, personalRating: null | halfStep(0..5), review, importedRating }
Editor = { bookId, originalRating, draft, ratingVersion }

setRating(bookId, value, expectedRatingVersion):
    reject unless value is null or an exact half-step in [0, 5]
    reject unless this personal-rating field is editable
    reject if book no longer exists or rating version changed
    if value == stored personalRating: return unchanged
    patch only personalRating, keyed by bookId, conditionally on ratingVersion
    on success: record undo { bookId, oldRating, newRating }
    on failure: retain old stored rating; expose persistent inline error

undoRating(transaction):
    conditionally patch only that book's personalRating to oldRating
    never restore a whole Book snapshot over a newer review
```

While saving, show **Saving rating…**, prevent overlapping rating writes for that book, and retain the exact pending value visibly marked as pending. Success shows the committed value and a nonmodal saved status. On failure retain the attempted value as a draft and show **Couldn’t save rating**, with Retry and Cancel reachable by keyboard; Cancel restores the committed display. On a version conflict, show the current committed value and ask the person to choose again rather than overwriting a concurrent edit. Never report Saved before persistence succeeds. Invalid or unsupported legacy fractions are displayed as exact imported/legacy values with an explanation; do not silently round them into the editable domain.

## Worked before/after

Illustrative fixture, not observed catalog data: book `b17`, title *The Left Hand of Darkness*, personal rating null, review “Remarkable worldbuilding.”; book `b18` has imported rating 3.5, read-only.

**Before, per the brief:** b17's empty rating looks like a zero-star failure. Clicking its fourth star deletes the review. b18's stars imply an edit affordance despite being read-only.

**After:** b17 reads **Not rated · Edit rating**. Clicking star four commits `personalRating = 4`; the review stays exactly “Remarkable worldbuilding.” Opening Edit rating, choosing 3.5, and applying stores 3.5; four filled stars appear with **3.5 of 5**. Clear rating stores null and returns **Not rated**, leaving the review intact. Undo restores 3.5 without restoring or replacing review content. b18 reads **Imported rating · Read-only · 3.5 of 5**, with rounded stars and no edit action; clicking the display performs no write.

## Acceptance checks and evidence status

**Passed — specification inspection only:** the contract distinguishes null, zero, half steps, editability, review ownership, stable identity, pointer and keyboard entry/exit, exact versus rounded presentation, persistence failure, and undo. The root skill, selected families, topic procedures, and supporting local guides were read by installed path, one file per command; the topic index was searched. Ratings-and-reviews was excluded because this task is object rating, not an App Store review prompt.

**Failed — supplied design as described:** missing ratings communicate failure; rating clicks delete review content; read-only imports imply editability. These are brief-reported defects, not independently reproduced failures.

**Not executed — implementation acceptance scenarios:**

| Scenario | Required result |
|---|---|
| Null, 0, 0.5, 3.5, 4.5, 5; save and reload | Null reads Not rated; zero reads 0 of 5; exact values survive; symbol rounding follows the stated tie rule. |
| Click selected star twice; clear twice | Same value remains stable; repeated clear is disabled/no-op; review and import data never change. |
| Keyboard-only set 3.5, cancel, clear, undo, redo | Complete task without pointer; visible focus; no trap; exact half-step edits; standard text/system shortcuts remain intact. |
| Read-only imported value | No misleading hover/edit state, keyboard mutation, semantic mutation action, or persistence write. |
| Sort by rating ascending/descending; edit amid reordering | Correct stable ID changes; sort waits until editing focus leaves; selection and review identity remain correct. |
| Empty catalog, long catalog, narrow/resized columns | No phantom editor in empty state; all books remain accessible; long titles still identify the edit target. |
| Save failure, conflict, book removal, rapid repeat activation | No false Saved state, lost review, wrong-row update, overlapping write, or silent overwrite; retry/cancel works. |
| Review edited between rating edit and undo | Undo changes rating only and preserves the newer review. |
| Full Keyboard Access, assistive input, VoiceOver on Mac | Reachable task path; meaningful exact values, names, states and errors; read-only content remains discoverable. |
| 200% text, light/dark, Increase Contrast | Essential labels/actions remain usable; measure contrast and hit regions; focus and editability remain discernible without color alone. |

## Evidence limits

Only local files and installed instructions were used; no web browsing occurred. Official links identify the source articles represented by the local snapshots, not pages fetched or verified during this task. Guidance files identify a 2026-10-25 snapshot/retrieval date; current Apple guidance and independent source review were not verified. Whole-symbol behavior comes from the local rating guide; half-step choices, zero-domain policy, rounding ties, save behavior, and key mappings are explicit product decisions.

No executable UI, device, SDK, GUI, assistive technology, contrast calculator, or accessibility inspector was run. No native component availability, compilation, actual focus traversal, VoiceOver output, target geometry, visual contrast, comfort, or runtime persistence behavior is established. The artifact is a framework-agnostic specification; the not-executed checks remain implementation work.
