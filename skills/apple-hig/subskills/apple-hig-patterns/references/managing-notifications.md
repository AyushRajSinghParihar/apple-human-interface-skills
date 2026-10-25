# Managing notifications

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/managing-notifications)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Request permission before sending notifications and respect later system choices, including silencing. Some locales exempt government alerts from complete silencing. Notifications can remain available even while Focus delays their alerts.

<a id="Integrating-with-Focus"></a>
## Integrating with Focus

Focus filters interruption by activity and allowed contacts/apps; scheduled summaries defer alerts to selected times. Communication notifications use sender-based decisions through supported SiriKit intents. Assign an interruption level to other notifications:

| Level | Intended urgency | Scheduled delivery override | Focus breakthrough | Silent override |
| --- | --- | --- | --- | --- |
| Passive | Leisurely information | No | No | No |
| Active | Ordinary timely update; default | No | No | No |
| Time Sensitive | Direct immediate personal impact | Yes | Yes | No |
| Critical | Urgent health/safety need | Yes | Yes | Yes |

Critical requires an entitlement because it can override delivery, Focus, and silent settings. People can choose whether Time Sensitive alerts break through.

<a id="Best-practices"></a>
## Best practices

Assign urgency honestly to preserve trust. Time Sensitive belongs to events happening now or within an hour, not merely content the app wants noticed. The system introduces and periodically re-evaluates this permission with the person, who can turn it off.

<a id="Sending-marketing-notifications"></a>
## Sending marketing notifications

Send promotions only after an explicit opt-in describing the content with a clear accept/decline choice. Never classify marketing as Time Sensitive. Provide an in-app notification settings screen so people can change informational and marketing preferences.

<a id="Platform-considerations"></a>
## Platform considerations

No additional iOS, iPadOS, macOS, tvOS, or visionOS rules are specified.

<a id="watchOS"></a>
### watchOS

Watch generally inherits the companion iPhone's notification settings. People can change them in the iPhone Watch app or through per-notification actions after a left swipe, such as temporary mute or disabling Time Sensitive alerts.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/UserNotifications>

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2021/10091>
  <https://developer.apple.com/videos/play/wwdc2020/10095>
