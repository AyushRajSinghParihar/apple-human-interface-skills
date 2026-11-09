Keep one stable Mac interface, optimized for keyboard and pointer, with touch as a secondary input for brief, intentional actions. Apple’s [macOS guidance](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos) recommends preserving desktop control sizes and density.

| Proposal | Do this instead |
|---|---|
| Make every control 44 pt tall and spread out the toolbar | Keep the visible controls and spacing unchanged. Enlarge **tap targets**, allowing touches slightly outside visible bounds to activate controls. Standard controls receive suitable tap targets automatically. |
| Switch to a larger “touch mode” | Keep the layout stable as people switch inputs. Use temporary expanding controls where touch needs more room, without rearranging the interface. |
| Make Smart Erase exclusive to a two-finger gesture | Expose Smart Erase through a discoverable tool or menu command, usable with keyboard and pointer. Treat the gesture as an optional shortcut. If retained, support it on both touch displays and trackpads, and check for conflicts with standard gestures. |
| Leave Shift-drag and hover menus without touch alternatives | Provide equivalent touch actions. For example, an explicit constraint toggle can replace holding Shift while dragging; touch-and-hold or a visible menu button can expose hover actions. |
| Leave the small stepper and brush-size slider as they are | Use standard controls’ automatic touch expansion. For custom controls, consider a temporary larger variant that appears on tap, remains visible and operable while held, and lingers briefly after release. |

These corrections follow Apple’s [macOS gesture guidance](https://developer.apple.com/design/human-interface-guidelines/gestures#macOS). Every function should remain reachable using keyboard and pointer, and pointer-only interactions need touch equivalents.

Validate on a touch display: switch inputs mid-task, check crowded targets for accidental activation, and confirm expanded controls remain visible around the finger. Those interaction checks haven’t been performed here.