Change all six decisions. Duo should adapt the same editing experience continuously as available space changes.

| Plan item | Recommended change |
|---|---|
| Fixed 375 pt layouts | Use size classes, safe areas, margins, and reserved regions. Expand and collapse the editor while preserving the selected photo and editing state; support multitasking widths. |
| Bars at the top outside | Preserve system placement: vertical side bars on the outer display and inner landscape display; ordinary horizontal bars in inner portrait. |
| Mirror the side toolbar for Arabic/Hebrew | Keep hardware-aligned bars on the same **physical side**. Adapt reading-order navigation and directional symbols appropriately. |
| Icons without titles | Supply meaningful symbols **and localized titles**, even when only icons are visible. Titles support expanded bars and overflow. |
| Canvas ignores the fold | Make the custom canvas respond to the center folding reserved region. Keep essential content and controls usable, with modest layout changes as folding progresses. |
| Controls cover the active inner camera | Move controls clear when the camera’s reserved region appears; adapt again when it disappears. |

These corrections follow Apple’s [Duo guidance](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo), using the installed HIG snapshot; the live article’s body wasn’t retrievable.

For your editor, I’d also prioritize editing tools over tabs during editing, keep pane-specific controls near their content, and define which secondary actions enter overflow first.

The supplied plan fails these six design checks. Runtime checks remain unexecuted: validate opening/closing without losing edits, partial folding, camera activation, Arabic/Hebrew, and multitasking on either side in Device Hub previews and on supported hardware.