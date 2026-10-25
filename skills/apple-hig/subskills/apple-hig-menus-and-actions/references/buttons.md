# Buttons

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/buttons)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

## Contents

- [Best practices](#Best-practices)
- [Style](#Style)
- [Content](#Content)
- [Role](#Role)
- [Platform considerations](#Platform-considerations)

A button performs an immediate action. Its visual style, visible symbol/text, and semantic role work together to explain what activation does.

<a id="Best-practices"></a>
## Best practices

Allow enough surrounding space for clear separation and easy selection. General hit regions should be at least 44×44 pt; visionOS targets need 60×60 pt. Custom buttons always need press feedback.

<a id="Style"></a>
## Style

Prefer system styles for built-in states, accessibility, and appearance adaptation. Use one or two prominent buttons per view for likely actions. Distinguish a preferred option through style rather than making related buttons different sizes. Keep label colors distinct from colorful content; the default monochrome often works best over rich backgrounds.

<a id="Content"></a>
## Content

Use a familiar symbol for a familiar action; use a short title-case verb phrase when words are clearer. Mac and visionOS can provide brief hover tooltips; text-labeled buttons usually explain themselves.

<a id="Role"></a>
## Role

Normal has no special meaning; primary is the expected/default action; Cancel abandons the current action; destructive signals data loss. Roles affect rendering, such as accent fill for primary and red for destructive. Primary can respond to Return and close a temporary view. Generally assign primary only to a nondestructive likely action. Application advice: consult the alert-specific deliberate-destruction exception before prescribing confirmation behavior.

<a id="Platform-considerations"></a>
## Platform considerations

No additional tvOS rules are specified.

<a id="iOS-iPadOS"></a>
### iOS, iPadOS

For delayed completion, show an activity indicator within the activating button, optionally changing its label to the current operation. The indicator replaces any button image while preserving context for the wait.

<a id="macOS"></a>
### macOS

<a id="Push-buttons"></a>
#### Push buttons

The standard push button can show text, imagery, or both and can serve as default. Use flexible height for tall icons or multiple text lines, otherwise retain standard sizing. Append an ellipsis when the button opens another window/view/app for further input. Consider spring loading through a dragged selection plus force-click on Magic Trackpad, preserving the drag afterward.

<a id="Square-buttons"></a>
#### Square buttons

These small glyph-only controls affect a nearby view, for example adding/removing table rows. They can act as push, toggle, or pop-up controls. Use them in the body rather than the frame, toolbar, or status bar. Prefer system symbols and omit introductory labels when proximity explains the function.

<a id="Help-buttons"></a>
#### Help buttons

Use the familiar system question-mark control, at most one per window, opening context-specific help when possible and top-level help otherwise. In a dialog with dismissal controls, place it in the opposite lower corner, aligned vertically with those controls. Without dismissal controls, or in settings, use either lower corner. Keep it in the view body and omit explanatory introductory text.

<a id="Image-buttons"></a>
#### Image buttons

Image buttons can act as push, toggle, or pop-up controls inside a view. Toolbar imagery instead belongs to a toolbar item. Allow about 10 pixels between image and clickable button edges and generally omit a visible system border. Put any needed label beneath the image.

<a id="visionOS"></a>
### visionOS

Buttons normally have a visible background and audible feedback. Circle suits glyph-only content, rounded rectangle or capsule suits text, and capsule suits text plus glyph. Standard states supply feedback; custom hover effects are not supported. A look-triggered tooltip can explain a glyph.

| Shape | Supported visual sizes |
| --- | --- |
| Circle | Mini 28 pt; small 32 pt; regular 44 pt; large 52 pt; extra large 64 pt |
| Text capsule | Small 32 pt; regular 44 pt; large 52 pt |
| Text-and-icon capsule | Regular 44 pt; large 52 pt |
| Rounded rectangle | Small 32 pt; regular 44 pt; large 52 pt |

Visual size does not remove the 60-pt targeting requirement. Use a discernible shape/fill except inside a larger clearly bounded toolbar, menu, alert, or ornament. On window glass, thin material suits the button; floating in space, use glass. Reserve white fill with black content for the system's toggled state. Prefer round/capsule forms for steady gaze, and a capsule for a standalone button. Keep centers at least 60 pt apart; add 4 pt padding around buttons 60 pt or larger to prevent hover overlap. Avoid rows/stacks of mini/small buttons. Prefer rounded rectangles for vertical text stacks and capsules for horizontal rows. Standard sounds matter because visionOS provides no haptics.

<a id="watchOS"></a>
### watchOS

Inline buttons are capsules with a contrasting material. Put corner actions in a toolbar so the system relocates title/time and gives controls Liquid Glass. Full-width buttons suit primary actions. Side-by-side buttons should share height and use short labels or glyphs; vertical one- and two-line buttons should also maintain common heights. Toolbar actions can navigate related areas or operate on current content.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Pop-up buttons](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons)
[Pull-down buttons](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons)
[Toggles](https://developer.apple.com/design/human-interface-guidelines/toggles)
[Segmented controls](https://developer.apple.com/design/human-interface-guidelines/segmented-controls)
[Location button](https://developer.apple.com/design/human-interface-guidelines/privacy#Location-button)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/SwiftUI/Button> — SwiftUI
<https://developer.apple.com/documentation/UIKit/UIButton> — UIKit
<https://developer.apple.com/documentation/AppKit/NSButton> — AppKit

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: December 16, 2025, June 9, 2025, February 2, 2024, December 5, 2023, June 21, 2023, June 5, 2023.
