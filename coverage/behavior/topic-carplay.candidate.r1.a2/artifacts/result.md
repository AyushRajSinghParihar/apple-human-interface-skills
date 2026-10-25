# CarPlay fuel-stop finder: distraction audit

Decision: revise the driving flow before release. Make finding and selecting a fuel stop the primary task; remove enrollment, general account configuration, full-address typing, and promotional animation from that path. CarPlay eligibility remains an unresolved release gate. These are specification decisions, not implemented or device-validated behavior.

## Evidence and routing

The complete supplied interface evidence is `interface.md`, line 1: CarPlay; drivers are asked to type a full address; an animated promotional map is shown; every iPhone account setting is exposed; six loyalty-enrollment steps precede route selection; product category eligibility is not established. No screens, code, control inventory, timing, or actual vehicle behavior were supplied.

Read the installed `apple-hig/SKILL.md`, searched its `references/topic-index.md`, then read the owning families and topic procedures before their source guides. Routes used:

- Technologies → CarPlay and Maps.
- Patterns → Managing accounts and Settings.
- Selection and input → Text fields.
- Foundations → Motion and Writing.

The Getting started family was also inspected: it has no separate CarPlay platform procedure; the dedicated CarPlay procedure supplies the driving model. All paths were resolved under `.agents/skills/apple-hig/`. Official links below identify the local guides' sources; no web pages were fetched.

## Ranked verified findings

Ranking is reviewer judgment based on task obstruction and likely attention demand, not measured crash risk. Findings are verified against the written brief only.

| Rank | Observed problem and effect | Source-backed rule | Correction and decision |
|---|---|---|---|
| 1 — High | Six-step loyalty enrollment is required before route selection. It forces an extended secondary task before the driving task can finish. | CarPlay calls for quick, minimal interactions and phone-dependent setup before driving. Accounts should be required only for essential core functionality. | Remove enrollment from route selection. Offer fuel finding without loyalty membership. Perform optional enrollment on the phone before driving or later when stopped. The brief establishes no essential account dependency; do not invent one. [CarPlay: iPhone interactions](https://developer.apple.com/design/human-interface-guidelines/carplay#iPhone-interactions), [Managing accounts](https://developer.apple.com/design/human-interface-guidelines/managing-accounts#Best-practices). |
| 2 — High | Asking drivers to type a full address creates lengthy manual input and visual checking. | CarPlay prioritizes minimal interactions. The generic text-field guide does not establish a CarPlay keyboard prohibition. | Replace address entry in the driving flow with nearby fuel-stop choices and previously prepared destinations where available. No phone-entry fallback while driving. This is a conservative product decision, not a claim that all CarPlay text entry is forbidden. [CarPlay](https://developer.apple.com/design/human-interface-guidelines/carplay), [Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields). |
| 3 — High | An animated promotional map competes with locating a fuel stop. Animation is verified; looping, duration, flashing, and gesture interference are unknown. | Motion should support the task; CarPlay content should be high-value and scannable. | Remove promotional animation and promotional overlays from the driving surface. Keep only task-relevant geographic context if the eligible template supports it. Retain system-owned task transitions without adding decorative delays. [Motion](https://developer.apple.com/design/human-interface-guidelines/motion#Best-practices), [CarPlay: Layout](https://developer.apple.com/design/human-interface-guidelines/carplay#Layout). |
| 4 — Medium | Every iPhone account setting is exposed. This imports non-driving decisions and expands the available interaction surface. Individual setting defects cannot be established without an inventory. | Keep settings small and distinguish task-local choices from infrequent account configuration; adapt to the minimal CarPlay driving task. | Keep account management on the phone for use before driving or when stopped. Expose only justified fuel-task choices in CarPlay, after an option-by-option review. Do not remove account management from the phone product. [Settings](https://developer.apple.com/design/human-interface-guidelines/settings#General-settings), [CarPlay](https://developer.apple.com/design/human-interface-guidelines/carplay). |

Separate gate: eligibility is explicitly unestablished, not disproved. Product/platform owners must establish the supported app category, required authorization, category-appropriate system templates, and permitted route-selection or handoff behavior before implementation or release. A fuel-related product name alone proves none of these. Do not fabricate an arbitrary car interface or assume that a finder may render turn-by-turn navigation. [CarPlay](https://developer.apple.com/design/human-interface-guidelines/carplay).

## Corrected behavior contract

This framework-agnostic model is conditional on eligibility and supported templates. Template selection and APIs remain unresolved. Generic Maps guidance does not authorize arbitrary map gestures or place cards in CarPlay; the category's system-template constraints govern. No SDK is assumed.

```text
Before release:
  require verified category, authorization, template and routing/handoff support

On CarPlay entry:
  restore useful prior selection if still valid
  never launch enrollment, general account settings, or address typing
  never start promotional animation
  request fuel results using already available context
  if context unavailable: show prepared choices if usable
  otherwise: explain unavailability in CarPlay; offer Retry and Back

Results:
  show concise station identity and relevant available location/distance data
  distinguish unknown data; do not invent prices, opening hours or route accuracy
  use category-appropriate system selection surface
  keep primary action prominent, generally toward the upper half
  selecting a station -> SelectedStop

SelectedStop:
  show station identity and available route summary
  primary action = "Start route" only when supported and actually starts routing
  otherwise use a truthful supported handoff label, such as "Open in Maps"
  Back -> Results, preserving prior selection and useful result context

Route request:
  preserve selected station while pending; suppress duplicate activation
  success -> actual supported routing/handoff outcome
  failure -> concise in-CarPlay explanation, Retry and Back
  canceled request -> SelectedStop; ignore late responses from canceled requests

Account expires or optional loyalty fails:
  continue basic fuel finding where possible
  never block waiting for phone login
  defer phone-only repair until stopped; keep Back available

Disconnect/reconnect:
  retain useful selection, revalidate availability, never auto-start a route
```

Nearby context and prepared choices are proposed inputs, not proven capabilities. Their data access and availability require implementation evidence. No new permission prompt or phone setup is required to complete a driving interaction; if no usable context exists, provide an honest unavailable state rather than redirecting the driver to the phone. Necessary errors stay in CarPlay. Example network failure: “Fuel stops unavailable. Try again.” Actions: “Retry”, “Back”. If phone-only setup is genuinely necessary: “Setup is needed. Complete it on iPhone when stopped.” Do not offer a driving-time phone continuation. [CarPlay: Error handling](https://developer.apple.com/design/human-interface-guidelines/carplay#Error-handling), [Writing](https://developer.apple.com/design/human-interface-guidelines/writing#Best-practices).

## Worked before/after

Scenario: a driver wants a nearby fuel stop and has not joined the loyalty program.

**Before, as supplied:** full-address typing, an animated promotional map, and the complete account-settings surface are present; six enrollment steps must precede route selection. The brief does not establish the ordering of the other surfaces, so no exact total interaction count is claimed.

**After, illustrative:** entry displays available nearby choices without enrollment. The driver selects “Station A”; its selected-stop view identifies the destination and offers the supported route action. The driver activates that action and routing or the verified handoff begins. Two selections from loaded results are a proposed design path, not an Apple-mandated limit or measured performance. Station A is fictitious. Back returns to the same results. A routing failure preserves Station A and offers Retry or Back. Declining loyalty never changes this path.

## Acceptance checks and current status

| Check | Supplied prototype evidence | Corrected contract / execution status |
|---|---|---|
| Reach route selection without loyalty enrollment | **Failed**, six required steps stated | Contract passes static review; implementation not executed |
| Complete ordinary fuel finding without full-address typing | **Failed**, driver typing requested | Contract passes static review; data availability and operation untested |
| Driving view excludes promotional animation | **Failed**, animated promotion stated | Contract passes static review; rendering untested |
| Driving view limits options to fuel task | **Failed**, all account settings exposed | Contract passes static review; detailed settings inventory still needed |
| Eligible category and supported templates/routing established | **Not established**, explicit evidence gap | Release gate remains open |
| Locked/inaccessible phone; expired account; missing context | No evidence | Not executed: basic task must remain independent of phone interaction; necessary failure stays in CarPlay |
| Empty results, network failure, route failure, Retry, Back, cancellation | No evidence | Not executed: preserve selection, discard stale responses, provide usable exits and no phone demand |
| Reconnect restores useful state without starting a route | No evidence | Not executed |
| Real controls, focus, readability and template rendering | No evidence | Not executed: verify touch and available rotary/controller input, supported displays, sunlight/night and automatic appearance |
| Motion accommodations and assistive access | No evidence | Not executed: task information and completion must survive reduced motion; inspect semantics and perform supported accessibility testing |

Static audit checks **passed**: each ranked finding traces to an explicit brief statement; proposed corrections have local source support; the contract covers success, failure, cancellation and deferred setup. These passes do not certify the prototype or a future implementation.

## Evidence limits

Only the supplied one-line specification and installed guidance were reviewed. Local guides are derived HIG snapshots dated 2026-10-25, not SDK references or proof of current authorization. There was no web, SDK, build, simulator, GUI, vehicle, audio, accessibility, or user-testing execution. No measured glance time, target size, contrast ratio, distraction reduction, or safety compliance is claimed. Missing labels, deletion controls, map attribution, focus order, audio interference, and unavailable keyboard behavior are inspection questions, not verified defects. Audio-specific CarPlay checks are pending only if the eventual product introduces audio. Approval of this design specification does not close the eligibility gate or establish driving usability.
