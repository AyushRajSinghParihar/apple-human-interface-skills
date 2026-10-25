# Offering help

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/offering-help)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Prefer intuitive tasks, adding concise contextual help when it improves understanding.

<a id="Best-practices"></a>
## Best practices

Match help to task complexity: inline guidance for a step or two, tutorials for larger goals. Keep help tied to the current action and dismissible. Use inclusive wording and visuals that match the actual platform/input device. Explain the app's specific effect rather than teaching familiar standard controls. If a unique control or unusual device orientation needs instruction, prefer a quick visual/animation over lengthy prose.

<a id="Creating-tips"></a>
## Creating tips

Choose popover tips to preserve content flow or inline tips when surrounding information should stay visible; inline annotations point to a control, while hints cover a general task. Tips suit features requiring no more than about three actions. Keep them to one or two direct actionable sentences, excluding promotion and unrelated flows. Use event/parameter eligibility so experienced users do not repeatedly see basics; set a reasonable overall cadence, such as once per 24 hours. A familiar filled symbol can help, but avoid repeating the same nearby feature image. Buttons can deep-link to settings, setup, or further explanation.

<a id="Platform-considerations"></a>
## Platform considerations

No additional iOS, iPadOS, tvOS, or watchOS rules are specified.

<a id="macOS-visionOS"></a>
### macOS, visionOS

Tooltips/help tags appear on pointer dwell on Mac, including iOS/iPadOS apps there, and on look or pointer dwell in visionOS. Describe only the indicated control's action, preferably with a verb, without repeating its name or explaining a larger task. Aim for 60–75 characters maximum, allowing localization growth; fragments and omitted articles can help. Use sentence case and generally omit terminal punctuation unless product style needs it. Adjust wording by control state where valuable.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Onboarding](https://developer.apple.com/design/human-interface-guidelines/onboarding)
[Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback)
[Writing](https://developer.apple.com/design/human-interface-guidelines/writing)
[Help menu](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Help-menu)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/TipKit>
<https://developer.apple.com/documentation/AppKit/NSHelpManager> — AppKit

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2023/10229>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: December 5, 2023, September 12, 2023.
