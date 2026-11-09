# Revision result

Patched `interface.md` in place into a concrete iOS/iPadOS photo collection specification. It replaces the supplied fixed six columns with available-width rules, preserves selected IDs and scroll context through rotation/resizing, adds text identification and honest description fallbacks, and replaces blank empty albums with an explained state. It also specifies bounded work for 20,000 items and distinguishes loading, failure and successful emptiness.

## Decisions and rationale

- Keep a familiar visual collection because the task is photo recognition. Use the same interaction for 20 and 20,000 photos; vary resource usage through virtualization and paging, rather than making large albums a different product.
- Derive columns from safe-area width, with a single-column accessibility arrangement. The 16 pt margins, 8 pt gaps, 104 pt target image minimum and resource budgets are proposed product values. They are not Apple mandates. [Collections](https://developer.apple.com/design/human-interface-guidelines/collections) supports familiar grids and cautious changes during manipulation; [Layout](https://developer.apple.com/design/human-interface-guidelines/layout) supports adaptation to available space and preserving functionality.
- Store identity independently of layout position. Rotation and resizing reflow the view while retaining selection, focus and anchor. Hold external insertions for explicit “Show updates”, keeping the viewed order predictable. This applies the collections guidance without preventing necessary environmental reflow.
- Keep image meaning and operation separate: readable title/date plus supplied descriptions, an honest missing-description fallback, named activation, selected state and non-color feedback. Detail shows the whole photo. These decisions follow [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility), [Image views](https://developer.apple.com/design/human-interface-guidelines/image-views) and [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons). Metadata cannot replace an absent visual description.
- Use semantic system text styles, wrapping and growing rows instead of shrinking labels. [Typography](https://developer.apple.com/design/human-interface-guidelines/typography) supports reducing columns and preserving information at enlarged sizes.
- Add explicit empty/pending/error transitions. Their exact copy, pagination and cache policy are application decisions; the local HIG does not establish their performance or prescribe these budgets.

## Worked before/after

Assume a 390 pt safe-area width, 20 photos, and selected photo IDs P07 and P18. The original only says six columns, so its actual margins and thumbnail size are unknown. Using the revised margins/gaps for a controlled comparison, six columns would leave (358 − 5 × 8) / 6 = 53 pt images. Rotation explicitly cleared selection, meaning came only from thumbnails, and zero items produced a blank screen.

After: W = 390 − 32 = 358; C = floor(366 / 112) = 3; S = (358 − 16) / 3 = 114 pt. Twenty photos occupy seven image rows, the last with two items. Each has readable identification and a named action. Resizing to a 768 pt safe-area width gives W = 736, six columns and 116 pt images. P07 and P18 remain selected by ID, the first visible ID is restored at its offset, and returning from detail restores that cell. An accessibility text size uses the specified wrapping single-column arrangement.

With 20,000 photos at 390 pt, the logical collection has 6,667 image rows, but cells and image decoding are limited to the viewport/prefetch region. There are 100 metadata pages of 200; at most five are resident. A deep anchor can fetch its indexed page directly. These are calculated/specification outcomes, not observed runtime results. At zero successfully loaded items, the explained empty message appears; failures retain a Retry route instead.

## Acceptance checks and status

Passed — static specification review:

- All four observed problems in the supplied one-paragraph spec have concrete replacements in `interface.md`.
- Width arithmetic independently checked for 320/390/768/1024 pt: 2/3/6/8 columns and 140/114/116/117 pt images respectively. Final partial rows are defined without fake filler items.
- State rules distinguish layout changes, explicit updates, removed IDs, detail return and final-item removal.
- Small/large data handling, bounded loading, stale-image protection, and empty/error distinctions have explicit acceptance criteria.
- Root skill was read from the installed path, followed by selected family procedures, topic procedures and local source guides. Topics used: Collections, Layout, Accessibility, Typography, Image views and Buttons. Each file read used its own command. Official links above are citations carried from those local guides; no web browsing was performed.

Failed:

- No revised implementation failure is established: only a specification was supplied. The original specification explicitly loses selection and lacks accessible image meaning and empty-state explanation; those defects are corrected in the contract, not demonstrated fixed in running software.

Not executed — release acceptance remains pending:

- On iPhone/iPad: all specified widths and resizing transitions, largest Dynamic Type/200% enlargement, Bold Text, Display Zoom, long labels, odd counts, edge focus and pointer feedback, and image crop/detail checks.
- VoiceOver, Switch Control, Full Keyboard Access, touch and pointer completion of the specified flows, including offscreen navigation and focus retention.
- Actual target-region and contrast measurements in light/dark/Increase Contrast; native safe-area rendering and physical comfort.
- 20,000-item profiling, memory pressure, paging correctness, deep restoration, cancellation, slow/error/retry cases and responsiveness on supported hardware.

## Evidence limits

Inputs consisted of the supplied `interface.md` and installed instructions/local HIG references. No photo assets, app implementation, screenshots, deployment targets, SDK documentation or runtime were supplied. This work changes the requested design artifact; it does not establish API availability, compilation, native component behavior, performance, accessibility conformance or device execution. The local guides identify a dated snapshot and original application guidance, not a verbatim or independently validated Apple manual. No current-web validation, device, SDK, GUI or accessibility execution is claimed. Performance budgets and data-service/index capabilities must be validated during implementation; absent content descriptions remain a content-access limitation.
