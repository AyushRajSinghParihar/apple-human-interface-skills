---
name: apple-hig-playing-haptics
description: Use when creating, reviewing, or adapting tactile feedback patterns, event meaning, synchronization, frequency, and hardware fallbacks.
---

# Give tactile events consistent causes

Read [the haptics guide](../../references/playing-haptics.md). This workflow is application advice; built-in device, trackpad, Pencil, and controller haptics are distinct support paths.

Inspect event semantics, existing visual/audio cues, target hardware, pattern/frequency, and create/review/adapt request. Obtain capability/configuration evidence; do not infer an iPad/Mac/TV/visionOS built-in actuator from support for a connected controller.

Use standard patterns with their documented meaning: success must not signal failure, and selection marks changing values. For physical metaphors match apparent weight/hardness and synchronize intensity/sharpness with the event. Choose brief discrete cues for ordinary app work and custom patterns only when the event needs them. Preserve functionality with haptics disabled. Check that repetition does not distract and vibration does not interfere with camera/microphone/motion work. On watch preserve named pattern meanings and avoid overlapping click floods; on Mac tie trackpad patterns to relevant drag/force boundaries. Pencil and controller support require compatible hardware.

Implement event-to-pattern/capability/fallback logic, provide a tactile cue specification, or review exact semantic/timing defects. Do not claim a comfortable result from a waveform or code listing alone.

**Worked transformation:** Before: a sketch tool emits long continuous vibration during every Pencil stroke and uses Success when saving fails. Decision: frequency interferes with drawing and the outcome cue is reversed. After: retain clear visual failure/recovery, use an appropriate supported error cue, and reserve brief tactile events for meaningful tool boundaries with an off path.

Deliver the artifact, cause/pattern/timing/hardware map, and nonhaptic alternative. Verify capability absent, disabled setting, rapid event sequences, and sensor-task coexistence. Fail for false semantic feedback, essential tactile-only information, or unsupported actuator claims. Physical comfort, synchronization, and sensor interference require hardware tests.

Load [feedback](../apple-hig-feedback/SKILL.md) for channel strategy or [gestures](../../../apple-hig-inputs/.topics/apple-hig-gestures/SKILL.md) for gesture-coupled cues.
