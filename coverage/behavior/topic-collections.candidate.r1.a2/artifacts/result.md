# Photo grid adaptation result

Patched interface.md in place, replacing the original single-paragraph behavior with an implementable iOS/iPadOS specification. The patch adds width-derived columns, image and caption geometry, Dynamic Type reflow, stable selection and scroll restoration, image descriptions and semantic actions, loading/empty/error states, and a bounded retrieval plan for 20,000 photos.

## Decisions and rationale

The task remains visual photo browsing. A familiar collection supports this better than changing the primary experience to text comparison. The same rules serve both album sizes; scale changes retrieval and navigation rather than reducing targets to fit more items. Narrow iPad windows follow available width, while wide windows expose more photos. Rotation and resizing preserve the album, selection, open photo, and location.

The fixed six-column rule is replaced by 104 pt minimum cells, 16 pt side margins, and 8 pt gaps. Accessibility text sizes use 240 pt minimum cells with growing captions. These are proposed product values, not HIG mandates. The 44 × 44 pt target baseline comes from the local button/accessibility guidance; the smaller accessibility-table minimum is not used as a density target. The layout guide's numeric TV grid examples do not apply to this iPhone/iPad specification.

Full-image fitting avoids an unverified crop hiding meaning. Captions and known descriptions provide information beyond thumbnail recognition. A filename fallback remains explicitly incomplete when photo descriptions are absent. Select/Done makes selection behavior discoverable without requiring long press; ID-based state prevents reuse and reflow from changing what is selected.

For 20,000 items, metadata pages, cell reuse, bounded prefetch/cache, and a lightweight month index avoid dependence on loading all images. The 200-item threshold/page size and 64 MiB decoded-cache cap are engineering proposals pending profiling. Empty, loading, and failure states are separate so a request failure never implies that an album contains no photos. No import or destructive capability was assumed.

## Worked before/after

Illustrative fixture: a 20-photo album, safe-area width 390 pt, selected photo IDs P07 and P08. Assume the old layout uses the same margins and gaps solely to compare geometry; the supplied brief specified no old spacing. Six columns would give (358 − 40)/6 = 53 pt cells. Rotating would clear selection under the supplied contract. Thumbnails alone could not identify content without vision, and a zero-photo result would produce a blank screen.

After: C = floor((358 + 8)/112) = 3, S = (358 − 16)/3 = 114 pt. Twenty photos occupy seven rows, with two photos in the final row. Select P07/P08, scroll until P07 is the first visible photo, then resize to a 768 pt safe area: six 116 pt cells; the selected-ID set remains {P07, P08}, and P07's row retains its viewport offset subject to boundary clamping. At 390 pt with accessibility text sizes, the grid becomes one 358 pt cell per row and captions wrap. Selection and focus still refer to the same IDs.

For a 20,000-photo fixture spanning multiple years, activate Jump to Month, choose October 2024, and load the page containing that month's first ID directly. Returning from detail restores that ID and offset. A late thumbnail response for a reused cell is discarded unless both ID and rendition match. A failed page retains current photos and offers Retry. A successfully loaded zero-item album instead explains “No Photos in This Album.” These are specified transitions, not executed app results.

## Acceptance checks

| Check | Pass condition | Status here |
|---|---|---|
| Artifact patch | Original four problems receive concrete replacement behavior in interface.md | Passed, static inspection |
| Geometry | W = 320/390/768/1024 pt gives C = 2/3/6/8 and S = 140/114/116/117 pt | Passed, arithmetic |
| Small/odd counts | 0, 1, 19, 20, 21 items: correct count, natural last row, no stretched final cells | Specified; runtime not executed |
| Large album | 20,000 items: direct month jump, bounded cells/cache/prefetch, no full-album decode; reach final item | Specified; profiling not executed |
| State continuity | Select two IDs, rotate both ways, resize iPad through narrow/wide, background/resume, open detail/Back: same IDs and anchor within boundary clamp | Specified; runtime not executed |
| Dataset changes | Deferred inserts do not move active targets; explicit update retains surviving IDs; removed anchor uses documented successor/predecessor; last removal enters empty state | Specified; runtime not executed |
| Text and layout | All supported Dynamic Type sizes including largest, at least 200% enlargement, Bold Text, long titles and localized labels: no lost actions, overlapping targets, or inaccessible full text | Specified; native rendering not executed |
| Image and reuse | Whole subjects visible without stretching; portrait/panorama and failed previews retain geometry; stale requests never show a different ID | Specified; rendering/network not executed |
| Nonvisual task | VoiceOver reads title, count, named grouped cells and selection state in locale order; select, jump, open and return without sight; focus retained at edge cells after reflow | Specified; VoiceOver not executed |
| Input | Touch scroll never activates; keyboard, Full Keyboard Access and Switch Control reach and activate all controls; no essential hover-only action; edge focus visible | Specified; input execution not performed |
| Visual preferences | Check light/dark and Increase Contrast with measured actual colors; selection identifiable without color; Reduce Motion retains state without spring/zoom | Specified; measurements/device checks not executed |
| Failures | Initial load, partial-page failure, preview failure, empty success, duplicate retry, memory pressure and offline recovery behave as defined | Specified; fault injection not executed |

No executed check failed. This does not imply that an implementation passes: no app implementation was supplied.

## Evidence and limits

Read the installed apple-hig root SKILL.md explicitly, searched its topic index, and read owning family routes before selected topic procedures and their source guides. Routes used: Getting started → Designing for iOS/iPadOS; Layout and organization → Collections; Foundations → Layout, Accessibility, Typography; Technologies → VoiceOver; Presentation → Scroll views; Content → Image views; Menus and actions → Buttons. Each instruction/source read used an individual file command. Official article/section links supporting material recommendations are included in interface.md.

Evidence is the supplied interface.md and installed local guidance dated October 25, 2026. No web browsing or independent verification of that snapshot was performed. The package describes itself as independent guidance derived from HIG, not an SDK reference. No screenshots, real photo metadata/descriptions, code, API availability, device, SDK compilation, GUI, accessibility execution, measured contrast, physical reach, memory trace, or frame timing evidence was supplied or produced. The revised document establishes a reviewable contract; runtime and content-quality checks remain open. Process-relaunch restoration requires implementation support and is explicitly not claimed.
