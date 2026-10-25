# Product feasibility and interface alternative

## Verdict

The brief in `interface.md` is **not supportable as written**. A native catalog is a feasible design direction; implementation feasibility and deployment remain conditional on SDK validation. This is a specification and local-source review, not a built or tested app.

| Brief requirement | Evidence and decision | Concrete replacement |
|---|---|---|
| tvOS web view | The installed Web views guide explicitly says tvOS web views are unsupported. Reject this dependency. | Native catalog and native item details populated from structured content. |
| Full browser on tvOS | The proposed host is unsupported; the Web views guide also discourages recreating a general browser within an app. This does not establish the status of every possible browser technology. | Bound the TV task to discovery and preview. No URL bar, arbitrary navigation, tabs, or browser history. |
| WidgetKit widget store on tvOS | The installed Widgets guide explicitly says widgets are unsupported on tvOS. WidgetKit branding does not establish a TV installation/hosting API. | A catalog of previews, with destination-platform labels; TV cards are app content, not system widgets. No TV “Install widget” action. |
| visionOS portal forces full immersion | The platform supports chosen spatial experiences, but guidance preserves user control over immersion and system Crown behavior. Forced immersion conflicts with that model. | Window-first browsing; optional portal preview with deliberate entry and return. |
| `AppleImmersionLock.disableDigitalCrown()` | The brief calls this hypothetical. No SDK or API documentation establishes its existence, signature, availability, or permission model. Reject it as an engineering dependency; do not substitute another remembered API. | Leave Crown behavior to the system. No lock, interception, or automatic re-entry to counteract the user's choice. |
| 2019 blog proves support | No blog contents or URL were supplied. Its claims cannot be inspected; its date alone does not establish current support. | Require official SDK documentation and a minimal compiled experiment for the selected deployment targets. |

Support limits above come from the supplied local snapshot: [Web views — Platform considerations](https://developer.apple.com/design/human-interface-guidelines/web-views#Platform-considerations) and [Widgets — Platform considerations](https://developer.apple.com/design/human-interface-guidelines/widgets#Platform-considerations). Crown and immersion decisions follow [Digital Crown — Apple Vision Pro](https://developer.apple.com/design/human-interface-guidelines/digital-crown#Apple-Vision-Pro) and [Immersive experiences](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences). These links identify the snapshot's official sources; they were not opened or verified online.

## Alternative: discover and preview, then configure on a supported destination

Assumption: the useful product task is discovering widget designs and previewing a spatial experience. Preserve that task, while removing unsupported hosting and coercive immersion. If actual purchase, distribution, or installation is essential, that is an unresolved product and platform workstream, not functionality delivered by this proposal. Initial scope is a read-only catalog without checkout or installation.

### Apple TV

Use a native full-screen catalog titled “Explore designs.” Present a short vertical list of categories, followed by a grid of large labeled previews for the chosen category. An item detail screen shows its title, preview image, concise description, supported destination labels, and an explicit “Preview only on Apple TV” explanation. Example content is simulated: “Daily overview — sample calendar and weather.” Never imply that sample values are live data.

Navigation contract:

1. Initial focus lands on the first category. Up/down moves between categories; a deliberate Select opens that category's grid.
2. Grid directions move among adjacent items. Movement changes focus only; Select opens details. At an edge, focus stays on the current item rather than wrapping unexpectedly.
3. Back from details returns to the same category and item; Back from the grid returns to its category; Back from the root retains system Home behavior. Holding Back retains system behavior.
4. Focus uses the platform treatment with room for enlargement. Press feedback is distinct from focus. This read-only release has no persistent selection badge to confuse with focus.
5. A content refresh preserves category and item identifiers. If the focused item is removed during directional navigation, choose a nearby item; if the category becomes empty, show “No designs available” and retain a parent return route.

Loading shows a labeled loading state. A failed initial load offers Retry; an empty catalog explains that there are no designs yet. If cached content exists, retain it with “Saved catalog — may be outdated” while refreshing. Retry returns to the same route. Item details are native text and imagery, not embedded HTML.

These choices follow [Designing for tvOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos#Best-practices), [Focus and selection — tvOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#tvOS), and [Remotes — Best practices](https://developer.apple.com/design/human-interface-guidelines/remotes#Best-practices). Across-room legibility and actual focus behavior remain untested.

### Apple Vision Pro

| Activity | Presentation | Reason |
|---|---|---|
| Browse, read details, compare designs | Movable standard window in Shared Space | Contained information does not require immersion. |
| Ordinary preview | Image/content inside the detail window | Provides a useful baseline without changing surroundings. |
| Optional spatial demonstration | Explicitly entered portal preview, conditional on SDK validation | A separate moment to demonstrate spatial content; not required for browsing. |

The detail window offers “Enter spatial preview” only for an item with a validated spatial asset and supported implementation. Otherwise it offers the ordinary preview with “Spatial preview unavailable.” The baseline catalog remains useful if immersive support is deferred entirely.

State contract: `Catalog → Item detail → Entering preview → Preview → Returning → Item detail`. Preserve item ID, category, scroll position, and any preview settings across this cycle. Do not open duplicate previews during entry. On entry failure or cancellation, remain at details with a concise explanation and Retry. “Return to catalog” leaves the preview and restores the originating item detail; it does not quit the app. System interruption never triggers automatic forced re-entry.

If implemented, use a progressive portal-style experience that leaves the person control over coverage. This is a design choice, not a verified API mapping. Full immersion is not an acceptance requirement. Keep key content and return controls centrally visible, provide a stable ground/reference, and let a stationary person use indirect targeting and activation with resting hands. Do not require walking, repeated reaching, custom hand replacement, room sensing, or Crown input interception. Transitions should be smooth and predictable. Crown adjustment and system exit remain available independently of the app's return control.

The window-first decision follows [Designing for visionOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos#Best-practices). Optional entry, state-preserving return, stationary interaction, and user-controlled coverage follow [Immersive experiences — Best practices](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences#Best-practices), [Promoting comfort](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences#Promoting-comfort), and [Transitioning between immersive styles](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences#Transitioning-between-immersive-styles).

## Acceptance checks and current results

**Passed — document/source inspection only:** Read the installed root skill, Getting started family and both platform procedures before platform guides. Searched the complete topic index for platform, web, widgets, portal, immersion, and Crown concepts. Read Content/Web views, System experiences/Widgets, Inputs/Digital Crown, Remotes, Focus and selection, and Foundations/Immersive experiences family/topic routes before their corresponding guides. The alternative removes the unsupported TV surfaces and hypothetical API, provides entry/return states, and preserves the catalog task.

**Failed — brief feasibility checks:** The original brief requires tvOS web views and widgets despite explicit local support exclusions. Its forced immersion removes documented user agency. Its evidence does not establish an implementable API or deployment contract. These are brief findings, not observed runtime failures.

**Not executed — implementation acceptance:**

- On Apple TV, traverse every category, item, Retry, and return route using Siri Remote. Focus must remain visible, never activate merely on movement, and never become trapped. Check enlarged items do not obscure labels and titles remain legible across the room.
- Load, fail, retry, refresh, empty a category, and remove the focused item. Confirm understandable states and restoration of the intended route.
- On Vision Pro, browse without immersion, enter/cancel/fail entry, return, and interrupt the preview. Confirm the same item and context survive and no forced re-entry occurs.
- On worn hardware, exercise Crown immersion/system actions and boundary behavior. The app must not suppress them. Check resting-hand use, seated/standing comfort, stable reference, and transitions.
- Validate reading order, control names, alternative activation, text scaling, and assistive navigation on supported platforms. No accessibility execution is established by this specification.
- Compile and run a minimal native catalog and optional portal against the chosen SDKs and minimum OS versions. Verify exact supported APIs, availability guards, scene lifecycle, and failure handling before accepting the spatial implementation.

## Evidence still needed

Choose target OS versions, hardware, implementation framework, and deployment channel. Obtain official SDK/API documentation and a suitable Apple build environment; none is supplied here. Verify scene/portal support and lifecycle instead of treating HIG terminology as API signatures. Supply the 2019 blog if its claims need an audit. Define the catalog content schema, asset rights, backend/error behavior, and whether distribution, purchases, accounts, or cross-device configuration are required. A real WidgetKit product on another platform needs its own surface/family, freshness, configuration, and availability review; this proposal does not promise it.

All conclusions use `interface.md` and the installed independent English HIG snapshot dated 2026-10-25. Local source presence does not establish independent source review or current SDK availability. No web browsing, SDK compilation, GUI, simulator, device, or accessibility execution was performed.
