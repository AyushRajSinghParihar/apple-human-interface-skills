# Focus and selection visual examples

Source: [Apple HIG Focus and selection](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection).

The iPad examples distinguish a halo following a photo's outline from a cell's
accent-colored highlighted content. The rounded-photo version adjusts the halo to
the target geometry. Preserve the distinction between the focus affordance and
the cell's content styling.

The tvOS button sequence shows different kinds of state, rather than five names
for one highlight:

| State | What the illustrated button communicates |
|---|---|
| Unfocused | Base scale and a small shadow keep it close to its background. |
| Focused | Enlargement, increased apparent elevation, and strong label contrast identify the current target. |
| Pressed/highlighted | The button reduces from its enlarged focus scale while retaining a clear activation response. |
| Selected | A persistent choice remains distinct from temporary focus; the illustration returns to base scale and lower elevation. |
| Unavailable | Reduced contrast and missing elevation communicate inactivity. |

The light/dark contextual pairs preserve these state relationships against
different content backgrounds. Their sample colors are a demonstration of system
rendering, not a universal custom-button palette. Leave room for enlargement and
prefer system focus behavior so appearance and input conventions remain coherent.
