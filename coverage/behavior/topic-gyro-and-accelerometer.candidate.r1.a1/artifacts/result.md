# Revised specification result

Patched interface.md in place. The original one-paragraph brief is now an interaction contract covering first play, motion-free steering, optional calibrated tilt, sensing lifecycle, reversible restart, layout, semantics, interruptions, and release acceptance scenarios. This deliverable is a specification revision, not an implemented game.

## Decisions and support

| Observed barrier | Revised decision | Local guidance supporting the decision |
| --- | --- | --- |
| Tilting is the only input | Default to four directional touch controls. Add a single-activation Step variant so sustained contact and quick responses are optional. Keep every level and reward available. | [Game controls — Touch controls](https://developer.apple.com/design/human-interface-guidelines/game-controls#Touch-controls), [Accessibility — Mobility and Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility). Step timing and simulation freezing are product design choices, not Apple-prescribed mechanics. |
| Standing is assumed; no calibration occurs | Allow seated/mounted play. Optional Tilt captures the person's comfortable neutral position and can be recalibrated while paused. Preserve the whole puzzle state when switching inputs. | [Gyroscope and accelerometer — Best practices](https://developer.apple.com/design/human-interface-guidelines/gyro-and-accelerometer#Best-practices); its routed procedure explicitly calls for alternatives and calibration decisions. The angle thresholds are provisional product values. |
| Shake irreversibly resets progress | Remove custom shake reset. Restart affects only the current level and has persistent Undo Restart/Redo Restart with durable snapshots. Standard system undo gestures remain available where applicable. | [Undo and redo — Best practices and iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#Best-practices). Persistent visible recovery is an intentional movement-free alternative. |
| A mounted iPad cannot be assumed handheld | Keep touch controls visible and reachable, adapt to narrow windows, preserve state on resizing, and pause rather than moving the marble during interruptions. | [Designing for iPadOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados#Best-practices), [Designing for iOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices). |
| Sensor lifecycle was unspecified | Collect only for optional Tilt calibration/play, process locally, and stop otherwise. Conditional authorization is requested at invocation, never as a Touch prerequisite. | [Privacy — Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission), [Gyroscope and accelerometer](https://developer.apple.com/design/human-interface-guidelines/gyro-and-accelerometer). Actual API authorization remains to be verified. |

All buttons have specified names, outcomes, state feedback, and at least 44 × 44 pt activation regions. This applies the [Buttons best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices) and conservatively resolves the local games guide's 28 pt table minimum versus 44 pt prose minimum. The chosen 12 pt inter-target gap is a product target, not a universal HIG rule. Text enlargement to at least 200%, semantic controls, and non-audio-only status follow [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility). Defaults and short contextual teaching follow [Designing for games](https://developer.apple.com/design/human-interface-guidelines/designing-for-games#Jump-into-gameplay).

## Worked before/after

**Before:** A seated player has an iPad fixed to a mount. Tilting is the only steering route, so the level cannot be played without moving the mount. A bump interpreted as a shake irreversibly resets progress. No neutral position can be set.

**After, specified behavior:** The player opens the same level in default Touch, chooses Use Step Touch, and presses Play. Roll Right advances the simulation 100 ms, then waits indefinitely for another action. Roll Up supplies the next step without moving the iPad. Pause → Restart Level saves the pre-restart marble position, velocity, hazards, inventory, and timer. Undo Restart restores that exact state, still paused; Resume returns to Step play. A physical bump cannot invoke the removed reset command. If the player later chooses Tilt, Set Neutral accepts the mounted attitude; Use Touch returns to movement-free control without restarting.

This example illustrates the contract. It is not an observed play session; level solvability and appropriate force/step tuning remain unproved.

## Acceptance and evidence status

**Passed — document/static checks:** Read the original brief and reread the revised interface.md. Confirmed that its text replaces all four explicit barriers: mandatory tilt, missing calibration, assumed standing, and irreversible shake reset. The contract specifies a complete motion-free action route, switching/state rules, sensor stop conditions, restart recovery, and observable release checks. `git diff --check` completed successfully after the interface patch.

**Failed:** No document-check failures identified. Runtime pass/fail results are unavailable.

**Not executed — required before release:**

- Complete every level with a fixed device and sensors unavailable, using both Continuous and Step Touch; verify hazard timing, precision, equal unlocks, and single-activation completion.
- Verify seated/reclined/mounted Tilt calibration, neutral drift, force response, latency, sensor interruptions, and authorization behavior. The 2°/15° thresholds and 100 ms step need testing and adjustment.
- Compare snapshots across input switches, interruptions, relaunch, repeated restart/undo/redo, and redo invalidation. Verify that shaking never triggers custom reset.
- Measure touch geometry and contrast; inspect portrait/landscape, narrow iPad windows, safe areas, and 200% text. Test reach and fatigue with players.
- Exercise VoiceOver, Switch Control, Full Keyboard Access, and AssistiveTouch across the complete input/control flow. Button semantics alone do not prove assistive operability or nonvisual maze play.

## Guidance consumption and limits

Used only supplied local files and installed instructions; no web browsing. Official links above are attribution from local references, not pages verified online. The installed references identify a 2026-10-25 snapshot and describe themselves as derived application guidance; no independent source/media review is claimed.

Audit route, rooted at `.agents/skills/apple-hig/`: explicitly read root `SKILL.md`, then interface.md, then searched `references/topic-index.md` for task concepts. Read owning family SKILL.md files before their topic procedures and read procedures before supporting guides:

- Getting started → Designing for iOS, Designing for iPadOS, Designing for games.
- Inputs → Gyroscope and accelerometer, Game controls.
- Foundations → Accessibility, Privacy.
- Menus and actions → Buttons.
- Patterns → Undo and redo (also searched its topic-index row).

Each instruction/reference read used a separate `cat` command for one installed file; topic-index searches used single-file `rg` commands. No external package paths were substituted.

Only a brief was supplied as product evidence. No game source, SDK, device, GUI, accessibility runtime, measurements, or level assets were executed or inspected. Maze physics, goal rules, and hazards are preserved as intended game concepts; their details were absent and must be supplied by implementation. This work makes the proposed behavior concrete and reviewable; it cannot certify device comfort, battery use, native rendering, compilation, all-level solvability, or accessibility conformance.
