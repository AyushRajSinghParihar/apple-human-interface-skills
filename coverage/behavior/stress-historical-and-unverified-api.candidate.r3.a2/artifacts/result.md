# Product feasibility and interface alternative

The brief is **not supportable as written**. A revised native catalog is a feasible design direction, but implementation feasibility and deployment remain unverified. This assessment uses only `interface.md` and the installed apple-hig instructions and local source guides. Official links below identify the guides’ sources; they were not opened online.

## Findings and decisions

| Brief claim | Evidence and judgment | Decision |
|---|---|---|
| tvOS web view hosts the store | The local Web views guide explicitly says web views are unsupported on tvOS. This is a documented surface limit, not an inference from an omitted platform section. | Replace embedded HTML with native catalog data and native screens. |
| tvOS store uses WidgetKit | The local Widgets guide explicitly says widgets are unsupported in tvOS. WidgetKit is not evidence of an arbitrary widget-hosting marketplace. | Show catalog entries and previews inside the app; do not label these as installed system widgets. No third-party code installation or widget hosting is promised. |
| Full browser within the store | Web views guidance discourages recreating Safari’s general feature set even on supported platforms; the tvOS support limit already blocks this proposed embed. | Bound the app to browsing its catalog and reading native descriptions. Omit address entry, tabs, arbitrary links, and browser history. |
| visionOS portal forces full immersion with `AppleImmersionLock.disableDigitalCrown()` | This identifier is explicitly hypothetical in the brief. No supplied SDK/API documentation establishes its existence or availability. Local visionOS, Crown, and immersion guidance preserves system control and deliberate entry/exit. A portal does not imply permission to disable system controls or require full immersion. | Remove the call and forced-immersion requirement. Start in Shared Space; retain Crown and system escape behavior. |
| A 2019 blog proves support | Only the team’s assertion is supplied, without the article or its claims. It cannot establish current platform support, API contracts, or deployment availability. | Treat the blog as unverified historical context, not shipping evidence. |

Source support: [Web views — platform considerations and best practices](https://developer.apple.com/design/human-interface-guidelines/web-views#Platform-considerations), [Widgets — platform considerations](https://developer.apple.com/design/human-interface-guidelines/widgets#Platform-considerations), [Digital Crown — Apple Vision Pro](https://developer.apple.com/design/human-interface-guidelines/digital-crown#Apple-Vision-Pro), [Immersive experiences — transitions](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences#Transitioning-between-immersive-styles).

These HIG snapshots support experience decisions; they are not SDK references. No replacement API names, minimum OS versions, entitlements, store approval, or framework availability are guaranteed here.

## Concrete alternative

Assumption: the useful task is discovering and previewing a curated collection of glanceable experiences. “Store” is interpreted as a catalog for this first version, because purchasing, installation, account ownership, and distribution requirements are absent. If paid acquisition or actual system-widget installation is essential, this alternative covers discovery only and requires a separately evidenced acquisition design.

### tvOS: native experience catalog

Screen contract:

- **Catalog:** heading “Explore experiences”; a vertically arranged set of large, focusable entries with title, representative image, and short purpose. Example simulated entry: “Daily outlook — preview today’s summary.” Entries are app content, not WidgetKit surfaces.
- **Entry detail:** title, native description, compatibility statement, static preview, and one “Open preview” action. Compatibility is “Not verified” until supported targets are evidenced; never display an “Install on Apple TV” promise.
- **Preview:** native read-only sample content, clearly marked “Sample preview.” It neither executes downloaded widgets nor suggests live data. Back returns to the detail screen.

Focus/navigation map: Catalog Up/Down moves between entries; Select opens the focused entry. Detail begins on “Open preview”; Select opens Preview. Back from Preview returns to its detail; Back from Detail returns to Catalog with the same entry and scroll position; Back at Catalog retains system Home behavior. Holding Back retains system behavior. Focus movement never launches content. Use native focus feedback with space for enlargement; distinguish focus from any persistent selection. No pointer hover is required. These are specified behaviors, not observed remote results.

Loading shows a native loading description; empty catalog says “No experiences available.” A failed load offers “Try again” as the initial focus target; Back still reaches the parent. If refreshing an existing catalog fails, retain the entries with an update-failure message. If a returning entry has disappeared, restore focus to a nearby remaining entry, or the empty-state route. No external URL automatically replaces the TV task; website-only material gets a native summary and a plain reference address, without claiming a browser handoff exists.

This follows [Designing for tvOS — best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos#Best-practices), [Focus and selection — tvOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#tvOS), and [Remotes — best practices](https://developer.apple.com/design/human-interface-guidelines/remotes#Best-practices).

### visionOS: grounded catalog, optional spatial preview

The base release uses a movable standard Shared Space window for Catalog → Detail → Sample preview. Ordinary browsing and reading remain usable there. There is no need to enter a portal to complete discovery. Standard indirect targeting and activation should work with resting hands; no custom Crown mapping or sustained reaching is specified.

A separately gated enhancement can add “Enter spatial preview” on an entry whose content demonstrably benefits from depth. Proposed storyboard: Detail → explicit entry request → optional mixed Full Space portal preview → “Return to catalog” → original Detail. The portal frames the sample while retaining surrounding context; it does not force a fully surrounding environment. If entry is declined, unavailable, or fails, remain on Detail with the native sample available. Save entry ID and route before entry; restore them after return or system interruption. A missing entry returns to Catalog with an explanation.

The preview is stationary and has a stable visual reference. No walking, room sensing, custom hands, or moving camera is required. Crown/system awareness controls remain available throughout; reducing immersion is never treated as an error or a reason to force re-entry. The app supplies its own clear return action as well. Full/progressive immersion is outside this release. The mixed portal enhancement is a design proposal pending SDK evidence, not a guaranteed implementation path; the Shared Space preview is the fallback.

This applies [Designing for visionOS — best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos#Best-practices), [Immersive experiences — immersion styles](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences#Immersion-styles), and [Immersive experiences — transitions](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences#Transitioning-between-immersive-styles).

## Acceptance checks and observed status

**Passed — document inspection only:** read the brief; explicitly read the installed root skill; searched the topic index; read Getting started family and both platform procedures before their source guides; read the Content, System experiences, Inputs, and Foundations families and selected procedures before their supporting guides. Each read used a separate single-file command. The specification removes tvOS web-view/widget hosting, the hypothetical API, and mandatory immersion. Both flows define return and failure behavior.

**Failed — original brief’s support claims:** tvOS embedded web view and widget surface conflict with explicit local guidance; forced Crown lock conflicts with system-agency guidance. The named hypothetical API and blog proof fail evidence sufficiency. These are specification findings, not runtime test failures.

**Not executed — required before implementation acceptance:**

| Check | Acceptance condition |
|---|---|
| SDK and deployment audit/build | Chosen minimum/target OS, devices, SDK/toolchain and every used symbol are documented and compile on supported Apple tooling; no reliance on the hypothetical lock API. |
| TV traversal | Every action is directionally reachable and escapable using Siri Remote; focus does not activate entries; return restores context; enlarged art does not clip. Verify error, empty, refresh, and removed-entry states too. |
| TV viewing | Titles, purpose, focus, and sample labels remain understandable across the intended viewing distance, including around 8 feet or farther as the TV guide describes. |
| Vision transitions | Browsing works without immersion. Explicit entry, rejection/failure, return, and system interruption preserve selection and task context. |
| System control | Crown immersion/Home/recentering and system awareness behavior remain intact on supported hardware; the app never traps or forces re-entry. |
| Physical comfort | Worn-device testing confirms resting-hand activation, stable references, comfortable viewing, and no required walking or sustained reach. |
| Accessibility | Verify meaningful labels, reading/navigation order, activation, and return with supported assistive technologies; standard components alone do not establish accessibility. |
| Data and distribution | Native content delivery, licensing, compatibility labels, and any eventual purchase/install flow match actual supported services and distribution rules. |

No SDK compilation, device, simulator, GUI, network, focus-engine, or accessibility execution is claimed. No runtime checks have passed on the basis of this document.

## Evidence still missing

- Current Apple SDK/API documentation and an installed supported toolchain, including availability and lifecycle rules for the selected visionOS presentation. HIG describes behavior, not a callable API contract.
- Deployment targets, device coverage, framework choice, and build artifacts. Obtain these before committing implementation estimates or availability promises.
- The actual 2019 blog and the precise claim it allegedly supports. Even if supplied, compare it with target-version official evidence before relying on it.
- Product definition of “widget store”: preview, installation, marketplace, or purchase; content format; publisher model; licensing and distribution requirements. No supplied evidence authorizes assuming arbitrary hosted code works.
- Actual catalog content, visual assets, implementation, screens, and content-service failure behavior. The examples here are simulated.
- Device-based remote, spatial comfort, system-control, and assistive-technology results against the acceptance matrix.

Local audit route: `apple-hig/SKILL.md` → `references/topic-index.md`; Getting started → Designing for tvOS and Designing for visionOS; Content → Web views; System experiences → Widgets; Inputs → Digital Crown, Remotes, Focus and selection; Foundations → Immersive experiences. Each selected topic’s source guide was read from that same installed package. The local snapshots are dated 2026-10-25 and remain local guidance, not independently verified current SDK evidence.
