# Shared gallery: Apple TV and Vision Pro interaction contracts

Design specification based on `interface.md`, not an implementation or device evaluation. The supplied gallery has 20 objects and details; no code, assets, dimensions, SDK versions, or runtime evidence were supplied. Object IDs below (`01`–`20`) are illustrative stable identities, not invented content names.

## Shared outcome and state

Browse all 20 objects, deliberately open one object's details, then return to the same place. “Select” means activate to inspect details; this brief does not imply multiselect, favorites, or a new saved-selection feature.

Store `galleryOrder`, `originObjectID`, and `galleryScrollAnchor` before opening `Detail(objectID)`. Keep this gallery state while details are open. Merely targeting an object never opens details, changes stored selection, or marks it viewed. If viewed status is later added, derive it from explicit activation, never gaze.

Shared transition: `Gallery → explicit activation(id) → Detail(id) → Back → Gallery(origin id, saved anchor)`. A failed detail load retains the object title, a visible Retry action and Back; Retry loads the same ID. An empty gallery shows “No objects available” with an exit route rather than a phantom focus target. These are product decisions for predictable recovery.

## Contract 1 — Apple TV / tvOS

**Surface and entry.** Use a component-based gallery, not a free cursor. Proposed layout: five columns by four rows in the supplied order, with vertical scrolling if needed. On first entry, focus object 01. Each image and title is a single actionable card. Use standard tvOS focus effects and leave space for focused artwork enlargement without clipping or covering adjacent labels. Final card dimensions require asset/layout validation. Start from tvOS's 66 × 66 pt default control size rather than designing to its 56 × 56 pt minimum. [Focus and selection — tvOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#tvOS), [Accessibility — Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility).

**Directional route.** For row r, column c, Left/Right moves to the preceding/following card in that row; Up/Down moves to the same column of the adjacent row. Boundaries do not wrap. Scroll the newly focused card into view. Every card is reachable: 01 → Right ×4 → 05 → Down ×3 → 20; reverse navigation also works. No hidden controls or pointer precision are needed. Swipes follow the same directions with system scrolling/momentum; clickpad directional presses offer discrete navigation. This route is a proposed layout contract, not a claim about an existing focus engine.

| Input/state | Required result |
|---|---|
| Move remote focus | Change target and its visual emphasis only; remain in Gallery |
| Clickpad Select press on card | Immediate pressed feedback; capture ID/anchor; open that detail |
| Detail entry | Present object heading/content and a labeled Back to Gallery control; initial component focus goes to Back to Gallery |
| Back button or Back to Gallery | Return to parent Gallery; restore scroll anchor and focus to origin ID after layout is ready |
| Back at gallery root | Preserve normal system Home behavior; holding Back also retains system behavior |
| Play/Pause | Do not repurpose for opening details; if media is later introduced, control active media |

Remote meanings follow [Remotes — Best practices and Buttons](https://developer.apple.com/design/human-interface-guidelines/remotes#Best-practices). Back follows hierarchy, not an arbitrary screen history.

**State appearance.** Unfocused cards recede; focused cards use the system raised/highlighted effect; pressed cards give immediate activation feedback. Any future persistent selected state uses a separate indicator that survives focus movement. Unavailable cards remain identifiable but inactive and skipped by directional focus. If the origin disappears while details are open, on explicit return choose the next available card in saved order, otherwise the previous; scroll to it. If none remain, show the empty state. During discrete navigation, removal of the focused card moves to a nearby one-step available target. These fallback choices are product rules applying [Focus and selection — Best practices](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Best-practices).

## Contract 2 — Vision Pro / visionOS

**Surface and entry.** Use an ordinary system-positioned window with a scrollable gallery and in-window detail navigation; this task needs no Full Space, head-locked UI, hand tracking, or custom gesture. Use four columns by five rows as an initial design, letting the window's layout expose fewer columns when needed. Keep the same object order and stable scroll anchor. The column count is a product proposal pending comfort testing, not a HIG requirement.

**Targeting is system hover.** Each image/title pair has one stable containing hit/hover region. Use standard rounded controls and subtle system hover; keep image, label and target bounds stable. Do not expand into neighbors or attach application logic to looking. Pre-tap gaze remains private and system-applied hover is distinct from connected keyboard/controller focus. Use at least 60 × 60 pt activation areas as the starting control size, with at least 16 pt margin around target bounds; verify final geometry at all supported layouts. The local eyes guide also offers at least 60 pt center separation as an alternative; this design chooses the margin rule. [Eyes — Making items easy to see, Encouraging interaction, Custom hover effects](https://developer.apple.com/design/human-interface-guidelines/eyes#Making-items-easy-to-see), [Accessibility — Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility).

| Input/state | Required result |
|---|---|
| Look at card | System hover feedback only; no navigation, stored state change, or dwell-to-open |
| Look and finger-thumb tap with hand resting comfortably | Explicitly activate targeted card; capture origin ID/anchor and open details |
| Standard indirect pinch/hold and drag to scroll | Scroll gallery with immediate visible movement; no card activation from scrolling |
| Activate visible Back to Gallery in details | Return in the same window; restore anchor and reveal originating card |
| Return under eye/hand input | No synthetic focus ring or forced gaze destination; hover follows the system's current target |
| Connected keyboard/controller navigation | Maintain a separate component-focus state; deliberate activation opens details; restore origin focus on return |

Prefer indirect interaction from rest. Direct touch may remain available through standard controls where appropriate, but no action requires reaching, raised arms, two hands, a prescribed hand, or body movement. Back is a visible labeled action rather than a custom wrist gesture; preserve palm/wrist system overlays. [Gestures — visionOS](https://developer.apple.com/design/human-interface-guidelines/gestures#visionOS), [Gestures — Working with system overlays](https://developer.apple.com/design/human-interface-guidelines/gestures#Working-with-system-overlays-in-visionOS).

**Return and disappearance.** Restore content location, not eye focus. If the origin is removed, reveal the next available object in saved order, otherwise the previous, without inventing hover. For keyboard/controller focus, a removed target during discrete navigation uses a nearby one-step target; for other input, hide its obsolete indicator. Empty data uses the shared empty state. Keep details and Back within comfortable view without repeated broad gaze shifts or depth refocusing. Sustained reading should normally be at least 1 m away; rely on system placement and validate actual reading distance/comfort rather than claiming a fixed placement from this document. [Eyes — Best practices](https://developer.apple.com/design/human-interface-guidelines/eyes#Best-practices), [Focus and selection — visionOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#visionOS).

## Decisions across both contracts

- Replace auto-open with explicit activation. TV focus and visionOS hover identify possible targets; neither is a persistent product selection.
- Preserve object identity and scroll position across detail navigation. TV restores component focus; eye/hand Vision Pro restores the content location without manufacturing gaze or focus.
- Expose each card as one named action using its actual object title, role and availability. Expose Back to Gallery and Retry as named controls; provide meaningful descriptions for informative imagery without duplicating titles. Reading/task order follows gallery order, then the detail heading, content and actions.
- Support the entire browse/open/return task through supported assistive input, including Switch Control, and visionOS hand/head Pointer Control. Speech is optional. Connected keyboard/controller focus is a separate path from hover. These are requirements awaiting platform verification.
- Labels and state remain understandable without color or sound. Text enlargement to at least 200% must preserve all content/actions through reflow/scrolling; default text starting points are 29 pt on tvOS and 17 pt on visionOS. Reduce Motion retains targeting/pressed distinctions with restrained static emphasis instead of unnecessary zoom/depth animation. Validate actual contrast in supported appearances, including Increase Contrast. [Accessibility — Vision, Mobility, Cognitive and visionOS](https://developer.apple.com/design/human-interface-guidelines/accessibility).

## Acceptance checks and evidence status

**Passed — document inspection only:** The brief was read. The two contracts preserve 20-object browsing and explicit detail activation; distinguish TV focus, visionOS hover and persistent selection; specify return restoration and removal/empty/error handling; provide remote and resting-hand routes. The finite TV route reaches all 20 proposed positions on paper. These are specification checks, not runtime passes.

**Failed — supplied concept, as described:** Looking opens details without deliberate activation; TV demands pinpoint pointer movement; return loses focus; Vision Pro requires raised arms. Each blocks or degrades the requested task and has a concrete replacement above. No implementation was inspected to confirm runtime defects.

**Not executed — required implementation/device checks:**

| Check | Observable pass criterion | Evidence still needed |
|---|---|---|
| TV browse/activate | Navigate every card and Back control with Siri Remote; focus is visible, never trapped; movement alone never opens details | Built app and actual remote/device recording; keyboard simulation is partial evidence only |
| TV visual feedback | Across-room labels are readable; enlarged focus art clips/obscures nothing; pressed and unavailable states are distinct | Final artwork, measured layout, TV viewing tests |
| TV return/removal | Open 01, 10 and 20, return via both routes; same ID and anchor restore; remove origin and verify fallback; root Back reaches Home | Runtime focus/scroll observations including delayed loading |
| Vision hover/activation | Sweep gaze across all visible cards without navigation or stored changes; deliberate tap opens only intended card; scrolling does not open it | Worn Vision Pro session and state/event inspection; no pre-tap gaze logging |
| Vision return | Open a scrolled-to object; Back restores location; eye input gets no artificial focus; keyboard/controller route restores its own focus | Device observations for each input path |
| Vision comfort/targets | Complete browse/open/return with resting hands; either hand works; targets remain separated and stable; no overlay conflict, repeated broad gaze or tiring reach | Measured geometry plus repeated worn-device comfort/recognition sessions |
| Recovery | Failed load offers usable Retry and Back; removed origin and zero available objects leave no stale target or dead end | Controlled runtime data/error fixtures |
| Accessibility | Complete the same task with platform-supported VoiceOver/Switch Control and visionOS Pointer Control/Zoom; names, order and activation are usable | Apple accessibility execution and Inspector results; supported input/platform matrix |
| Preferences/layout | At 200% text all titles/actions remain available; Reduce Motion preserves meaning; contrast passes measured chosen criteria in supported appearances | Rendered layouts, contrast measurements and preference execution |

No device, SDK compilation, GUI, accessibility, gesture-recognition, or physical-comfort testing was performed. Source support comes solely from the installed local HIG snapshot; official links above are attribution and were not browsed. No claims about newer releases or API availability are made.

## Local guidance audit

Read the installed `apple-hig/SKILL.md`, then `subskills/apple-hig-inputs/SKILL.md`, then the `focus-and-selection`, `eyes`, `remotes`, and `gestures` topic `SKILL.md` files under that family's `.topics/`, before their corresponding `references/*.md` source guides. For assistive alternatives, read `subskills/apple-hig-foundations/SKILL.md`, its `.topics/apple-hig-accessibility/SKILL.md`, then `references/accessibility.md`. Every read used a separate `cat` command, with paths resolved from `/tmp/hig-eval-kpmt1ybf/.agents/skills/apple-hig`. The work used local files only.
