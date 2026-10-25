---
name: apple-hig-healthkit
description: Use when designing or reviewing health-data authorization, changing access, Activity rings, Apple Health compatibility artwork, or consumer-facing health terminology.
---

# Request health information for a specific health task

Read [HealthKit](../../references/healthkit.md). Inspect the actual health/fitness feature, required data types, current authorization flow, displayed metrics, and requested design/review/adaptation. Preserve the existing stack and health content; this is UI/data-access guidance, not clinical advice. The source covers iOS/iPadOS/watchOS, excluding Mac/TV/visionOS.

Tie each requested datum to a useful health/fitness function and protect granted information. Request access where context explains it rather than at launch, using concise purpose/benefit explanation with standard authorization UI. Recheck changing access when needed; do not treat previously available data as proof of continuing permission. Keep sharing management in system privacy settings instead of conflicting app switches, and maintain the required privacy-policy disclosure.

If using Activity rings, confirm they represent one clearly identified person's Move, Exercise, and Stand data. Preserve supplied colors/opacity/proportions, spacing, and unmasked presentation; adapt the surrounding container rather than redesigning the rings. Separate other ring-like graphics so meanings do not merge. Do not use rings for unrelated metrics, decoration, branding, or redundant notifications.

For compatibility, use the supplied noninteractive Apple Health icon unchanged with the consumer app named nearby. Avoid Health-app screenshots, decorative composites, and using “HealthKit” as a consumer-facing product explanation.

**Worked transformation:** Before, a wellness app asks for all health data on launch and recolors Activity rings to show water, sleep, and mood. Decision: access needs a feature purpose and rings have specific metric meaning. After, a hydration feature requests only relevant access when invoked, hydration uses its own labeled visualization, and any supplied activity component retains its intended person's Move/Exercise/Stand semantics.

Deliver the data-purpose/authorization contract and corrected metric/artwork presentation. Fail if unrelated access is required, changed permissions leave misleading claims, or ring/compatibility art changes meaning. Report actual authorization/data behavior separately from static review; do not claim health accuracy or medical efficacy from UI work.

Use [CareKit](../apple-hig-carekit/SKILL.md) for care-plan tasks and [Privacy](../../../apple-hig-foundations/.topics/apple-hig-privacy/SKILL.md) for sensitive-data lifecycle decisions.
