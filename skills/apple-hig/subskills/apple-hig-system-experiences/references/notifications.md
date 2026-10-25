# Notifications

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/notifications)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Notifications deliver timely high-value information after consent. People control styles, urgency, delivery, previews, sound, and badges through system settings.

<a id="Anatomy"></a>
## Anatomy

Notifications can appear as banners, Lock/Home/desktop views, badges, and Notification Center entries. Direct communications can emphasize a sender or group image/name instead of the ordinary app-icon treatment.

<a id="Best-practices"></a>
## Best practices

Keep updates concise and useful; do not repeat the same event because the person has not responded. Avoid instructions that require remembering a later app task; offer an immediate action when useful. Use alerts for error situations. In the foreground, integrate incoming information subtly into the current UI instead of duplicating it with an interruption. Do not expose confidential, personal, or sensitive details to nearby observers.

<a id="Content"></a>
## Content

Use a brief title only when it adds context; direct communications use the sender's name, and generic noncommunication titles can defer to the app name. Titles use title case without punctuation. Bodies use short complete sentences with sentence case/punctuation; leave truncation to the system. Provide a generic preview-hidden description that conveys category without private details. Do not repeat app name or icon because the system supplies them, including a small app badge on communication avatars. Sound can reinforce identity but cannot be the sole essential signal. Custom sounds should be brief, distinctive, and well produced; custom vibration alongside them is not programmatically available through this guidance.

<a id="Notification-actions"></a>
## Notification actions

Offer up to four simple useful actions that save opening the app. Use short title-case outcome labels and recognizable glyphs, without app branding or filler. Do not add an Open App button when ordinary notification activation already opens its related content. Prefer nondestructive actions; mark and adequately contextualize any destructive one.

<a id="Badging"></a>
## Badging

Use badge numbers for unread notifications, never unrelated temperatures, dates, prices, or scores. Clear/update them promptly when notifications are addressed; a count of zero removes related entries from Notification Center. Keep important information discoverable in the app because badges can be disabled. Do not imitate badges with a custom component to bypass that preference.

<a id="Platform-considerations"></a>
## Platform considerations

No additional iOS, iPadOS, macOS, tvOS, or visionOS rules are specified.

<a id="watchOS"></a>
### watchOS

Watch delivery uses short and long looks and Notification Center. A companion iPhone app can supply default watch interfaces; custom relevant assets/actions improve the result.

<a id="Short-looks"></a>
#### Short looks

Raised-wrist short looks disappear when the wrist lowers. Keep them discreet and basic, especially the title, and deliver critical information elsewhere too because this presentation is brief.

<a id="Long-looks"></a>
#### Long looks

Long looks offer more detail and scroll with touch or crown, dismissing on tap or lowered wrist. Static views include a message plus prepared text/images; dynamic views access full notification content. Keep the system sash and bottom Dismiss structure. Always package a static fallback for offline/unreachable-companion cases and prefer a dynamic view too. Rich custom content and interruptible animation can avoid opening the app. Tint or blur the sash; blur suits a top photo. Content defaults transparent; white at 18% opacity matches system notification backgrounds, or use a suitable custom color. Up to four custom buttons appear above the fixed Dismiss action; companion notification categories can configure them.

<a id="Double-tap"></a>
#### Double tap

Supported watches invoke the first nondestructive action for double tap. Place the most likely response first, such as the commonly chosen time extension.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Managing notifications](https://developer.apple.com/design/human-interface-guidelines/managing-notifications)
[Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/UserNotifications/asking-permission-to-use-notifications> — User Notifications
<https://developer.apple.com/documentation/UserNotificationsUI>
<https://developer.apple.com/documentation/UserNotifications>

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2021/10091>
  <https://developer.apple.com/videos/play/wwdc2020/10095>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: October 24, 2023.
