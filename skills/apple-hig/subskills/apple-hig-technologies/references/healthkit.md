# HealthKit

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/healthkit) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

HealthKit stores health/fitness data for iOS/iPadOS/watchOS. Request access only for an actual health/fitness function and protect every permitted datum.

<a id="Privacy-protection"></a>
## Privacy protection
Provide a clear privacy-policy URL for the App Store. Request data when context explains the need rather than at launch, and account for changing authorization whenever access is needed. Add brief purpose/benefit explanations to the standard permission screen without imitating it in custom UI. Keep health-data sharing management in system privacy settings rather than extra in-app switches that redirect its flow.

<a id="Activity-rings"></a>
## Activity rings
Use the provided rings only for one clearly identified person’s Move, Exercise, and Stand progress. Do not repurpose rings for other data or display those three metrics with a different ring design. Preserve ring/background colors, opacity, and proportions; adapt surrounding UI instead. Keep an outer margin at least the inter-ring gap and prevent cropping/overlap. To enclose in a circle, adjust the container corner radius rather than masking the rings. Separate any other ring-like graphics with spacing, labels, lines, color, or scale. Rings are informative, not decoration or branding; exclude them from icons, marketing, and app notifications. Activity-related notifications should add app-specific value instead of repeating system progress updates.

<a id="Apple-Health-icon"></a>
## Apple Health icon
Use only the supplied unmodified icon to indicate compatibility, with Apple Health named nearby. Keep it at least as large as neighboring health-app icons and clear space at least one tenth of its height. Do not use it as a button, inline word replacement, composite decoration, circular mask, recolored/outlined/shadowed treatment, or substitute for text. Do not show Health-app screenshots or imagery in the app/marketing; the approved progress-ring component is a separate permitted case.

<a id="Editorial-guidelines"></a>
## Editorial guidelines
Call the consumer app Apple Health or the Apple Health app; HealthKit is a developer framework name, unsuitable for product explanations. Preserve capitalization except in uniformly uppercase layouts. Use the system’s localized translation of Health.

<a id="Platform-considerations"></a>
## Platform considerations
No extra iOS/iPadOS/watchOS rules; macOS/tvOS/visionOS are unsupported.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/healthkit) for linked Apple design assets and implementation resources.

<a id="Related"></a>
#### Related
The official article links the adjacent HIG topics relevant to this guidance.

<a id="Developer-documentation"></a>
#### Developer documentation
Use the framework references linked by Apple for current API availability and implementation details.

<a id="Videos"></a>
#### Videos
Apple’s linked design sessions provide demonstrations and additional implementation context; no video review is implied here.
