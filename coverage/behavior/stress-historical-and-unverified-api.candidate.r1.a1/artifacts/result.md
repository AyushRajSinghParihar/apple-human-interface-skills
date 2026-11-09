# Product decision

The brief is not supportable as written. Preserve the apparent product goal—discover content and preview a spatial experience—but replace its platform assumptions. The alternative below is a feasible design direction based on local guidance, not a verified implementation or a deployment commitment. No framework or minimum OS version is selected because the brief supplies neither deployment requirements nor SDK evidence.

## Findings and decisions

| Brief claim | Evidence and effect | Decision |
|---|---|---|
| tvOS embeds a web view and full browser | The installed Web views guide explicitly says web views are unsupported on tvOS. It also discourages recreating a general browser within embedded content; that advice is distinct from the platform restriction. | Replace HTML browsing with native catalog and detail screens. Do not promise an embedded or external browser on Apple TV. |
| tvOS hosts a WidgetKit widget store | The installed Widgets guide explicitly says widgets are unsupported in tvOS. An in-app card is not a system widget. | Offer a content catalog with previews usable inside this app. Remove WidgetKit, system-widget installation, and widget-store claims from the TV scope. |
| visionOS portal calls `AppleImmersionLock.disableDigitalCrown()` | The brief calls this hypothetical; no supplied API documentation supports its existence or availability. HIG describes system-owned Crown controls and retained user control of immersion. | Reject the call and forced-immersion requirement. Do not substitute another guessed API. |
| A 2019 blog proves support | Only an assertion about the blog is supplied, without its text, URL, platform scope, or reproducible sample. It cannot establish current SDK support or override the local platform restrictions. | Treat it as unverified historical context, not implementation evidence. |

These findings use the installed snapshot, not live Apple documentation. Official links below identify the source articles; they were not opened. HIG supports experience decisions, not method signatures, deployment availability, entitlements, distribution eligibility, or SDK compilation.

Source support: [Web views — Best practices and Platform considerations](https://developer.apple.com/design/human-interface-guidelines/web-views#Platform-considerations); [Widgets — Platform considerations](https://developer.apple.com/design/human-interface-guidelines/widgets#Platform-considerations); [Digital Crown — Apple Vision Pro](https://developer.apple.com/design/human-interface-guidelines/digital-crown#Apple-Vision-Pro); [Immersive experiences — Best practices and transitions](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences#Best-practices).

## Concrete interface alternative

Assumption: “store” means discovery, not a confirmed purchase requirement. Initial scope is a free, curated content catalog. If monetization or actual system widgets are essential, product scope must be revisited; this alternative does not fulfill those requirements silently.

### tvOS: native content catalog

Screen contract:

- **Catalog:** title “Explore”, category selection, and native content cards. Each card has a title, preview image, and short content type. Example fixture: “Mountain retreat — Spatial scene”; fixture data is illustrative, not a supplied asset.
- **Detail:** large preview, title, description, supported destinations, and a primary “Preview on TV” action when a TV rendition exists. A spatial-only item instead says “Spatial preview requires Apple Vision Pro”; do not show a nonfunctional launch action.
- **TV preview:** a native image/text rendition with “Return to details”. No arbitrary URLs, HTML execution, downloads of widget extensions, or system-widget installation.

Interaction map: Catalog → select card → Detail → Preview on TV → TV preview. Back from preview returns to that detail; Back from detail restores the selected card and catalog position. Focus and activation are separate: moving focus never launches content. Preserve the selected category and item across loading and return paths. These are proposed application behaviors, not claims that a framework supplies them automatically.

Loading shows a labeled loading state. An empty catalog shows “No content available” and Retry. Fetch failure shows Retry and Back. Refresh preserves available content with “Updated [time]”; stale content is visibly labeled. A missing preview offers Retry or Return to details. Do not imply that catalog items are live WidgetKit widgets. No cross-device transfer is required for this version; any later handoff needs its own supported mechanism and failure contract.

### visionOS: grounded browsing and optional preview

Begin in a Shared Space catalog window, with the same item identity and detail content. The initial detail offers “Open spatial preview”; browsing does not enter immersion. First scope uses a bounded spatial presentation with surroundings visible and no room scanning, virtual hands, or forced movement. “Return to catalog” restores the item and position.

An optional later immersive mode is gated on deployment/API verification and a demonstrated content benefit. Its explicit “Enter immersive preview” action explains the transition before entry. Prefer mixed immersion initially; progressive immersion can be considered when adjustable environmental coverage serves the content. Full immersion is not required for catalog access or completion. This follows the guide’s preference for grounded starting experiences and intentional entry, rather than asserting that full immersion is universally prohibited.

State contract:

| State/event | Result |
|---|---|
| Detail → Open spatial preview | Request supported presentation; retain detail/item state. |
| Presentation unavailable, declined, or fails | Stay in Detail; explain “Spatial preview unavailable”; retain ordinary preview and Retry. |
| Preview → Return to catalog | End preview and restore Detail for the same item. Exit does not quit the app. |
| User changes immersion with system controls | Yield to the system; do not relaunch or force stronger immersion. |
| Interruption or system exit | Preserve item and useful progress; resumption returns to a grounded state with an explicit Resume option. |

The app does not intercept, disable, or remap the Crown. System volume, immersion, recentering, accessibility, and Home behavior remain system-owned. Provide a visible app exit in addition to system controls. Keep interaction stationary and bring content to the viewer. Stronger immersion must preserve boundary awareness; the guide describes an approximately 1.5 m boundary for progressive/full experiences, not a safe walking requirement. Actual system behavior and comfort require device evidence.

Source support: [Immersive experiences — Immersion and passthrough, Promoting comfort, Transitioning between immersive styles](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences); [Digital Crown — Apple Vision Pro](https://developer.apple.com/design/human-interface-guidelines/digital-crown). Native catalog structure, labels, loading policy, and state restoration are design proposals, not quoted HIG mandates.

## Acceptance checks and observed status

**Passed — document inspection only:** the alternative defines catalog/detail/preview transitions, loading/empty/error recovery, task restoration, explicit spatial entry/exit, and a grounded fallback. It removes tvOS web-view/widget dependencies and the hypothetical Crown API. These passes establish specification coverage only.

**Failed — original brief against local guidance:** tvOS web-view support; tvOS system-widget support; preservation of user control in the forced-immersion proposal. The hypothetical method also fails the evidence gate: this is not proof that every conceivable API is absent, but there is no basis to use this one.

**Not executed — implementation acceptance:**

| Check to execute later | Acceptance condition |
|---|---|
| SDK/platform availability review and build | Document exact supported SDK APIs, OS versions, capabilities, and deployment targets; compile both targets without hypothetical or unsupported calls. |
| TV navigation with supported remote | Every card/action is reachable; focus does not activate; Back restores item/category/position; errors have working recovery. |
| Catalog state fixtures | Loading, empty, offline, stale, missing media, long titles, and unsupported destinations show the specified states without dead ends. |
| Spatial entry/failure/exit | Entry is explicit; failure keeps Detail usable; app exit and system exit preserve state; resumption does not force immersion. |
| Vision Pro Crown and boundary behavior | System controls remain available; changing immersion or leaving does not trigger app coercion; boundary/passthrough behavior is preserved. |
| Accessibility and rendering | On target platforms, verify assistive-technology labels/order, focus, readable text, noncolor status, and reachable entry/exit actions with appropriate settings and inputs. |
| Worn-device comfort | Stationary use is practical; content does not demand walking; transitions and peripheral motion are comfortable. |

No device, simulator, SDK, GUI, accessibility, network, or build execution occurred. No native rendering, physical comfort, API availability, or distribution compliance is claimed.

## Evidence still missing

1. Product requirements: whether purchases, third-party widget installation, arbitrary browsing, a portal specifically, or mandatory full immersion are essential. The replacement deliberately narrows those capabilities.
2. Target device/OS matrix, minimum deployment versions, existing stack, distribution plan, and supported input/accessibility requirements.
3. Apple SDK and matching API documentation with availability annotations, followed by a compiled minimal prototype. Current support cannot be guaranteed from remembered framework details or this HIG snapshot.
4. The cited 2019 article and its exact claim, plus current authoritative corroboration if the team continues to rely on it.
5. Real catalog data/assets, content-service contract, freshness needs, account/privacy needs, and any purchase requirements. Authentication and commerce flows are outside the supplied brief.
6. Target-device navigation, accessibility, system-control, interruption, spatial boundary, and comfort results against the checks above.

## Local reading audit

All paths below resolve under `/tmp/hig-eval-6gx568lr/.agents/skills/apple-hig/`. Each file was explicitly read with a separate single-file command. Root was read before routing; selected family and topic procedures were read before their supporting guides.

- Root: `SKILL.md`; supplied project brief: `/tmp/hig-eval-6gx568lr/interface.md`.
- Content: `subskills/apple-hig-content/SKILL.md` → `.topics/apple-hig-web-views/SKILL.md` → `references/web-views.md` (topic/reference paths relative to that family).
- System experiences: `subskills/apple-hig-system-experiences/SKILL.md` → `.topics/apple-hig-widgets/SKILL.md` → `references/widgets.md`.
- Exact-term routing: searched `references/topic-index.md` for immersion, vision, web, widgets, and Digital Crown.
- Foundations: `subskills/apple-hig-foundations/SKILL.md` → `.topics/apple-hig-immersive-experiences/SKILL.md` → `references/immersive-experiences.md`.
- Inputs: `subskills/apple-hig-inputs/SKILL.md` → `.topics/apple-hig-digital-crown/SKILL.md` → `references/digital-crown.md`.
- Also read `subskills/apple-hig-technologies/SKILL.md` to assess integration routing; no SDK-backed integration was selected and no technology-specific API claim was made.

No web browsing or external source retrieval was used.
