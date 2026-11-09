# Pointing devices: lessons from the inspected images

These original observations accompany Apple's [Pointing devices HIG](https://developer.apple.com/design/human-interface-guidelines/pointing-devices), inspected on 2026-10-25; the cursor table follows the source update of 2026-10-28. Read the [article guide](../../subskills/apple-hig-inputs/references/pointing-devices.md) for platform behavior and cursor API roles.

The padding diagrams measure outward from the visible control: approximately 12 pt on every side of the filled rounded button, and 24 pt around an unfilled label or standalone symbol. These are extended interaction regions, not instructions to enlarge the artwork by that amount. The custom-pointer example displays live width and height beside a resize handle; its sample dimensions illustrate useful feedback, not required values.

The Mac cursor examples communicate operation through shape. Preserve system cursor roles and appearance rather than drawing replacements:

| Visible cue | Meaning retained in the article guide |
|---|---|
| Diagonal arrow | Ordinary selection |
| Open hand, then closed fist | Content can be dragged, then is being dragged |
| Arrow beside a miniature menu | Contextual menu |
| Crosshair | Precise selection |
| Arrow with an X badge | Dropped reference disappears; original item is retained |
| Arrow with a plus badge | Copy while dragging |
| Curved arrow | Create a link or alias while dragging |
| Insertion beam, oriented for the text direction | Text insertion |
| Arrow with a prohibition badge | Drop is unavailable |
| Extended index finger | URL link |
| Arrow against a perpendicular bar, or paired opposing arrows | Resize in the indicated direction or axis |
| Magnifier with a plus or minus sign | Zoom in or out of a canvas or object |

A one-way resize pointer shows the allowed direction as a black triangle and the blocked direction as a gray one; the two-way form shows both in black. In the source update of 2026-10-28, each cursor image has a light appearance only. Use the system pointers instead of drawn replacements, so that these small differences stay accurate.
