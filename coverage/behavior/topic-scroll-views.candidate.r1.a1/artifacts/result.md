# Revised iPhone itinerary interaction specification

This is a framework-agnostic design contract. `interface.md` reports three nested vertical scrollers, missing end affordance, a sticky booking action covering the final stop, unexpected navigation on an edge pull, and enlarging text. No implementation or screen geometry was supplied. All behavior below is proposed; illustrative stop names and measurements are fixtures, not observations.

## Decisions

1. **One vertical scroll owner.** Render the itinerary, its groups, stops, and full descriptions in a single continuous vertical document. Former inner scrollers become content-sized, non-scrolling groups. Preserve hierarchy through headings and indentation, without fixed-height description boxes. No horizontal overflow, paging, or app-controlled zoom is introduced; system accessibility zoom remains available. HIG advises avoiding same-axis nesting rather than universally forbidding all nesting. [Scroll views — Best practices](https://developer.apple.com/design/human-interface-guidelines/scroll-views#Best-practices).

2. **Show continuation and completion.** Keep the conventional transient vertical position indicator. Let the following item continue naturally beyond the viewport; do not crop text deliberately or force whole-stop snapping. Add a persistent in-flow footer after the last stop: “End of itinerary · N stops.” For an empty itinerary use “No stops yet”; do not label an incomplete/loading dataset as the end. The explicit footer is a product decision; HIG recommends suggesting offscreen content beyond transient indicators. [Scroll views — Best practices](https://developer.apple.com/design/human-interface-guidelines/scroll-views#Best-practices).

3. **Reserve booking space instead of overlaying the document.** Layout order is navigation area, flexible scroll viewport, then content-sized booking area, including bottom safe-area clearance. The viewport ends above the booking area's top edge. Include 16 pt of document padding after the end footer (a product spacing choice). Recalculate the viewport whenever the booking area, safe area, orientation, or text size changes. Never subtract a hard-coded button height. This design needs no scroll-edge blur because the action does not overlap scrolling content. If a future implementation introduces overlap, it must separately reserve sufficient scroll clearance and use the appropriate edge separation; an edge effect alone does not make content reachable. HIG limits edge effects to overlapping floating UI and prefers automatic styling. [Scroll views — Scroll edge effects](https://developer.apple.com/design/human-interface-guidelines/scroll-views#Scroll-edge-effects).

4. **Predictable input at boundaries.** Vertical drag/flick anywhere over a stop or its description moves the one itinerary owner. At the top or bottom, retain supported platform elastic feedback; release settles at the same boundary with no route change. Remove the app's pull/overscroll-to-navigation handler and any distance threshold for it. Preserve standard system navigation gestures and provide a visible “Back” action when there is a previous route. A system Back gesture may navigate; an ordinary vertical edge pull must not. Gesture movement cancels pending button activation. [Gestures — Best practices and Custom gestures](https://developer.apple.com/design/human-interface-guidelines/gestures#Custom-gestures).

5. **Preserve content when text grows.** Use semantic title, heading, body, supporting-text, and action-label roles. Body starts from the iOS 17 pt default or an equivalent readable style. Honor Dynamic Type or equivalent sizing, including Larger Accessibility Text, and Bold Text. Allow unlimited wrapping, grow rows, and stack time above stop name when inline placement no longer fits. Essential text and booking labels must not truncate. Support at least 200% enlargement and test every supported size, including the largest accessibility size. Do not substitute pinch zoom for text resizing. These are sourced recommendations applied to this design, not evidence of runtime support. [Typography — Supporting Dynamic Type](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type), [Accessibility — Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision).

6. **Keep booking deliberate and reachable.** Proposed label “Review Booking” opens the existing booking review flow; it does not itself purchase. This outcome is an explicit assumption because booking semantics were not supplied. Use one prominent button with a matching accessible name, button role, visible press feedback, and at least a 44 × 44 pt activation region, with no overlapping targets. Back is a separate, lower-emphasis action. Retain itinerary state when returning from review. If opening review requires asynchronous work, indicate activity in the initiating button, suppress duplicate activation, and restore an actionable state with an inline explanation on failure. Do not invent a completed booking from a successful press. [Buttons — Best practices, Content, and iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices). The accessibility guide also lists a smaller minimum; this design chooses its 44 × 44 pt iOS default, consistent with the button guide, rather than using that minimum as a density target. [Accessibility — Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility).

If the reserved booking area would leave less than one current body-text line plus vertical content padding visible, move the same booking action into document flow after the end footer. This content-fit fallback is a product decision, not an Apple threshold. It preserves reading access on short viewports at extreme text sizes; there is only one booking button in either layout.

## Scroll, position, and reveal contract

Maintain `itineraryId`, stable item IDs, one document offset, and an anchor consisting of the first visible text block and its viewport-relative position. Do not retain offsets for former inner containers.

```text
layout:
  nav = measured navigation and top safe-area region
  booking = measured wrapped action region including bottom safe area
  viewport = available bounds minus nav minus booking
  if viewport cannot fit one current body line plus content padding:
    booking becomes final document item; reserve bottom safe area in document
  document = ordered groups/stops + completion footer + optional booking + padding
  offset range = [0, max(0, document.height - viewport.height)]

vertical input over document:
  delegate to sole scrolling owner; never dispatch navigation from overscroll

before text/layout change or leaving for review:
  capture visible block ID and relative position
after reflow or return:
  restore that block's position, clamped to offset range
  if block was removed, use next surviving block, otherwise previous block
  do not reset to top, recenter every row, or force bottom merely because near it

reveal(target):
  use the unobscured viewport
  if relevant target portion is visible: leave offset unchanged
  otherwise move the minimum distance needed to expose it
  if target exceeds viewport: expose relevant start/caret, not entire block
```

Reflow restoration should be immediate rather than an added animated sweep. Normal user scrolling retains platform feedback. If later search, editing, or selection is added, apply this reveal rule to results, insertion points, selection extension, and actions on an offscreen selection; do not add those features merely for this specification. This follows the HIG's minimal-reveal guidance. [Scroll views — Best practices](https://developer.apple.com/design/human-interface-guidelines/scroll-views#Best-practices).

Expose document order as title, group headings, stops in itinerary order, end footer, and booking action; Back remains in navigation. All required actions must be reachable and activatable through supported assistive input, with text labels and button semantics. These are implementation requirements pending execution, not claims about current focus order. [Accessibility — Mobility and Speech](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility).

## Worked before/after

**Before, as reported:** A vertical drag inside a stop description can remain trapped in one of three vertical scrollers. Near the boundary, a pull can navigate away. At the bottom, the booking overlay covers the final stop; there is no completion cue. Exact gesture recognizers, sizes, and stop content are unknown.

**After, illustrative fixture:** Three stops are “Station,” “Museum,” and “Hotel.” A drag starting within Museum's long description advances the same document toward Hotel without a handoff. At the maximum offset, Hotel's final line and “End of itinerary · 3 stops” can be read above the reserved “Review Booking” area. Another vertical pull provides boundary feedback and returns to that position without navigation.

For a numeric layout example only: available height after navigation/top clearance is 640 pt; measured booking area including bottom clearance is 88 pt; viewport is 552 pt. If the padded document is 1,400 pt tall, maximum offset is 848 pt. At that offset the document bottom aligns with the viewport bottom, above booking. With larger text, suppose booking grows to 120 pt and document to 2,100 pt: viewport becomes 520 pt and maximum offset 1,580 pt. The same rule still exposes the final text. A reader anchored at Museum stays at Museum after reflow, subject to boundary clamping, rather than jumping to the old numeric offset or to Hotel.

## Acceptance checks and status

**Passed — specification inspection only:** The revised contract assigns one vertical owner, removes same-axis inner scrolling, defines both boundary outcomes, reserves measured booking space, supplies an end cue, defines reflow restoration and minimal reveal, and includes an extreme-height fallback. The arithmetic in the illustrative fixture is internally consistent. Installed root → family → topic procedures → source guides were read for scrolling, gestures, typography, accessibility, and buttons; the topic index was searched before finalizing routes.

**Failed — supplied design as reported, not reproduced:** Scroll trapping, unexpected pull navigation, missing end affordance, and final-stop occlusion are reported in `interface.md`. No independent runtime failure is claimed.

**Not executed — implementation acceptance:**

| Check | Pass condition |
|---|---|
| Ownership and long content | Drag/flick from every former nested region in both directions; one document moves and every stop/description is reachable without a handoff or dead zone. |
| Boundaries and navigation | Repeated vertical pulls at both ends never change route; supported elastic feedback settles correctly. Visible Back and standard system Back still work. |
| Completion and clearance | Short, one-stop, and long fixtures show the correct end footer; final text/footer can be fully exposed above booking and safe-area exclusions. Empty/incomplete data never falsely claims completion. |
| Enlarged text | Default, 200%, every supported text size through largest accessibility size, and Bold Text preserve full stop text and action labels; no clipping, horizontal reading scroll, target overlap, or inaccessible content. Exercise short-viewport inline fallback. |
| Layout and return | Rotate, change text size while midway through a long description, open review, and return. Same anchor is retained where possible; deleted-anchor fallback and boundary clamping are deterministic. |
| Booking interaction | Hit region measures at least 44 × 44 pt; pressing produces feedback and opens review once. Scrolling over it does not activate it. Test pending/error recovery if asynchronous opening exists. |
| Assistive input | On a supported Apple environment, traverse all stops and footer, reach/activate Back and booking with VoiceOver, Switch Control and Full Keyboard Access; focused content stays unobscured. Measure actual reading/action order rather than inferring it from this document. |
| Reveal extensions | If search/editing/selection exists, offscreen result, insertion point and extended selection reveal only as far as needed; already visible targets do not jump. Otherwise mark these cases not applicable. |
| Visual separation | Measure actual label/foreground contrast and legibility in light/dark and Increase Contrast; booking remains clearly separated from content. No decorative scroll-edge overlay is added. |

## Evidence limits

Only `interface.md` and installed local skill instructions/reference snapshots were used. Official links above identify the supporting articles/sections; they were not opened or checked online. The package describes itself as independent, dated application guidance, not an SDK reference or a verbatim Apple manual. No claim of current API availability, independent source review, or media review is made.

No application implementation, screenshots, measured geometry, device, SDK, simulator, GUI, accessibility execution, or physical gesture testing was available or performed. There is no compilation or runtime pass. Actual gesture recognition, native rendering/elasticity, font behavior, focus order, contrast, and physical usability remain to be verified. The booking destination, sample content, spacing, anchor algorithm, end-footer wording, and constrained-height fallback are explicit product decisions or assumptions rather than Apple mandates.
