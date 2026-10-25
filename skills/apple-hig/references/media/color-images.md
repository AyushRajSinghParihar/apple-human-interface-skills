# Color: lessons from the visual examples

Source: [Apple HIG — Color](https://developer.apple.com/design/human-interface-guidelines/color), independently inspected in the 2026-10-25 snapshot. These are original descriptions; no Apple artwork is included.

## Appearance and emphasis

A note-editing interface keeps the same controls and selection across light, dark, and increased-contrast presentations, while their actual color values change. Preserve the role and readability of a color rather than matching one screenshot's pixels.

The toolbar comparison gives every control a saturated blue background in the rejected design. In the clearer design, only the completion action has that strong fill; close, formatting, and sharing controls recede. A colored primary action communicates priority only when other controls leave it room.

## Cultural interpretation

The two market charts show the same rising curve with different locale conventions: green in the English example and red in the Chinese example. A rising or falling value needs meaningful text, shape, and a locale-aware interpretation; a color's familiar meaning in one market is insufficient evidence for another.

## Adaptive references

The source swatches demonstrate separate ordinary-light, ordinary-dark, increased-contrast-light, and increased-contrast-dark values. The local Color article retains the dated RGB reference tables. Use system color APIs for the actual interface because these values and their rendering context can change.
