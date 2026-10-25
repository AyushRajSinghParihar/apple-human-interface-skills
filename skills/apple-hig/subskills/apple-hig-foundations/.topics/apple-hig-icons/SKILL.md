---
name: apple-hig-icons
description: Use when choosing, creating, reviewing, or adapting interface glyphs or Mac document icons, including metaphors, template rendering, optical alignment, and localization.
---

# Make a glyph communicate one action or concept

Read [Icons](../../references/icons.md). Inspect the actual command/content meaning, surrounding label, available glyphs, target platforms, and requested design/review/adaptation. Distinguish interface glyphs from launcher icons before changing assets. Keep the existing stack and produce a corrected glyph assignment, asset specification, or implementation.

Name the intended action first, then choose a recognizable metaphor. For standard actions, consult the guide's mappings instead of assigning a novel symbol to a familiar command. Prefer a suitable SF Symbol; otherwise define simple tintable template artwork with consistent stroke, perspective, complexity, and weight alongside adjacent text. Use optical padding to balance asymmetric art rather than merely centering its bounding box.

If a symbol contains actual characters or reading-direction cues, localize or provide the appropriate directional form. Avoid cultural assumptions in people/metaphors; give custom glyphs meaningful accessible descriptions. Prefer scalable vector/custom-symbol assets for interface art. Use supplied authorized product symbols rather than redrawing Apple hardware.

For Mac document icons, switch from command semantics to file-type identification. Preserve the folded-paper shape, keep meaningful artwork clear of the fold, and simplify/thicken small variants down to the guide's 16 px context. Consult its document canvas and center-art specifications; app-icon canvases are not interchangeable.

**Before → decision → after:** A task toolbar uses a heart for Save and a detailed full-color illustration for Delete. Decision: familiar actions need stable, consistent metaphors. After, appropriate standard save/delete glyphs share template rendering and weight; the playful illustration moves into content where it does not imply a command.

Check each glyph at its actual displayed size beside text, in supported direction/appearance and selected state. Fail if reduction loses the metaphor, a familiar action is mislabeled, or tinting destroys essential meaning. State unverified screen-reader names or native rendering separately from visible artwork findings.

Use [SF Symbols](../apple-hig-sf-symbols/SKILL.md) for symbol variants/rendering or [App icons](../apple-hig-app-icons/SKILL.md) when identifying the product rather than an interface action.
