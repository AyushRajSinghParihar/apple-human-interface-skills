# Drag and drop

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/drag-and-drop)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Drag and drop transfers selected content from a source to a destination in one container, across containers, or across apps. Defaults generally move within a container and copy between containers; interapp drops always copy. Support the platform's touch, pointer, keyboard-accessibility, VoiceOver, and spatial gestures where available, including Universal Control between Mac and iPad.

<a id="Best-practices"></a>
## Best practices

Support dragging consistently, using native text components' built-in behavior. Always offer another route, such as copy/move commands, and expose accessible source/destination descriptors. Change move/copy defaults only with strong expected behavior and data-loss considerations. Allow grouped items when useful, including adding items during an iPad drag. On Mac, people can gather a group from selections in several apps. Prefer undo, confirm an irreversible drop where needed, or offer a meaningful reversal such as canceling a share. Offer content representations from richest to simplest: for example native object, vector PDF, transparent PNG, then JPEG. Consider spring-loaded controls: iPad hovering can activate, while Mac force-click can activate without releasing the drag.

<a id="Providing-feedback"></a>
## Providing feedback

Show a translucent drag representation after about 3 pt of movement and retain it through the drop. Adjust size or flock multiple items when it clarifies the expected result, avoiding constant radical changes. Highlight only the currently eligible target or show an unavailable cue; remove feedback on exit. On failure, visibly return to source or use a fade/expansion disappearance rather than implying success.

<a id="Accepting-drops"></a>
## Accepting drops

Autoscroll a destination near its edges while the drag remains inside. Choose the richest accepted representation and extract only relevant fields, such as a contact's email for a recipient field. Check Option at drop time for an in-container forced copy; releasing it before drop restores move. Show transfer progress and a placement placeholder for slow drops, and report when dropping initiates a task such as printing. Preserve compatible text styles or adopt destination styling when incompatible. Keep dropped content selected. For an in-container copy, deselect the original; for an intercontainer transfer, deselect source content; moved content leaves the source.

<a id="Platform-considerations"></a>
## Platform considerations

Drag and drop is unsupported in tvOS and watchOS.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

Support adding items to an active drag, flocking feedback, and multiple simultaneous drops as needed for multitouch gathering.

<a id="macOS"></a>
### macOS

Allow export to Finder in a format the app can reopen, such as an event file, or a clipping where appropriate; a clipping is distinct from Clipboard. Permit dragging a background selection without activating its window. When possible, dragging an unselected background item should not disturb the existing selection. A count badge can show dragged/accepted item count, and pointer shapes can communicate copy, link, disappearance, or rejection. Prefer one continuous select-and-drag motion for a single item.

<a id="visionOS"></a>
### visionOS

Associate draggable content with a user activity where possible so dropping into empty space opens the appropriate window/scene, as with a URL or Quick Look content. People pinch and hold a virtual object while dragging it in any direction, including along depth.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Universal Control](https://support.apple.com/en-us/HT212757)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/UIKit/drag-and-drop> — UIKit
<https://developer.apple.com/documentation/AppKit/drag-and-drop> — AppKit
<https://developer.apple.com/documentation/FileProvider>

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2021/10059>
  <https://developer.apple.com/videos/play/wwdc2021/10289>
  <https://developer.apple.com/videos/play/wwdc2020/10206>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: October 24, 2023, June 21, 2023.
