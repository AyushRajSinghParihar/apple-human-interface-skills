# Apple Pencil and Scribble

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

Pencil supports precise drawing, annotation, handwriting, and control activation on iPad. Scribble converts handwriting to text privately on-device.

<a id="Best-practices"></a>
## Best practices
Honor physical-pencil expectations, including writing in margins. Let marks appear immediately without a preliminary mode switch. Allow Pencil to activate ordinary controls so people can stay with one input. Respond naturally to supported tilt, pressure, orientation, and barrel roll; use pressure for continuous qualities such as opacity or brush size. Feedback should directly follow the content touched. Keep controls clear of either hand, with repositioning if necessary.

<a id="Hover"></a>
## Hover
Preview the likely mark’s size/color before contact; avoid continually changing the preview with height, which adds distraction without predicting the stroke. Never initiate an action merely from hover. Use a representative middle value for pressure-sensitive properties so the preview is visible without covering the canvas. A squeeze/modifier can reveal nearby contextual tool choices. Restrict marking previews to Pencil where mouse previews would be confusing.

<a id="Double-tap"></a>
## Double tap
Respect the person’s preferred mapping when meaningful: current tool/eraser, current/previous tool, color picker, or no action. If these do not fit, use a suitable mode change. Offer custom behavior as an explicit opt-in choice and make the active mode discoverable. Avoid content-changing or destructive operations because accidental taps happen; prefer easily reversible changes.

<a id="Squeeze"></a>
## Squeeze
Pencil Pro squeeze can invoke an app action or a user-selected App Shortcut. It works only while the paired screen is on and the tip is not touching it; the result may occur outside the person’s visual attention. Treat a squeeze as one quick discrete action, not sustained or rapid repeated pressure. Show resulting UI near the tip and keep actions nondestructive and reversible.

<a id="Barrel-roll"></a>
## Barrel roll
Use Pencil Pro rotation to vary a mark, such as a highlighter angle. Reserve barrel roll for marking behavior rather than navigation or displaying controls.

<a id="Scribble"></a>
## Scribble
Standard text fields/views, search, and editable web text support handwriting automatically except password fields. Custom fields should accept writing without prior focus/tap. Enable natural text-entry spaces beyond visible fields where appropriate. Hide placeholders when writing begins and avoid distracting autocomplete. Keep the target field and transcribed text stationary during writing and selection; defer unavoidable move/resize/autoscroll until a pause. Provide a sufficiently large writing area, enlarging before entry or during a pause rather than mid-stroke.

<a id="Custom-drawing"></a>
## Custom drawing
PencilKit provides a low-latency canvas, tools, and ink. Its colors normally adapt to Dark Mode, but disable that dynamic change when annotating fixed art such as a photo/PDF so marks remain visible. Regular-width tool pickers include undo/redo; compact ones do not, so consider toolbar alternatives and standard three-finger undo/redo gestures.

<a id="Platform-considerations"></a>
## Platform considerations
This source limits Pencil/Scribble guidance to iPadOS and marks the other platforms unsupported.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble) for linked Apple design assets and implementation resources.

<a id="Related"></a>
#### Related
The official article links the adjacent HIG topics relevant to this guidance.

<a id="Developer-documentation"></a>
#### Developer documentation
Use the framework references linked by Apple for current API availability and implementation details.

<a id="Videos"></a>
#### Videos
Apple’s linked design sessions provide demonstrations and additional implementation context; no video review is implied here.

<a id="Change-log"></a>
## Change log
Source revision dates: May 7, 2024, September 12, 2023, November 3, 2022.
