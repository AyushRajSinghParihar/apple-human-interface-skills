Keep one consistent Mac interface, with touch as an additional input. Apple’s updated guidance calls for preserving Mac control sizes and density while using larger touch targets and controls that expand during touch interaction. [Designing for macOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos)

| Proposal | Do this instead |
|---|---|
| Make everything 44 pt tall and spread out the toolbar | Keep the familiar toolbar layout. Enlarge touch **hit regions** without unnecessarily enlarging visible controls. Ensure adjacent targets remain unambiguous. |
| Switch to a larger “touch mode” | Keep layout, selection, and tool state stable as people switch between touch, keyboard, and pointer. Allow individual controls to expand temporarily when touched. |
| Make Smart Erase exclusive to a two-finger gesture | Expose Smart Erase as a discoverable tool and menu command usable with a pointer and keyboard. A custom gesture can supplement that access; preserve standard gestures and avoid system conflicts. [Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures) |
| Leave Shift-drag without touch support | Make **Shift + touch-drag** produce the same result as Shift + pointer-drag. For use without the keyboard, consider an explicit option such as “Constrain proportions.” |
| Leave essential hover controls inaccessible | Reveal relevant hidden controls when someone taps their general location, preserving the current selection. Also expose essential actions in a touch-and-hold context menu. Hide revealed controls after use or inactivity; don’t permanently display every hover control. [Pointing devices](https://developer.apple.com/design/human-interface-guidelines/pointing-devices) |
| Leave the small stepper and slider untouched | Use native expanding controls where available, and verify equivalent behavior for custom controls. Keep them compact at rest, with larger interaction surfaces during touch. Provide a synchronized numeric brush-size field for exact adjustments. [Design for touch on Mac](https://developer.apple.com/videos/play/tech-talks/111456/) |

Design for brief, intentional reaches to the screen; retain efficient pointer and keyboard workflows for sustained drawing.

Before shipping, test switching inputs mid-task, accurate targeting in the dense toolbar, selection preservation when revealing controls, and precise brush-size adjustment. These are acceptance checks; physical usability hasn’t been tested here.