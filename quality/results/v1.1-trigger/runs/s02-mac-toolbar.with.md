Based on your description, I’d prioritize three changes:

1. **Remove the custom window-close button.** If it closes the window, use the standard macOS close control at the upper left. A second close button among toolbar actions creates ambiguity and risks accidental dismissal. If it ends a specific task, use a clear action such as “Done” or “Cancel.” [HIG: Windows](https://developer.apple.com/design/human-interface-guidelines/windows)

2. **Make ambiguous actions readable.** Icon-only buttons are appropriate for recognizable actions; unfamiliar commands need text. Add descriptive tooltips and meaningful accessibility labels to icon buttons. Missing visible labels alone doesn’t establish that VoiceOver labels are missing—those need verification. [HIG: Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars) · [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)

3. **Reassess the 14-button default.** Apple doesn’t prescribe a universal maximum, but that many equally prominent actions can make scanning difficult. Keep frequent actions visible, group related tools, and consider customization. Use native toolbar overflow as the window narrows. Every toolbar action should also have a menu-bar command. [HIG: Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars)

My suggested layout is navigation/sidebar controls on the left, a smaller set of grouped common tools in the center, and inspector/search or a primary task action on the right.

This is a description-based review; actual spacing, symbol clarity, narrow-window behavior, and keyboard/VoiceOver operation remain unverified.