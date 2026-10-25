# Revision result

Patched interface.md in place, replacing the single-paragraph brief with an implementable entry, intensity, motion, control, exit, and restoration contract. This is a specification repair; no application implementation was supplied.

## Decisions and reasons

| Supplied behavior | Revised decision | Basis |
| --- | --- | --- |
| Reading removes all passthrough | Read in Shared Space; optional Enter Reef opens progressive Full Space at low coverage | Least immersion needed for the task; deliberate entry |
| Continuous camera roll | Stationary horizon/seabed; no automatic world or camera motion | Stable visual references and visionOS motion comfort |
| Settings require walking around reef | Central Open Settings and stationary specimen commands | Seated use, resting hands, small-room context |
| Exit loses selected specimen | Return to Lesson restores selection and lesson checkpoint; relaunch stays grounded | Clear return semantics and preservation of useful state |

Progressive immersion was selected for optional habitat context and user-adjustable coverage. Full replacement is unnecessary for reading or specimen inspection. Digital Crown control stays with the system. Animation intensity is handled separately through Pause Animation and Reduce Motion. Low initial coverage, checkpoint fields, control labels, duplicate-open handling, and failure recovery are concrete product decisions, not numerical or API mandates from Apple.

The revised specification also defines interruptible transitions, unavailable-specimen recovery, real-hand retention, accessible alternatives to direct manipulation, text reflow, target spacing, and pending verification. The 1.5 m boundary is approximate system behavior, not a room-size requirement.

## Worked before/after

Before: A seated learner reads about a clownfish. Reading hides the room and starts continuous roll. To change settings they must walk around the reef. Leaving immersion discards the clownfish selection.

After: The learner reads the same lesson in Shared Space and selects the clownfish. Nothing changes presentation until Enter Reef is activated. Progressive immersion opens at low coverage with a stable seabed and horizon; the Crown adjusts coverage. The learner opens settings from the central control surface with hands resting, pauses decorative animation, and selects Return to Lesson. The lesson reappears at the same reading position with the clownfish and its inspection orientation intact. Reopening the app restores that checkpoint in Shared Space, without automatic reef entry.

## Acceptance checks and status

Passed — static specification checks:

- Reading, specimen selection, and relaunch explicitly preserve passthrough and require deliberate entry for the reef.
- Entry, pending entry cancellation, failure, duplicate activation, exit, interruption, and relaunch have defined outcomes.
- All four observed problems have replacement behavior in interface.md; selection, orientation, lesson position, and completed steps survive exit.
- Stationary controls replace walking; camera roll is removed; Crown and boundary agency remain explicit.
- Reduced-motion behavior retains learning information and does not remove exit or settings.

Failed: no outstanding specification check identified in this static review. This does not establish a passing implementation.

Not executed — implementation acceptance gates:

1. Read, select, and relaunch: confirm no automatic immersive entry. Enter Reef twice rapidly: only one space opens. Cancel during opening or simulate failure: retain the lesson and selection, with no surprise retry.
2. Adjust the Crown and invoke system visibility/recentering controls: confirm user agency, predictable progressive coverage, real surroundings, and system boundary response. Do not treat the approximate boundary as obstacle protection.
3. From seated postures and different heights, complete selection, inspection, settings, pause, and exit with resting hands. Confirm no walking, repeated head turns, overhead reach, overlapping hover regions, or head-locked controls. Measure target regions and spacing against the specification.
4. Trigger Reduce Motion before and during exploration; rapidly change specimens and exit mid-transition. Confirm no world rotation, stale animation queue, lost state, or forced delay. Test physical comfort on worn Vision Pro.
5. Exit from exploration, settings, and pending entry; interrupt the app and relaunch. Compare checkpoint fields exactly. Simulate missing specimen content and verify the explicit recovery choice.
6. Test supported assistive navigation/activation, hand/head Pointer Control, Switch Control, Zoom, 200% text reflow, and meaningful names/states. Verify exit is always reachable. Measure contrast in actual reef, light/dark, and Increase Contrast contexts; confirm learning content is available without sound or reliance on 3D visuals.
7. Verify SDK availability, native rendering, persistence failures, and transition cancellation in the eventual implementation. Check ambience ducking and frame performance on the target hardware.

## Evidence and routing limits

Only the supplied one-paragraph interface.md and installed package were used; no web access occurred. Official links below identify the articles represented by local snapshots, not freshly verified pages.

Auditable route: read installed apple-hig/SKILL.md; searched references/topic-index.md for visionOS, immersion, motion, accessibility, spatial layout, and controls; read the getting-started, foundations, and menus-and-actions family SKILL.md files; read their designing-for-visionos, immersive-experiences, motion, spatial-layout, accessibility, and buttons topic procedures before reading each corresponding source guide. All paths resolved under .agents/skills/apple-hig. Each file read used its own cat or rg command.

Material guidance: [visionOS best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos#Best-practices) supports grounded ordinary work and resting interaction; [immersive experiences](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences) supports deliberate transitions, preserved agency, stationary exploration, ground planes, and restrained environments; [motion](https://developer.apple.com/design/human-interface-guidelines/motion#visionOS) supports removing world rotation and maintaining references; [spatial layout](https://developer.apple.com/design/human-interface-guidelines/spatial-layout) supports spatial anchoring and separated targets; [accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) supports motion accommodation and alternative access; [buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#visionOS) supports named actions, standard states, and visionOS targeting. The buttons guide requires 60 pt targets while accessibility lists a smaller minimum; this specification conservatively uses 60 × 60 pt rather than treating the smaller minimum as a recommendation.

No device, simulator, SDK build, GUI, accessibility tool, contrast measurement, tracking, boundary, persistence, or comfort execution occurred. The local guides are dated derivative guidance, not SDK documentation or proof of independent source review. Actual progressive initial coverage, asynchronous lifecycle handling, persistence, and assistive behavior require implementation and Apple-environment verification.
