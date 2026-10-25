# Playing haptics

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/playing-haptics)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Haptics complement sight and sound through supported devices: iPhone controls, watch Taptic Engine, Force Touch trackpads, compatible controllers, and Apple Pencil Pro. Apple Pencil Pro and some trackpads provide haptics when connected to compatible iPad models. The built-in watchOS Taptic patterns combine tactile feedback with an audible tone. iPad/Mac/TV/visionOS controller haptics are distinct from built-in device haptics.

<a id="Best-practices"></a>
## Best practices

Preserve the documented meaning of standard patterns; use generic/custom patterns rather than reassigning success to failure or vice versa. Build consistent cause-and-effect relationships and synchronize tactile intensity/sharpness with the visual/audio event. Avoid overuse, testing frequency with people. Nongame apps usually benefit from brief discrete events; long effects can distract or make Pencil use uncomfortable. Allow haptics to be disabled without losing functionality. Check that vibration does not interfere with camera, microphone, or motion-sensor tasks.

<a id="Custom-haptics"></a>
## Custom haptics

Combine transient impulses and continuous vibrations, changing intensity for strength and sharpness for qualities ranging from soft/organic to crisp/mechanical. Optional audio can reinforce the same event. Adapt patterns to context, such as a stronger large impact than a small jump.

<a id="Platform-considerations"></a>
## Platform considerations

<a id="iOS"></a>
### iOS

Native controls on supported iPhones provide standard haptics; feedback generators can expose notification, impact, and selection patterns.

<a id="Notification"></a>
#### Notification

Use Success for completed work, Warning for a cautionary outcome, and Error for failure.

<a id="Impact"></a>
#### Impact

Light/medium/heavy represent the apparent object weight; rigid/soft describe hardness or flexibility. Match them to a visual physical metaphor, such as snapping or collision.

<a id="Selection"></a>
#### Selection

Use selection feedback while a UI value changes.

<a id="macOS"></a>
### macOS

With Magic Trackpad, Alignment marks a position/size alignment or meaningful boundary; Level change marks discrete force/pressure transitions; Generic covers other appropriate feedback. Trigger in relation to drag or force-click behavior.

<a id="watchOS"></a>
### watchOS

Series 4 and later provide crown haptic detents, with native controls marking item boundaries. Standard meanings are Notification for a significant attention-worthy event, Up/Down for crossing important value thresholds, Success/Failure for outcomes, Retry for a recoverable failure, Start/Stop for an explicitly initiated activity, and Click for predefined increments. Use clicks sparingly to avoid overlapping patterns.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback)
[Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/CoreHaptics>

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2021/10278>
  <https://developer.apple.com/videos/play/wwdc2019/520>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: May 7, 2024, June 21, 2023.
