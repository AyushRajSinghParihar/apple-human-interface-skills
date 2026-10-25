# Revised iPhone photo-story paging specification

## Scope and decisions

The supplied `interface.md` reports 47 undifferentiated dots for unrelated destinations, a dot action that can delete the current page, stale selection after swiping, and unnamed accessibility buttons. These are brief-reported behaviors, not independently reproduced runtime findings.

Specify an optional, three-page introduction to **one photo story**. Three pages and the sample copy below are product decisions, not an Apple page-count requirement or supplied content. Each page is a flat, ordered peer with a stable ID, unique title, photo, caption, and description where the photo adds information. Unrelated destinations remain outside this sequence; preserve them in the host app's destination model. Their names and organization were not supplied, so this specification does not invent that navigation.

| Order | Stable ID | Illustrative title | Purpose |
| --- | --- | --- | --- |
| 1 | arrival | Arrival | Establish the story's place |
| 2 | discovery | Discovery | Introduce its central moment |
| 3 | reflection | Reflection | Close the introduction |

Use three equally spaced dots centered near the bottom, below content and above the action row. Fill the current dot and show visible text “Page 1 of 3” (updated with selection). Keep one dot image type. Apple recommends page controls for ordered peers, rather than unrelated destinations, and suggests evaluating direct-access layouts beyond about ten pages; that is guidance, not a hard maximum. If all 47 destinations must remain directly reachable, use a separately designed labeled destination list or grid rather than restoring 47 dots. [Page controls — Best practices](https://developer.apple.com/design/human-interface-guidelines/page-controls#Best-practices)

The page control is interactive secondary navigation with an automatic-style background: visible during interaction, with sufficient separation from photos. Tapping the control before/after its active position moves one page backward/forward; it does not promise arbitrary dot selection on iPhone. Scrubbing selects successive pages continuously, bounded by the first and last pages; dragging beyond an edge accelerates toward that boundary. Discrete changes animate briefly; rapid scrubbing updates without animated page scrolling. Do not combine scrubbing with minimal styling. These follow the locally supplied iOS guidance. [Page controls — iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/page-controls#iOS-iPadOS)

## Interaction and state contract

- Open a fresh introduction on `arrival`. Horizontal content swipes move through this story only. Forward/backward follow the locale's reading direction; neither wraps nor switches stories at an edge. A canceled drag restores the current page and indicator.
- Provide visible `Previous` and `Next` buttons as precision-free alternatives. Disable Previous on page 1 with its disabled state exposed. On the last page replace Next with `Start Story`, which opens the full current story. Swiping beyond the last page does not complete or dismiss the introduction.
- Provide `Skip Introduction` on every page; it opens that same story. Both completion and skip persist a dismissed flag so later launches do not repeat the introduction. Provide `Replay Introduction` from the story's help area; replay starts on page 1 and does not clear the dismissed flag. Interruption before dismissal preserves the current page ID for resumption. These are proposed product behaviors applying the optional-learning guidance. [Onboarding — Best practices](https://developer.apple.com/design/human-interface-guidelines/onboarding#Best-practices)
- Paging actions never mutate story content or delete pages. There is no delete action in this introduction. Do not merely relabel a destructive handler: detach it from every paging input.
- One horizontal paging owner controls the content. Do not add a redundant horizontal scrollbar. Maintain story title, footer, and a small neighboring-page preview as context during paging. If enlarged captions overflow, allow vertical scrolling inside the current page, with its own vertical indicator; keep the footer outside that scrolling region and avoid same-axis nesting. No photo zoom gesture is introduced here. [Scroll views — Best practices and iOS](https://developer.apple.com/design/human-interface-guidelines/scroll-views#Best-practices)
- Freeze page order during a drag or scrub; apply externally revised content after settlement. Preserve selection by stable ID on insertion/reordering. If the selected page is removed, select its next surviving neighbor, otherwise its previous neighbor. Update content, count, selected dot, and accessible value together. Hide the page control for one page; for zero pages show “Introduction unavailable” with `Open Story` and no paging controls. Bundle introduction assets where practical; an unavailable image gets a descriptive placeholder and caption without blocking paging or skip. [Onboarding — Additional content](https://developer.apple.com/design/human-interface-guidelines/onboarding#Additional-content)

Framework-agnostic state model (indices below are zero-based):

```text
state = { pages, currentID, dismissed, interactionToken }
index = indexOf(pages, currentID)       // never stored separately

select(targetIndex, input):
    if pages.empty: return
    j = clamp(targetIndex, 0, pages.count - 1)
    currentID = pages[j].id
    interactionToken += 1
    renderSnapshot(pages, currentID)  // content, dots, count, buttons, semantics
    persistResumeID(currentID)
    transitionTo(j, animate = discrete(input) and not reduceMotion)
    // stale animation callbacks cannot change currentID or overwrite snapshot

previous / tapBefore / accessibleDecrement -> select(index - 1, input)
next / tapAfter / accessibleIncrement     -> select(index + 1, input)
settledSwipe(targetIndex)                 -> select(targetIndex, swipe)
scrub(targetIndex)                        -> select(targetIndex, scrub)
cancelDrag                               -> restoreSnapshot(currentID)
skip / startStory                        -> persistDismissed(); openCurrentStory()
```

Serialize discrete input events; each operates on the latest selected ID. Render updates form one transaction. Animations are presentation only and cannot write selection. Freeze incoming page-list changes while an interaction is active, then reconcile IDs once. Reduce Motion uses immediate replacement instead of sliding; no autoplay, timers, zoom, or parallax are part of this introduction.

## Accessible and visible controls

Expose the dot strip as **one adjustable page-position control**, named “Introduction page,” with value “Page 2 of 3, Discovery,” and bounded increment/decrement actions. Individual dots are not unnamed buttons or separate accessibility stops. Previous and Next remain ordinary named buttons and offer the same outcomes if adjustable actions are unavailable in the chosen framework. Page count and title must never become stale. [VoiceOver — Descriptions](https://developer.apple.com/design/human-interface-guidelines/voiceover#Descriptions)

Reading order is: page title (heading), meaningful photo description with its caption, page-position control, Previous, Next/Start Story, Skip Introduction. Decorative images are omitted from accessibility navigation. Avoid repeating caption text in the photo description. Offscreen pages are excluded from navigation. Keep focus on the initiating persistent control after paging and notify assistive technology of the updated title/position once after settlement; if Next becomes Start Story, preserve focus on that action slot with its updated name. On opening the full story, move focus to its heading. Exact announcement delivery requires implementation testing. [VoiceOver — Navigation](https://developer.apple.com/design/human-interface-guidelines/voiceover#Navigation)

Use at least 44 × 44 pt activation regions for buttons, with separated nonoverlapping targets; the dots can remain visually small inside the larger control. Next/Start Story is the single prominent action; other actions are secondary. Supply press and focus feedback. Labels may wrap and the action row may stack at enlarged text sizes. These dimensions are specified in iOS logical points, not Linux pixels. [Buttons — Best practices and Style](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices)

Support text enlargement to at least 200%, retaining every caption and action through reflow/vertical scrolling. Use an opaque neutral footer when photos compromise legibility; selection also has a filled shape and numeric position rather than color alone. Measure final text/background contrast in light, dark, and Increase Contrast appearances. Honor Reduce Motion as specified above. The local accessibility guide supplies the text-scale and motion guidance; final colors and measured geometry are unavailable. [Accessibility — Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision), [Accessibility — Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility#Cognitive)

## Worked before/after

**Before, as reported:** A person sees 47 indistinguishable dots. A swipe changes stories while the selected dot remains unchanged. Tapping a dot can delete the current page. Accessibility offers unnamed buttons, so neither destination nor consequence is clear.

**After, illustrative trace:** Open Arrival: content ID `arrival`, first filled dot, “Page 1 of 3,” Previous disabled. Swipe forward: one transaction selects `discovery`; its photo/title, second filled dot, visible count, and accessible value all become page 2. Tap the control after its active indicator: select `reflection`, show “Page 3 of 3,” and replace Next with Start Story. Try moving forward again: remain on Reflection without wrapping, deleting, or opening another story. Activate Previous: return to Discovery. Activate Skip Introduction: open the same full story and remember dismissal. Relaunch: open the host story experience without replaying the introduction. Replay Introduction intentionally returns to Arrival.

Nonvisual equivalent: reach “Introduction page, Page 1 of 3, Arrival,” increment to Discovery, read its heading/description/caption, then activate Next to reach Reflection and Start Story to enter the full story. No precision dot targeting or content swipe is required. This is a specified walkthrough, not a VoiceOver test result.

## Acceptance checks and evidence status

**Passed — document inspection only:** Read `interface.md`, the installed root skill, topic-index matches, and the selected family → topic procedure → source guides for Page controls, Scroll views, Accessibility, VoiceOver, Buttons, and Onboarding. This specification defines stable identities, bounded movement, one selection authority, deletion isolation, alternate controls, and skip/resume behavior. No application behavior has been demonstrated.

**Failed — supplied baseline description:** Peer-page structure, nondestructive paging, swipe/indicator synchronization, and named accessibility controls fail the intended contract according to `interface.md`. These failures were not reproduced.

**Not executed — implementation acceptance checks:**

| Check | Required result |
| --- | --- |
| First/last boundaries | Previous disabled at first; forward attempts at last stay put; no wrap or story switch. |
| Every input | Buttons, side taps, swipes, scrub, and accessible adjustments select the same page and update all representations together. Canceled drags leave selection unchanged. |
| Rapid input | Repeated taps, direction reversals, scrubbing, and interrupted animations never restore stale content or values; rapid scrub has no animated page-scroll flashes. |
| Data safety | Before/after page and story records are identical after every paging input. No paging route invokes deletion. |
| Page-list changes | Insert/reorder retains selected ID; removal uses the defined neighbor; count and semantics update together; zero/one-page cases match the contract. |
| Accessibility task | VoiceOver, Switch Control, and Full Keyboard Access can traverse and complete or skip the flow. Names, roles, values, heading order, focus retention, and single settled update match the contract; offscreen pages do not interrupt reading. |
| Layout and preferences | At 200% text, supported iPhone sizes/orientations, and light/dark/Increase Contrast, content and actions remain reachable; measure contrast and hit regions. Reduce Motion removes sliding without losing state. |
| Lifecycle | Fresh entry, interrupted resume, completion, skip across relaunch, and explicit replay follow the specified persistence rules. |
| Missing assets | Photo failure preserves caption, paging, completion, and skip; there is no indefinite blocking download. |

## Evidence limits

Only local supplied text and installed guidance were used; no web access was performed. Official links above identify the source sections represented by the local package, whose guides are dated 2026-10-25; they were not fetched or independently verified. Local references are derived guidance, not SDK documentation, and their existence does not establish independent source review.

No implementation, screenshots, asset set, actual destination inventory, persistence store, or target framework was supplied. The three-page content and help route are explicit proposed decisions requiring product content integration. No device, SDK compilation, GUI, accessibility execution, contrast measurement, target measurement, or performance test occurred. Runtime acceptance remains open; this deliverable is a framework-agnostic interaction specification.
