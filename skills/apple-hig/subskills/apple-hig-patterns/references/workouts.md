# Workouts

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/workouts)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Workout sessions should keep attention on activity and useful progress. Watch/phone/tablet can gather activity metrics; larger stationary devices can present live or recorded classes, but the activity-data session guidance below targets iOS/iPadOS/watchOS.

<a id="Best-practices"></a>
## Best practices

Use watch workout sessions to keep relevant metrics visible between wrist raises, with elapsed/remaining time, calories, distance, and useful lap/interval controls. Keep unrelated navigation out of the active session. A familiar arrangement separates session controls, live metrics, and Now Playing pages. Give the active session a recognizable layout with changing values. Make pause/resume/end easy to target and communicate start/stop clearly.

Explain sensor limitations with concrete information instead of hiding them. A pool swim uses no GPS; water can prevent heart-rate readings while accelerometer data still supports calories, laps, and distance. An Other workout can credit brisk-walk-equivalent calories when sensors are unavailable. Open-water GPS distance depends on freestyle, while accelerometer-based calorie tracking can continue despite missing heart rate. Tailor wording to the actual supported workout rather than copying one limitation to every activity.

End with a clear recorded-data summary and optionally standard Activity rings for daily-goal context. Discard or confirm saving sessions that end only a few seconds after starting. Use large high-contrast prioritized metrics for people moving. Retain Activity rings' defined measures, colors, and usage rules.

<a id="Platform-considerations"></a>
## Platform considerations

No additional iOS, iPadOS, or watchOS rules are specified. This workout-session pattern is unsupported in macOS, tvOS, and visionOS; that does not preclude recorded fitness media there.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Activity rings](https://developer.apple.com/design/human-interface-guidelines/activity-rings)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/WorkoutKit>
<https://developer.apple.com/documentation/HealthKit/workouts-and-activity-rings> — HealthKit

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2025/322>
  <https://developer.apple.com/videos/play/wwdc2023/10016>
  <https://developer.apple.com/videos/play/wwdc2021/10009>
