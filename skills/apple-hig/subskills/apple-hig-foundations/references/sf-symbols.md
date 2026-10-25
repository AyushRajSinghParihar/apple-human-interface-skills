# SF Symbols

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/sf-symbols) · Retrieved 2026-10-25.

This is original application guidance based on the source text. Independent media review is recorded separately in the coverage report.

SF Symbols offers configurable glyphs aligned with San Francisco text. Check individual symbol and feature availability against the deployment OS. Symbols and confusingly similar forms must not become app icons, logos, or other trademarks; inspect the license and per-symbol restrictions.

<a id="Rendering-modes"></a>
## Rendering modes
Symbols contain semantic layers. Monochrome gives all layers one tint with transparent cutouts. Hierarchical varies one tint’s opacity by layer importance. Palette assigns multiple colors; with two colors for three hierarchy levels, secondary and tertiary share a color. Multicolor uses intrinsic meaning-bearing colors and may allow tinting some layers. Use system colors for appearance/accessibility adaptation. Even automatic mode needs legibility checks at actual sizes and backgrounds.

<a id="Gradients"></a>
## Gradients
SF Symbols 7 adds single-source-color linear gradients across rendering modes, custom/system colors, and custom symbols. They work at all sizes but show best on large symbols.

<a id="Variable-color"></a>
## Variable color
Represent changing strength, capacity, or another quantity by activating layers at thresholds from 0–100%. Exclude stable parts, such as a speaker body, from the changing layers. Use hierarchical rendering for depth; variable color communicates change rather than spatial hierarchy.

<a id="Weights-and-scales"></a>
## Weights and scales
Nine weights, ultralight through black, correspond to San Francisco text weights. Small, medium (default), and large scales are relative to cap height. Change scale to adjust symbol emphasis without breaking weight matching to same-point-size text.

<a id="Design-variants"></a>
## Design variants
Outline generally suits text-adjacent lists/toolbars; fill adds emphasis for selected tabs and swipe actions. Enclosing circles/squares can improve small-size clarity; slash expresses negation/unavailability. Variants can combine, and standard views often select outline/fill automatically. Language/script variants adapt to device language across Latin, Arabic, Hebrew, Hindi, Thai, CJK, Cyrillic, Devanagari, and Indic numerals.

<a id="Animations"></a>
## Animations
Use animations to convey an action, state, or ongoing work, with speed, repetition, reversal, and playback suited to that purpose and the app’s tone. Avoid concurrent effects that distract or send conflicting signals.

|Effect|Meaning and behavior|
|---|---|
|Appear / Disappear|Gradual entry / exit|
|Bounce|One elastic enlargement or movement then original state; normally plays once|
|Scale|Persistent size change until reset or effect removal|
|Pulse|Opacity changes on annotated layers or optionally all layers; useful for ongoing work|
|Variable color|Cumulative or one-layer-at-a-time sequence; may autoreverse or hide inactive layers|
|Replace|Down-up for state change, up-up for forward progression, off-up to emphasize next state|
|Magic Replace|Related shapes intelligently transition badges/slashes; unrelated pairs fall back to down-up or a chosen direction|
|Wiggle|Directional back-and-forth emphasis, including a potentially missed action|
|Breathe|Opacity and size change together to suggest ongoing activity|
|Rotate|Whole-symbol or selected-layer rotation, such as fan blades|
|Draw On / Draw Off|SF Symbols 7 path drawing using guide points; simultaneous, staggered, or sequential layers|

Variable-color open-loop symbols have endpoints that do not meet; closed-loop shapes support seamless continuous repetition. All library symbols and custom symbols can animate across modes, weights, and scales, but custom art needs testing.

<a id="Custom-symbols"></a>
## Custom symbols
Export a similar template and edit vectors while matching detail, optical weight, alignment, position, and perspective. Keep the meaning simple, inclusive, recognizable, and directly tied to content or action. Do not modify copyrighted Apple product/feature symbols marked by an Info badge, nor reproduce those products in custom art.

Annotate layers with hierarchy or colors for supported modes. Negative side margins can optically align wide badges; follow names such as `left-margin-Regular-M`. Annotate animation layers/groups and use Z-order for variable-color sequence direction. Test every preset. Whole underlying shapes plus an annotated erase layer preserve information for correct animation better than destructive cutouts. Use the component library for common badges/enclosures rather than baking variants into the base. Add accessible labels for custom symbols.

<a id="Platform-considerations"></a>
## Platform considerations
No extra platform-specific rules are provided.

<a id="Resources"></a>
## Resources
Consult the [official article](https://developer.apple.com/design/human-interface-guidelines/sf-symbols) for linked Apple design assets and implementation resources.

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
Source revision dates: July 28, 2025, June 10, 2024, June 5, 2023, September 14, 2022.
