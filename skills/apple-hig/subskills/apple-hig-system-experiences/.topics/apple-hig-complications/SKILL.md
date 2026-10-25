---
name: apple-hig-complications
description: Use when creating, reviewing, or adapting watch-face complication families, timelines, placeholders, tinting, and content destinations.
---

# Design timely information for the chosen face slot

Read [the complication guide](../../references/complications.md), including the selected family/template specifications. The workflow is application advice; preserve unresolved source typos instead of silently choosing dimensions.

Inspect glance purpose, data changes/sensitivity, watchOS version, supported face families, artifact, and create/review/adapt mode. Establish useful changing information and exact tap destination. Distinguish modern WidgetKit families from older ClockKit templates; a Lock Screen accessory elsewhere is a widget, not a watch complication.

Support useful families with tailored content, using a recognizable launcher fallback only when meaningful data cannot fit. Map each variant to relevant content, not generic app home. Choose closed percentage rings versus open arbitrary-range gauges deliberately. Preserve legibility in tint/Always On and protect private values. Schedule useful timeline entries under reload/storage limits; do not promise continuous updates. Supply static placeholders separately from content assets at their required dimensions. Consult the reference tables for family/device sizes; its conflicting legacy inline cell must be verified against the target template before production art.

Implement variants/timeline/deep links or deliver a family/data/state specification; reviews identify the exact family/rendering/data defect. Treat static inspection as insufficient proof of physical wrist readability.

**Worked transformation:** Before: a transit complication uses one full-color station logo for every slot and refreshes a countdown every second. Decision: it is a static launcher with an unrealistic budget. After: tailor the next departure to circular/inline/rectangular slots, retain recognizable destinations, use meaningful timeline/system time updates, and provide tinted/private/placeholder states.

Deliver the artifact, family mapping, timeline/freshness, private state, placeholders, and destinations. Verify slot fit, tint, long values, no data, stale entries, and tap identity. Fail for unsupported template sizing claims, unlimited reload assumptions, or private Always On disclosure. Native family/timeline/device execution remains a separate verdict.

Load [widgets](../apple-hig-widgets/SKILL.md) for shared WidgetKit strategy, [gauges](../../../apple-hig-status/.topics/apple-hig-gauges/SKILL.md) for range meaning, or [watch-faces](../apple-hig-watch-faces/SKILL.md) for curated configurations.
