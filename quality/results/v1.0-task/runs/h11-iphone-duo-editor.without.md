I’d revise all six points. Apple’s [iPhone Duo design guidance](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo) calls for these changes:

| Your plan | What to change |
|---|---|
| Fixed 375 pt layouts | Use resizable layouts, size classes, margins, and safe areas. Support compact outer and regular inner layouts, plus multitasking sizes. |
| All bars at the top | Follow system vertical bars on the outer display and inner landscape. Inner portrait retains horizontal bars. |
| Mirror the side toolbar for Arabic/Hebrew | Keep it on the same physical side; its placement follows the hardware. Localize its contents appropriately. |
| Icons without titles | Supply both symbols and localized titles. Icons can appear alone, but overflow and expanded presentations need titles. |
| Canvas ignores the fold | Use reserved-region APIs for custom UI; keep important content and interactive handles clear of the folding region. |
| Controls cover the active inner camera | Move controls aside when the camera activates and its reserved region appears. |

For the editor, keep the photo, editing state, and tools consistent across displays. Use extra inner-display space for an inspector or tool panel, with small adjustments as the device folds. An immersive canvas can span the display, provided its controls remain accessible. [Apple’s design walkthrough](https://developer.apple.com/videos/play/tech-talks/111466/)

Because editing is task-focused, prioritize editing actions when space runs short: minimize the tab bar and use system overflow for secondary actions.