Keep one stable Mac interface that works with touch, mouse, trackpad, and keyboard. Revise the proposal as follows:

| Proposal | Do instead |
|---|---|
| Make every control 44 pt tall and spread out the toolbar | Keep familiar macOS control sizes and toolbar density. Improve **hit areas**, which can extend beyond visible artwork, without creating overlapping targets. Don’t treat 44 pt as a universal Mac control-height requirement. |
| Switch to a larger layout when someone touches the screen | Keep the layout stable as inputs change. Touching a tool shouldn’t move neighboring controls or resize the canvas. Preserve selection, active tools, and in-progress work. |
| Make Smart Erase exclusive to a two-finger gesture | Expose **Smart Erase as a visible tool and menu command**, usable with touch and pointer input. A gesture can provide an optional shortcut; it shouldn’t unlock exclusive functionality or conflict with standard gestures. |
| Require Shift-drag or hovering for some tools | Provide explicit touch-operable equivalents: for example, a **Constrain** toggle for Shift-drag and a tappable options button for hover menus. Keep the existing keyboard and pointer shortcuts. |
| Leave the small stepper and brush-size slider unchanged | Review these specifically for finger precision. Give increment/decrement actions comfortable, distinct targets; consider separate −/+ buttons. Make the slider easy to acquire and drag, show live brush-size feedback, and provide a synchronized numeric field for exact values. |

Apple’s relevant guidance covers [Mac conventions](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos), [consistent input switching](https://developer.apple.com/design/human-interface-guidelines/pointing-devices), [gesture alternatives](https://developer.apple.com/design/human-interface-guidelines/gestures), and [slider precision](https://developer.apple.com/design/human-interface-guidelines/sliders).

Validate the revised design on the intended touch hardware: complete every drawing task without hover or a physical modifier key, switch inputs mid-task without layout changes, and check accidental neighboring activations. Those hardware checks remain untested here.