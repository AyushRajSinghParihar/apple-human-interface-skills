# Product brief evaluation and feasible alternative

## Verdict and evidence boundary

The brief in `interface.md` is not supportable as written. Its product intent can be preserved as a native catalog of curated content on tvOS and an optional spatial preview on visionOS. This is a design specification, not an implemented or SDK-validated application. No framework was supplied; framework selection remains open.

Only supplied local material and the installed apple-hig package were used. Official links below identify the articles behind the local guidance; they were not visited. The package is an independent, dated HIG interpretation, not an SDK reference. Its references record retrieval/snapshot dates of 2026-10-25, with differing article revision dates. Neither those dates nor a local file's existence establish API availability or independent review.

| Brief claim | Finding and effect | Decision |
|---|---|---|
| tvOS web view hosts the store | Local Web views guidance explicitly says tvOS web views are unsupported. The proposed hosting surface cannot be promised. | Render curated catalog data as native app content. Do not ship embedded HTML navigation. |
| tvOS WidgetKit widget store | Local Widgets guidance explicitly says widgets are unsupported in tvOS. A catalog card is not a system widget. | Remove tvOS WidgetKit/install/placement promises. Use clearly labeled in-app content previews. |
| Full browser inside the product | Web views guidance discourages recreating a general browser, independently of tvOS's unsupported status. | Bound discovery to catalog → detail → preview. No URL bar, tabs, arbitrary links, or browser history. |
| `AppleImmersionLock.disableDigitalCrown()` forces full immersion | The brief calls this hypothetical; no declaration or SDK evidence is supplied. Crown immersion and system actions belong to the person/system in the local guidance. | Delete the call and lock requirement. Do not substitute another invented API. Preserve system control. |
| A 2019 blog proves support | The post itself, URL, claims, and tested environment are absent. Its date alone cannot prove current support, availability, or deployment eligibility. | Treat as unverified historical context. Require current SDK and deployment evidence before implementation commitments. |

Source basis: [Web views — Best practices and Platform considerations](https://developer.apple.com/design/human-interface-guidelines/web-views), [Widgets — Platform considerations](https://developer.apple.com/design/human-interface-guidelines/widgets), [Digital Crown — Apple Vision Pro](https://developer.apple.com/design/human-interface-guidelines/digital-crown). These are scoped findings from the local snapshot, not claims that every possible implementation technology was exhaustively investigated.

## Concrete replacement contract

Assumption: the useful task is to discover, inspect, and preview curated experiences. The brief supplies no content model, transaction requirements, or installation mechanism. The first version is a read-only catalog with app-owned previews; “store” does not imply purchases, downloaded executable content, or system widget installation. If those are essential business requirements, this alternative needs additional product and technical work before approval.

### tvOS: native catalog and preview

Use a large, legible catalog with a title, category row, and a grid of artwork cards. Each card shows a name and short purpose. Detail shows artwork, description, availability text, and “Open preview.” Example content, explicitly simulated: “Garden scene — A quiet garden preview.” Call these “experiences,” not installable widgets. A preview uses packaged app-owned content and native rendering selected after SDK verification. A static image and description remain the baseline when no richer preview is available.

Navigation contract:

- Catalog opens with focus on the first category. Left/right moves among categories; a deliberate Select applies the category and preserves focus there. Down enters its first card. Left/right traverses cards, up/down traverses rows; Up from the first row returns to the selected category. Edges stop predictably.
- Focus highlights/enlarges a card without opening it; Select opens Detail. Leave room for enlarged art. Distinguish unfocused, focused, pressed, and unavailable appearances. Unavailable entries show explanatory text and offer no inactive action target.
- Detail initially focuses “Open preview”; Select opens Preview. Back returns from Preview to Detail, then to Catalog with category, scroll position, and originating card restored. Back at Catalog retains the system Home behavior, as does holding Back. This hierarchy replaces browser Back/Forward.
- A missing preview leaves Detail readable with “Preview unavailable” and a reachable Back route. A removed originating card restores the nearest remaining card; an empty result focuses the category row.
- No pointer hover, game controller, account, or companion device is necessary for ordinary browsing. No personal data is shown in the baseline shared-TV catalog. Future saved items require an explicit viewer/profile policy.

Content states: initial loading shows a stable catalog shell and “Loading experiences.” Successful load displays cards; empty category says “No experiences in this category.” Failure offers “Try again” reachable from the category row. During refresh retain existing content; on failure label it “Couldn’t update — showing saved catalog,” with its last-updated time. Returning from detail does not reset the catalog. These state choices are product decisions.

Guidance: [Designing for tvOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos), [Focus and selection — tvOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection), [Remotes — Best practices and Gestures](https://developer.apple.com/design/human-interface-guidelines/remotes). Across-room readability and actual focus behavior remain device checks.

### visionOS: window first, optional portal preview

Start in a movable Shared Space window containing the same catalog and detail. Ordinary browsing and reading remain usable without immersion. Do not add a volume merely to make flat catalog information spatial.

Storyboard/state contract:

| State | Visible content and action | Transition and preserved state |
|---|---|---|
| Browsing | Catalog window; selected experience and detail; “Enter spatial preview” only for suitable spatial content | Activation deliberately requests an optional progressive Full Space portal-style preview. Window-only preview remains available. |
| Entering | Brief progress feedback; prevent duplicate entry requests | Success enters Preview. Rejection/failure returns to Detail with “Spatial preview unavailable” and Retry; preserve selected item and catalog position. |
| Preview | Stationary scene with stable ground/reference, restrained peripheral motion, and visible “Return to catalog” | System Crown control remains available. No trapping, automatic re-entry, or app-defined remapping of Crown actions. |
| Returning/interrupted | Return to less immersive catalog context, rather than intentionally quitting the app | Restore selected item, category, scroll position, and any preview progress. If the system suspends/ends the experience, restore that context on next activation; do not promise the window remains visible after a system exit. |

Progressive immersion is a proposed style because a portal preview can retain surroundings while the person varies coverage. Full immersion is not required. If this content has no demonstrated spatial benefit, omit the immersive branch entirely. The scene requires no walking, forced head turns, custom virtual hands, or room sensing. Keep important content in comfortable view, support indirect targeting/activation with hands resting, and use standard labeled controls with equivalent accessible actions. Do not require repeated reach. Exact scene APIs, supported styles, lifecycle behavior, and minimum OS versions remain unverified.

Provide app enter/return controls in addition to retaining system controls. Preserve passthrough, recentering, boundary, and system interruption behavior; never redraw content to defeat them. The local guide describes an approximately 1.5 m boundary for progressive/full immersion; that is source context, not a guaranteed app-controlled radius or measured behavior here.

Guidance: [Designing for visionOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos), [Immersive experiences — Immersion styles, Promoting comfort, and Transitioning between immersive styles](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences), [Digital Crown — Apple Vision Pro](https://developer.apple.com/design/human-interface-guidelines/digital-crown).

## Acceptance checks and current results

“Passed” below means document inspection only. No executable interface was supplied or created.

| Status | Check / acceptance condition | Evidence |
|---|---|---|
| Passed — static | Unsupported tvOS surfaces and hypothetical Crown call are removed from the replacement contract | Replacement uses native catalog content and preserves system agency. |
| Passed — static | Every proposed task has an explicit route, return, state preservation, and unavailable-content behavior | Catalog/detail/preview routes and spatial storyboard above. |
| Passed — static | Ordinary browsing works conceptually without immersion or arbitrary web browsing | Both platform contracts retain a bounded catalog. |
| Failed — brief review | Original brief must use supported platform surfaces and substantiate API claims | tvOS web/widget assumptions conflict with local guidance; hypothetical API and 2019 proof are unsubstantiated. |
| Not executed | Build against selected SDK/deployment targets; verify all chosen types, members, availability, entitlements, scene transitions, and distribution requirements | No SDK or API documentation supplied; no compilation evidence. |
| Not executed | Remote traverses every active control, shows clear focus, activates only deliberately, restores originating card, and exits every screen | Requires actual tvOS implementation and supported remote/device testing. Include empty/error/removal cases and focus enlargement. |
| Not executed | Titles, descriptions, focus art, and error actions remain understandable across the room, including long/localized content | Requires rendered layouts and television viewing; no screenshot or GUI evidence. |
| Not executed | Enter, refuse entry, retry, return, Crown adjustment, Home/system interruption, and resume preserve context without forcing re-entry | Requires visionOS runtime and worn-device verification. |
| Not executed | Portal remains comfortable across postures; resting eye/hand interaction works; surroundings and boundary awareness remain available | Requires worn Vision Pro tests; source reading cannot establish comfort, tracking, or physical behavior. |
| Not executed | Assistive users can discover, understand, activate, and leave all controls; reading order, labels, contrast, text adaptation, and alternative inputs work | Requires implemented semantics and platform accessibility execution, including VoiceOver and relevant alternative input methods. |

## Evidence still required and release decisions

1. Confirm the actual product goal: catalog/preview versus paid acquisition, installation, or distribution of third-party widgets. Supply content schemas, assets, preview behavior, account needs, and data-refresh requirements. If installing tvOS widgets remains mandatory, reject that scope under the supplied guidance rather than relabeling native cards as widgets.
2. Choose minimum tvOS/visionOS versions, devices, framework, SDK/Xcode versions, and distribution route. Supply current official SDK documentation locally and compile a minimal prototype on an appropriate Apple development host. HIG is design evidence, not a guarantee of API signatures or availability.
3. Supply the cited 2019 post and its exact argument if the team wants it assessed. Even then, validate its claims against the chosen current SDK and deployment constraints. Do not infer the hypothetical API is real, or claim an exhaustive proof of its nonexistence.
4. Supply rendered prototypes and device results for the pending checks above, including assistive technology results. No device, SDK, GUI, browser, haptic, or accessibility execution occurred in this evaluation.

Proceed with the revised design contract for prototyping. Hold implementation/release feasibility claims until deployment and SDK evidence is available. The original forced-immersion requirement remains rejected as a design decision even if some future technical mechanism were alleged.

## Installed guidance audit

Explicitly read installed root `.agents/skills/apple-hig/SKILL.md`, then each selected family and topic procedure before its supporting guide. Every read command addressed one file using `cat` or `sed`; no web browsing was used.

All paths below resolve under `.agents/skills/apple-hig/subskills/`:

| Family read (`SKILL.md`) | Topic procedures read (`.topics/<topic>/SKILL.md`) | Supporting guides read (`references/`) |
|---|---|---|
| `apple-hig-content` | `apple-hig-web-views` | `web-views.md` |
| `apple-hig-system-experiences` | `apple-hig-widgets` | `widgets.md` |
| `apple-hig-getting-started` | `apple-hig-designing-for-tvos`, `apple-hig-designing-for-visionos` | `designing-for-tvos.md`, `designing-for-visionos.md` |
| `apple-hig-inputs` | `apple-hig-digital-crown`, `apple-hig-focus-and-selection`, `apple-hig-remotes` | `digital-crown.md`, `focus-and-selection.md`, `remotes.md` |
| `apple-hig-foundations` | `apple-hig-immersive-experiences` | `immersive-experiences.md` |

The platform procedure routed detailed TV movement to Focus and selection/Remotes and Full Space decisions to Immersive experiences. No widget is proposed in the replacement, so widget rendering variants and timeline tests are out of scope. Browser-history tests are likewise out of scope after removing web embedding. Detailed spatial geometry, custom eye targets, and sensing are deferred rather than asserted validated.
