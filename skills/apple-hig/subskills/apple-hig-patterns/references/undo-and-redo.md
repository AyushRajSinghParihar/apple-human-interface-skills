# Undo and redo

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

Undo/redo supports safe exploration when people can predict the affected action and see its outcome.

<a id="Best-practices"></a>
## Best practices

Describe the target in menu labels or the iPhone shake confirmation. Reveal offscreen changes, for example scrolling to restored text, so people do not repeat undo because nothing seemed to happen. Avoid arbitrary history limits; support the meaningful action sequence since opening or saving. Group related incremental adjustments when a batch undo helps, and consider reverting a larger set. Use standard menus/shortcuts/gestures first; add dedicated buttons only when needed, with standard symbols in a toolbar.

<a id="Platform-considerations"></a>
## Platform considerations

No additional visionOS rules are specified. Undo/redo is unsupported in tvOS and watchOS in this pattern guidance.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

Preserve standard three-finger swipe and iPhone shake behavior. The system supplies Undo/Redo plus a trailing space in alert titles; add only one or two precise words describing the operation.

<a id="macOS"></a>
### macOS

Put commands at the top of Edit and preserve Command-Z for Undo and Shift-Command-Z for Redo.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback)
[Pointing devices](https://developer.apple.com/design/human-interface-guidelines/pointing-devices)
[Standard keyboard shortcuts](https://developer.apple.com/design/human-interface-guidelines/keyboards#Standard-keyboard-shortcuts)
[Edit menu](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Edit-menu)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/Foundation/UndoManager> — Foundation

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2017/802>
