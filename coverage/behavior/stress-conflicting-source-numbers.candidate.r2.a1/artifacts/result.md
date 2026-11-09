# Qualified specification and decisions

The iPad proposal needs revision: 28×28 pt is the accessibility table’s minimum, not Apple’s default. Specify at least 44×44 pt activation regions for this footer. Withhold the Mac accented-rendering promise: the local widget support table excludes it, while prose mentions Mac group tinting. That source conflict remains unresolved.

This is a design review and replacement specification based on `interface.md` and the installed local HIG package. No rendered app, implementation, screenshots, deployment target, or SDK evidence was supplied. Official links below identify the sources represented by the local snapshot; they were not opened or verified online.

## iPad footer action

**Source interpretation.** The accessibility Mobility table lists iOS/iPadOS default controls as 44×44 pt and minimum controls as 28×28 pt. Buttons recommends general hit regions of at least 44×44 pt and enough surrounding space for easy selection. The minimum and recommended/default sizes describe different levels of guidance; the smaller value does not authorize calling a dense custom control the default. Neither value alone proves accessibility or comfort. [Accessibility — Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility), [Buttons — Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices).

**Replacement contract.**

- Retain the footer action, but give each actual activation region a width and height of at least 44 pt. A visible glyph may remain 28×28 pt if legible; visual size and hit geometry are separate.
- Replace the 2 pt gap with a provisional 12 pt clear gap between activation-region edges. This is a project design choice for separation, not an Apple universal spacing minimum. The accessibility source suggests around 12 pt padding for bezelled elements and 24 pt outside visible edges for elements without a bezel; those qualified suggestions are not interchangeable with a mandated inter-target gap. Determine bezel treatment and review spacing in context before sign-off.
- Expand the footer or reflow actions if needed. Do not enlarge hit regions into neighboring targets. For example, two centered 44 pt regions around existing 28 pt controls whose edges are 2 pt apart would overlap by 14 pt; invisible padding alone cannot repair that arrangement.
- Prefer an appropriate system button style in the existing framework. If the control remains custom, supply perceivable press feedback and correct enabled/disabled and focus behavior. Use a short outcome-specific label, or a familiar symbol with an accessible action name. Do not assign primary/default or destructive status without knowing the action’s consequence. [Buttons — Style, Content and Role](https://developer.apple.com/design/human-interface-guidelines/buttons).
- Normal activation invokes the named action once. If completion is delayed, show activity in the activating button, preserve context, and prevent duplicate submission while pending; on completion expose the actual success or failure. This pending branch applies only if the product action requires it. [Buttons — iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS).

**Still missing:** actual label/symbol, outcome, affected object, reversibility, number of neighboring actions, bezel treatment, footer dimensions and supported iPad layouts/input methods. These determine final semantics, emphasis, recovery and spacing. The proposed size does not settle those decisions.

## Mac widget

**Source interpretation.** The Appearances table lists Mac full-color for Desktop and Notification Center, vibrant for Desktop, and accented as “Not supported.” The Accented section records conflicting prose about Mac group tinting. Use the explicit platform table as the conservative planning boundary, without claiming it conclusively establishes current SDK capability. “No additional macOS rules” does not resolve the contradiction or establish support. [Widgets — Appearances](https://developer.apple.com/design/human-interface-guidelines/widgets#Appearances), [Rendering modes](https://developer.apple.com/design/human-interface-guidelines/widgets#Rendering-modes).

**Replacement contract.**

- Scope the provisional design to a system-small Mac desktop widget, with Notification Center as a second context only if required. This is the smallest locally documented supported family; confirm it fits the actual useful glance before production. Do not invent an app purpose from the rendering proposal. [Widgets — System family widgets](https://developer.apple.com/design/human-interface-guidelines/widgets#System-family-widgets).
- Replace “promises accented rendering on Mac” with: “Design for full-color light/dark on Mac Desktop and Notification Center where offered; provide a meaningful vibrant desktop presentation. Mac accented rendering is uncommitted pending support verification.” These are context-dependent treatments, not a promise that users can select every mode everywhere.
- Preserve the main fact, label and state without relying on accent color. In vibrant mode use grayscale brightness for emphasis, checking actual contrast; varying white opacity alone is not a substitute. Do not describe a monochrome screenshot as proof of the accented rendering mode. [Widgets — Vibrant](https://developer.apple.com/design/human-interface-guidelines/widgets#Vibrant).
- Provisional content contract: one useful changing fact with its context label; include age when freshness affects interpretation. Ordinary activation opens the corresponding app content. No in-place controls are proposed until a focused action is identified. Keep last known useful data visible during refresh, distinguish stale/unavailable data, and explain sign-in if required. Refresh is system-controlled, not continuous. Preview data must be realistic and marked simulated when applicable. [Widgets — Best practices](https://developer.apple.com/design/human-interface-guidelines/widgets#Best-practices), [Previews and placeholders](https://developer.apple.com/design/human-interface-guidelines/widgets#Previews-and-placeholders).

**Still missing:** widget purpose and data, required family/surface, supported macOS releases, framework/SDK, configuration/authentication needs, sensitivity policy, update cadence/stale threshold, destination and realistic example data. The content contract is provisional until those are supplied.

## Acceptance checks and evidence status

| Check | Current status | Required evidence / acceptance condition |
|---|---|---|
| Local instruction and source routing | Passed, document inspection | Installed root → Menus and actions / Foundations / System experiences → Buttons / Accessibility / Widgets topic procedures → their respective source guides were explicitly read, in that order per route. |
| Claim that 28×28 pt is the iPad default | Failed, supplied proposal | Corrected here to 44×44 pt default/recommended target; 28×28 pt remains identified only as the table minimum. |
| Current iPad geometry against replacement spec | Failed at specification level | Supplied 28×28 pt regions and 2 pt gap do not meet this replacement contract. No runtime geometry was measured. |
| Revised iPad hit geometry and separation | Not executed | Layout/runtime measurements show ≥44×44 pt regions, provisional ≥12 pt clear gaps, no overlap, and correct activation at target edges across supported layouts. Reassess separation for actual bezel/context and physical use. |
| Button behavior and accessibility | Not executed | Verify named outcome, press feedback, disabled/pending behavior as applicable, no duplicate commit, appropriate recovery, and no unintended keyboard/default activation. On supported Apple environments verify accessible name/role/state, focus order and activation with VoiceOver, Full Keyboard Access, Switch Control and relevant pointer/assistive input. |
| Text and footer adaptation | Not executed | Long/localized labels and at least 200% text enlargement preserve essential labels/actions without clipping or overlapping targets; verify light/dark contrast with measured colors and Increase Contrast treatment where needed. [Accessibility — Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). |
| Unqualified Mac accented support promise | Failed, supplied proposal | Removed here. Restore only after resolving official support for the precise OS, SDK, family and surface; the conflicting local sentence is insufficient. |
| Mac rendering and content | Not executed | On target macOS inspect full-color light/dark and desktop vibrant, confirming meaningful hierarchy without color/background dependence, readable long text and edge values, accurate previews, correct deep links and honest stale/auth/unavailable states. Verify supported accessibility settings and assistive access to content/actions. |
| SDK availability/build and system mode selection | Not executed | Check current official HIG, WidgetKit/SDK documentation, availability declarations and release notes for the selected deployment range; compile and exercise a minimal widget on the target Mac contexts. Record OS/SDK versions and observed rendering mode. SDK symbol presence alone does not prove a particular surface offers it. |

## Verification boundary

The local guides are derived guidance dated/retrieved 2026-10-25, not an SDK reference or independently verified current Apple documentation. The Mac contradiction needs current official-source and target-system evidence; no online check was performed because this task is local-only. The iPad minimum/default distinction is supported locally, while current wording, actual target geometry, spacing comfort, native rendering and accessibility behavior still need confirmation. No device, simulator, GUI, SDK compilation, Accessibility Inspector or assistive-technology execution is claimed.

Local source files used, relative to `.agents/skills/apple-hig/`: `subskills/apple-hig-menus-and-actions/references/buttons.md`, `subskills/apple-hig-foundations/references/accessibility.md`, and `subskills/apple-hig-system-experiences/references/widgets.md`, after their installed family and topic procedures.
