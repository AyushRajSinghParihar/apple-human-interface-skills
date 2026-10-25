# Action button

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/action-button) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

On supported iPhone and Apple Watch models, people assign the Action button in setup or Settings to a system feature or App Shortcut. Treat it as another fast entry point for a recurring function, equivalent in intent to invoking that shortcut through Siri or Spotlight.

<a id="Best-practices"></a>
## Best practices
Expose essential useful functions rather than an extra Open App shortcut, because system launch, widgets, icons, and complications already cover launching. Labels appear in Settings: use title case, a present-tense verb, at most three words, and omit unnecessary articles/prepositions. Rely on the system’s setup/usage explanation instead of duplicating it.

<a id="Platform-considerations"></a>
## Platform considerations
The source marks this unsupported on iPadOS, macOS, tvOS, and visionOS.

<a id="iOS"></a>
### iOS
Keep people in their current context where possible. Use snippets or Live Activities for lightweight interaction and status instead of always opening the app; a timer can gather duration and start a Live Activity directly.

<a id="watchOS"></a>
### watchOS
A first press can start a workout/dive or place a waypoint. A later press should logically advance/support that chosen task, such as recording a segment or changing workout modality. Prefer one memorable secondary function and be cautious about multiple context-dependent ones. Do not normally use repeated presses to end the main activity; provide completion in UI. Pressing Action and side button together should pause, except when pausing would harm the experience or safety, such as losing dive depth/time tracking.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/action-button) for linked Apple design assets and implementation resources.

<a id="Related"></a>
#### Related
The official article links the adjacent HIG topics relevant to this guidance.

<a id="Change-log"></a>
## Change log
Source revision dates: September 12, 2023, September 14, 2022.
