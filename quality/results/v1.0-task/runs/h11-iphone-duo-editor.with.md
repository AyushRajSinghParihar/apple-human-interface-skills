Change all six points. Apple’s [iPhone Duo guidance](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo) calls for an adaptable iPhone experience that preserves the editing task through folding.

| Your plan | Recommended change |
|---|---|
| Fixed 375 pt outer layout and two fixed inner panels | Use **available size, size classes, safe areas, layout margins, and reserved regions**. Support continuous resizing and Split View. Preserve the selected photo, edits, and editing context when opening or closing. |
| Move outer-display toolbars and tabs to the top | Preserve **system side placement** on the outer display and the inner display in landscape. Inner portrait uses ordinary horizontal bars. Keep controls near the pane they affect. |
| Mirror the side toolbar in Arabic and Hebrew | Keep hardware-aligned bars on the **same physical side**, including in RTL. Localize reading order and directional navigation separately. Respect asymmetric safe areas and either-side multitasking. |
| Icons with no titles | Supply **a meaningful symbol and a localized title**, unless an item is text-only. Compact bars can show symbols; expanded representations and overflow need titles. Titles needn’t remain visibly displayed everywhere. |
| Custom canvas ignores the partly folded hinge | Make the custom layout respond to the **center folding reserved region**. Keep necessary controls and editing interactions usable on either side, with modest adjustments as the fold changes. Full-screen drawing doesn’t exempt the canvas from reserved-region handling. |
| Controls remain over the active inner camera | Move controls aside when the **inner camera reserved region becomes active**. Respond dynamically when camera use begins and ends. |

The placement, RTL, and labeling rules are covered under [Vertical controls](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls); hinge and camera handling are covered under [Reserved regions](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Reserved-regions).

For this photo editor, I’d also prioritize editing tools over tabs during the editing task, keeping secondary commands in system overflow. Define toolbar group priorities so common actions and completion controls stay reachable.

Before sign-off, preview closed → open → partially folded → closed, camera activation, Arabic/Hebrew, and Split View on either side. Verify that edits persist and every action remains reachable. **The six proposed decisions fail the guidance review; runtime behavior hasn’t been tested.**