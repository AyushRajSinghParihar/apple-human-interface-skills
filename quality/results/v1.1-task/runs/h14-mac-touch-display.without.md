Keep one stable Mac interface that works with touch, pointer, and keyboard. Revise the proposal as follows:

| Proposal | Do instead |
|---|---|
| Make everything 44 pt tall and spread out the toolbar | Preserve standard Mac control sizes and toolbar density. Improve **hit areas**, including invisible padding where appropriate, without unnecessarily enlarging the visible controls. Height alone doesn’t ensure a usable target. |
| Switch to a larger “touch mode” | Keep layout and control sizes stable as people switch inputs. For small or dense controls, offer a temporary expanded version when tapped. |
| Make Smart Erase exclusive to a two-finger gesture | Expose Smart Erase as a discoverable tool or command usable with touch and pointer. A custom gesture can be an optional shortcut; avoid conflicts with system gestures. |
| Require Shift-drag or hover | Provide touch-accessible controls—for example, a constraint toggle and a tappable menu button. Also preserve modifier behavior: Shift plus a touch drag should produce the same result as Shift plus a pointer drag. |
| Leave the small stepper and brush slider unchanged | Use native controls with their touch expansion behavior where available. For custom controls, provide a temporary enlarged stepper or slider on tap, keeping the surrounding layout stable. |

For hover-revealed controls, let a tap in their general location reveal them before the person chooses an action. citeturn896408search0

These changes follow Apple’s guidance on stable layouts, temporary control expansion, consistent input behavior, and native touch controls. Validate complete drawing workflows using touch alone, then test switching inputs mid-task. citeturn896408search3turn924022view1turn776488view1