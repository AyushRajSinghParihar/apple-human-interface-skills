# Product brief evaluation and interface alternative

The brief is not supportable as written. A revised interface is supportable as a design proposal, conditional on SDK and deployment verification. This review uses only `interface.md` and the installed apple-hig instructions and references. No web research, SDK compilation, GUI, device, network, or accessibility execution was performed.

## Findings and decisions

| Brief claim | Evidence and effect | Decision |
|---|---|---|
| tvOS web view hosts the store | The local Web views guide explicitly says web views are unsupported on tvOS. This is affirmative guidance, not an inference from an omitted platform section. | Replace the embed with native catalog and detail screens. |
| Full browser inside the store | The same guide discourages recreating a general browser and recommends keeping embedded browsing appropriate to the immediate app task. This is design advice, separate from the tvOS support restriction. | Remove address entry, arbitrary navigation, tabs, and web history. Provide native summaries. |
| WidgetKit widgets on tvOS | The local Widgets guide explicitly says widgets are unsupported in tvOS. HIG is not a WidgetKit API availability reference. | Treat catalog items as app-owned content previews, never as installed or running system widgets on TV. Do not promise a WidgetKit host, arbitrary widget loading, or third-party installation. |
| `AppleImmersionLock.disableDigitalCrown()` forces full immersion | The brief calls the API hypothetical; no declaration or SDK evidence is supplied. Local immersion guidance preserves Digital Crown and system awareness controls. | Reject this dependency and the forced-immersion requirement. No replacement lock API is proposed. |
| A 2019 blog proves support | Neither the blog text nor its URL is supplied. Its date alone establishes neither relevance nor API availability for the requested targets. | Treat it as an unverified historical assertion, with no implementation authority here. |
| Current deployment is feasible | Deployment targets are undecided and SDK/API documentation is absent. | Leave minimum OS, framework availability, entitlements, distribution, and compilation unverified. |

Material guidance: [Web views — platform considerations and best practices](https://developer.apple.com/design/human-interface-guidelines/web-views#Platform-considerations), [Widgets — platform considerations](https://developer.apple.com/design/human-interface-guidelines/widgets#Platform-considerations), and [Immersive experiences — immersion and passthrough](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences#Immersion-and-passthrough). These links identify the official source articles; only their installed local adaptations were read.

## Concrete alternative

Assumption: the underlying task is to discover visual information experiences and preview one before using it. The brief does not establish commerce, account, installation, or cross-device synchronization requirements. The first version is a catalog and preview experience; a purchase or installation store remains outside this proposal until those requirements are defined.

### tvOS: native experience catalog

Use app-owned native screens and a bounded data model: item ID, title, summary, preview asset, supported destination description, and last-updated time. Preview assets are images or app-rendered sample content, not executable widgets or HTML. No framework is mandated by the supplied project.

Example content is simulated: an item titled “Daily overview” shows “Three upcoming events · sample data” with a descriptive image. Label it “Preview,” not “Installed widget.” Do not imply support on a destination until verified.

| State | Visible content and actions | Transition and retained state |
|---|---|---|
| Catalog loading | Catalog title and loading status | Success opens catalog; failure shows explanation and Retry. |
| Catalog ready | Focusable item cards with title and short summary | Select opens item details; retain selected item and catalog position. |
| Empty catalog | “No experiences available” and Retry | Retry reloads without an empty focus trap. |
| Item details | Title, native summary, labeled preview, compatibility status, Preview action | Preview opens app-owned preview; Back restores the selected card. |
| Preview | Sample content, explicit “Sample data” label, Return to details | Return restores item details. Remote Back has the same destination. |
| Refresh/offline | Keep cached content with “Last updated …” and offline status; Retry | Successful refresh replaces content without losing selection. With no cache, show the error state. |
| Removed/unavailable item | “This experience is unavailable” and Return to catalog | Return restores the nearest available catalog item. |

Navigation map: `Catalog → Item details → Preview`; reverse navigation returns one level and preserves context. Browser history is absent because there are no web pages. External URLs are not opened on TV. If external information is needed, show a native summary and a readable destination address for use on another device; do not claim automatic handoff or a companion app exists.

These screen, caching, and navigation choices are product proposals. The source-backed constraint is the exclusion of unsupported TV web/widget surfaces. Avoid rendering fake system widgets with misleading in-app behavior, consistent with [Widgets — best practices](https://developer.apple.com/design/human-interface-guidelines/widgets#Best-practices).

### visionOS: optional spatial preview

Start with the catalog and details in Shared Space. Replace the automatic portal with a deliberate “Enter spatial preview” action and an explanation: “View this experience around you. Return to the catalog at any time.” Use mixed immersion for the initial spatial preview. Stronger immersion is optional and deferred until there is a demonstrated content need and verified platform implementation; the brief supplies neither.

| Event | Required outcome |
|---|---|
| Enter preview | Preserve item ID, catalog position, and preview progress before requesting the transition. Show a pending state that prevents duplicate entry. |
| Entry succeeds | Show stationary content and a visible “Return to catalog” action. No walking through a portal is required. |
| Entry fails or is canceled | Remain in the catalog, preserve selection, explain failure when appropriate, and permit retry. |
| Return to catalog | Leave the immersive presentation and restore selection/progress without quitting the app. |
| System interruption or scene dismissal | Preserve task state; reconcile the displayed screen with actual presentation state when the app resumes. Never immediately force reentry. |
| Digital Crown or system awareness action | Leave system control intact; do not intercept, disable, or promise suppression. |

Keep the initial preview stationary, with central important content and restrained peripheral detail. Do not request room sensing or custom hand replacement for this version. If a custom environment is later introduced, its ground plane, motion, sound, movement expectations, permissions, and comfort require a separate design and device validation.

This follows the preference for grounded browsing, explicit transitions, and preserving work in [Immersive experiences — best practices](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences#Best-practices), [comfort](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences#Promoting-comfort), and [transitions](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences#Transitioning-between-immersive-styles). These are experience requirements, not evidence of specific scene APIs or supported OS versions.

## Acceptance checks and present results

“Passed” below means a static document check only. No runtime result is implied.

| Check | Result now | Release acceptance evidence |
|---|---|---|
| Brief uses supported TV surfaces | **Failed: original brief.** Local references explicitly exclude its web views and widgets. | Revised implementation contains native screens and no TV web/widget dependency. |
| Brief preserves system immersion control | **Failed: original brief.** Its forced lock conflicts with the supplied guidance. | Remove the hypothetical dependency; on-device Crown/system awareness controls remain effective. |
| Alternative has bounded navigation and explicit exits | **Passed: specification inspection.** All defined screens have return/error paths. | Execute Catalog → Details → Preview → Details → Catalog, including failure and removed-item paths; verify restored focus and state. |
| Alternative avoids invented APIs and TV widget promises | **Passed: specification inspection.** No API implementation or installation claim is made. | Inspect implementation and compile against documented APIs for chosen targets. |
| Loading, offline, stale, empty, and failed-entry behavior | **Passed: specified; not executed.** | Exercise each with fixtures and interruptions; stale/sample content must remain visibly labeled. |
| Remote focus, readable TV content, and accessible names/order | **Not executed.** | Test actual TV navigation, viewing distance, focus restoration, VoiceOver labels/order, and noncolor status meaning. |
| Spatial entry/exit, interruptions, passthrough, comfort, and system controls | **Not executed.** | Test on target hardware; confirm stationary use, preserved state, available exit, and normal system behavior. A screenshot cannot establish these results. |
| Build, SDK availability, deployment, and distribution | **Not executed / unresolved.** | Document target OS versions and hardware, verify API declarations/availability and required capabilities, then compile and run. |

Web-page Back/Forward and widget timeline/rendering-family checks are inapplicable to this alternative because it implements neither an embedded browser nor a system widget. They have not been marked as successful tests.

## Evidence still missing

- SDK/API documentation and an installed Apple build environment for the chosen targets. Verify any eventual framework and symbol names there; Linux document review cannot establish Apple compilation or runtime behavior.
- Agreed minimum tvOS/visionOS versions, supported hardware, deployment/distribution requirements, and target-specific capability constraints. The dated local HIG snapshot is not a current SDK compatibility matrix.
- The actual 2019 blog and its claimed evidence, if the team wants that claim audited. It cannot substitute for target-specific official API evidence.
- Product definition: whether items are first-party previews, downloadable content, third-party widgets, or purchases; what “store” means; data sources, rights, authentication, privacy, and any cross-device destination. Third-party hosting and installation remain unproven.
- Real catalog assets, localized/long text, empty/error fixtures, and any existing code. The supplied brief contains no interface screenshots, implementation, or executable prototype.
- Mac-based SDK build results and actual target-device tests for focus, accessibility, lifecycle, system controls, and spatial comfort. No such execution evidence was supplied or produced.

## Local instruction audit

Read the installed root `apple-hig/SKILL.md` explicitly, then these family → topic procedure → source-guide routes under `/tmp/hig-eval-uc3j11i4/.agents/skills/apple-hig/`:

- `subskills/apple-hig-content/SKILL.md` → `.topics/apple-hig-web-views/SKILL.md` → `references/web-views.md` within that family.
- `subskills/apple-hig-system-experiences/SKILL.md` → `.topics/apple-hig-widgets/SKILL.md` → `references/widgets.md` within that family.
- `subskills/apple-hig-foundations/SKILL.md` → `.topics/apple-hig-immersive-experiences/SKILL.md` → `references/immersive-experiences.md` within that family.

Each file was consumed with a separate `cat` command, with procedures read before their supporting source guides. The local references identify snapshots/retrieval dated 2026-10-25 and describe themselves as application guidance derived from Apple sources. Their existence does not establish independent review, SDK support, or runtime verification.
