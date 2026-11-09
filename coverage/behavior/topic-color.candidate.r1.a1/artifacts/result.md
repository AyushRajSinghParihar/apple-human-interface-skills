# Transit disruption dashboard: revised interaction specification

## Scope and evidence

Design specification for iOS/macOS, independent of framework or Apple SDK. The task is to identify a route’s service status, select it, and read its disruption details across appearances. `interface.md` supplies only a prose description: white backgrounds, light gray body text, red/green dots as the sole status signal, and slightly darker red for selection. It supplies no exact colors, implementation, screenshots, route data, or control behavior.

Confirmed barriers in that description: status disappears without color discrimination; selection and disruption share a red encoding. Light gray body text is a contrast concern, not a measured failure. The route names and messages below are illustrative, not supplied service data.

## Decisions and source basis

1. Assign color by purpose: surface hierarchy, primary/secondary text, interaction, selection, and service status have separate tokens. Do not use separator colors for body text. Prefer a platform semantic resolver where available; otherwise use the explicit custom fallback below. Never copy numeric system swatches as production constants. [Color — System colors](https://developer.apple.com/design/human-interface-guidelines/color#System-colors).
2. Keep disruption red and normal service green as supplementary cues, with a persistent status phrase and distinct symbol. Unknown service is neutral and explicitly named. Status is information, not an error action or a link. No colored whole-row fill for disruption. [Color — Inclusive color](https://developer.apple.com/design/human-interface-guidelines/color#Inclusive-color), [Accessibility — Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision).
3. Make selection independent of service status: selection background plus a neutral leading rule and the word “Selected.” Reserve a separate focus outline for keyboard focus. On macOS, honor the user’s accent for interactive focus and appropriate platform selection styling; never recolor service status to match the accent. [Color — macOS](https://developer.apple.com/design/human-interface-guidelines/color#macOS).
4. Follow system appearance and accessibility preferences; do not add an app-only appearance switch. Re-resolve every visible role on a preference change without losing selection, focus, detail content, or scroll position. Preserve iOS base/elevated surface hierarchy rather than simply inverting colors. [Dark Mode — Best practices](https://developer.apple.com/design/human-interface-guidelines/dark-mode#Best-practices), [Dark Mode — iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/dark-mode#iOS-iPadOS).
5. Use opaque content surfaces for this revision. This is a product choice that keeps status independent of wallpaper and content behind the dashboard. No glass is required. If a host adds translucent chrome later, resolve its local appearance separately, keep ordinary labels monochrome, and retest composited contrast; do not reuse a global light/dark assumption for glass. [Color — Liquid Glass color](https://developer.apple.com/design/human-interface-guidelines/color#Liquid-Glass-color), [Dark Mode — macOS](https://developer.apple.com/design/human-interface-guidelines/dark-mode#macOS).

## Semantic role contract

| Token | Use and platform mapping intent |
|---|---|
| `surface.base` | Dashboard background; ordinary system background on iOS, window background on macOS |
| `surface.content` | Opaque route/detail content; secondary surface within the base on iOS, content/control background on macOS |
| `surface.elevated` | Foreground detail panel when presented above content; resolve elevation separately on iOS |
| `text.primary` | Route names, status phrases, disruption instructions; primary label semantics |
| `text.secondary` | Supporting timestamp/source metadata; secondary label semantics, never disabled text |
| `status.disrupted` | Warning triangle with exclamation mark; phrase “Service disrupted” stays primary text |
| `status.normal` | Circle with check mark; phrase “Normal service” stays primary text |
| `status.unknown` | Diamond with question mark; phrase “Status unavailable” stays primary text |
| `selection.fill/text` | Paired selected-content roles; fallback uses `surface.selected` and `text.primary` |
| `selection.marker` | Leading rule and “Selected” use selected text role; never a warning tint |
| `interaction.accent` | Actual links and focus treatment only; platform focus role/user accent on Mac |
| `separator` | Decorative dividers only; not needed to identify rows or selection |

Symbols are framework-independent vector shapes, not a dependency on SF Symbols or emoji. Their status text remains visible even if symbols cannot render. Route-brand colors, if introduced, must stay separate from service status.

### Explicit fallback palette

These are proposed custom opaque sRGB colors, not Apple system values. Columns are `(appearance, Increase Contrast)`. Use the palette when no reliable semantic-color adapter exists. `surface.elevated = surface.content` in this flat fallback; an elevated panel additionally has a solid `text.secondary` boundary. All content text is on content, elevated, or selected surfaces, not directly on the dashboard base.

| Role | Light, off | Dark, off | Light, on | Dark, on |
|---|---|---|---|---|
| `surface.base` | #F4F5F7 | #10151C | #FFFFFF | #000000 |
| `surface.content` | #FFFFFF | #1C2530 | #FFFFFF | #080C10 |
| `surface.selected` | #E8EDF5 | #29384A | #E3E8EF | #162230 |
| `text.primary` | #17212B | #F1F5F9 | #000000 | #FFFFFF |
| `text.secondary` / `status.unknown` | #475569 | #CBD5E1 | #1F2937 | #E2E8F0 |
| `status.disrupted` | #9F1239 | #FDA4AF | #7F1231 | #FFC0CB |
| `status.normal` | #166534 | #86EFAC | #14532D | #B9F6CA |
| `interaction.accent` | #1D4ED8 | #93C5FD | #153EAB | #BFDBFE |

Keep status glyphs on an opaque content-colored patch inside selected rows, including with a native selection fill. This prevents the status color from colliding with an arbitrary user-selected accent. Selection text must use the foreground paired with the actual selection fill. Do not assume fallback foregrounds work on a native accent fill.

Reduce Transparency leaves the opaque fallback unchanged. Increase Contrast selects its column independently of appearance. Do not lower opacity for metadata, unknown status, hover, or an inactive window. Inactive native selection may use the platform’s paired unemphasized selection roles; retain “Selected” and the marker. Decorative separators may use `text.secondary` at full opacity or be omitted.

## Interaction and state contract

Each route row has stable identity, route name, status phrase/symbol, optional supporting summary, and a selection slot. The complete row is one selectable target. Status symbols are not extra controls. Reading order is route name, status, summary, selection state. Supply an accessible route name, current status, and selected state; omit duplicate decorative symbol descriptions.

```text
state = {selectedRouteId, focusedRouteId, routes, appearance, contrast, transparency}

render(row):
  selected = row.id == selectedRouteId
  surface = selected ? selection.fill : surface.content
  show route name and status phrase using the paired readable text role
  show status glyph using status[row.status] on opaque surface.content
  if selected: show leading rule and visible "Selected"
  if focused: show separate outer focus outline with an opaque backing gap

on row activation (tap, click, keyboard or assistive activation):
  selectedRouteId = row.id
  show that route's detail content and persistent service status
  preserve the route's status; selection does not rewrite its color or meaning

on service update:
  update status phrase, glyph, summary and details together
  retain selectedRouteId and focusedRouteId
  do not infer "Normal service" from missing or failed data

on appearance / contrast / transparency / user-accent change:
  resolve all role pairs atomically, including open detail surfaces
  retain route selection, focused item, details and scroll position
```

Use ordinary platform selection/navigation behavior for the eventual container. Focus alone never selects a route. A focused unselected route must remain distinguishable from the selected route. Do not turn a service update into an automatic selection or navigation event. Unknown status includes a plain-language explanation if provided; a last-known timestamp is supporting information, not evidence of current normal service. Freshness thresholds require a separate data contract.

At 200% text enlargement, wrap status phrases and “Selected” onto additional lines rather than replacing them with dots or clipping them. This is a preservation requirement, not a new typography system. [Accessibility — Vision and Speech](https://developer.apple.com/design/human-interface-guidelines/accessibility).

## Worked before → after

Illustrative route: **Route A**, currently disrupted and selected.

**Before:** White row, light gray “Route A,” red dot; selecting makes the red slightly darker. Without hue discrimination, neither disruption nor selection is reliably identifiable. Its contrast ratio is unknown.

**After, light fallback:** Selected fill #E8EDF5, primary text #17212B, leading primary-colored rule and visible “Selected.” The status reads **“Service disrupted — replacement buses between Central and Park.”** A #9F1239 warning triangle sits on a #FFFFFF opaque patch. Status and selection are independently readable in monochrome.

**After switching to dark while selected:** Fill becomes #29384A and text #F1F5F9; triangle becomes #FDA4AF on #1C2530. The same route and details remain selected. If focus moves to Route B, only its focus outline moves; Route A retains “Selected.” If Route A returns to normal service, its symbol and phrase change to “Normal service,” while its selection marker remains.

## Acceptance checks and observed results

Project thresholds: require at least 4.5:1 for all essential text and status glyphs; aim for 7:1 for custom text, especially small text. Require at least 3:1 for focus/selection boundaries against their adjacent backing. These conservative project gates do not claim full accessibility conformance. The local Accessibility guide gives its scoped Inspector table (up to 17 pt all weights: 4.5:1; 18 pt all weights and bold at any size: 3:1); the Dark Mode guide gives 4.5:1 and a custom-color aim of 7:1. This design chooses the stricter common floor rather than exploiting the lower text allowances. [Dark Mode — Colors](https://developer.apple.com/design/human-interface-guidelines/dark-mode#Dark-Mode-colors), [Accessibility — Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision).

**Passed — specification/static calculation only:**

- All three service states have persistent text plus distinct shapes. Selection has its own text/marker; no essential state relies on hue alone.
- Four explicit fallback variants and live preference transitions are specified.
- A local Python 3 calculation used opaque sRGB inputs in the palette table: linearize each component with the standard 0.04045 breakpoint, compute luminance with weights 0.2126/0.7152/0.0722, and ratio `(lighter + .05)/(darker + .05)`. Results below are rounded; gates used the underlying values. Each cell is contrast on content / selected surface.

| Foreground | Light | Dark | Light increased | Dark increased |
|---|---:|---:|---:|---:|
| Primary | 16.29 / 13.86 | 14.13 / 10.90 | 21.00 / 17.06 | 19.62 / 16.08 |
| Secondary / unknown | 7.58 / 6.45 | 10.43 / 8.04 | 14.68 / 11.92 | 15.91 / 13.05 |
| Disrupted | 8.02 / 6.82 | 8.19 / 6.31 | 10.33 / 8.39 | 12.76 / 10.46 |
| Normal | 7.13 / 6.07 | 11.02 / 8.50 | 9.11 / 7.40 | 15.97 / 13.10 |
| Accent | 6.70 / 5.70 | 8.58 / 6.62 | 9.09 / 7.39 | 13.81 / 11.32 |

**Failed / limits found:** The supplied design fails the non-color status requirement by description. The proposed default secondary text on a light selected row is 6.45:1, below the 7:1 aspiration but above the 4.5:1 gate; use primary text for essential disruption instructions. Accent-colored link text also misses that aspiration in some default cases; keep it for actual interactions. No runtime failure was established.

**Not executed — implementation acceptance gates:**

- Render iOS and macOS in light/dark × Increase Contrast off/on × Reduce Transparency off/on. All essential text, symbols, focus and selection cues must meet their actual composited pair thresholds; inspect resting and scrolled content. Recalculate native semantic/accent pairs independently of fallback measurements.
- Change system appearance and preferences with a selected row and open details. No light-only element, lost selection/focus, scroll jump, or merged elevated panel may remain.
- Test macOS user accents and active/inactive windows. Status must retain its meaning, selection text must use its paired foreground, and focus must remain separately visible.
- View without color and at 200% text size: identify normal, disrupted, unknown, selected and focused states; complete route selection and read details with no clipped essential content.
- Test touch/pointer, keyboard and supported assistive activation. Focus must reach each route; activation must open the correct details. Verify actual accessible names, state exposure and reading order with the relevant Apple tools, including VoiceOver; this document does not establish them.
- Test physical displays, bright/dim environments and relevant display profiles. Confirm symbol outlines and opaque patches remain legible rather than relying on numeric contrast alone.

## Evidence limits and audit trail

Only supplied local files and installed instructions were used. No web browsing occurred; official URLs above identify source articles recorded by the local package, not independently checked pages. The package labels its sources as a dated 2026-10-25 snapshot and does not establish independent review merely through file presence.

Read order, each through its installed path: root `apple-hig/SKILL.md`; project `interface.md`; `subskills/apple-hig-foundations/SKILL.md`; that family's `.topics/apple-hig-color/SKILL.md`, `.topics/apple-hig-dark-mode/SKILL.md`, `.topics/apple-hig-accessibility/SKILL.md`; then its `references/color.md`, `references/dark-mode.md`, `references/accessibility.md`. Each file was read by a separate `cat` command. All skill paths resolve under this project's `.agents/skills/apple-hig/`.

This is a revised design contract, not a working dashboard. The contrast calculation validates only proposed opaque fallback pairs, not native rendering, antialiasing, transparency, desktop tinting, or the original palette. No Apple device, SDK compilation, GUI, Accessibility Inspector or assistive-technology execution occurred. Native semantic mapping and behavioral acceptance remain implementation work; no API availability or platform feasibility beyond this specification is asserted.
