# Gallery specification repair

Edited [interface.md](interface.md) in place. The original brief required look-to-open, exact per-person gaze heatmaps, continuous staring, and small controls that jumped toward gaze. The patch replaces all five assumptions with concrete interaction, data, geometry, and acceptance contracts.

## Decisions and patch summary

- Looking provides private system hover; explicit finger-thumb tap or equivalent supported activation opens the image. Hover cannot run app business logic. [Eyes](https://developer.apple.com/design/human-interface-guidelines/eyes)
- Detail persists until Back to Gallery is activated, restoring the originating tile and gallery scroll position. Explicit persistence and context restoration are product decisions applying deliberate activation and explicit dismissal guidance. [Accessibility — Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility#Cognitive)
- Removed gaze heatmaps with no replacement analytics. Permission is not a workaround for private gaze. Prohibiting inferred gaze histories and activation telemetry is a conservative product decision beyond the platform boundary itself. [Privacy — visionOS](https://developer.apple.com/design/human-interface-guidelines/privacy#visionOS)
- Specified stable system buttons, combined thumbnail/title targets, 60 × 60 pt activation regions, separation, and no gaze-following movement. Hover, activation, persistent state, and keyboard/assistive focus are distinct. [Eyes — Making items easy to see](https://developer.apple.com/design/human-interface-guidelines/eyes#Making-items-easy-to-see), [Buttons — visionOS](https://developer.apple.com/design/human-interface-guidelines/buttons#visionOS)
- Chose a standard Shared Space window for the assumed 2D gallery, resting-hand input, visible return controls, and alternative input paths. No immersion or custom tracking is necessary for this task. [Designing for visionOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos), [Gestures — visionOS](https://developer.apple.com/design/human-interface-guidelines/gestures#visionOS), [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)

Source qualifications: Eyes describes general custom hover, but Buttons says custom button hover is unsupported; the patch uses standard effects. Accessibility lists a 60 × 60 pt default and a 28 × 28 pt minimum for visionOS, while Buttons calls for 60 × 60 pt targets. The patch uses 60 × 60 pt and separates visible size from activation geometry. These passages do not establish SDK API availability.

## Worked before/after

**Before:** A person glances at “Blue Harbor.” It opens immediately, the app records where they looked, controls jump toward their eyes, and looking away closes the image because continuous staring stopped.

**After:** Looking at “Blue Harbor” produces system hover only. A deliberate tap activates “Open Blue Harbor,” saves the originating tile and scroll position, and opens detail. The person looks away or changes input; the image stays open and controls stay put. Activating Back to Gallery restores the saved context. No eye coordinates, hover history, or gaze-derived event is collected. Assistive activation follows the same transitions; user-enabled system Dwell Control does not imply an app gaze callback.

## Acceptance checks and status

| Status | Check | Evidence |
| --- | --- | --- |
| Passed — static document review | Every original assumption has a concrete replacement. | Revised activation, persistence, privacy, stable geometry, and feedback contracts. |
| Passed — static document review | Browse/open/inspect/return and alternative activation are specified. | State table and alternative-input requirements; not execution evidence. |
| Passed — static document review | Numerical rules retain visionOS scope and pt units; source tensions are disclosed. | Target section distinguishes activation geometry, defaults/minima, and standard hover. |
| Failed — original brief | Deliberate activation and private-gaze boundary. | Original text explicitly required opening by looking and exact gaze heatmaps; replaced in the specification. No runtime fix is claimed. |
| Not executed | Sweep gaze without activating; open once, look away, wait, and return with context intact; inspect data writes. | Needs an implementation and event/data inspection. |
| Not executed | Measure hit geometry and hover overlap; assess responsiveness, distraction, comfort, and posture. | Needs rendered layout and a worn Vision Pro for physical claims. |
| Not executed | Complete the path using keyboard, VoiceOver, Switch Control, Pointer Control, and system Dwell Control. | Needs supported Apple runtime/configurations and actual assistive use. |
| Not executed | Check 200% text, Zoom, Reduce Motion, Increase Contrast, contrast measurements, and sound-off feedback. | Needs implemented UI and accessibility preference testing. |

## Evidence limits and route

Read the installed root `.agents/skills/apple-hig/SKILL.md`, inspected interface.md, and searched the installed topic index for visionOS, eyes/gaze, gestures, and accessibility. Read the Getting started, Inputs, Foundations, and Menus and actions families, then their selected topic procedures before reading the corresponding source guides: Designing for visionOS, Eyes, Gestures, Privacy, Accessibility, and Buttons. Each instruction/source file was read by installed path with one file per command.

Used only supplied local files and installed guidance. The local articles describe application guidance derived from Apple HIG, with snapshot retrieval dated 2026-10-25; official links were not fetched. No independent media review or current SDK verification is implied. No app implementation, screenshot, measured UI geometry, device, SDK build, GUI, accessibility execution, telemetry inspection, or physical comfort testing was available or performed. The deliverables are an edited specification and this decision record; runtime acceptance remains pending.
