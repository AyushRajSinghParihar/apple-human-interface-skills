---
name: apple-hig-widgets
description: Use when creating, reviewing, or adapting widgets across families, surfaces, rendering modes, freshness policies, and focused interactions.
---

# Build a widget around one useful glance

Read [the widgets guide](../../references/widgets.md), including the context/rendering tables relevant to the requested destination. The procedure and example below are application advice; use the guide for supported families, dimensions, and platform facts. Do not turn a reference size into a universal fixed production canvas.

## Establish purpose and destination

Inspect the supplied app, widget design/code, data model, or brief. Determine create, review, or adaptation mode, target OS/surface, widget family, useful changing information, sensitivity, and the app destination after activation. If no family or surface is given, choose the smallest supported one that communicates the requested purpose, state the assumption, and design that concrete variant.

Write the glance question the widget answers. Reject a static app-icon replica or a compressed app dashboard as the purpose. Decide what the person needs immediately, what appears on closer inspection, and what belongs in the app. Record source update frequency separately from system refresh opportunity; neither a design mockup nor an API response proves continuous widget updates.

## Produce a surface-specific contract

1. Choose family and content hierarchy together. A small variant should carry a clear fact or focused action; larger variants add useful information under the same core purpose instead of stretching the small layout. Consult the supported-context tables before proposing variants: tvOS does not support widgets, and accessory, system, and spatial-only families are not interchangeable. Keep specification tables in the reference rather than copying them into the deliverable.
2. Define data behavior: configuration or useful automatic content, realistic preview, initial placeholder, signed-out explanation when sign-in is required, available data during refresh, and stale/unavailable content. Specify freshness wording when age changes the interpretation. Match timeline requests to meaningful changes and expected viewing; use system date/time presentation for changing time where applicable. Keep useful existing data visible while refreshing. If the requested value requires frequent updates for a bounded event, load live-activities instead of promising a constantly refreshing widget.
3. Map interactions to outcomes. Ordinary activation opens the relevant app content; native buttons/toggles may perform simple relevant actions in place. Give separate targets distinguishable purposes and deep-link precisely. Inline accessories have one tap target, so collapse competing controls into one useful destination rather than drawing fake independent buttons. Do not recreate navigation, forms, or a miniature app inside the widget.
4. Design required rendering variants rather than relying on brand color. Establish primary versus accent hierarchy for accented mode and meaningful grayscale emphasis for vibrant mode. Preserve labels, symbols, or shapes that carry state when color disappears. Check light/dark, tint/clear, background removal, and low-light/Always On variants only where that surface uses them. The source table excludes accented Mac support while prose conflicts; disclose the inconsistency and verify current official support before promising it. Do not resolve it by inventing a capability.
5. Make layout flexible: system text styles and actual text, adaptable margins, container-relative corner shapes, and assets that remain useful when scaled. Use the reference's size guidance for the selected context, including iPad canvas-versus-device scaling. Review accessibility text sizes for supported platforms and ensure reduced detail preserves the glance question, rather than simply shrinking every element.
6. Apply the destination's consequential branch. For StandBy/CarPlay, prioritize large glanceable information, removable backgrounds, and low-light StandBy red monochrome. For a shared HomeView Modular face, assess whose information becomes visible to the household and choose a safe summary/configuration. For watch Smart Stack, prioritize relevance and a legible compact hierarchy. For visionOS, specify near/default and distant simplified content, surface/mounting suitability, frame/treatment choice, palette/lighting variants, and scale range; distant views enlarge key information and remove controls. Recessed-only mounting cannot support horizontal placement, and frame-width choices cannot be repaired with layout adaptation after selection.

Perform the authorized work: implement the widget in the supplied stack when requested, produce an annotated variant/state specification for design, or report evidence-backed defects with concrete replacements for review. For adaptation, retain the glance question while changing family, hierarchy, interactions, and appearance for the destination.

## Deliver and verify

Deliver the changed artifact with a compact variant contract: purpose; surface/family; primary content; freshness/stale policy; configuration/auth state; tap/in-place-action destinations; rendering variants; and destination-specific checks. Include realistic example data and mark simulated data as simulated. A review must identify the affected variant and observed evidence, not merely repeat best practices.

Verify that each variant answers its glance question with long/localized text, realistic edge values, and relevant accessibility sizes. Follow each tap and in-place action to its intended object; confirm rendering changes preserve meaning when color/background disappears. Check stale content cannot masquerade as live data and previews accurately represent the chosen variants. Fail the design for unsupported family/surface claims, unbounded refresh promises, sensitive shared content without a deliberate policy, unreadable tinted hierarchy, or separate inline tap targets. Distinguish static inspection from timeline/runtime, VoiceOver, spatial distance/lighting, device rendering, and household behavior tests; do not claim these were run on a Linux host.

## Worked transformation

**Before:** A reading app proposes one stretched widget for phone Home Screen and Lock Screen. It shows six book covers, a red “overdue” dot, and three tiny controls; the brief promises second-by-second updates.

**Decision:** The useful glance is “What am I reading next?” Home Screen and accessory contexts need different hierarchies. Reading progress can refresh meaningfully without a continuous timer, and overdue status must survive desaturation.

**After:** A small Home Screen variant shows the current book title, progress text, and a precise open-book destination; a larger variant adds the next queued book under the same purpose. An inline Lock Screen variant reads `Continue: The Orchard` with one destination. Replace the color-only dot with `Due tomorrow` where relevant, retain last known progress during refresh, and preview believable data. Verify tint/grayscale legibility and deep links; label refresh timing as system-controlled. This is a proposed design, not measured behavior of a real app.

## Conditional handoffs

Use live-activities for bounded frequently updated events; complications for watch-face-specific placement; controls for a system control rather than informational widget; layout for unresolved adaptive geometry; and accessibility for reading order or contrast failures. Carry the variant contract forward so related work preserves the original glance purpose.
