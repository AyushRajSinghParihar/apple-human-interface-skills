# Conservation-photo adaptation result

Revised interface.md in place as an implementable, framework-agnostic iPadOS specification. The supplied brief reports five barriers: distorted proportions, a hidden scale marker, image-only identification, misleading stock imagery while loading, and gesture-only inspection without reset. Each now has a concrete correction and observable acceptance condition.

The revision defines uniform aspect fitting, a scale caption based on verified evidence, descriptive text, visible zoom/pan/reset alternatives and preserved state on resize. Its state table distinguishes previews, ready content, cached refresh and recoverable failure. Zoom factors, pan increments and timeout are explicit product choices rather than HIG mandates. Official source links accompany the recommendations in interface.md.

## Worked before/after

Hypothetical fixture, not a supplied asset: an oriented 3000 × 2000 px photo has a verified 10 mm marker near its bottom-right edge. The viewport is 600 × 600 pt.

Before: independent square-fill scaling gives sx=0.2 and sy=0.3, making vertical features 1.5 times their correct relative proportions. The decorative border conceals the marker; a stock placeholder can be mistaken for evidence. A person unable to pinch cannot inspect through an alternative, and there is no reset.

After: s=min(600/3000,600/2000)=0.2 pt/px. Display size is 600 × 400 pt, with 100 pt neutral space above and below. All edges and the marker remain visible. Caption: “Photographed scale bar: 10 mm.” A hypothetical verified description could read “Pale specimen on dark background; a narrow surface crack extends from the upper edge toward the center.” These example observations must not be assigned to an actual photo without verification; identity belongs in the separate heading.

Zoom In produces z=1.25 and a 750 × 500 pt image. Horizontal overflow is 150 pt; vertical panning is unavailable. Pan Right moves the viewed region right by up to 150 pt per press, clamped to its boundary. At z=2 the image is 1200 × 800 pt; the marker may be offscreen, so the zoomed-view notice and scale caption remain. Reset View restores the centered 600 × 400 pt complete photo. Failed loading instead shows a truthful error and Retry, with no substitute photograph.

## Acceptance checks and evidence

Passed — static specification review and worked arithmetic only:

- Uniform sizing, full-edge and marker visibility at fit/reset, and exclusion of image-obscuring decoration are specified.
- Worked fit computes to 600 × 400 pt with 100 pt top/bottom letterboxing; 1.25× fit has horizontal overflow only.
- Identification, verified descriptions, missing-data wording, scale text and semantic order are specified.
- Zoom/reset/pan outcomes, limits, boundary availability, input equivalence and 44 × 44 pt hit-region targets are specified.
- Loading, preview, ready, failure, retry, stall, cached refresh and obsolete-response handling are specified without fake photos or progress.

Failed — the supplied brief's five stated behaviors fail the revised contract. These are reported specification defects, not runtime observations. No implementation was supplied to establish runtime correction.

Not executed — implementation acceptance scenarios:

| Scenario | Required observable result |
| --- | --- |
| Wide/tall/square photo fixtures with markers at each edge | Uniform proportions and complete marker at fit/reset; no decoration or controls conceal pixels |
| All zoom levels, pan boundaries and repeated reset | Limits clamp; enabled states match available movement; reset restores complete evidence |
| Touch gestures, visible buttons, pointer, keyboard | Equivalent operations; focus preserved; no hover dependency or reserved-gesture interception |
| VoiceOver, Switch Control, Full Keyboard Access walkthrough | Identify specimen, read description/scale, inspect, reset and retry without pinch/drag; correct roles/order/current values; no repeated loading announcements |
| Narrow multitasking, rotation, intermediate resizing, 200% text | Selection and inspection context preserved; labels/actions wrap and stay reachable; fit still shows all image evidence |
| Slow/offline, corrupt decode, 30-second stall, preview success/full failure | Honest status, bounded wait, no unrelated photo, recoverable Retry and usable navigation |
| Repeated Retry, failed cached refresh, selection change during request | Single pending retry; cache/inspection retained on same-asset failure; stale response cannot replace current selection |
| Light/dark, Increase Contrast, Reduce Motion | Measured readable contrast and focus; separate nonoverlapping hit regions; no automatic spring motion or concealed pixels |

No device, SDK, GUI, assistive-technology, contrast-measurement or network-timing execution was performed. No real asset was available to verify marker readability, description accuracy or useful maximum zoom resolution. Those remain implementation/content acceptance work, not claimed passes.

## Local guidance audit

Explicitly read the installed apple-hig root SKILL.md and searched references/topic-index.md for the task concepts. For platform adaptation, read Getting started family → Designing for iPadOS topic procedure → source guide first. Then read each owning family and selected topic procedure before its guide: Content/Image views; Foundations/Accessibility and Layout; Patterns/Loading; Menus and actions/Buttons; Inputs/Gestures; Presentation/Scroll views; Technologies/VoiceOver. All paths were resolved within .agents/skills/apple-hig. Each file read used a separate cat command; the index search used rg against that one file. No web browsing was used. Local guidance and official links establish the design basis, not runtime behavior.
