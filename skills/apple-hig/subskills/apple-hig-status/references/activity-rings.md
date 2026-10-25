# Activity rings

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/activity-rings)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Activity rings represent one person's daily Move, Exercise, and Stand progress. watchOS uses three rings. iOS can show all three when paired to Apple Watch or a single approximate Move ring without one.

<a id="Best-practices"></a>
## Best practices

Use rings where progress is relevant, particularly health/fitness experiences contributing to HealthKit. A workout metrics or completion screen can connect the session to daily goals. Keep rings exclusively for their defined activity measures; do not restyle them for unrelated data or portray these measures using a competing ring treatment. Identify the individual with a name, photo, or avatar, and never aggregate multiple people's data into one ring element.

Preserve the standard rendering: no changed colors, opacity filters, shadows, gradients, or other added effects. Show a black background, ideally in a circular enclosing view made with corner radius rather than a circular mask. Leave black visible outside the outermost ring; add a thin black outer stroke only if needed. Scale the element appropriately and adapt surrounding UI rather than altering the rings. Maintain an outer margin at least as wide as the gap between rings, without cropping, overlap, or encroachment.

For directly associated labels and current/goal values, use these RGB colors:

| Measure | R | G | B |
| --- | --- | --- | --- |
| Move | 250 | 17 | 79 |
| Exercise | 166 | 255 | 0 |
| Stand | 0 | 255 | 246 |

If other ring-like elements must coexist, separate them clearly with spacing, lines, labels, scale, or color. Do not repeat system Activity progress notifications or include the ring element in notifications. A notification can reference activity only in a way specific to your app. Do not use rings as decoration, background graphics, label embellishment, branding, an app icon, or marketing artwork.

<a id="Platform-considerations"></a>
## Platform considerations

No additional iPadOS or watchOS rules are specified. Activity rings are unsupported in macOS, tvOS, and visionOS.

<a id="iOS"></a>
### iOS

HealthKitUI supplies HKActivityRingView and adapts automatically to pairing. With Apple Watch paired, all three rings appear; without it, the Move estimate draws on steps and workouts from other apps. Historical records can therefore legitimately mix one-ring and three-ring presentations as pairing changes.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Workouts](https://developer.apple.com/design/human-interface-guidelines/workouts)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/HealthKitUI/HKActivityRingView> — HealthKit

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2025/322>
  <https://developer.apple.com/videos/play/wwdc2021/10009>
  <https://developer.apple.com/videos/play/wwdc2023/10016>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: March 29, 2024, December 5, 2023.
