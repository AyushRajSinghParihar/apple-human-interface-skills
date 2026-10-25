# Transit disruption dashboard: revised interaction specification

## Scope and evidence

This is a framework-agnostic design for iOS and macOS. `interface.md` supplies white backgrounds, light-gray body text, red/green status dots, and a slightly darker red for selection. It supplies no RGB values, implementation, screenshot, or interaction details. Contrast failure cannot be measured for that original palette; hue-only status and shade-only selection are confirmed by the brief.

The task is to identify a route's service condition, select it, and read its disruption details. The row/detail interaction and expanded status vocabulary below are proposed product decisions, not observed existing behavior. No Apple SDK is required.

## Decisions and semantic roles

Separate service status, selection, keyboard focus, and action tint. Preserve each meaning across appearance changes. Prefer a host's genuine semantic colors when available; resolve them by purpose rather than copying Apple's dated swatches. Otherwise use the explicit opaque fallback below. These recommendations follow [Color: System colors and Inclusive color](https://developer.apple.com/design/human-interface-guidelines/color#System-colors).

| Role | Contract |
|---|---|
| `surface.canvas` | Overall dashboard surface; use the host's ordinary background hierarchy, or grouped hierarchy if the implementation groups routes. |
| `surface.row` | Opaque route-row surface. Status colors are evaluated against this surface. |
| `surface.detail` | Distinct detail surface; retain the host's base/elevated distinction on iOS. |
| `text.primary` | Route name, status words, disruption explanation, essential times. Never use separator or disabled colors for these. |
| `text.secondary` | Supporting metadata, such as last updated time; still readable. |
| `separator` | Decorative grouping boundary only; never the sole selection signal. |
| `action.accent` | Interactive actions only. Honor the user's macOS accent preference; do not use that preference to redefine transit severity. |
| `selection.outline` | Primary foreground outline plus visible “Selected” text; independent of service status and accent. |
| `focus.outline` | Host focus indicator, or primary-foreground outer ring in fallback. Separate from persistent selection. |
| `status.*` | Fixed semantic category with a word and distinct shape. Never tint the entire row by severity. |

Status mapping is a product taxonomy: `normal` = green circle with check + “Normal service”; `delayed` = amber triangle with exclamation + “Delayed”; `suspended` = red octagon with stop mark + “Service suspended”; `unknown` = neutral diamond with question mark + “Status unavailable”. The data adapter must map documented upstream codes explicitly. An unmapped, missing, or stale status becomes unknown, with a last-updated explanation; it must not imply normal service. The freshness threshold must come from the feed contract and remains unresolved here. Route identity colors, if later added, must stay separate from these status roles.

The icons are generic vector geometry, not SF Symbols requirements. Status words remain visible in monochrome. Shapes can be decorative to assistive technology because the adjacent text carries their full meaning. See [Accessibility: Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision).

### Concrete fallback color sets

These are proposed custom sRGB values, not Apple system constants. All are opaque. Columns are light, dark, light with Increase Contrast, and dark with Increase Contrast.

| Token | Light | Dark | Light increased | Dark increased |
|---|---|---|---|---|
| `surface.canvas` | #F2F4F6 | #101214 | #FFFFFF | #000000 |
| `surface.row`, `surface.detail` | #FFFFFF | #181C20 | #FFFFFF | #101214 |
| `text.primary`, selection/fallback focus outlines | #17212B | #F3F6F8 | #000000 | #FFFFFF |
| `text.secondary` | #465563 | #B9C5D0 | #283440 | #E3EAF0 |
| `status.suspended` | #A31825 | #FFB4B8 | #7C0012 | #FFDADD |
| `status.normal` | #176534 | #8BE0A8 | #004820 | #C4F7D4 |
| `status.delayed` | #805000 | #FFD58A | #603900 | #FFE9BC |
| `status.unknown` | #505C68 | #BAC5CF | #303B46 | #E0E7ED |

Status glyphs use their status foreground on `surface.row`; status words use `text.primary`. Fallback separators use `text.secondary`. Fallback action labels use `text.primary` with a persistent underline; their interactive role does not depend on hue. Native integrations may use adaptive accent/link roles after verifying contrast. No invented fixed blue approximates a user's accent.

Fallback selected rows retain their normal fill and status color, gain a 2 logical-unit inset outline in `text.primary`, and display “Selected”. Focus adds a separate 2-unit outer ring with a 2-unit surface-colored gap. Reserve space so rings do not clip. These dimensions are product choices, not HIG numerical requirements. At increased contrast, boundaries remain explicit; do not rely on barely different neutral fills. Fallback detail has a primary-foreground border to distinguish it from its surroundings.

## Interaction and appearance contract

Each route row contains route name, visible status glyph and words, update time, and selection indicator. A single selection activates its detail region. On iOS that region may be a detail destination with Back; on macOS it may be adjacent. Both preserve selected route identity when returning. No separate dot target is needed.

1. Activating a route sets its stable ID as selected, updates the detail content, and exposes the selected state programmatically. The previous row loses its outline and “Selected” text. Status does not change.
2. Keyboard focus alone does not select a route. Tab/host navigation reaches route controls; Enter or Space activates them. Expose an appropriate selectable-control role, route/status name, and selected value through the framework's accessibility layer.
3. Data updates replace the selected route's status text, glyph, and detail together. Keep selection and focus stable; never flash red/green. If the route disappears, clear selection and show “Route no longer available”; do not silently select another route.
4. Follow system appearance, without a duplicate in-app switch. Re-resolve all roles on light/dark or accessibility preference changes, including while a detail destination is active. Preserve selection, focus, navigation, and scroll position; do not reload the feed because appearance changed.
5. Use opaque status surfaces in all settings. Reduce Transparency therefore does not change their meaning or contrast. Do not add glass to this design. A future translucent surface requires a new compositing audit, including resting/scrolled content and local appearance.
6. Allow status words and details to wrap at 200% text enlargement. Selection indicators move to a new line if needed. Do not truncate essential route/status meaning. Start from platform text defaults and comfortable target defaults: iOS 17 pt text and 44 × 44 pt targets; macOS 13 pt text and 28 × 28 pt targets. These are defaults from the supplied guidance, not interchangeable cross-platform minima.

Appearance behavior follows [Dark Mode: Best practices, Dark Mode colors, and platform considerations](https://developer.apple.com/design/human-interface-guidelines/dark-mode). Input and enlargement requirements follow [Accessibility: Vision, Mobility, and Speech](https://developer.apple.com/design/human-interface-guidelines/accessibility).

```text
renderRow(route, state, environment):
    palette = resolveSemanticRoles(environment.appearance,
                                   environment.increaseContrast,
                                   environment.platformAccent)
    status = normalizeFeedStatus(route, feedFreshnessPolicy)
    drawOpaqueRow(palette.surface.row)
    show(route.name, palette.text.primary)
    show(status.shape, palette.status[status.kind])
    show(status.words, palette.text.primary)
    show(route.updateDescription, palette.text.secondary)
    if state.selectedID == route.id:
        drawInsetSelectionOutline()
        show("Selected", palette.text.primary)
    if state.focusedID == route.id: drawSeparateFocusRing()
    exposeSelectableRoute(route.name, status.words, selected)

onAppearanceOrContrastChanged(environment):
    invalidateResolvedColorsForAllVisibleAndCachedSurfaces()
    rerenderPreservingInteractionState()
```

## Worked before/after

Illustrative input: Route 24 has suspended service; Route 7 has normal service; Route 24 is selected.

**Before:** Both rows have white backgrounds and light-gray body text. Route 24 has a red dot, made slightly darker for selection; Route 7 has a green dot. Without hue, neither service condition nor selection is reliably expressed. No numeric contrast conclusion is possible.

**After, light fallback:** Route 24 has a #FFFFFF surface, #17212B route name and “Service suspended”, #A31825 octagon, and #17212B outline plus “Selected”. Route 7 has “Normal service” and a #176534 check-circle, without a selection outline. Route 24's detail explicitly says “Service suspended”; any explanation comes from actual feed data.

**Switch to dark while Route 24 is selected:** Row surfaces become #181C20, primary text/outlines #F3F6F8, suspended glyph #FFB4B8, and normal glyph #8BE0A8. Route 24 stays selected with its detail and scroll position intact. Turning Increase Contrast on resolves the dark-increased column. Even when all colors are rendered gray, words, shapes, and the selection outline preserve the same task information.

## Acceptance checks and observed results

**Passed — specification/static evidence:** Every status has words and shape; selection is independent of severity; all fallback custom roles have four variants; live appearance changes preserve interaction state by contract. These establish specification completeness, not implemented behavior.

**Passed — numerical fallback calculation:** A headless Python 3 calculation used WCAG relative luminance for opaque sRGB: linearize each channel, compute `L = .2126R + .7152G + .0722B`, then `(lighter L + .05)/(darker L + .05)`. Inputs are exactly the row-background and foreground hex values above. Ratios below are ordered primary, secondary, suspended, normal, delayed, unknown:

| Mode / background | Calculated ratios |
|---|---|
| Light / #FFFFFF | 16.29, 7.66, 7.74, 7.12, 6.85, 6.84 |
| Dark / #181C20 | 15.78, 9.76, 10.18, 10.87, 12.35, 9.77 |
| Light increased / #FFFFFF | 21.00, 12.69, 11.26, 10.78, 10.08, 11.41 |
| Dark increased / #101214 | 18.77, 15.46, 14.59, 15.74, 15.76, 15.04 |

All calculated pairs exceed 4.5:1. The local Dark Mode guide recommends at least 4.5:1 and aiming for 7:1 with custom colors, especially small text. Light delayed/unknown glyphs fall below that aspirational 7:1; their accompanying small text uses primary foreground, which exceeds it. The Accessibility guide's separate Inspector table has size/weight qualifications; this specification chooses the stricter 4.5:1 floor for all these pairs rather than treating the table as blanket conformance.

**Failed — supplied design's semantic redundancy:** Red/green dots alone and darker red selection do not convey their meanings independently of color. The revised contract corrects this; implementation is still pending. No original measured contrast failure is asserted.

**Not executed — implementation acceptance gates:**

- Exercise select → inspect detail → appearance switch → contrast switch → Back. Same route, status, focus, and reading position must persist; no light-only cached elements may remain.
- Repeat all four appearance/contrast combinations with Reduce Transparency off/on. Verify actual rendered text, glyph, outline, action, and selected/focused pairs on every real surface; minimum 4.5:1 for the specified essential foregrounds. Host semantic colors and composited pixels need their own measurements.
- In grayscale, distinguish every status, selection, and keyboard focus without consulting color. Verify macOS user accents, inactive-window selection, and wallpaper changes do not redefine status or hide selection.
- At 200% text size, all essential words and actions remain available without overlap or clipping. Measure actual platform target geometry and ring clearance.
- Complete route selection/detail/back using keyboard and supported assistive input. Verify accessible name, role, selected value, focus visibility/order, and no duplicate decorative-glyph announcements on actual iOS/macOS environments.
- Inspect light/dark hierarchy and glyph outlines on devices in bright and dim environments and relevant display profiles. A fallback palette calculation cannot establish these results.

## Evidence limits and source audit

Only supplied local files and installed instructions were used; no web requests were made. Official links identify the source articles, not independently verified current guidance. The installed references are application guidance based on an Apple HIG snapshot retrieved 2026-10-25, not SDK documentation or proof of independent source review.

Auditable reading route: installed `apple-hig/SKILL.md` → `interface.md` → Foundations family → relevant topic-index rows → Color, Dark Mode, and Accessibility topic procedures → their respective source guides. Each file was read in its own shell command. No platform feasibility or SDK integration is claimed.

No application was implemented or run. No device, GUI, SDK compilation, native rendering, accessibility tool, VoiceOver, or physical-environment test was performed. The successful Python 3 calculation verifies only the listed opaque numerical pairs; an initial `python` command was unavailable. Feed status mapping and freshness policy require the actual upstream contract before shipping. The proposed interactions, colors, and checks are ready for implementation, with runtime results explicitly pending.
