---
name: apple-hig-typography
description: Use when choosing, reviewing, or adapting Apple-platform text hierarchy, system/custom fonts, Dynamic Type, Bold Text, legibility, or spatial text.
---

# Preserve readable hierarchy as text grows

Read [Typography](../../references/typography.md). Inspect the actual text roles, font files/styles, platform, viewing context, and resizing behavior. Establish design, review, or adaptation mode. Use the guide's platform style/size tables when exact values matter; do not reproduce the entire specification or confuse its minimum with a comfortable default.

Assign semantic roles before choosing sizes: title, body, supporting detail, and actionable label need a clear relationship. Prefer system text styles and runtime font APIs so optical design/tracking adapt to size. If a custom face is needed, verify weight/legibility and provide equivalent text-size and Bold Text behavior; thin faces may need more size than the table suggests. Use loose leading for sustained/wide reading, avoiding tight leading across three or more lines.

Decide how content expands. Grow containers, permit labels to wrap, stack timestamps/glyphs, and reduce columns rather than aggressively truncating essential reading. Scale meaningful glyphs with the text. Preserve hierarchy while prioritizing the content people intend to read; not every decorative/transient number must grow identically.

Apply platform differences: macOS has no Dynamic Type, so use appropriate standard-control fonts and explicit product text accommodations rather than promising that API behavior. On visionOS, favor readable 2D text, explicit styles for New York, little extrusion, and viewer-facing object labels; do not rely on cast shadows against unpredictable surroundings. Watch uses its own font conventions, including complication typography.

**Worked transformation:** Before, a book list fixes custom thin titles to one line and leaves status glyphs tiny at larger text sizes. Decision: reading and status must remain usable together. After, titles use a legible role/weight, wrap into growing rows, supporting text stacks, and meaningful glyphs scale while selection/actions stay available.

Deliver corrected type roles, resizing rules, or implementation with supported-size examples. Fail if essential content is clipped without a full-text route, hierarchy collapses, or Bold Text/custom sizing breaks controls. Record tested sizes and actual font measurements; device-distance legibility, native shaping, and spatial comfort need supported execution.

Use [Layout](../apple-hig-layout/SKILL.md) for reflow, [Accessibility](../apple-hig-accessibility/SKILL.md) for task-level access, or [Right to left](../apple-hig-right-to-left/SKILL.md) for mixed-script alignment.
