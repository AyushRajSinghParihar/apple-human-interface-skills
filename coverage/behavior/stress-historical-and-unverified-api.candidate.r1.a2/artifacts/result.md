# Product feasibility and interface alternative

## Verdict

The brief in `interface.md` is not supportable as written. A native TV catalog and a user-controlled spatial preview are feasible design directions, conditional on deployment and SDK verification. This is a specification and local-source review, not an implementation or a successful platform build.

Assumption: the useful product task is discovering small information experiences and previewing them. The brief provides no content model, purchase flow, or installation contract. This alternative preserves discovery and preview; it deliberately changes the promise of installing system widgets on TV. If arbitrary widget installation or forced immersion is essential to the business requirement, this alternative does not satisfy that requirement and the product scope must change.

## Evidence-backed decisions

| Brief claim | Assessment from supplied evidence | Decision |
|---|---|---|
| tvOS web view hosts the store | The installed web-view guide explicitly says web views are unsupported on tvOS. | Replace HTML hosting with native catalog screens using structured content. No embedded browser dependency. |
| WidgetKit widgets on tvOS | The installed widget guide explicitly says widgets are unsupported on tvOS. WidgetKit is not evidence of a TV widget-hosting or store-installation capability. | Offer in-app information panels, clearly named as app content. Do not claim system widget installation, persistence outside the app, or WidgetKit support on TV. |
| Full browser | The web-view guide discourages recreating Safari's general browser feature set; that advice is distinct from the explicit tvOS support exclusion. | Remove arbitrary URL entry, browser tabs, and web history from the TV experience. Render bounded catalog descriptions natively. |
| Portal disables Crown and forces full immersion | The visionOS and Crown guides retain system control of immersion and Home behavior. The named `AppleImmersionLock.disableDigitalCrown()` is expressly hypothetical in the brief and has no supplied API documentation. | Reject the lockout interaction. Do not ship or propose that call as real. Absence of documentation alone does not prove that a symbol can never exist; the design must preserve system agency regardless. |
| 2019 blog proves support | Neither the blog contents nor its URL is supplied. Its date and the team's assertion cannot establish current platform/API support. | Treat it as unverified historical context, not implementation evidence. |

Material source links, copied from the installed references and not fetched: [Web views — Platform considerations and Best practices](https://developer.apple.com/design/human-interface-guidelines/web-views#Platform-considerations), [Widgets — Platform considerations](https://developer.apple.com/design/human-interface-guidelines/widgets#Platform-considerations), [Digital Crown — Apple Vision Pro](https://developer.apple.com/design/human-interface-guidelines/digital-crown#Apple-Vision-Pro), and [Immersive experiences — Immersion and passthrough](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences#Immersion-and-passthrough).

These are local HIG-derived snapshots, not SDK declarations or independent verification of current Apple documentation. No deployment version or framework availability is guaranteed here.

## Concrete interface contract

### tvOS: “Explore panels”

Use native platform components where suitable. Initial scope is a public, read-only catalog without accounts, purchases, third-party executable content, or installation. Example content below is simulated.

1. **Catalog:** title “Explore panels”, followed by a single vertical collection of generously sized rows. Each row has artwork, a title such as “Daily sky”, and a one-line description. Initial focus is the first available item. Keep text legible across a room and reserve space for enlarged focus artwork.
2. **Detail:** activating a row opens its native detail screen with title, description, a labeled static preview, and one primary action, “Open panel”. State explicitly: “Runs inside this app.” Preview artwork must not masquerade as an interactive system widget.
3. **Panel:** opens an app-owned information screen. For the simulated example, show “Daily sky”, sample conditions, and “Sample data”. Real data later requires a defined provider and freshness policy. It remains app content, with no out-of-app persistence promise.

Remote route: Up/Down moves among catalog items; a deliberate Select opens detail, and Select on “Open panel” opens the panel. Focus movement alone never opens content. Back moves panel → detail → catalog; restore the originating item and scroll position. At the catalog root, retain system Home behavior; holding Back retains its system behavior. No browser-history interpretation of Back. Every interactive element must have a directional route in and out, without a pointer.

Focused, pressed, and unavailable states are distinct. Unavailable catalog entries carry explanatory text and have no active open action. When an item disappears, restore a nearby valid item; if none remain, show an empty state. Loading shows a readable status; failure shows an explanation and reachable Retry action; retry preserves any available catalog content. Empty state says “No panels available” with Retry. These are proposed application behaviors, not claimed automatic framework features.

Source basis: [Designing for tvOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos#Best-practices), [Focus and selection — tvOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#tvOS), and [Remotes — Best practices](https://developer.apple.com/design/human-interface-guidelines/remotes#Best-practices).

### visionOS: browse in a window; preview by choice

The catalog and detail task begins in a movable Shared Space window. Reading, selecting, and viewing the ordinary preview remain usable there. No task requires immersion. The initial release can deliver this window-only path while immersive implementation remains unverified.

An optional, later “Enter spatial preview” action may offer a portal-style progressive experience only if the content benefits from it and the selected SDK/deployment target supports the implementation. “Portal” describes the experience; it is not an API name. Do not silently substitute full immersion. Keep the selected item ID and catalog position across transitions.

| State | User action or event | Result |
|---|---|---|
| Window detail | Enter spatial preview | Preserve selection; request entry once; show pending feedback and prevent duplicate requests. |
| Entry pending | Entry succeeds | Show a stationary preview with a stable reference and a visible “Return to catalog” action. |
| Entry pending | Entry is declined, unavailable, or fails | Stay in the detail window, retain selection, explain that spatial preview is unavailable; ordinary preview remains usable. |
| Spatial preview | Crown/system action | Allow system immersion, recentering, awareness, and Home behavior. Do not intercept, disable, or immediately counteract it. |
| Spatial preview | Return to catalog | Leave the preview and restore the selected detail in its window. Return means less immersion, not quitting. |
| Any state | System interruption or scene dismissal | Reconcile actual scene state on return, preserve selected content, and require a fresh deliberate action for reentry. |

Keep important content central; allow indirect activation with hands resting. Do not require walking, repeated reaching, artificial camera travel, custom virtual hands, or room-sensing permissions for this preview. Provide a stable visual reference and restrained transitions. Exact geometry and transition timing require prototype and device evidence. The window preview remains the fallback if spatial presentation cannot be delivered.

Source basis: [Designing for visionOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos#Best-practices), [Immersive experiences — Best practices](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences#Best-practices), [Transitioning between immersive styles](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences#Transitioning-between-immersive-styles), and [Digital Crown](https://developer.apple.com/design/human-interface-guidelines/digital-crown#Apple-Vision-Pro). Choosing optional progressive immersion is this proposal's application decision, not an Apple requirement.

## Acceptance checks and present status

**Passed — document inspection only:** inspected `interface.md`; read the installed root, relevant families, platform procedures, surface/input procedures, and their references in route order. Searched the topic index before finalizing the route. The alternative removes TV web-view/widget dependencies, rejects Crown lockout, defines focus/return routes, and specifies failures and preserved state. No web access was used.

**Failed — original brief's supportability checks:** TV web-view hosting and TV system widgets conflict with explicit local support exclusions. Forced Crown lockout conflicts with the documented interaction model. The claimed blog/API proof is insufficient. These are brief-level findings, not observed runtime failures.

**Not executed — implementation acceptance gates:**

- On the chosen tvOS target, traverse every catalog/detail/panel/error action using Siri Remote. Pass only if focus is visible, enlargement is unclipped, no region traps focus, Select is deliberate, and Back restores the stated hierarchy and position. Check legibility from the actual viewing distance, including approximately 8 feet or farther as discussed in the local TV guide.
- On the chosen visionOS target, enter, decline, fail, interrupt, and leave spatial preview. Pass only if the ordinary window remains a usable fallback, context survives, and repeated scene requests do not race or force reentry.
- On a worn Vision Pro, exercise Crown/system exit and awareness behavior. Pass only if the app does not block or undo system control. Confirm stationary use, resting-hand activation, stable references, and comfort across postures. Source inspection does not establish these results.
- Verify accessible names, action semantics, reading order, and equivalent activation with platform assistive technologies on implemented screens. No accessibility execution or conformance is claimed.
- Compile and run against selected supported SDKs and deployment versions; verify every chosen API's availability, scene lifecycle, framework support, and any required capabilities. No SDK compilation, simulator run, GUI run, or device execution occurred.

## Missing evidence and release decisions

Before engineering commitment, choose minimum OS versions, hardware targets, implementation stack, content scope, and whether the portal adds enough value to justify a second phase. Obtain current official SDK documentation and a suitable Apple build environment to validate exact APIs and availability. This work did not install an SDK or GUI software.

The cited 2019 blog, real catalog assets/schema, data provider, refresh expectations, and failure responses remain absent. Purchases, accounts, external website handoff, cross-device state sync, and third-party installation are outside this proposed first scope and need separate requirements and support verification if requested. No App Store or distribution approval is inferred.

The local references carry snapshot/retrieval dates of 2026-10-25 and varied source revisions. Those dates do not independently establish present SDK support. With browsing prohibited and API documentation absent, current availability remains an explicit evidence gap. Preserve the window-only and native TV fallback rather than filling that gap with remembered API names.

## Local audit trail

All paths resolve under `.agents/skills/apple-hig/`. Each instruction/reference file was read in its own `cat` command; the index was searched with `rg`.

- Root: `SKILL.md`; routing search: `references/topic-index.md` for tvOS, visionOS, web views, widgets, immersion, and Digital Crown.
- Getting started family: `subskills/apple-hig-getting-started/SKILL.md`; `.topics/apple-hig-designing-for-tvos/SKILL.md` and `.topics/apple-hig-designing-for-visionos/SKILL.md`; then `references/designing-for-tvos.md` and `references/designing-for-visionos.md` within that family.
- Content family: `subskills/apple-hig-content/SKILL.md`; `.topics/apple-hig-web-views/SKILL.md`; then `references/web-views.md`.
- System experiences family: `subskills/apple-hig-system-experiences/SKILL.md`; `.topics/apple-hig-widgets/SKILL.md`; then `references/widgets.md`.
- Inputs family: `subskills/apple-hig-inputs/SKILL.md`; `.topics/apple-hig-digital-crown/SKILL.md`, `.topics/apple-hig-remotes/SKILL.md`, `.topics/apple-hig-focus-and-selection/SKILL.md`; then their matching `references/*.md` files.
- Foundations family: `subskills/apple-hig-foundations/SKILL.md`; `.topics/apple-hig-immersive-experiences/SKILL.md`; then `references/immersive-experiences.md`.
