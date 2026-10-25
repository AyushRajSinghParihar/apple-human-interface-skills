# Audio gain adjustment — revised specification

Platform: macOS recording editor. This is an implementable design contract; no framework or existing implementation is supplied.

## Scope and value contract

Adjust the selected clip's nondestructive gain only. Do not change playback speed, pitch, playhead, source samples, selection or system output volume. Playback speed remains a separately owned value with no gain event binding.

Use a system horizontal linear slider with the persistent introductory label **Clip gain:** and a synchronized numeric field labeled **Gain (dB)**. Show **Applied: −6.0 dB** separately from **Draft: −3.0 dB** while editing. Use decibels of amplitude gain relative to unity: 0 dB means unchanged amplitude, not silence. The proposed product range is −60.0 to +12.0 dB, in 0.1 dB increments; mute is outside this control's scope. These numbers are product choices, not HIG limits.

Map normalized leading-to-trailing position p to g = −60 + 72p dB, clamped to the endpoints and rounded to 0.1 dB. Label ticks −60, −30, 0 and +12 dB at their proportional positions; do not put 0 dB at the midpoint. The audio multiplier is 10^(g/20), not a linear amplitude mapping. Expose the exact signed value with one decimal and dB in the readout and thumb tooltip.

## State and commit model

- **Known/clean:** initialize draft from the selected clip's applied value. Apply Gain and Cancel are disabled until an edit exists.
- **Editing:** dragging, track clicking, arrow adjustment and numeric entry change only the draft. Update the displayed draft immediately; no audio or document change occurs on press, movement, key repeat, focus loss or pointer release. Show persistent text: “Not applied. Playback uses the applied gain.” Live feedback here is the exact draft value; audible preview is deliberately withheld because the brief reports a dangerous jump.
- **Valid/dirty:** enable **Apply Gain** and **Cancel**. Apply Gain is a normal system push button, not a window-wide Return default. Cancel discards the draft and restores the applied display. Escape cancels from anywhere within the gain group. No edit is added to history on cancellation.
- **Applying:** explicit Apply Gain activation validates again and pauses running playback before updating gain. If playback cannot be paused, leave gain unchanged and report failure. Apply the value atomically to the same clip; remain paused and show “Applied +3.0 dB. Playback paused; resume to audition.” If already paused, show “Applied +3.0 dB.” Do not automatically resume or start audio. Disable duplicate application while awaiting the result. Only confirmed model success updates Applied and creates history. Failure retains the draft and old applied value with “Gain was not applied. Try Apply Gain again.”
- **Unknown/unavailable:** show “Gain unavailable” and “— dB”; omit the thumb and value fill rather than implying any numeric position. Disable gain editing and Apply Gain. Explain “The clip's gain could not be read. Reselect the clip to retry.” No fallback to maximum or invented 0 dB. A successful reread initializes from the actual value. An out-of-range stored value shows its actual value and an unsupported-range explanation; never silently clamp persisted data.
- **Interrupted:** selection change, window close or an external gain update discards unapplied draft without writing it. Identify the new selected clip and show its actual applied gain. Report “Unapplied gain discarded” when a dirty draft is lost. An in-flight application must retain clip identity and serialize selection/external changes until its success/failure resolves; it must never write to the newly selected clip.

For every positive draft show “Boost may cause clipping or loud playback. Apply pauses playback; resume deliberately.” This is a caution, not a measured clipping prediction or hearing-safety guarantee. It does not disappear on a timer and does not rely on red color or a sound. No numerical safe-listening threshold is claimed.

## Exact entry, keyboard and access

The numeric field accepts signed finite locale-formatted numbers in dB; units remain outside the editable text. Permit partial input while typing. Return validates and stages a value without applying it. Leaving the field also validates without applying. Reject blank, nonnumeric, nonfinite, out-of-range or more-than-one-decimal values with nearby text explaining the valid range and precision. Preserve invalid text for correction and disable Apply Gain; never silently coerce it. Escape restores the applied value and clears validation.

With the slider focused, Left/Down decrease and Right/Up increase the draft by 0.1 dB; held arrows repeat the same increment and stop at bounds. Numeric text-field arrows retain text-editing behavior. Tab/Shift-Tab traverse slider, numeric field, Apply Gain, Cancel in visual order, skipping unavailable controls through system behavior. Supply visible focus and standard focused-button keyboard activation. A keyboard user can stage, apply, cancel and recover without a pointer; preserve system accessibility shortcuts.

Expose the slider's name “Clip gain,” adjustable role, draft value in decibels, bounds and 0.1 dB increment; expose the field's name, unit, validation and disabled reasons. Applied and Draft remain distinguishable in accessible text. Status and warnings must be available to assistive input without hearing audio. Prefer native semantics; actual announcements require Mac verification.

Use system text/styles with persistent readable labels; preserve labels, values, warnings and actions at 200% text enlargement through reflow. Check light/dark and Increase Contrast appearances. Separate targets without overlap. Start from the local accessibility guide's macOS 28 × 28 pt control target; for these buttons use 44 × 44 pt nonoverlapping activation regions while retaining standard visual sizing. The local Buttons guide gives a general 44 × 44 pt rule whereas Accessibility gives macOS 28 × 28 pt default/20 × 20 pt minimum; the larger button activation region is this specification's conservative resolution, not a universal macOS minimum.

## Recovery

Each successful Apply Gain creates one undo unit for that clip, regardless of drag distance or arrow repeats. Edit menu commands at the top are **Undo Clip Gain** (Command-Z) and **Redo Clip Gain** (Shift-Command-Z). Undo/redo discard any draft, pause playback before restoring gain, restore exactly the prior/next value and reveal the affected clip and applied value. A failed pause/write creates no history change. A new successful edit after undo clears redo. Preserve meaningful history during the open document session, including saves; reopening starts a new session. Cancellation and failed writes do not clear redo.

## Guidance basis

Local installed HIG snapshots informed these choices; the links identify official articles and were not fetched:

- [Sliders — macOS](https://developer.apple.com/design/human-interface-guidelines/sliders#macOS): bounded linear control, introductory label, useful ticks and exact/live feedback where feasible.
- [Text fields — Best practices](https://developer.apple.com/design/human-interface-guidelines/text-fields#Best-practices): persistent purpose, locale-aware numeric formatting and understandable validation.
- [Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards#Best-practices) and [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility): complete alternative operation and perceivable states.
- [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Role), [Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback#Best-practices) and [Undo and redo — macOS](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#macOS): explicit actions, proportional nearby feedback and standard reversible edit commands.

Staging all gain edits, pausing on application, the range, precision and warning policy are product decisions motivated by the supplied failure description.
