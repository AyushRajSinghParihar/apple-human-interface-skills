Keep one stable Mac interface, with touch as an additional input. Apple’s [macOS touch guidance](https://developer.apple.com/design/human-interface-guidelines/gestures#macOS) supports these changes:

| Proposal | Do this instead |
|---|---|
| Make every control 44 pt tall and spread out the toolbar | Preserve normal Mac control sizes and spacing. Enlarge **tap targets beyond visual bounds** where needed; prefer standard framework controls, which get system-configured targets. |
| Switch to a larger “touch mode” | Keep layout and control sizes stable as people switch between touch, keyboard, and pointer. |
| Make Smart Erase exclusive to a two-finger gesture | Expose it as a tool or command usable with keyboard and pointer. Treat the gesture as an optional shortcut, support touch and trackpad, and test for conflicts with system gestures. |
| Leave Shift-drag and hover actions without touch alternatives | Add touch-accessible equivalents—for example, a constraint toggle for Shift-drag and tapping to reveal hidden actions. |
| Leave the small stepper and slider unchanged | Use native expanding controls. For custom controls, consider a temporary enlarged version that remains visible during manipulation and briefly after release. |

For hover menus specifically, Apple recommends revealing hidden controls when someone taps their general location. See [Pointing devices](https://developer.apple.com/design/human-interface-guidelines/pointing-devices).