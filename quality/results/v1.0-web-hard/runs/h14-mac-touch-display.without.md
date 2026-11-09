Keep one consistent Mac interface that supports touch, mouse, trackpad, and keyboard. Revise the proposal as follows:

| Proposal | What to do instead |
|---|---|
| Make everything 44 pt tall and spread out the toolbar | Preserve normal Mac control sizes and density. Enlarge **touch hit regions** without enlarging every visible control or spacing out the whole toolbar. Apple recommends larger tap targets while retaining the Mac layout. |
| Switch to a larger “touch mode” | Keep controls in predictable positions as people switch inputs. Adapt individual interactions when touched rather than changing the entire layout. |

These changes follow Apple’s [macOS design guidance](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos).

- **Make Smart Erase available through a visible tool or command**, usable with touch and a pointer, with keyboard access. A custom two-finger gesture can be an optional shortcut, provided it doesn’t conflict with standard gestures. Core functionality needs alternatives to gestures. [Accessibility guidance](https://developer.apple.com/design/human-interface-guidelines/accessibility)
- **Support Shift-drag with touch as well as a pointer.** Also offer an onscreen option, such as a “Constrain proportions” toggle, so the same result is possible without holding Shift.
- **Give essential hover controls a touch path.** Reveal them when someone taps their general location, preserve the current selection, and also expose essential actions in a touch-and-hold context menu. Hide temporary controls when finished; don’t make every hover element permanently visible. [Pointing-device guidance](https://developer.apple.com/design/human-interface-guidelines/pointing-devices)
- **Update the stepper and brush-size slider for touch.** Prefer native controls that expand during touch interaction. Custom versions should provide equivalent temporary expansion and comfortable adjustment while retaining their compact resting appearance. [Design for touch on Mac](https://developer.apple.com/videos/play/tech-talks/111456/)

Validate complete drawing workflows using touch alone, then while alternating between touch, keyboard, and pointer—especially selecting tools, constraining edits, erasing, and adjusting brush size.