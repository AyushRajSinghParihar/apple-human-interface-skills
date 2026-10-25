# Decisions and changes

Patched `interface.md` in place, replacing the supplied one-paragraph iOS/iPadOS specification with a concrete interaction contract. The original explicitly required tilt, omitted calibration, assumed standing, and irreversibly reset progress on shake.

- Buttons are the default and can complete the entire game with a stationary device. Cardinal steering has explicit hold, release, speed, and collision behavior. Step steering lets a single activation advance 100 ms, with physics and time frozen between actions, avoiding a continuous-hold or fast-response requirement.
- Tilt remains optional. It calibrates around a comfortable seated, standing, or mounted posture; includes recentering; and pauses for orientation changes. Mode changes preserve the attempt. Unavailable or declined motion access leads back to Buttons.
- Shake reset is removed. Restart Level is visible, scoped to one attempt, and recoverable through a durable snapshot. Saving failure prevents reset.
- The specification defines safe-area placement, 44 × 44 pt targets, spacing, pressed states, semantic action names, interruption behavior, completion feedback, and a bounded sensing lifecycle.

The HIG supports alternative input, comfortable controls, clear actions, and relevant permission timing. Buttons as default, Step steering, 12 pt spacing, calibration angles, and durable recovery are project decisions, not quoted Apple mandates. The calibration angles and Step duration are provisional and need play testing. No framework replacement or SDK API choice was necessary for this specification task.

# Worked before/after

Before: A seated person has an iPad fixed to a mount. They cannot tilt it to move the marble. Moving the mount accidentally shakes the device and permanently loses progress. There is no calibrated neutral angle.

After: They launch in Buttons mode and choose Step steering in Pause. Activating Move Right advances physics for 100 ms and freezes; they take as long as needed to select Move Up. Cardinal inputs can reach the goal without touching the mount. An accidental shake does nothing. If they choose Restart Level, Restore Previous Attempt recovers the exact prior board, velocity, items, and timer, even after relaunch. If they later choose Tilt, play stays paused while they set their preferred neutral angle; Use Buttons remains available throughout.

# Acceptance checks

These are release checks for the future implementation unless explicitly marked as static inspection.

| Check | Expected result | Status |
|---|---|---|
| Revised artifact inspected | `interface.md` contains stationary input, calibration, and recoverable restart contracts replacing all four supplied barriers | Passed: specification inspection |
| Source routing inspected | Installed root, selected families, and selected topic procedures read before their respective references | Passed: file-read evidence |
| Stationary complete loop | With device mounted and motion access unavailable, enter, complete every level, recover from failure, and advance using only Buttons | Not executed |
| Step steering | Single activations advance exactly one interval; no simulation/timer drift during scanning; all levels remain solvable without chords or time pressure | Not executed |
| Mode change | Switch with nonzero velocity and collected items; all state survives, simulation remains paused, Resume starts without stale input | Not executed |
| Calibration/posture | Seated, flat, mounted, and standing neutral positions work; unstable sampling retries safely; recenter and rotation preserve progress | Not executed |
| Authorization and lifecycle | No launch request or Buttons sensing; denial/failure retains playable alternative; sampling stops at pause, background, switch, and completion | Not executed |
| Reset recovery | Shake has no effect in either mode; restart touches only current attempt; restore survives relaunch; snapshot failure prevents reset | Not executed |
| Input interruption | Release, cancellation, background, and return cannot leave a direction stuck | Not executed |
| Layout and access | Measure target size/separation and safe-area clearance on iPhone/iPad in both orientations; enlarged labels do not obscure necessary actions | Not executed |
| Assistive input | Switch Control and Full Keyboard Access reach and activate all essential controls; focus alone never steers; assistive direction activation takes one Step | Not executed |
| Feedback | Pressed state remains visible around finger; goal/error/recovery states are readable without audio or haptics | Not executed |

Failed checks: none observed in the revised document's static review. This does not mean runtime checks passed. The original supplied specification fails the stationary-play, posture, calibration, and safe-reset design requirements by its explicit wording.

# Evidence and limits

Only local supplied files and installed instructions were used. No web browsing occurred. Official links below and in the revised specification are attribution copied from the local guidance, not evidence of visiting those pages.

Auditable route, rooted at `.agents/skills/apple-hig/`:

1. Read `SKILL.md`, then supplied `interface.md`; searched `references/topic-index.md` for motion, accessibility, games, and buttons.
2. Read families `subskills/apple-hig-inputs/SKILL.md`, `subskills/apple-hig-foundations/SKILL.md`, and `subskills/apple-hig-menus-and-actions/SKILL.md`.
3. Read Inputs procedures `.topics/apple-hig-gyro-and-accelerometer/SKILL.md` and `.topics/apple-hig-game-controls/SKILL.md`; Foundations procedure `.topics/apple-hig-accessibility/SKILL.md`; Menus and actions procedure `.topics/apple-hig-buttons/SKILL.md`; then their corresponding reference files.
4. Followed the sensor procedure's permission/minimization route by reading Foundations `.topics/apple-hig-privacy/SKILL.md` before `references/privacy.md`.

Each read/search used one file per shell command. These local references describe themselves as derived guidance snapshots dated 2026-10-25; their presence does not establish independent source review or current SDK availability.

Material source links: [Game controls — Touch controls](https://developer.apple.com/design/human-interface-guidelines/game-controls#Touch-controls), [Accessibility — Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility), [Accessibility — Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility#Cognitive), [Gyroscope and accelerometer](https://developer.apple.com/design/human-interface-guidelines/gyro-and-accelerometer#Best-practices), [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons), and [Privacy — Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission).

No game implementation, level geometry, screenshots, SDK project, or hardware measurements were supplied. No build, device, GUI, Accessibility Inspector, VoiceOver, Switch Control, Full Keyboard Access, haptic, battery, latency, or comfort execution occurred. No whole-game accessibility or App Store disclosure eligibility is claimed. Spatial nonvisual play remains unevaluated; labelled steering alone cannot establish it. Level solvability, tuning, native rendering, authorization behavior, and durable persistence remain implementation evidence gaps.
