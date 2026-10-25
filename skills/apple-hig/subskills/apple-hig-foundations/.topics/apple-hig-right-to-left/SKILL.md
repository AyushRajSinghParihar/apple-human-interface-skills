---
name: apple-hig-right-to-left
description: Use when adapting or reviewing Apple-platform layouts, text, numbers, controls, sequences, or custom symbols for Arabic, Hebrew, or mixed-direction content.
---

# Mirror meaning rather than every pixel

Read [Right to left](../../references/right-to-left.md). Inspect target language/region, text samples, custom layout/assets, and the intended task. Establish design, review, or adaptation mode. Preserve the existing framework's directional behavior before adding manual overrides; mark locale-specific assumptions requiring native-language review.

Classify each directional element. Reading-order navigation, progress controls, endpoint labels, and meaningful ordered image collections generally reverse position/direction. Literal physical directions or controls aimed at a specific onscreen place retain that meaning. Preserve photographs, logos, universal signs, and ordinary object/tool handedness; localize strongly directional art rather than blindly flipping it.

Handle text at the right level. Short labels follow interface alignment; longer paragraphs follow their own language, including mixed-language content. Keep list alignment consistent even when one entry uses another script. Preserve digit order in numbers, phones, and card numbers while adapting locale-specific numeral/currency formatting and the position of ordered sequences.

Use directional/localized SF Symbol variants. Review a custom complex glyph component by component: its base, badge position, actual text, and negation slash can have different needs. If Latin uppercase neighbors Arabic/Hebrew labels, evaluate optical balance rather than assuming equal numeric point size looks equal. Hardware-linked controls retain any platform-specific physical placement instead of inheriting a generic mirror rule.

**Worked transformation:** Before, an Arabic cycling app flips the map photo, bicycle glyph, phone digits, and Back arrow together. Decision: only reading-order navigation should mirror; the other elements describe real content or fixed sequences. After, Back and progress order adapt, the map/photo and bicycle handedness remain correct, and phone digits retain their internal order under localized formatting.

Deliver a corrected directional screen/asset mapping or implementation. Fail if reading-order navigation points the wrong way, digits reverse internally, real artwork changes meaning, or a mixed-language paragraph follows the wrong alignment. Use representative content in actual layout; screenshots cannot verify keyboard/cursor/bidirectional editing behavior.

Use [Layout](../apple-hig-layout/SKILL.md) for adaptable leading/trailing structure, [SF Symbols](../apple-hig-sf-symbols/SKILL.md) for localized glyphs, or [Writing](../apple-hig-writing/SKILL.md) for translated wording.
