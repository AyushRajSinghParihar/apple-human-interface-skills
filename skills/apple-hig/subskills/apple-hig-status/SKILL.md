---
name: apple-hig-status
description: Use when designing Apple-platform loading feedback, numerical gauges, ratings, or HealthKit Activity progress.
---

# Apple HIG: Represent progress, value or judgment honestly

Use this family to select and compose topic procedures. Infer the platform and
requested work from the supplied project; preserve its framework and constraints.

## Work through the decision

1. Identify the meaning: an operation completing, a value in a range, a ranking, or personal Activity goals. Enter Progress indicators, Gauges, Rating indicators or Activity rings accordingly.
2. For progress, separate measured completion from unknown duration and define completion/failure behavior. A gauge is not a waiting indicator; Activity rings do not represent arbitrary app completion.
3. Choose labels, cancellation or recovery according to the operation and platform. Preserve meaning through indeterminate states and avoid implying accuracy absent actual measurements.
4. Deliver the status/value model, visible and accessible representation, transition rules and checks that reveal misleading progress or inaccessible information.

## Enter the topic procedure

Read the selected topic’s SKILL.md before its supporting guidance. For a review,
inspect actual evidence and return findings; for an implementation request, make
the authorized change; for design or adaptation, produce a usable specification
or patch. Load related topics only when the chosen procedure calls for them.

- [Activity rings](.topics/apple-hig-activity-rings/SKILL.md)
- [Gauges](.topics/apple-hig-gauges/SKILL.md)
- [Progress indicators](.topics/apple-hig-progress-indicators/SKILL.md)
- [Rating indicators](.topics/apple-hig-rating-indicators/SKILL.md)

## Completion evidence

Report the concrete decisions or changes, their source support, and which checks
passed, failed or were not executed. A source citation or a list of links is not
the requested work product. Retain platform exceptions and unresolved source
conflicts; the absence of a platform subsection does not establish support.
