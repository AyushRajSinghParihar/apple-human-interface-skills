---
name: apple-hig-activity-rings
description: Use when creating, reviewing, or adapting the system Move, Exercise, and Stand ring presentation for one person.
---

# Preserve the activity measures' identity

Read [the activity-ring guide](../../references/activity-rings.md). This workflow is application advice; the rings' rendering and defined measures are source constraints.

Inspect the measures, individual identity, HealthKit-related context, platform/pairing state, artifact, and create/review/adapt request. Establish whether the proposed data really are Move/Exercise/Stand for one person. Do not transform arbitrary goals or team totals into Activity rings.

Use the standard ring rendering for its defined measures and identify the individual. Preserve black background, outer clearance, standard colors, and unmodified rendering rather than branding the rings. Adapt surrounding layout, not opacity/gradients/shadows of the element. Keep competing ring-like graphics clearly separate. On iOS, allow the supplied system behavior to reflect pairing and historical one-ring/three-ring differences rather than “correcting” them into identical displays. Do not claim support on Mac/TV/visionOS. Avoid decorative/marketing use and repeated system Activity notifications.

Implement the relevant standard presentation or provide an annotated ring/context specification; reviews must name exact data/rendering misuse. Keep RGB label/value facts in the reference rather than duplicating its table.

**Worked transformation:** Before: a challenge app recolors Activity rings purple and combines three friends' totals into one branded ring. Decision: system measures and personal identity are being misrepresented. After: show an unmodified individually identified Activity element where relevant; present the team challenge separately with its own clearly distinct chart.

Deliver the artifact, measure/person/pairing contract, and surrounding clearances. Verify no crop/overlap, black margin, correct identity, and legitimate historical ring variation. Fail for aggregated people, unrelated measures, altered ring styling, or decorative reuse. Health data, pairing, and device rendering need actual runtime evidence; Linux inspection proves none of them.

Load [workouts](../../../apple-hig-patterns/.topics/apple-hig-workouts/SKILL.md) for session context or [charts](../../../apple-hig-content/.topics/apple-hig-charts/SKILL.md) for unrelated/team data.
