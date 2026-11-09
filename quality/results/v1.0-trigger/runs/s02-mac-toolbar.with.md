Based on your description, I’d revise the toolbar in three areas:

- **Remove the custom Close button if it closes the window.** Use macOS’s standard close control at the upper left. A second close control at the right creates ambiguity and uses space intended for app actions. If it finishes an editing task instead, give it an appropriate label such as **Done**. [Apple: Windows](https://developer.apple.com/design/human-interface-guidelines/windows)
- **Review which of the 14 actions need constant visibility.** Fourteen isn’t automatically a violation, but it can make frequently used commands harder to find. Keep the main actions visible, group related tools, consider customization, and let the standard toolbar handle overflow as the window narrows. [Apple: Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars)
- **Make each action understandable.** Icon-only buttons are appropriate for familiar, recognizable actions. Use text where a symbol’s meaning is unclear, add brief tooltips, and ensure every icon-only control has an accessible action name. Visible labels aren’t required on every button. [Apple: Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons)

Also ensure **every toolbar action is available in the menu bar**, so people retain access when the toolbar is hidden or customized.

This is a description-based review; icon recognition, spacing, menu coverage, accessibility names, and narrow-window behavior remain unverified.