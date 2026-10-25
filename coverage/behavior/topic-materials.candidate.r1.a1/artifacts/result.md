# Revised visionOS weather dashboard interaction specification

## Scope and decisions

The supplied `interface.md` reports strongest opaque panels on every nested card, text directly over busy passthrough, recessed alerts, arbitrary opacity for state, and competition between controls and content. These are brief-level observations; no rendered interface or implementation was supplied.

Assumption: a window-based dashboard in Shared Space, for reading current weather and forecasts, changing the displayed location, and refreshing data. Example controls and weather values below are proposed product details, not observations of an existing implementation. Retain the same data and selection when changing presentation.

| Surface or role | Revised contract | Reason and source |
|---|---|---|
| Window root | Preserve the platform's adaptive window glass. No custom opaque window fill and no manually tuned passthrough opacity. All dashboard text lives within a supporting window/content surface. | visionOS window glass is normally unmodifiable and preserves awareness of surroundings. [Materials: visionOS](https://developer.apple.com/design/human-interface-guidelines/materials#visionOS) |
| Forecast sections | Use regular visionOS content material for meaningful groups, such as current conditions and hourly forecast. Nested rows inherit their section surface; use spacing and semantic separators instead of another panel per row. | Regular material separates sections. Removing redundant nesting is a product decision to reduce competition. [Materials: visionOS](https://developer.apple.com/design/human-interface-guidelines/materials#visionOS) |
| Controls and selection | Put location and Refresh controls in a dedicated, stable control area above the forecast. Use thin visionOS material for custom button/selection emphasis; prefer standard control behavior if the eventual stack provides it. Content cards are not all glass buttons. | Thin emphasizes buttons and selection; functional controls and ordinary content have different roles. [Materials](https://developer.apple.com/design/human-interface-guidelines/materials#visionOS) |
| Foreground emphasis | Reserve thick visionOS material for a dark custom foreground element that must stand distinctly above regular content. Do not apply it automatically to all nested cards or modify native alert material. | Thick distinguishes a dark element above regular material. Thickness is not a substitute for correct depth. [Materials: visionOS](https://developer.apple.com/design/human-interface-guidelines/materials#visionOS) |
| Text and symbols | Ordinary values, headings, and essential status use semantic vibrant `label`; timestamps and explanations use `secondaryLabel`. Reserve `tertiaryLabel` for inactive, low-priority content. No fixed sampled foreground colors. | Foreground roles adapt with the material. [Materials: visionOS](https://developer.apple.com/design/human-interface-guidelines/materials#visionOS) |
| State | Selected location has a persistent selected marker and name. Loading says “Updating…”; stale data says “Last updated …”; failure says “Couldn’t update weather” with Retry. Disabled controls expose disabled semantics and a reason where needed. Never encode any of these solely by opacity or color. | Pair essential distinctions with words or shapes; semantic colors preserve purpose. Exact copy and markers are product decisions. [Color: Inclusive color](https://developer.apple.com/design/human-interface-guidelines/color#Inclusive-color) |

Do not transplant the general regular/clear Liquid Glass distinction or iOS material tiers into visionOS as an assumed API inventory. The local guide's specific visionOS thin/regular/thick roles govern custom components here. Clear glass over rich media and the suggested 35% media dimmer do not address this text dashboard. visionOS has no separate Dark Mode; test changing surroundings and local adaptive appearances instead. [Materials](https://developer.apple.com/design/human-interface-guidelines/materials#visionOS)

## Interaction and state contract

These names describe semantic roles, not SDK classes or shader recipes:

```text
Dashboard = {location, selectedPeriod, cachedForecast, updatedAt,
             request: idle | updating | failed, alert: none | urgentDecision}

render:
  root = adaptiveWindowGlass
  controls = distinct control area; thin material where custom emphasis is needed
  contentSections = regularMaterial
  nestedRows = inherit section material
  foreground = semantic role resolved against actual supporting material
  stateMeaning = explicit text + marker + exposed semantic state

activate Refresh or Retry:
  if request == updating: do not start a duplicate request
  request = updating; keep cached forecast and selection visible
  show "Updating…"; expose Refresh as temporarily unavailable

update succeeds:
  replace forecast for the requested location; update timestamp
  request = idle; remove failure text; restore Refresh

update fails:
  request = failed; preserve cached forecast and its actual timestamp
  show "Couldn’t update weather" and Retry in context
  if no cache exists: show "Weather unavailable" and Retry, never invented values

activate location choice:
  commit location and selected marker only through deliberate activation
  fetch its forecast; never relabel old-location data as the new location
  preserve selected period where applicable
```

A routine refresh failure does not open a modal alert. A weather advisory that needs no immediate decision remains readable content with a severity word, symbol, and Details action. If a future product condition genuinely warrants immediate attention and a decision, use one modal alert at a time. This specification does not invent an urgent weather trigger from the brief. [Alerts: Best practices](https://developer.apple.com/design/human-interface-guidelines/alerts#Best-practices)

For such an alert, Shared Space placement is slightly in front of, and attached to, the parent window; moving the window moves the alert. If Full Space is later supported, center the alert in the wearer's field of view. Do not render it recessed inside a forecast card. Prefer platform alert presentation when available; otherwise preserve these semantics in the renderer. No numerical depth offset is established by the supplied source. [Alerts: visionOS](https://developer.apple.com/design/human-interface-guidelines/alerts#visionOS)

The alert blocks underlying dashboard actions, retains location/period/scroll state, and restores the initiating control on dismissal where it still exists. A proposed informational urgent acknowledgment uses a concise contextual title, useful message, and one “Done” default acknowledgment. A decision alert requires outcome-named actions and a safe cancellation path before implementation; it must not reuse that acknowledgment contract blindly. For cancellable alerts, Cancel and attached-keyboard Escape/Command-Period dismiss without committing. Do not stack repeated alerts; update or queue distinct conditions. These exit and restoration details are product interaction decisions informed by [Alerts: Buttons](https://developer.apple.com/design/human-interface-guidelines/alerts#Buttons).

## Worked before/after

**Before, from the brief:** every nested card is strongly opaque, while some text sits directly over busy passthrough. An alert appears recessed; state depends on arbitrary opacity. A person cannot reliably distinguish controls, status, and forecast hierarchy from those treatments.

**After, proposed example:** the person reads “London · 12°C” on the adaptive window's supported content area. “Hourly” is one regular-material section; its 14:00 and 15:00 rows share that surface. The selected location control has thin-material emphasis and a selected marker. Refresh is visibly separate from the forecast.

They activate Refresh. The dashboard retains the London forecast and says “Updating…”. If the request fails, it shows “Couldn’t update weather”, “Last updated 10:30”, and Retry on the same supporting surface. No panel fades to convey failure, and no routine modal interrupts reading. If an independently justified modal condition occurs, its presentation is in front of the parent, never behind the forecast. Closing it preserves the selected forecast period.

## Acceptance checks and status

**Passed — specification inspection only:** this document maps every supplied defect to a replacement contract; separates controls from content; preserves adaptive root glass; defines explicit states, retained data, and alert placement/exits; uses no SDK dependency or fabricated numerical opacity/depth constant.

**Failed — supplied design description:** repeated strongest opaque cards, unsupported text over busy passthrough, recessed alerts, and opacity-only state conflict with the intended hierarchy above. These are failures reported by the brief, not independently measured rendering failures.

**Not executed — implementation acceptance:**

1. Render bright, dark, colorful, and visually busy surroundings; inspect initial and scrolled compositions. Essential text must remain readable on a supporting material, controls distinguishable, and necessary surroundings visible. Reject a full opaque-window replacement.
2. Inspect the material tree: nested forecast rows inherit regular sections; custom buttons/selection use thin emphasis; thick is reserved for distinct foreground need. No static opacity value carries state meaning.
3. Exercise refresh success, failure, no-cache failure, repeated activation, and location changes. Verify truthful location/timestamp association, no duplicate requests, explicit status, and retained selection.
4. Exercise a justified modal with parent movement, dismissal, repeated triggers, and attached-keyboard actions. Verify front placement, parent attachment, blocked background activation, no stacking, correct outcomes, and restored task state. Test Full Space placement only if that mode is implemented.
5. Repeat with Increase Contrast and Reduce Transparency, separately and together. Honor platform material adaptation; do not override a user-requested reduction in transparency to preserve the default aesthetic. Essential content, state, and actions must survive. Measure actual composited foreground/background contrast with documented calculator inputs; no contrast ratio can be calculated from the brief.
6. Verify reading and actions at at least 200% text enlargement without lost labels or controls. Verify meaningful control names, roles, values, and selected/disabled state with supported keyboard and assistive input, including visionOS Pointer Control and Zoom. Check comfortable target spacing and viewing placement on supported hardware. [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility#visionOS)

## Evidence limits and audit route

Only local files were used; official links identify the articles underlying the installed snapshot and were not browsed. The local source guides report a 2026-10-25 snapshot and are application guidance derived from Apple, not SDK documentation or proof of independent review. No screenshots, rendered colors, source code, SDK, device, GUI, accessibility tools, or runtime results were supplied or executed. Native vibrancy, contrast, alert behavior, physical comfort, and assistive navigation remain unverified. A semantic material token alone cannot reproduce or prove native spatial appearance.

Read from the installed package in this project, one file per shell command: root `apple-hig/SKILL.md`; relevant rows of `references/topic-index.md`; Foundations family → Materials procedure → Materials reference; Color procedure → Color reference; Presentation family → Alerts procedure → Alerts reference; Accessibility procedure → Accessibility reference. Each procedure was read before its source guide. The work is a material and interaction specification for an already specified visionOS interface, not a platform-feasibility or SDK implementation assessment.
