# Marble puzzle — revised interaction specification

Platform: iOS/iPadOS. Preserve the marble, maze, hazards, goal, level unlocks, and saved progress. Support seated, reclined, handheld, tabletop, and mounted use; never require standing, shaking, or repositioning the device to complete a level. No engine or SDK is prescribed by the supplied brief.

## First play and motion-free steering

Open the current puzzle paused with **Play** and **Controls** visible. New installations default to **Touch**. Teach in context: “Use the arrows to roll the marble. Device movement is optional.” No motion access or calibration is required for Touch.

Display four labeled directional buttons, **Roll Up**, **Roll Down**, **Roll Left**, **Roll Right**, in a directional cluster below the board. Directions are relative to the displayed maze, not physical device attitude. In Touch, ignore sensor input entirely. A single finger is sufficient; diagonal movement can be composed from sequential directions. Keep **Pause** visible during play. Pausing freezes the simulation, timer, and input immediately; **Resume** continues only after explicit activation.

Provide two immediate commands in Controls:

- **Use Continuous Touch**: selected by default. Holding an arrow applies a normalized unit force along that axis, using the same force cap and hazards as Tilt. Release, touch cancellation, sliding outside the target, or interruption removes that force. Opposite directions cancel; normalize simultaneous perpendicular directions so diagonals have no extra force. Ordinary inertia remains; no input may remain stuck after cancellation.
- **Use Step Touch**: each ordinary activation advances the same simulation by 100 ms with unit directional force, then freezes it. Retain resulting position and velocity for the next step; no simulation or timer advances while choosing the next action. Holding does not repeat. This permits deliberate single activations through touch or assistive input without sustained contact or fast responses. Show “Step mode — choose a direction.” Pause remains available. The 100 ms interval is a proposed tuning value, not an Apple threshold; validate precision on every level before release.

Both paths reach every level and goal without accessories or motion. Apply the same unlocks and rewards; no motion-only gates or penalty for Step mode. Level validation must establish solvability with the supplied force and step interval. The brief supplies no geometry or physics from which to prove that today.

## Optional Tilt and calibration

Controls is reachable before Play and from Pause. Opening it freezes and snapshots the level, marble position/velocity, hazards, timer, and collected items. **Use Touch** stops sensing and restores the saved Touch variant. **Use Tilt** enters calibration while gameplay remains frozen; show “Hold or mount the device in a comfortable position, then choose Set Neutral.” **Set Neutral** samples the current attitude as neutral; **Use Touch** remains available throughout. Never require a horizontal device or a standing person.

Relative to neutral, map pitch to displayed up/down and roll to left/right. Proposed initial tuning: a 2° dead zone per axis, linear response from 2° to 15°, clamped at unit force beyond 15°; normalize the combined vector. These are product starting values requiring hardware validation. **Set Neutral** can be repeated from paused Controls after changing posture or mount. Never recalibrate silently during play. Calibration commits only on a valid sensor sample; otherwise show “Tilt unavailable. Use touch controls.” Keep the board frozen until Resume. Switching controls preserves the complete snapshot and never restarts the level.

Collect device attitude only during explicit calibration and active Tilt gameplay. Stop updates in Touch, menus, pause, background, and level completion. Process samples on device; do not persist or transmit raw samples. Explain optional sensing at selection: “Tilt uses device movement to steer the marble.” If the chosen implementation requires system authorization, request it only then, with purpose copy: “Device movement steers the marble when you choose Tilt.” Verify actual API authorization requirements during implementation; this specification does not assert a universal motion prompt. Unavailable, denied, or interrupted sensing pauses the game and offers Use Touch without losing progress or repeatedly prompting.

## Restart and recovery

Remove the custom shake-to-reset handler. A shake never starts a level again or erases progress. Preserve system accessibility gestures and standard system undo behavior where applicable; physical shake is never a required route.

Pause exposes **Restart Level** as a secondary action. Activation stores a durable pre-restart snapshot and resets only the current level to its initial state, still paused. Show **Undo Restart** persistently, with “Level restarted”; it does not expire on a timer or after resuming. Undo restores the exact snapshot, displays the restored board, and remains paused. **Redo Restart** reapplies that restart until a new gameplay action invalidates redo. Treat each restart as one history unit; retain restart history for the current level across save/relaunch, and clear it only when explicitly leaving that level for another. Show the boundary in Controls help. Completed-level unlocks and rewards are never reset. Restarting repeatedly must not overwrite the only recovery snapshot. No global erase-progress command is part of this specification.

## Layout, semantics, and state

Use system buttons for commands where practical. Every button has an activation region at least 44 × 44 pt on iOS/iPadOS, with 12 pt clear separation as a product layout target; regions cannot overlap. The arrows have visible direction symbols and the accessible names above, button roles, enabled state, and press outlines visible outside the finger. Use text plus a checkmark to identify the active input variant. Pause/Resume and recovery actions retain explicit names; sound and haptics are optional reinforcement, never the only feedback.

Keep arrows in the lower reachable control area, separate from the maze, Home indicator, and system gesture edges. On wide iPad layouts, keep the control cluster near a lower corner with a **Move Controls Left/Right** command; compact widths put it below the board. Portrait, landscape, and iPad window resizing retain the entire maze and control route; pause on a geometry change, clear held input, preserve state, and require Resume. A Tilt geometry change requires Set Neutral again before resuming. Enlarged labels reflow into taller rows rather than shrinking targets or clipping; support at least 200% text enlargement. If space is insufficient, keep the maze fit and allow the paused control area to scroll.

Give controls a logical navigation sequence: Play/Resume, directional actions, Pause, Controls, then available recovery commands. Each must support ordinary activation for assistive input; Step mode must not depend on raw touch-down events. Full nonvisual maze navigation is outside the evidence supplied: accessible button names alone do not establish blind playability. Do not advertise that claim without a board representation and task-level testing.

Backgrounding, loss of input focus, or sensor failure clears held directions, freezes the simulation, and saves the current state. Relaunch restores paused with the prior input preference and restart history. Tilt requires a new neutral position after relaunch. No interruption, orientation change, or control-mode change may spend a life or reset progress.

## Release acceptance contract

1. With the device fixed in a mount and motion unavailable, enter, steer, avoid hazards, complete every level, pause, restart, undo, and resume using Touch alone; repeat with Step mode and single activations.
2. Switch Touch → Tilt → Touch mid-level. Verify identical position, velocity, hazard state, timer, inventory, and unlocks before Resume. Calibrate while seated and mounted; neutral causes no steering. Verify cancellation/unavailable authorization preserves state.
3. Shake in all states: no custom reset or progress loss. Restart twice, undo twice, redo, then move and verify redo invalidation. Relaunch and recover the saved restart snapshot.
4. Interrupt while holding each direction; verify zero held input on return and no simulation advance until Resume. Repeat for background, resizing, rotation, and sensor loss.
5. Inspect target geometry, safe areas, 200% text, light/dark contrast, pressed feedback, and compact iPad layouts. Exercise focus and activation with VoiceOver, Switch Control, Full Keyboard Access, and AssistiveTouch on supported Apple environments; verify Step mode has no response deadline.

These are requirements for a future implementation, not executed device results. See result.md for decision support and evidence limits.
