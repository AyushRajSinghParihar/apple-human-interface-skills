# Marble puzzle — revised input specification

Platform: iOS/iPadOS. Guide the marble through the existing puzzle to its goal. Preserve puzzle geometry, collision rules, unlocked levels, and completion records. Play must work seated, with the device flat or mounted, without standing, tilting, shaking, or owning an accessory.

## Entry and input choice

First launch defaults to Buttons. Before Play, show: “Guide the marble with the direction buttons. You can also choose Tilt.” Show current control mode in text. All menus use ordinary onscreen controls; motion never navigates menus.

Pause exposes immediate commands “Use Buttons” and “Use Tilt” (the current mode is identified in adjacent status text), plus Resume. Selecting a mode preserves the exact board, marble position and velocity, elapsed puzzle time, and collected items; keep simulation paused until Resume. Persist the selected mode across launches. A saved Tilt preference must still offer Use Buttons before requiring any motion.

## Buttons: complete stationary play

Display four separate directional buttons labelled Move Up, Move Down, Move Left, and Move Right in a lower control area outside the board. Directions refer to the screen, regardless of physical posture. One finger suffices; no diagonal chord, drag, repeated tapping, or simultaneous actions are required to complete a level. Level review must ensure all routes are traversable with cardinal steering.

Normal touch: holding a direction applies a constant screen-relative steering acceleration; releasing removes that acceleration and applies the same friction as neutral tilt. Cap acceleration and speed at the existing tilt mode maxima. Opposing inputs cancel; perpendicular inputs, if used, normalize to the same maximum acceleration. Do not let buttons obscure hazards or the goal.

Also expose “Use Step Steering” and “Use Hold Steering” in Pause, with current steering style in text. Step steering is a non-repeating activation alternative for assistive input or anyone avoiding holds: each directional activation advances the same physics engine for 100 ms with that steering acceleration, then freezes the simulation and puzzle timer. Collisions and goal detection still run throughout that interval. Resume in Step mode waits for the next activation; the marble never drifts while someone scans controls. The 100 ms interval is a proposed tuning value, to be checked against every level; it is not an Apple requirement. No completion or unlock penalty for either style.

Use system buttons where possible. Every interactive target is at least 44 × 44 pt with 12 pt clear separation (project spacing choice). Direction controls have visible borders and pressed feedback extending outside the finger-covered center. Place controls inside safe areas, clear of the Home indicator and other system obstructions. On iPad, keep them reachable rather than stretching across the full display. Reflow board and controls in portrait, landscape, and enlarged text layouts without overlapping targets. Keep secondary controls above the steering area.

Each control exposes its visible action name, button role, enabled state, and activation. Assistive activation of a direction uses one Step interval rather than requiring a synthetic hold. Pause and Resume are always reachable. Verify Switch Control and Full Keyboard Access navigation and activation; focus movement alone must not steer. Step mode offers unlimited decision time between actions. These are implementation requirements, not a claim that the whole spatial puzzle is already accessible to every assistive technology.

## Optional tilt: comfortable neutral and lifecycle

Use Tilt pauses play and opens calibration instructions: “Sit or stand comfortably. Hold or mount your device at the angle you want to use, then tap Set Neutral.” Never assume upright posture. Set Neutral samples a stable baseline over 0.5 seconds; if unstable, retain the paused board and show “Keep the device still and try again,” with Set Neutral and Use Buttons available. Stability tolerance must be tuned on hardware; no universal sensor threshold is assumed.

Relative to that baseline, tipping the top away steers up, toward the person steers down, and lowering the left/right edge steers left/right. Start with a 2-degree neutral dead zone and linearly reach maximum steering at 15 degrees from neutral; these are provisional product tuning values. Recenter is always available from Pause and repeats calibration without restarting. Orientation changes pause play, clear held inputs, and require recalibration before Tilt resumes; Buttons may resume immediately.

Collect motion only during requested calibration and active Tilt play. Stop collection in Buttons mode, Pause, background, or completion. Process samples on-device, discard after deriving steering, and do not log, upload, or retain raw samples. If the chosen API requires authorization, request it only when Use Tilt is invoked, with purpose: “Motion data lets you steer the marble by tilting your device.” Do not invent an API or assume all sensor access displays a permission prompt. Missing hardware, denied access, or sensor failure leaves the board paused with an explanation and Use Buttons; never gate play on granting motion access.

## Pause, interruption, and recovery

Pause freezes simulation and timer and clears pending input. Backgrounding or input interruption does the same; returning requires explicit Resume. Resume restores the saved simulation state but never a stale pressed direction. In Buttons mode, incidental device movement has no gameplay effect. Shake has no reset binding in either mode.

“Restart Level” is a secondary onscreen action in Pause, never an automatic shake response or default keyboard action. It snapshots the current level state durably before resetting only that level to its start; unlocked levels and completion records remain intact. Stay paused and show “Level restarted” with “Restore Previous Attempt.” That action restores position, velocity, collected items, and timer, then stays paused. Keep the recovery snapshot across app relaunch and ordinary play until the next explicit Restart Level replaces it; disable Restore only when no snapshot exists, with “No previous attempt to restore.” If snapshot saving fails, do not reset; show the failure and retain the current attempt. No irreversible progress-reset command is part of this flow.

At the goal, stop simulation and sensing, record completion once, and show textual “Level Complete” with Next Level and Replay Level. Sound or haptics may supplement visible state, never carry success or errors alone.

## Source basis and scope

This is a specification patch, not executable game code. Touch alternatives and target sizing follow [Game controls — Touch controls](https://developer.apple.com/design/human-interface-guidelines/game-controls#Touch-controls); motor alternatives and decision time follow [Accessibility — Mobility and Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility). Optional sensing follows [Gyroscope and accelerometer — Best practices](https://developer.apple.com/design/human-interface-guidelines/gyro-and-accelerometer#Best-practices); collection and permission timing follow [Privacy — Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission). Labels, press feedback, and ordinary action semantics follow [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons). Calibration values, Step steering, recovery persistence, and default mode are product decisions requiring implementation validation.
