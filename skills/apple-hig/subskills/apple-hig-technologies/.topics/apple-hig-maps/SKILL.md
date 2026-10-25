---
name: apple-hig-maps
description: Use when designing or reviewing interactive maps, annotations and overlays, selected-place cards, indoor floors, legal attribution, or Watch map snapshots.
---

# Keep geographic context visible while revealing useful detail

Read [Maps](../../references/maps.md). Inspect the map task, region, annotations, overlays, cards, platform/window, and requested design/review/adaptation. Preserve the existing map stack. Establish which geometry and interactions are actually supplied; do not invent routes, location accuracy, or current place details.

Choose ordinary saturated map emphasis or muted geography for rich custom overlays. Preserve pan/zoom/rotation and distinguish selected features. Cluster nearby points until zoom can separate them. Place custom overlays at the appropriate level so they do not erase necessary map labels/detail. Keep Apple logo/legal links visible and stable with the guide's spacing/size exceptions, including the lowest resting position of movable cards.

Choose place-card presentation by available space and needed detail. Keep the selected location visible, avoid duplicating existing details, and test small/resized windows. A card opened outside a map must include a map. Use a clear place-name/address/details affordance rather than an unexplained generic action.

For indoor maps, disclose detail with zoom, label floors through a concise picker, combine color with icons for services, and retain surrounding streets/transit. Bound panning so the venue remains partly visible and provide useful routing/handoff. On Watch, use a static snapshot that opens Maps, with at most five annotations and the smallest region covering important points; do not promise full interactive map controls there.

**Before → decision → after:** A campus locator overlays opaque building labels, hides attribution behind a draggable card, and lets indoor panning lose the venue entirely. Decision: details must preserve context and legal information. After, coherent annotations cluster, the selected-building card leaves its location visible, attribution sits above its resting edge, and indoor panning retains campus context with a clear floor picker.

Deliver corrected map/card/overlay states or implementation. Fail if expected gestures are blocked, selection disappears beneath detail, required attribution is obscured, or a Watch snapshot requires scrolling. Actual map data freshness, routing, native cards, and location behavior need service/device tests; static review cannot verify them.

Use [Color](../../../apple-hig-foundations/.topics/apple-hig-color/SKILL.md) for overlays and [Privacy](../../../apple-hig-foundations/.topics/apple-hig-privacy/SKILL.md) if the task requests personal location access.
