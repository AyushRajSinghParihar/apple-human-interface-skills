# iPhone package tracker: revised Home Screen quick actions

## Scope and evidence

This is a framework-agnostic interaction specification based on `interface.md` and the installed apple-hig package. The supplied interface is a brief, not an executable implementation: it describes nine actions, mostly account settings, unlabeled icons, “Track latest” opening a generic welcome screen, and a stale package advertised when nothing is tracked. Individual settings labels, existing routes, account model, and package schema are not supplied.

The decisions below define proposed behavior. “Active package” means a tracked package that is neither delivered, archived, nor deleted; this is a product definition, not an Apple requirement. Equivalent existing domain states may be mapped explicitly during implementation.

## Decisions and action contract

Offer two stable shortcuts and a third only when a valid active package exists. Remove account settings from this surface; retain their ordinary in-app entry points. All actions are navigation or draft creation, never immediate data mutation. The same tasks must remain available inside the app.

Apple's local [Home Screen quick actions guidance — Best practices](https://developer.apple.com/design/human-interface-guidelines/home-screen-quick-actions#Best-practices) recommends useful, concise shortcuts, no more than four, predictable contextual updates, and familiar monochrome symbols rather than emoji. The exact two-plus-one set and ordering below are product decisions.

| Position / stable action ID | Visible title | Subtitle | Icon intent | Destination and availability |
| --- | --- | --- | --- | --- |
| 1 / `add-package` | Add Package | None | Monochrome plus glyph | Always offered. Open the tracking-number entry form, ready for input. Create no package until the user submits valid input. Cancel returns to the prior in-app context or package list on a cold start. |
| 2 / `view-packages` | View Packages | None | Monochrome shipping-box glyph | Always offered. Open the package list. With zero packages, show “No packages yet” and an Add Package action. |
| 3 / `track-latest` | Track Latest | None | Monochrome location glyph | Offer only with a validated active package. Open that exact package's tracking detail, including status and last-update time. |

Every row has a text title as well as an icon. Use a familiar SF Symbol if available through the eventual platform integration, otherwise a monochrome glyph derived from the official Quick Action template. Exact assets and SDK identifiers remain implementation work. Let the system place icons and render the menu; do not encode left/right placement in custom artwork. No package names, addresses, or tracking numbers appear in shortcut text.

“Latest” means the active package with the most recent successful user tracking-detail visit, falling back to the most recently added active package. Break timestamp ties by stable package ID. Carrier background updates do not change this ranking. This is a deterministic product policy; it does not claim Apple prescribes recency ordering.

## Dynamic publication and destination identity

Publish a complete replacement set after local data is ready, after a successful tracking-detail visit, and after add, delivery, archive, deletion, or account changes. Keep the two stable actions in their positions. If there is no eligible package, publish only those two; do not publish a disabled or stale Track Latest row.

Bind Track Latest to an opaque package ID and its account/context generation at publication. Do not recalculate “latest” on selection: the selected shortcut retains its target even if another package becomes more recent. Revalidate ownership and active status before showing content. Immediately clear the dynamic row on sign-out or account change, and rebuild only from the new context. A previously published shortcut can still arrive, so clearing the menu alone is insufficient.

If the bound package is deleted, delivered, archived, inaccessible, or belongs to a previous account, open the current package list with “This package is no longer available here.” Do not show the old package's details or silently substitute a different package. If the list is empty, show its empty state and Add Package. Rebuild shortcuts after resolving the invalid target.

On a fresh installation or before a valid local snapshot is available, publish only the stable pair. If the platform retains an older dynamic action, the handler still validates it. Offline operation may use a locally validated package with a visible last-update time and an offline status; never present cached tracking events as a live refresh. Network failure must not redirect to Welcome.

## Launch and interruption contract

Use the same dispatcher for cold and warm entry. A new shortcut intent takes precedence over restored navigation state. For a normal icon launch without a shortcut, restore meaningful prior state. This applies the local [Launching guidance — Best practices](https://developer.apple.com/design/human-interface-guidelines/launching#Best-practices) and its routed procedure's explicit launch-intent precedence.

```text
onShortcut(action):
    persist pendingIntent(actionID, boundTarget, contextGeneration, requestID)
    preserve current unsaved work without submitting or discarding it
    initialize only session, local data, and routing dependencies
    if existing app access gate is required:
        retain intent through the gate
        cancellation leaves data unchanged and clears the pending request
        successful completion resumes resolution, with context revalidation
    resolve pendingIntent:
        add-package   -> existing unsaved add draft, otherwise empty add form
        view-packages -> current package list or empty state
        track-latest  -> validated bound package detail, otherwise fallback list
        unknown       -> current package list, without mutation
    acknowledge request only after destination is presented
    clear completed intent; duplicate requestID does not stack destinations
```

Do not introduce an access gate solely for shortcuts. If an existing required gate interrupts launch, never treat its welcome/authentication screen as completion of Track Latest. Resume the pending intent after completion. If the account changes during that gate, discard the old package target and use the fallback list. A newer explicitly selected shortcut supersedes an older pending request. If the process stops before presentation, retry the pending navigation on resumption and revalidate it; completed requests must not replay.

First usable content is the requested form, list, or detail with local content and working controls. Defer carrier refresh, imagery, analytics, and shortcut re-ranking until they no longer block routing. Do not hold a branded welcome screen while these complete. Any iOS static launch screen should match the initial content structure, appearance, and supported orientation, without unlocalized text; actual matching requires implementation inspection. No startup duration is claimed.

## Worked before / after

**Supplied before:** A person long-presses the app icon and encounters nine actions, mostly account settings, with unlabeled icons. Track latest opens Welcome. In the no-tracking state the menu still advertises a stale package.

**Proposed after, populated state:** Account A has active packages P17 and P23. P17 was last viewed at 10:00 and P23 at 09:00. The menu shows Add Package, View Packages, Track Latest, each with its named monochrome icon. Track Latest binds to P17. Selecting it with the app terminated opens P17's tracking detail after initialization, even if restoration previously pointed to Settings. A carrier update for P23 at 10:05 does not change this destination.

**Proposed after, empty/racing state:** Removing the last active package republishes only Add Package and View Packages. View Packages opens “No packages yet.” If the user selects an old Track Latest reference before replacement takes effect, validation rejects the missing target and opens that empty list with the availability message and Add Package. It never displays the removed package or ends at Welcome.

## Acceptance checks and status

**Passed — document inspection only:** This specification defines at most three app-provided shortcuts, text titles and icon intent, stable and conditional availability, deterministic ranking, bound destinations, account-change invalidation, warm/cold routing, empty and removed-content fallbacks, interruption handling, and a worked transformation. These are specification coverage checks, not execution results.

**Failed — supplied proposal against the revised contract:** The brief's nine actions exceed the local guidance's four-action limit; unlabeled icons omit the specified titles; the generic welcome destination fails Track Latest's task contract; the stale package fails availability validation. These findings are based on the supplied description, not observation of a running app.

**Not executed — implementation acceptance scenarios:**

| Scenario | Required observable result |
| --- | --- |
| Fresh install / no local snapshot / zero active packages | Only the stable pair is published; View Packages reaches the empty list when empty. |
| Multiple active packages | Ranking follows user visits, then added time, then ID; background carrier updates do not reorder the target. |
| Warm and cold selection of each action | Requested destination appears; restored Welcome, Settings, or another detail cannot replace it. |
| Package disappears or becomes ineligible between publication and selection | Fallback list and availability message; no substituted package; dynamic set rebuilt. |
| Sign-out / account switch / old retained shortcut | Old-account content is never displayed; only current-context shortcuts remain after rebuild. |
| Offline launch | Valid cached detail shows last-update time and offline status; routing remains usable without a carrier refresh. |
| Required gate canceled, completed, or interrupted | No mutation on cancel; correct pending destination on completion; account revalidation before content. |
| Process interruption / duplicate callback / second shortcut | Resume safely, avoid duplicate screens, and honor the newer explicit request. |
| Existing unsaved add draft | Preserve and reopen the draft; navigation does not submit or erase it. |
| Long translations, right-to-left text, large text, VoiceOver, light/dark appearance | Titles remain understandable and associated with their actions; glyphs remain legible; destination names and reading behavior are verified on the actual system surface. |
| Launch appearance / supported rotation / ordinary launch | No distracting launch-screen mismatch; ordinary launch restores prior state while shortcut launch preserves its requested target. |

The localization and assistive-technology rows are pending validation conditions, not a completed accessibility review.

## Evidence limits

Read locally, in order: installed apple-hig root procedure; supplied interface; relevant topic-index rows; Menus and actions family, Home Screen quick actions procedure and source guide; Patterns family, Launching procedure and source guide. Package root: `.agents/skills/apple-hig/`. Both consulted source guides label their snapshot 2026-10-25. Official links above identify source sections; they were not browsed.

No application code, deep-link handlers, package dataset, icon assets, screenshots, SDK documentation, device, GUI, or accessibility execution was available or used. No SDK compilation, actual Home Screen ordering, refresh timing, localization fit, launch performance, or VoiceOver behavior is established. The eventual integration must verify platform publication/dispatch capabilities and execute the pending checks. This document supplies a behavioral contract without assuming an Apple SDK is installed or inventing API names.
