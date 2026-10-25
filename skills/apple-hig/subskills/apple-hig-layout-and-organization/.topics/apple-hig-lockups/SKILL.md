---
name: apple-hig-lockups
description: Use when creating, reviewing, or adapting tvOS focusable cards, caption buttons, monograms, or posters.
---

# Design the whole focused unit

Read [the lockup guide](../../references/lockups.md). Lockups are tvOS-specific; the procedure below is application advice for that component, not a cross-platform support claim.

Inspect the supplied content, focus/navigation arrangement, platform, and create/review/adapt request. Identify the atomic unit people choose and its header/content/footer. Obtain both focused and unfocused states or mark expansion/tilt unknown.

Choose a card for combined review/rating content, caption button for titled content, monogram for a person, or poster for artwork-led choice. Keep dimensions consistent within a logical group while fitting the actual content. A monogram should prefer an available portrait with initials as fallback. A poster's optional title/subtitle can appear on focus; essential identity must remain understandable in context. Set caption-button focus tilt to the row, stack, or grid navigation direction and reserve enough space for the entire unit's expansion without neighboring overlap.

Implement the lockup, provide focused/unfocused annotated layouts, or report concrete expansion and identity defects. For adaptation to another platform, retain the content relationship using an appropriate supported component rather than calling it a native lockup.

**Worked transformation:** Before: a TV cast grid scales portraits alone while their names remain stationary and the focused portrait covers its neighbor. Decision: portrait and labels are one focusable person. After: group them as monograms that grow together, use consistent cell sizing, and reserve expansion space; missing portraits use initials.

Deliver the chosen form, focus bounds, content hierarchy, and activation outcome. Navigate every edge/corner and verify neighboring content, readable labels, and fallback identity. Fail for overlapping focus states, header/footer detached from content, or inaccessible unnamed choices. Linux layout inspection cannot prove remote-input tilt or native TV focus behavior.

Load [designing-for-tvos](../../../apple-hig-getting-started/.topics/apple-hig-designing-for-tvos/SKILL.md) for platform navigation or [collections](../apple-hig-collections/SKILL.md) for the surrounding grid.
