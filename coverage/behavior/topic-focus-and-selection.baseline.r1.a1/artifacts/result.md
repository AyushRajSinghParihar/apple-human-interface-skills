# Apple TV project browser audit

## Scope and evidence

The supplied `interface.md` identifies tvOS and explicitly reports five behaviors. The findings below are verified against that written description, not reproduced in an application. Ranking reflects potential harm and task obstruction; frequency and actual damage are unknown.

Guidance was read locally, in this order: installed `apple-hig/SKILL.md` → `subskills/apple-hig-inputs/SKILL.md` → its routed `references/focus-and-selection.md` and `references/remotes.md`. The complete topic index was also inspected. All paths resolve within `.agents/skills/apple-hig/`. This installed Inputs family routes directly to article references; it supplies no separate topic procedure for these articles. No web access was used. Official links below identify the sources of the local snapshot, not pages checked live.

## Ranked findings and decisions

| Rank | Verified supplied behavior | Effect and correction | Basis |
|---|---|---|---|
| 1 — Critical | A disabled destructive control remains activatable. | The unavailable appearance promises protection that activation does not enforce; destructive work could occur. Remove it from directional focus targets and reject activation at the action boundary whenever unavailable, including queued or stale events. | tvOS unavailable state is inactive and unreachable: [Focus and selection, tvOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#tvOS). Action-boundary enforcement is the proposed implementation safeguard. Actual deletion is not evidenced. |
| 2 — High | Navigation enters a dead end at a carousel boundary. | Users can become unable to continue browsing or reach another control. Define directional neighbors across carousel and surrounding regions; retain a reverse route. An outward direction at a true content edge may leave focus in place, but must not trap the user or strand available controls. | tvOS requires directional access to every interactive item: [Focus and selection, Best practices](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Best-practices). Preserve familiar remote directions: [Remotes, Best practices](https://developer.apple.com/design/human-interface-guidelines/remotes#Best-practices). The exact broken direction and layout are not supplied. |
| 3 — High | Initial focus starts offscreen. | The current interaction target is hidden at entry. On first browser entry choose an available visible project; if none exists, choose a visible available browser action. Reveal a restored offscreen target before presenting its focus state. | Focus identifies the interaction target; tvOS uses visible component focus: [Focus and selection](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection). The entry and reveal policy is a concrete design application, not a quoted initialization rule. |
| 4 — High | Focused cards look identical to selected cards. | Users cannot distinguish the next activation target from their persistent project choice. Store and render focus and selection independently; moving focus must not change the selected project. | Distinct unfocused, focused, pressed, selected and unavailable states; tvOS normally requires separate activation: [Focus and selection, tvOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#tvOS). |
| 5 — Medium | Returning from detail jumps to the first card. | Users lose their browsing position and must retrace navigation. Save the originating project ID, carousel and viewport; restore that card on returning to this browser. Use a deterministic nearby fallback if it no longer exists. | Restoration is a product decision consistent with avoiding unsolicited focus movement: [Focus and selection, Best practices](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Best-practices). It is not an explicit universal restoration mandate in this snapshot. Back follows the parent hierarchy: [Remotes, Best practices](https://developer.apple.com/design/human-interface-guidelines/remotes#Best-practices). |

## Corrected behavior specification

For this specification, “selected project” means one persistent project choice, committed by an explicit press. Assume pressing an available project both commits that choice and opens its detail. The supplied description does not define selection semantics; this is a reviewable product decision, not an observed fact. If opening detail and choosing a project are separate product actions, give them explicit separate commands while keeping the same independent focus state.

| State | Presentation and behavior |
|---|---|
| Unfocused, unselected | Receded card with readable project identity. |
| Focused, unselected | Raised/lit focus treatment; reserve space so enlargement is not clipped. No selected badge. |
| Unfocused, selected | Persistent checkmark plus “Selected” label, with receded card appearance. |
| Focused, selected | Focus treatment and persistent selection badge together. |
| Pressed | Immediate transient press feedback; ends on release/cancel. Cancellation does not commit. |
| Unavailable | Visibly inactive, with an explanatory label where useful; excluded from focus navigation and action execution. A selected project becoming unavailable retains its selection marker until an explicit choice or product removal rule changes it. |

Prefer system focus effects when the eventual framework provides them; the raised/lit treatment describes the required experience without assuming an Apple SDK. Selection has a text/shape cue independent of focus or color. These treatments apply the local [tvOS state guidance](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#tvOS).

```text
state:
  focusTargetID = null                 // project or browser control
  selectedProjectID = null             // independent persistent choice
  pressedTargetID = null
  returnAnchor = {projectID, carouselID, oldIndex, viewport} or null

enterBrowser(reason):
  if reason == returningFromOwnDetail:
    target = available(returnAnchor.projectID)
      or nearestAvailableInSavedCarousel(returnAnchor.oldIndex)
      or firstAvailableProject()
      or visibleAvailableBrowserAction()
  else:
    target = firstVisibleAvailableProject()
      or visibleAvailableBrowserAction()
  restoreRelevantViewportIfReturning()
  revealWithFocusMargins(target)
  focusTargetID = target.id

direction(input):
  target = directionalNeighbor(focusTargetID, input, availableTargets)
  // Horizontal neighbors traverse the carousel, revealing adjacent cards.
  // Up/down lead to spatially aligned available rows or surrounding controls.
  // No implicit wrap; an absent outward neighbor leaves focus unchanged.
  if target exists:
    revealWithFocusMargins(target)
    focusTargetID = target.id
  // Never mutate selectedProjectID here.

pressBegin(id):
  if id == focusTargetID and available(id): pressedTargetID = id

pressCancel(): pressedTargetID = null

pressCommit(id):
  validPress = (id == pressedTargetID and id == focusTargetID)
  pressedTargetID = null
  if not validPress or not available(id): return
  if isProject(id):
    returnAnchor = snapshotStableIDAndBrowserPosition(id)
    selectedProjectID = id
    openDetail(id)
  else:
    dispatchAction(id)                 // action handler revalidates availability

executeDestructiveAction(action, projectID):
  if not currentlyAllowed(action, projectID): return REJECTED
  performActionAtomicallyWithEligibilityCheck(action, projectID)
```

Build the directional graph from actual layout, not arbitrary index jumps. Every available interactive target must have a directional path from browser entry and a route back to the browsing region. An unavailable destructive control is excluded from this requirement. Do not add carousel wrapping merely to mask a broken graph.

Restoration uses stable IDs, not array indices. If the original card was removed, choose the nearest available card in its saved carousel (ties prefer the preceding card), then another available project, then a visible available browser action. For an empty browser, show an empty-state message and a meaningful available action such as Back or Create if supported. Do not invent a project selection. These fallback choices are proposed policies. During discrete directional navigation, if the focused item disappears, use a nearby one-step target, consistent with the local focus guidance; do not reset to the first card after ordinary data refreshes.

## Worked before/after

Illustrative fixture: one carousel contains projects A–F; A–C fit initially, F is near the end, A is selected, and a disabled Delete control is visible. The fixture names and layout are invented to demonstrate the correction.

| Step | Before, based on reported defects | After, specified behavior |
|---|---|---|
| Enter browser | Focus begins offscreen; exact target is unknown. | A is visible and focused, with both its focus treatment and selected badge. |
| Move right to B | Focus and selection appearances are indistinguishable. The description does not establish whether selection data changes. | B is raised/lit without a selected badge; A retains its “Selected” badge. Selected ID remains A. |
| Continue right to F | Boundary navigation can dead-end. | Each next card is revealed. At F, outward Right stays on F; Left returns to E, and Up/Down reach applicable neighboring regions. |
| Press F | Existing activation semantics are unspecified. | Press feedback appears; successful commit sets selected ID to F, saves F and viewport, and opens F detail. |
| Back to parent browser | Focus jumps to first card. | F and its viewport are restored; F is focused and selected. |
| Attempt disabled Delete | Report says it remains activatable. | Directional navigation skips Delete. A direct or queued activation attempt is rejected with zero destructive side effects. |

## Acceptance checks

These are required future checks, not executed test results. A framework-neutral model can exercise transitions and action guards; visual and remote checks require the eventual running interface.

1. **Entry:** With projects, without projects, and with the saved target initially offscreen, browser entry produces a visible available focus target. No focus decoration is clipped after reveal.
2. **State independence:** Starting with A selected, focus B, then C. Selected ID remains A. Explicitly activate C: selected ID becomes C. Cancel a press: selection and navigation remain unchanged. Render all six state rows above, including focused-and-selected together.
3. **Reachability:** Enumerate available targets and directional edges at both carousel ends and across rows/controls. From entry, every available target is reachable; every carousel end permits an escape or reverse path. Repeat after scrolling and data changes. An outward no-op alone is not a failure.
4. **Return:** Open a nonfirst project and return from its detail. Assert the same stable ID and viewport context. Reorder projects while detail is open: restore the ID. Remove/disable it: apply the documented fallback without selecting a different project merely because focus moved.
5. **Unavailable action:** Navigate toward disabled Delete, send direct activation, and queue activation before disabling it. Assert no focus on it and zero destructive operations in every case. Recheck eligibility at execution to cover stale UI state.
6. **Remote behavior:** On the eventual interface, verify directional swipe/press feedback and Back to the parent browser. Preserve system Back/Home behavior; no custom pointer is needed for this browser.

## Evidence limits

Only a one-sentence interface description and the installed guidance were inspected. There is no supplied implementation, screenshot, focus graph, event trace, or test harness. No device, simulator, SDK, GUI, remote, accessibility service, or automated behavioral execution occurred. Color contrast, motion, clipping, actual focus timing, exact boundary geometry, accessibility announcements and real destructive side effects remain unverified. The corrections are specifications, not implemented fixes. The local HIG references identify a 2026-10-25 retrieval snapshot; their existence does not establish independent source or media review. No current online guidance or linked implementation API was checked.
