# Feedback

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/feedback)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Feedback communicates state, outcomes, consequences, and recovery. Match delivery intensity to significance: passive status can remain available in context; unexpected irreversible loss needs attention before it happens.

<a id="Best-practices"></a>
## Best practices

Make feedback accessible through complementary visual, text, sound, and haptic signals rather than relying on one sense. Put routine state near the relevant item. Reserve alerts for critical, ideally actionable information. Warn before unexpected irreversible data loss, while avoiding warnings for ordinary expected deletion. Confirm completion when the task is significant, such as a payment, rather than adding noise to every successful action. When a command cannot run, explain the reason and how to proceed.

<a id="Platform-considerations"></a>
## Platform considerations

No additional iOS, iPadOS, macOS, tvOS, or visionOS rules are specified.

<a id="watchOS"></a>
### watchOS

Avoid indeterminate wait indicators that imply people must keep watching. Reassure them when a notification will communicate completion instead.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Playing audio](https://developer.apple.com/design/human-interface-guidelines/playing-audio)
[Playing haptics](https://developer.apple.com/design/human-interface-guidelines/playing-haptics)
[Motion](https://developer.apple.com/design/human-interface-guidelines/motion)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/UIKit/animation-and-haptics> — UIKit

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2018/803>
  <https://developer.apple.com/videos/play/wwdc2017/802>
