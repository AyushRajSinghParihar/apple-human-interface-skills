# Apple TV adaptation result

Patched `interface.md` in place, expanding the supplied paragraph into a concrete tvOS catalog, focus-route table, state model, media contract, recovery behavior, and acceptance contract.

## Decisions

| Before | Revised specification | Purpose |
|---|---|---|
| 12-point text | Semantic tvOS styles: 38 pt recipe titles, 29 pt body/actions, 25 pt metadata; enlargement through 200% | Across-room reading; avoid treating the 23 pt source minimum as a default |
| Dense touch targets | Three-column caption-button collection, one focusable unit per recipe, expansion space; action areas at least 66 × 66 pt | Remote operation with room for system focus |
| Pinch to zoom | Growing labels, fewer columns, scrollable full details | Complete task with Siri Remote |
| Invisible focus | Native highlight/enlargement and explicit directional routes | Show location and available action |
| Details loses prior item | Stable ID, retained order and scroll anchor, deterministic removal fallback | Preserve browsing context |
| Audible autoplay on focus | Static artwork; Select opens details; explicit Play/Resume starts media | Separate navigation from activation |

The patch also defines interruption/resume, Back, loading/retry/empty states, captions as a content-readiness requirement, and conditional profile isolation. Three columns, spacing targets, and the details-to-play flow are product decisions consistent with guidance, not universal HIG requirements. No framework replacement or new discovery integration is presumed.

## Worked before/after

Illustrative fixture, not real supplied catalog data: “Roasted Tomato Pasta,” ID `recipe-42`, row 4, column 2, retained progress 03:12.

Before: navigating to the tiny label leaves focus invisible and starts sound. Opening details and returning loses the item; pinch zoom is needed for reading.

After: directional movement visibly highlights the whole lockup. A 30-second dwell stays silent and static. Select stores the ID and scroll anchor, then opens readable details focused on “Resume at 3:12.” Select resumes playback. Play/Pause pauses; Back exits to details; Back again restores the same recipe and catalog anchor. At 200% text fewer columns preserve the ID, although its column can change. If removed, focus moves to the next available item in retained order, then previous if needed.

## Acceptance checks

Passed — static specification inspection only:

- Each supplied problem has an explicit replacement in the patched file.
- Focus entry, directions, boundaries, activation, player exit, and catalog restoration are defined.
- Text units, enlarged-text behavior, media intent, interruption, loading, failure, and empty states are specified.

Failed: no executed check recorded a failure; this does not imply that a future implementation passes.

Not executed — required before implementation acceptance:

| Check | Passing evidence needed |
|---|---|
| Remote traversal | All recipes/actions reachable and escapable, stable short rows and edges, no incidental activation |
| Focus geometry | Whole lockup remains visible without clipping/overlap, including long titles and missing artwork |
| State | Worked return restores ID/anchor; interruption, refresh, removal, and text changes follow the contract |
| Playback | Focus dwell silent; deliberate playback, pause, scrub, quick exit, and resume retain correct video/time |
| Reading | Default/200% text and Bold Text preserve all actions; television reading works at 8+ feet |
| Accessibility/content | Contrast measured, Increase Contrast checked, supported assistive traversal and captions tested; visual-only cooking instructions assessed |
| Recovery/profiles | Retry preserves video/time; Back works; applicable viewer switch does not expose prior viewer's progress |

## Guidance and evidence limits

Explicitly read the installed root `.agents/skills/apple-hig/SKILL.md`, searched its topic index, then followed family → topic procedure → supporting article routes. Read Designing for iOS and Designing for tvOS procedures first for platform adaptation. Additional routes: Inputs → Focus and selection, Remotes; Layout and organization → Collections, Lockups; Foundations → Typography, Accessibility; Patterns → Playing video. All paths came from this installed package; each read command consumed one file.

Official article links for material decisions are included in `interface.md`. They attribute the local snapshot and were not browsed. The video source overlaps aspect-fit and aspect-fill at exactly 2:1; the specification defers to system behavior instead of inventing an exclusive boundary. Guidance preferences such as preferring system players remain preferences; explicit product contracts are distinguished from source requirements.

Evidence is limited to the supplied paragraph and installed instructions/references. No real catalog, app implementation, artwork, rendered fonts, media tracks, device, SDK, simulator, GUI, or accessibility execution was inspected or tested. No web browsing was used. Static specification review cannot establish native rendering, focus-engine behavior, remote comfort, measured contrast, playback correctness, profile integration, or accessibility conformance.
