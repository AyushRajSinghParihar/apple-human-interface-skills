---
name: apple-hig-sf-symbols
description: Use when selecting or configuring SF Symbols, rendering modes, weights, variants, variable color, animations, custom symbols, or symbol availability.
---

# Configure the symbol's meaning before its decoration

Read [SF Symbols](../../references/sf-symbols.md). Inspect the intended action/state, neighboring type, background, deployment OS, and existing glyph implementation. Establish design, review, or adaptation mode. Produce the requested symbol assignment/configuration or custom-symbol specification within the existing stack. Check individual symbol/feature availability and licensing; library symbols cannot become product trademarks or app icons.

Select the semantic variant before styling: outline for ordinary text-adjacent controls, fill for supported emphasis/selection, enclosure for small-size clarity, or slash for negation. Let standard views choose variants when appropriate. Match symbol weight to adjacent text, then use scale to adjust emphasis without mismatching stroke weight.

Choose rendering by information. Monochrome suits one tint; hierarchical communicates layer importance; palette assigns intentional semantic colors; multicolor preserves intrinsic meaning. Variable color represents a quantity by activating layers and should exclude stable parts. It is not a substitute for hierarchy. Use adaptive colors and test the actual size/background rather than trusting automatic rendering.

If animating, select an effect whose meaning matches the event: a once-only bounce for feedback differs from ongoing pulse/breathe activity or a replacement state transition. Avoid simultaneous effects that conflict. For custom art, start from an appropriate template, preserve optical alignment, annotate whole layers/erase behavior and animation groups, and test presets. Do not modify restricted Apple product/feature symbols.

**Before → decision → after:** A fan control bounces forever and changes the whole icon's tint to show speed. Decision: rotation conveys operation while variable layers can convey quantity; the housing stays stable. After, an appropriate supported symbol configuration separates operating feedback from a labeled speed value, respects motion preferences, and keeps its housing readable.

Deliver names, supported variants/modes, state mapping, and fallback choices or implementation. Fail if a symbol is unavailable on the deployment OS, rendering erases a meaningful layer, or animation implies work after it stopped. Native/custom-symbol animation and localized variants require actual supported previews; static inspection cannot verify them.

Use [Icons](../apple-hig-icons/SKILL.md) when selecting a metaphor, [Motion](../apple-hig-motion/SKILL.md) for interaction timing, or [Right to left](../apple-hig-right-to-left/SKILL.md) for directional semantics.
