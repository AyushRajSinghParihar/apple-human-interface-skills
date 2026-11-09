# Gain adjustment repair

Patched interface.md in place, replacing the one-line defect description with a concrete macOS interaction contract. The revised specification labels clip gain in dB, isolates it from speed, defines its range and mapping, stages edits until explicit application, pauses playback before application, represents unknown values without a maximum-position thumb, and supplies keyboard entry, validation, feedback and undo/redo.

## Decisions

Use a bounded horizontal system slider plus exact numeric entry. The −60.0 to +12.0 dB range and 0.1 dB precision are proposed product choices requiring audio-engine confirmation. Linear travel represents dB, with nonlinear amplitude conversion explicitly defined. Local [Sliders guidance](https://developer.apple.com/design/human-interface-guidelines/sliders#macOS) supports the component, labels and exact feedback; it does not prescribe these audio numbers.

The dangerous early commit warrants withholding audible draft preview. Pointer release only finishes staging; Apply Gain pauses playback and commits, with deliberate resumption left to the person. This trades immediate audible audition for controlled application. A positive-gain caution communicates risk without claiming measured clipping or safe listening. Feedback, explicit button roles and grouped undo follow the locally read guidance linked in interface.md.

Unknown gain is unavailable data rather than maximum gain. A valid read is required before editing. Gain and speed have independent ownership. Keyboard users receive the same staging, application, cancellation and recovery path. Invalid numeric input remains available for correction.

The local sources differ on target geometry: Buttons states a general 44 × 44 pt rule; Accessibility gives macOS 28 × 28 pt default and 20 × 20 pt minimum. The specification conservatively assigns 44 × 44 pt activation regions to its buttons without enlarging their native visual styling. Actual geometry is unmeasured.

## Worked before/after

Illustrative values, not a recorded execution: a clip begins at −6.0 dB and playback speed 1.0×. In the supplied before description, moving an unlabeled slider changes speed and commits a dangerous gain jump before release; the amount and timing are unspecified.

After: drag to p = 0.875, which maps to +3.0 dB. The display reads Applied −6.0 dB / Draft +3.0 dB with the positive-gain caution. During movement and after release, the applied gain remains −6.0 dB and speed remains 1.0×. Escape restores the clean −6.0 dB state. Alternatively, Apply Gain first pauses playback, then commits +3.0 dB (amplitude multiplier approximately 1.4125), reports success and stays paused. One Command-Z restores −6.0 dB (approximately 0.5012) while speed remains 1.0×. No unrequested playback restart occurs.

## Acceptance checks

Static specification audit — passed:

- All five supplied defects have explicit replacement requirements in interface.md.
- Endpoints map p=0 to −60 dB and p=1 to +12 dB; p=0.5 maps to −24 dB, 0 dB lies at p=5/6, and p=0.875 maps to +3 dB. Checked by arithmetic, not an audio-engine run.
- Commit, cancellation, invalid data, unknown data, interruption, failure and recovery are specified; guidance-backed recommendations and product choices are distinguished.

Original brief — failed by supplied description: meaningful label/units, gain-only behavior, controlled commit with feedback, truthful unknown state and keyboard operation. These are reported defects, not independently reproduced failures.

Implementation acceptance — not executed; each must pass on the eventual implementation:

1. Drag, click, arrow-repeat and release at endpoints/intermediate points. Display the mapped draft exactly; keep applied gain, speed and audio unchanged until Apply Gain.
2. Enter −6.0, 0.0 and +3.0; test locale decimal separators, partial minus, blank, NaN, infinity, 12.1 and 0.05. Accept valid precision; preserve and explain rejected input. Return/focus loss must never apply.
3. Activate Apply while playing and paused. Verify pause precedes any gain write; no automatic resume. Inject pause/write failure and delay; verify truthful state, retry, duplicate prevention and no erroneous history entry.
4. Cancel/Escape after pointer and keyboard edits; switch clips or close with a dirty draft. Verify no write. Change selection during application and confirm only the captured clip can receive the write.
5. Load unknown, unreadable and out-of-range gain. Verify no maximum thumb/fill, no fabricated default, explanatory text, disabled editing and correct reread recovery.
6. Apply two values, undo twice, redo, save, undo, then apply a new edit. Verify exact clip/value restoration, grouped history, paused playback, visible target, save-session retention and redo invalidation only after successful new work.
7. On macOS, finish the task using keyboard only and Full Keyboard Access, including validation correction and Cancel. Test VoiceOver/assistive adjustment for names, units, state, increments and status. Confirm text editing and system shortcuts remain intact.
8. Inspect native layout, focus, 200% text reflow, light/dark/Increase Contrast, measured contrast and actual nonoverlapping hit regions. Essential information must remain available without hearing or color distinctions.

## Evidence limits and reading audit

Only the supplied interface.md and installed local instruction package were used; no web access. The installed root SKILL.md was explicitly read first. The topic index was searched for gain-control concepts and selected components. Each instruction/source read used a separate cat command, with family and topic procedures read before their supporting guides:

- Selection and input → Sliders, Text fields → sliders.md, text-fields.md.
- Inputs → Keyboards → keyboards.md.
- Foundations → Accessibility → accessibility.md.
- Patterns → Feedback, Undo and redo → feedback.md, undo-and-redo.md.
- Menus and actions → Buttons → buttons.md.

All paths resolve under .agents/skills/apple-hig/ in this project. Official links are attribution from local snapshots, not evidence of online verification. There is no application code, screenshot, SDK build, device/GUI session, audio measurement or accessibility execution in the supplied evidence. This work repairs the specification; it does not establish runtime correctness, native rendering, acoustic safety, assistive behavior or framework availability. No runtime check is reported as passed.
