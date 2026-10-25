# Revised Apple TV movie lockup specification

## Scope and evidence

Design artifact for tvOS remote browsing, based on `interface.md`. The brief reports detached poster/title/duration, focus enlargement overlapping neighbors, a selection badge inside cropped art, and disappearing translated titles. These are supplied observations, not independently reproduced defects. No screenshots, code, font measurements, device results, or movie catalog were supplied.

Assumptions: movies open a detail destination before playback; the existing badge represents a persistent selected choice. Its business meaning is unspecified: preserve the existing selected value and selection operation; do not reinterpret it as Saved or Watched. The example below uses “Selected.” No Apple SDK or particular UI framework is required.

## Decisions and family

Use one atomic focusable movie lockup: artwork content plus a footer containing title, duration, and optional persistent selection status. All parts grow and shrink together. The footer, badge, and focus treatment belong outside the artwork's crop mask. The entire unit activates one destination; metadata and status are not separate remote stops.

| Form | Use and contract |
|---|---|
| Movie caption button (default) | Artwork with always-visible title and duration below; use when comparison requires readable names before focus. Horizontal tilt for a shelf, vertical tilt for a stack; both axes only if later arranged as a grid. |
| Movie poster (artwork-led variant) | Use when recognizable art is the primary choice. Optional title/duration may appear on focus, but reserve their footer space in all states. Keep persistent selection status visible even when unfocused. If art cannot identify the movie, use the caption form. |
| Movie review card | Only for a future rating/review choice, with review header/content/footer; do not substitute it merely for a movie poster. |
| Person monogram | Only for cast/person choices, using portrait or initials; outside this movie implementation. |

These choices follow [Lockups — forms and spacing](https://developer.apple.com/design/human-interface-guidelines/lockups). Apple permits poster captions on focus; making caption-button titles permanent is this product's readability decision. Do not impose one universal poster aspect ratio: fit each asset without distortion, using containment and neutral letterboxing if cropping would lose meaningful content. Missing/failed art gets a neutral placeholder and visible title, without changing focus or activation.

## Layout contract

Coordinates below are proposed logical points, not measured pixels or mandated Apple lockup dimensions. Map them consistently into the implementation's coordinate system. Keep the complete maximum focus envelope inside the content-safe rectangle. The local [Layout — tvOS](https://developer.apple.com/design/human-interface-guidelines/layout#tvOS) guide specifies primary-content insets of 80 pt horizontally and 60 pt vertically; use any larger effective safe inset reported by the environment.

Default caption unit, unfocused:

```text
width 320 pt
┌──────────────────────────┐
│ artwork region 320×360 pt │  asset contained, ratio preserved
└──────────────────────────┘
12 pt gap
Title: 32 pt Semibold, 40 pt line height, up to 2 lines
8 pt gap
Duration: 29 pt Regular, 36 pt line height
8 pt gap
✓ Selected: 29 pt Medium, 36 pt line height (reserved even if absent)
```

Base height is 540 pt. Footer aligns to the locale's leading edge. Reserve two title lines and the status line across each shelf, so neighboring units have consistent dimensions. No header is needed. Keep footer text on an opaque neutral surface, never directly on variable poster colors. Use a high-contrast outline for focus, checkmark plus localized text for selection. Color alone carries neither state.

For a framework without native focus effects, the proposed focused maximum scale is 1.06, centered on the whole unit, with a 12 pt outward allowance per edge for outline, shadow and any tilt. Clip shadows to that allowance; bound tilted corners within it. Prefer platform effects when available, but measure their actual maximum envelope and enlarge spacing accordingly rather than assuming 1.06 matches native behavior. Reserve space before focus changes; do not move neighbors on focus.

```text
maxEnvelope(w,h) = (1.06*w + 24, 1.06*h + 24)
baseGapX >= max(40, 0.06*w + 24)
baseGapY >= max(100, 0.06*h + 24)  // if multiple shelves
```

This conservatively permits adjacent outgoing/incoming units to be enlarged simultaneously. At 320×540, envelopes are 363.2×596.4 pt; choose 48 pt horizontal gap (pitch 368) and 100 pt vertical gap (pitch 640). There is 4.8 pt horizontal clearance even with two maximum envelopes. Apply the envelope to the complete footer, not just the image. Edge items scroll fully into the safe rectangle before their focus treatment can be clipped. A higher z-index is not a substitute for clearance.

Typography uses semantic title/supporting/status roles. Prefer the platform face where available; otherwise use a licensed readable sans-serif with appropriate script coverage and equivalent sizing/Bold Text behavior. The local [Typography — legibility and scaling](https://developer.apple.com/design/human-interface-guidelines/typography#Ensuring-legibility) guide lists tvOS default 29 pt and minimum 23 pt; 23 pt is not the target for these labels. Exact proposed sizes and spacing above are product choices.

## Long text, localization and accommodations

Never delete or overwrite the full localized title. Wrap at language-appropriate boundaries, falling back to grapheme-safe breaks for long unbroken words. Default shelf titles may end in an ellipsis after two lines, but Select always opens a detail destination with the complete title at the top, wrapping without a line limit. Long detail content scrolls by remote, with an ordinary Back exit; no timed marquee or press-and-hold is required to read it. Full title and localized duration remain in the semantic name even when visually abbreviated.

Support text scaling from 100% through at least 200%, plus all sizes offered by the chosen platform integration. Scale meaningful status glyphs and honor Bold Text. At larger text sizes, switch to a vertical stack of wide caption units: width equals safe width minus focus-envelope allowance; reduce the art region if necessary, allow unlimited title lines, and compute height from shaped text. Scroll to reveal the full focused unit where possible; when it exceeds viewport height, open details for unbounded reading. Preserve focused movie ID, selection, and return position during reflow. Do not shrink text to keep the original count of movies onscreen. This applies [Typography — Dynamic Type](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type) and [Accessibility — Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision).

Mirror leading/trailing alignment and ordered shelf placement in RTL. Directional input still moves toward the physical neighbor on that side. Preserve artwork orientation and digit order; localize duration formatting. Use bidi isolation for mixed-script titles and metadata, and language-aware alignment for long detail paragraphs. See [Right to left](https://developer.apple.com/design/human-interface-guidelines/right-to-left). Translation quality and script shaping require subsequent native-language/layout review.

## State and interaction contract

| State/event | Required behavior |
|---|---|
| Unfocused | Receded unit; default form still shows title/duration and selected status. |
| Focused | Whole unit raised/highlighted/enlarged within reserved envelope; no navigation or selection mutation. |
| Pressed | Immediate distinct visual feedback on deliberate Select press; release activates once. Cancellation restores focus. |
| Selected | Independent persistent boolean; checkmark/text survive focus loss and artwork changes. Selection changes only through the product's explicit selection operation. |
| Unavailable | Inactive, skipped by directional focus; show localized “Unavailable” in status area. If also selected, retain both meanings and grow the footer consistently for that shelf. |
| Missing art | Same named actionable movie, neutral placeholder, no layout jump. |

Entry restores the last available focused ID and shelf scroll position; first entry chooses the first available movie in reading order. Left/right move between available shelf neighbors; at an end remain there without wrapping. Up goes to the existing parent navigation region if present; otherwise stays. Down stays in a single shelf, or enters the nearest available item in the next shelf if the host supplies one. No internal label or badge intercepts directions. An empty shelf exposes a noninteractive empty message and preserves the parent/Back route.

Select opens details for the focused ID; it does not toggle the badge or start playback on focus. Back from details restores this movie and scroll position in its parent shelf; Back from the shelf opens its hierarchical parent, and at app root delegates Home behavior to the system. Preserve held-Back system behavior and Play/Pause control of any active media. These mappings apply [Focus and selection — tvOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#tvOS) and [Remotes](https://developer.apple.com/design/human-interface-guidelines/remotes).

```text
onDirectionalInput(direction):
    target = availablePhysicalNeighbor(focusedID, direction)
    if target exists:
        focusedID = target.id
        reveal(target.maximumEnvelope)
        interruptOldFocusTransitionAndRenderCurrentTarget()
onSelectRelease(validPress):
    if validPress and focusedID is available:
        remember(focusedID, scrollPosition)
        openMovieDetails(focusedID)
onSelectionChanged(id, value): selected[id] = value
```

If a focused movie is removed during discrete directional navigation, move to a nearby available one-step target. For other removal contexts, clear the obsolete indicator rather than guessing a replacement; the next directional input reenters the available group. Never activate a removed ID. Preserve selection by stable movie ID through reordering.

Focus transitions are interruptible; rapid navigation never queues stale enlargement. Reduce Motion uses a stationary outline/brightness change without scaling, tilt, bounce or parallax; keep the same reserved space and state meaning. This follows [Motion — feedback](https://developer.apple.com/design/human-interface-guidelines/motion#Providing-feedback) and [Accessibility — Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility#Cognitive).

Expose each available unit as one named actionable semantic element: full localized title, localized duration, selected state, and “Opens movie details” action. Avoid duplicate artwork/title stops. Expose unavailable content as labeled inactive content. This specifies intended semantics; spoken order and assistive activation remain untested.

## Worked before/after

Synthetic fixture: movie A, title “Die außergewöhnliche Reise durch die verborgenen Welten”, duration 127 minutes, selected=true; neighbor B is an ordinary unselected movie.

Before, as described by the brief: A's title and duration have no clear relationship to its poster; enlargement covers neighboring labels; selection sits inside the crop; translated title disappears. No original coordinates or screenshot exist to quantify this state.

After, default caption form: A occupies a 320×540 pt base unit. Its title wraps into the reserved two-line area, with ellipsis only if actual font measurement requires it; duration reads localized “2 Std. 7 Min.” and “✓ Ausgewählt” sits outside the artwork mask. The whole focused unit fits the 363.2×596.4 pt maximum envelope. B's center is 368 pt away, preserving at least 4.8 pt clearance even during simultaneous focus transitions. Moving right to B leaves A's selected status visible. Returning to A and pressing Select opens details with the complete German title; Back restores A. At 200% text, A becomes a wide stacked caption unit, with measured wrapping and recomputed height. No particular line break or real rendered fit is claimed by this fixture.

## Acceptance checks and current results

| Check | Pass condition | Current status |
|---|---|---|
| Brief coverage | All four reported problems have explicit corrections above | Passed: document inspection |
| Geometry arithmetic | Proposed default envelopes do not intersect at stated pitches | Passed: arithmetic only; not rendered geometry |
| Original interface | Related metadata, unobscured focus, persistent badge, readable translations | Failed as reported in brief; not reproduced |
| State independence | Move focus A→B; A remains selected; no detail opens until Select | Not executed |
| Edge traversal | Enter, traverse every edge/corner supplied by host, activate, Back; no clipped unit, trap or unexpected wrap | Not executed |
| Expansion | Check all animation frames, tilt extremes, focused/unfocused/pressed states, shadows and footer bounds against neighbors and safe area | Not executed |
| Text matrix | 100%, 150%, 200%, all platform sizes, Bold Text; short, long, unbroken, German and mixed Arabic/Latin titles retain full-text route and status | Not executed |
| Fallbacks | Missing art, missing duration (“Duration unavailable”), unavailable/selected combinations, removal, empty shelf and reorder preserve identity and exit | Not executed |
| Preferences/semantics | Reduce Motion preserves focus; assistive navigation announces one full named unit, state and action; detail reading/Back complete the task | Not executed |
| Contrast and TV viewing | Measure actual text/background/focus/status contrast; review default and Increase Contrast schemes, available appearances, supported TVs/settings, and viewing at 8 feet or farther | Not executed |

Use a product target of at least 4.5:1 for all footer text against its actual surface; measure the implemented palette rather than inferring from color names. This conservative project target is not a replacement for the scope-qualified contrast table in the local Accessibility guide. Control activation covers the whole unit, comfortably above that guide's tvOS 66×66 pt default; actual accessibility hit geometry still needs inspection.

## Evidence limits and source trace

Read the installed root `.agents/skills/apple-hig/SKILL.md`, searched its topic index, then read the owning family and topic procedure before each supporting reference. Families used: getting-started (designing-for-tvos), layout-and-organization (lockups), inputs (focus-and-selection, remotes), foundations (typography, accessibility, right-to-left, layout, motion). References resolve within that same installed package. Official links above identify the articles/sections behind local guidance; they were not fetched. Local references describe dated application guidance derived from Apple, not SDK documentation or independently reviewed source claims.

Only local text inspection and specification arithmetic were performed. No web browsing, SDK compilation, GUI, simulator, Apple TV, Siri Remote, VoiceOver, accessibility inspection, font shaping, contrast calculation, or physical-distance test was executed. Runtime checks remain pending implementation in a supported environment. No framework availability, native rendering fidelity, accessibility conformance, or device comfort is established by this document.
