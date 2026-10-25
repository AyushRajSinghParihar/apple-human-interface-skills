---
name: apple-hig-accessibility
description: Use when designing, reviewing, or adapting Apple-platform interfaces for text enlargement, sensory access, assistive input, motor access, cognitive needs, or accessibility preferences.
---

# Make the task accessible

Read [Accessibility guidance](../../references/accessibility.md) before applying platform values. This procedure turns that guidance into task-level changes; its artifact format and prioritization are application engineering advice, not additional Apple requirements.

## Establish what can be evaluated

Identify the supported platform, the person's task from entry to completion, and whether the request is design, review, or adaptation. Inspect the supplied screens, content, interaction description, semantics, or implementation. Record which evidence exists: a screenshot can establish visible labels and geometry, but cannot establish spoken names, focus order, alternative activation, or preference behavior. Continue using explicit assumptions when the platform or behavior is missing; ask only when the choice changes the requested result.

For a review, connect each finding to an observed barrier and its consequence for that task. Separate untested behavior needing verification from confirmed defects. For a design or adaptation, change the authorized artifact itself: a revised screen specification, interaction contract, or implementation. A general accessibility checklist alone is not the deliverable.

## Remove the barriers that the task contains

Trace the task without assuming sight, hearing, fine motor control, speech, or fast responses. Select the applicable branches:

- **Reading and visual distinctions:** Preserve content and available actions when text enlarges. Use the guide's platform-specific text defaults and minima; its resizing guidance is at least 200%, with 140% stated for watchOS. Reflow or expose another usable arrangement rather than clipping essential labels. Pair color distinctions with text, shape, or symbols. Evaluate actual foreground/background combinations in light and dark appearances; use a contrast calculator and preserve the guide's stated contrast-table scope instead of claiming that its values alone establish conformance. If the default scheme falls short, specify the Increase Contrast treatment.
- **Information carried by sound or imagery:** Identify what information would disappear when sound or sight is unavailable. Choose captions for synchronized audible events, subtitles for dialogue translation, audio description for visual events, or transcripts for a complete text account according to the content. Specify descriptions for meaningful interface/content imagery and omit redundant decoration. Pair essential sound feedback with a perceivable visual or appropriate haptic equivalent.
- **Manipulation and navigation:** Distinguish visible control size from its actual activation area and separation. Use the guide's platform default as the starting point; its smaller minimum is not a blanket recommendation for dense controls. Replace essential complex or repeated gestures with a labeled onscreen action. Make the complete task navigable and activatable with the supported keyboard and assistive input paths; speech must not be necessary. Preserve system accessibility shortcuts. For custom controls, specify names, roles, values, states, and task order rather than assuming their appearance supplies semantics.
- **Time, motion, and comprehension:** Give people time to read and act; prefer explicit dismissal when transient content requires attention. If motion is present, define a Reduce Motion version that retains state and meaning while reducing automatic movement, bounce, zoom, or depth changes. If media autoplays, provide playback control and consider a global preference; honor Dim Flashing Lights where applicable. Keep the task's navigation and wording consistent rather than adding instructional clutter.

Apply the relevant platform condition. For Assistive Access on iOS/iPadOS, focus on core tasks with one interaction per screen and the source's two confirmations for difficult-to-reverse actions in that mode. For visionOS, keep controls in comfortable view, avoid head-locked content and repeated large gestures, and accommodate hand/head Pointer Control and Zoom. These conditions do not apply automatically to every platform.

## Deliver and check the result

Return the revised artifact or evidence-based review, including the barrier, the concrete change, and its acceptance check. State which platform/preferences were considered and which claims remain unverified. Prioritize blockers to completing the task over cosmetic refinements.

Exercise each selected alternative along the same entry-to-completion path. Fail the check if essential content or actions disappear at the specified text scale, information remains available through only one sense, a required gesture has no equivalent, focus cannot reach/activate a necessary control, or a requested motion accommodation removes meaning. Measure contrast and activation geometry when the evidence permits; report missing measurements rather than inventing them. Use Accessibility Inspector and relevant VoiceOver, Switch Control, Full Keyboard Access, AssistiveTouch, or Pointer Control tests on supported Apple environments. Static inspection or a Linux run cannot establish those runtime results, Apple-device comfort, or App Store Accessibility Nutrition Label eligibility.

## Worked transformation

**Before:** An iPad astronomy log marks observation quality only with green/red dots, announces saving with a chime, and exposes Delete only by a two-finger gesture.

**Decision:** Logging must remain understandable without color or sound and operable without that gesture. Retain compact rows while making status and actions explicit.

**After:** Each row reads “Clear” or “Clouded” alongside its symbol; saving exposes a persistent “Saved” state; a labeled row action opens Delete. The screen specification includes expanded-text reflow, semantic row status, and keyboard/assistive activation acceptance checks. These are proposed changes until the actual implementation passes those checks; the specification does not claim VoiceOver was tested.

## Continue only where needed

For detailed spoken structure and rotor navigation, use [VoiceOver](../../../apple-hig-technologies/.topics/apple-hig-voiceover/SKILL.md). For text reflow/type choices use [Typography](../apple-hig-typography/SKILL.md); for a motion accommodation use [Motion](../apple-hig-motion/SKILL.md). If spatial comfort dominates the task, use [Spatial layout](../apple-hig-spatial-layout/SKILL.md). Keep the task's accessibility acceptance checks when handing off.
