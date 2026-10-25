# iPhone neighborhood-events review

## Scope and evidence

The useful outcome is **find a nearby event and understand when and where it happens**. The supplied `interface.md` is the sole product evidence: a short behavioral description, with no rendering, code, control inventory, or executable app. “Verified” below means explicitly documented in that brief, not independently reproduced. Severity ranks task impact; it is reviewer judgment, not measured user research.

## Ranked findings and decisions

| Rank | Verified observation | Effect and principle | Correction / decision |
| --- | --- | --- | --- |
| 1 — High | Launch opens an unrelated merchandise page. | Finding events starts with an unrelated detour. Purpose and agency favor direct access to useful content. | Ordinary fresh launch opens **Events**, with nearby-event content or its truthful empty/error state. Merchandise is an optional secondary destination. An explicit event link opens that event. |
| 2 — High | Opaque decoration obscures event times. | People cannot reliably judge whether an event fits their schedule. Simplicity and craft require usable essentials; delight should support the task. | Remove decoration from the time/content region. Keep title, date, time, and venue in unobstructed flow; confine expressive decoration to backgrounds or separate regions. |
| 3 — High | Navigation labels change after each tap. | Equivalent navigation becomes unpredictable and people must relearn destinations. Familiarity calls for consistent appearance and behavior. | Give every destination an immutable identity and stable concise label. Change selection styling, not destination names, after navigation. Preserve each destination’s context. |
| 4 — High | Actions give no pending or success feedback. | People cannot tell whether an action started or completed and may repeat it. Familiarity requires clear progress and change feedback. | Distinguish activation, pending work, confirmed outcome, and failure. Keep routine feedback beside the affected item; show success only when the underlying operation confirms it. |
| 5 — Medium | Promotional content has greater prominence than events. | The hierarchy favors a secondary commercial goal over finding events. Purpose and simplicity favor the core task. | Put events first in reading and visual priority. Keep promotions subordinate and clearly identified, without replacing event results or covering their information. |

Source support: findings 1 and 5 apply [Purpose, Agency, and Simplicity](https://developer.apple.com/design/human-interface-guidelines/design-principles); finding 2 applies [Delight and Craft](https://developer.apple.com/design/human-interface-guidelines/design-principles) and [Layout — Visual hierarchy](https://developer.apple.com/design/human-interface-guidelines/layout#Visual-hierarchy); finding 3 applies [Familiarity](https://developer.apple.com/design/human-interface-guidelines/design-principles#Familiarity); finding 4 applies [Feedback — Best practices](https://developer.apple.com/design/human-interface-guidelines/feedback#Best-practices) and, for delayed button actions, [Buttons — iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS). These links identify official source articles; only the installed local guidance was read.

## Tradeoffs resolved

A merchandise-first launch gives promotions immediate exposure but delays the stated task. An events-first launch with optional merchandise access preserves commercial discovery and direct access to events. Choose the latter; the exact secondary placement is a product proposal, not an Apple-mandated arrangement.

Removing all expression could simplify the screen but unnecessarily erase character. Choose expressive backgrounds and small contextual feedback, with no overlap of essential content. A satisfying emotional response remains a usability hypothesis.

Keep navigation identity stable while allowing content to change. The brief does not identify whether navigation uses tabs, links, or buttons. Do not mandate a tab bar without the destination inventory. If it is top-level tabs, use the [Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars#Best-practices) contract: destinations rather than commands, retained section state, available empty destinations, and short labels.

## Control and surface inspection map

| Supplied surface | Candidate procedure | Known / unresolved inspection question |
| --- | --- | --- |
| Navigation labels | Tab bars for top-level destinations; Buttons for navigation commands | Label instability is documented. Destination count, actual component, Back behavior, and state retention are unknown. |
| Unnamed actions | Buttons; Feedback | Missing outcome feedback is documented. Labels, outcomes, roles, reversibility, hit regions, and whether any control is a persistent selection are unknown. Inventory these before assigning semantics. |
| Merchandise launch and promotions | Design principles; Layout | Competing purpose and hierarchy are documented. Exact screen geometry and promotional format are unknown. |
| Event times and decoration | Layout | Occlusion is documented. Extent, text metrics, contrast, and layout constraints are unknown. |

No unsupported search, purchase, permission, or account defects are inferred.

## Corrected behavior specification

This is a framework-agnostic contract, not SDK code. Preserve the existing stack.

```text
Destination = { immutableId, stableLabel, retainedRoute, retainedScroll }

on ordinaryFreshLaunch:
    select Events
    show event content, or explicit empty/error state
on explicitEventLink(eventId):
    open matching event; provide a path back to Events
on selectDestination(id):
    retain current destination context
    restore destination[id] context
    leave all destination labels unchanged
on returnFromEventDetail:
    restore Events content context and scroll
on interruptAndResume:
    restore selected destination and event context
    reconcile unresolved operations; never infer success from elapsed time

layout:
    prioritize Events heading and event content
    group each event's title, date/time, and venue
    keep decoration outside essential content bounds
    allow content to wrap and rows to grow as space/text changes
    keep essential content/actions inside appropriate safe regions
    make promotions secondary without blocking event access
```

These layout and continuity decisions follow [Layout — Adaptability and safe areas](https://developer.apple.com/design/human-interface-guidelines/layout) and [Designing for iOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices). Their exact rendering requires implementation evidence.

For an actual delayed action, bind this state model to its real outcome and object:

```text
idle --activate--> pending(requestId, objectId)
    show press feedback immediately
    show in-button activity indication and operation-specific text
    suppress duplicate submission for the same operation
pending --confirmed success--> resolved
    show the confirmed result beside the affected object
pending --confirmed failure--> failed
    preserve context; explain failure and offer a meaningful retry
pending --uncertain result--> unresolved
    reconcile with the operation's truth source before enabling a duplicate
```

Routine completion should use a subtle state change rather than a blocking success alert. Do not add sound or haptics as the sole essential signal. Cancellation and undo depend on actual operation semantics; leaving a screen must not pretend to cancel a remote operation. This is a proposed recovery contract, not evidence of current behavior.

## Worked before / after

Illustrative event and action data below are invented to demonstrate the correction; neither a save feature nor these labels are established by the brief.

**Before, supported by the brief:** A newcomer opens the app, sees merchandise, navigates using labels that change, encounters an obscured event time, and activates an action without feedback. Promotions remain more prominent than events.

**After, illustrative walkthrough:** Launch shows **Events**. An unobstructed item reads “Neighborhood market · Saturday, 10:00–14:00 · Oak Square.” Opening it preserves the list context. If the product offers a delayed **Save Event** command, tapping it shows **Saving…** in that control; confirmed persistence produces **Saved** beside the event. Failure instead shows “Couldn’t save this event. Try again.” Returning to Events restores the previous position and keeps its label. Merchandise remains optional and secondary.

**Returning person:** After an interruption while viewing that event, restore the event and reconcile any pending save. Back returns to the same list position. Do not redirect them to merchandise. These document walkthroughs provide a coherent target flow; they do not establish usability or successful persistence.

## Acceptance checks and status

**Passed — document inspection:** Target platform and primary outcome are explicit. All five ranked observations trace directly to `interface.md`. The proposed flow has no merchandise gate, uses stable destination identities, separates essential content from decoration, and distinguishes pending, success, failure, and uncertainty. These are specification checks only.

**Failed — supplied baseline description:** Direct task entry, unobstructed event times, stable navigation labels, visible action feedback, and events-first hierarchy fail according to the brief. No runtime reproduction occurred.

**Not executed — implementation acceptance:**

1. Fresh launch reaches Events; event links reach the matching event. Empty and failed event retrieval states explain what happened without substituting promotions.
2. Repeated navigation leaves destination labels unchanged. Back, section switching, interruption, and resumption preserve event and list context. Empty sections remain discoverable if tabs are used.
3. Render at the smallest and largest supported content areas, intermediate sizes, portrait/landscape, enlarged text, and long localized content. Event times remain readable; no essential content overlaps decoration, bars, or hardware regions. Record actual dimensions/settings when run.
4. Exercise delayed, successful, rejected, unavailable, and uncertain action outcomes. Pending indication appears at the initiating control; duplicate requests are suppressed; success follows confirmation; retry preserves context and cannot silently duplicate an operation.
5. Inspect actual controls: labels match outcomes, custom buttons show press feedback, and iPhone button hit regions meet the local guide’s general minimum of 44 × 44 pt with clear separation. No hit-region measurements are available now. See [Buttons — Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices).
6. On an implemented iPhone experience, verify primary-action reach, system Back interaction, and interruption recovery. Verify nonvisual feedback interpretation and accessible control identification with appropriate assistive-technology testing; these are pending checks, not diagnosed accessibility failures.

## Evidence limits and routing record

Read the installed root `apple-hig/SKILL.md`, then the Getting started family and its Design principles and Designing for iOS procedures before their source guides. Searched the complete topic index for task concepts and candidate controls. Also read Foundations → Layout, Navigation and search → Tab bars, Menus and actions → Buttons, and Patterns → Feedback, each family and topic procedure before its supporting source guide. Paths resolve within `.agents/skills/apple-hig/`; individual files were read in separate shell commands.

The local articles are dated application guidance derived from Apple’s HIG, not an SDK reference or proof of independent source review. No web browsing, media review, device, simulator, SDK build, GUI, or accessibility execution occurred. There is no supplied visual rendering to assess contrast, type, spacing, touch comfort, or actual promotional scale. Privacy, cultural inclusion, and real-world emotional response cannot be judged from this brief. No source conflict was identified in the guidance used. The deliverable is an auditable review and proposed behavior, not an implemented or validated app.
