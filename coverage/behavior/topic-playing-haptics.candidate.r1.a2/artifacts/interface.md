# iPhone private journal — revised feedback specification

Platform: iOS on iPhone. Requested haptics may be unavailable on some devices or suppressed by configuration. This specification defines behavior, not SDK implementation. Preserve the existing editor and upload feature.

## Feedback contract

Text and accessible status are authoritative. Haptics are optional reinforcement; disabling or failing to play them must never change stored content, upload behavior, status, recovery actions, or confirmation information. No app-added sound accompanies these events, so private journaling remains quiet.

| Event / truth source | Persistent feedback near the entry | App-requested haptic |
| --- | --- | --- |
| Keystroke, paste, deletion, cursor movement | Normal editor content and caret | None. Remove heavy impacts and do not replace them with selection clicks. Leave system keyboard behavior to iOS. |
| Local write pending | “Saving on this iPhone…” | None |
| Local persistence confirms current revision | “Saved on this iPhone” | None; routine autosave must not produce repeated success cues. |
| Local persistence fails | “Couldn’t save on this iPhone. Keep this entry open and try again.” Offer “Retry save”; retain editor text. | None; durable error and recovery remain available. Do not claim local safety. |
| User starts Upload or Retry upload for a locally saved revision | “Uploading…”; suppress duplicate activation while that attempt is active | None; starting work is not success. |
| Upload service confirms that revision was accepted | “Uploaded” for that revision | One brief standard notification Success, if eligible. |
| Upload fails or is rejected | “Couldn’t upload. Saved on this iPhone.” Offer “Retry upload”. Add a verified actionable reason when known, such as “Check your connection.” | One brief standard notification Error, if eligible. Never use Success or an impact as a failure signal. |
| Upload outcome unknown after interruption | “Upload not confirmed. Saved on this iPhone.” Offer “Check upload status”; reconcile before retrying | None; do not invent success or failure. |

The local-safety wording above is permitted only after local persistence confirms the relevant revision. Require local save before starting upload; if it fails, use the local-save error state instead. Preserve entry text, selection, and editing context through errors. Retry must reuse the entry/revision identity so it cannot create duplicate entries.

Keep local-save and upload states distinct. If someone edits while an older revision uploads, show current local status plus “Earlier version uploaded” when that older revision completes; never label new edits Uploaded. Ignore stale/duplicate callbacks for replaced attempts. On returning to the entry, restore or reconcile its status rather than clearing an unresolved error. Editing stays available while upload runs.

## Haptic eligibility and timing

Use the standard iOS notification meanings above. No custom waveform, continuous vibration, heavy impact, or per-keystroke app haptic is needed: typing has no collision/weight metaphor and repetition distracts from writing. Native feedback must not be layered with an extra app cue for the same outcome.

Emit at most one outcome cue per explicit foreground upload attempt, at the same state transition that updates its visible status. Repeated callbacks and automatic/background retries produce no extra cues. Serialize cues; if one is already playing, drop the next optional cue rather than queueing a burst. Do not replay outcomes when unlocking, returning to the foreground, or reopening an entry. These frequency rules are product decisions, to be validated for comfort on hardware.

Before playback, require the existing app haptic preference to be enabled and the selected implementation to support the requested feedback under the current device/configuration. Respect system suppression. If unsupported, suppressed, interrupted, or playback fails, silently omit the cue; never substitute an invented vibration or block the state transition. Do not infer hardware support from iOS alone. Verify exact API/capability checks and availability against the target SDK during implementation.

The app’s existing haptic-off preference controls only app-requested tactile output. Turning it off cancels pending app cues immediately; turning it on does not replay history. It must not remove any confirmation, error, or recovery action.

## Nonhaptic access and privacy

Status is durable inline text, not a timed toast, color-only mark, or modal alert for routine upload failure. Expose its same wording as accessible status, and label recovery actions by their visible names. Status changes must be perceivable without sight or vibration through supported assistive technology; avoid repeated announcements on keystrokes and preserve editing focus. Actual announcement behavior requires implementation and device testing.

Keep feedback generic: never include journal text or entry titles in haptic-related status, diagnostics, or notifications. This repair adds no background notifications, audio, permissions, or telemetry. Playback requires no journal content; upload retains the existing user-invoked transfer scope. Data needed here is entry/revision and attempt identity, persistence/transfer result, preference, and capability state. Keep these local for feedback; do not add collection. Existing upload consent, security, and retention are unspecified and require separate review, not assumed protection.

## Guidance basis

Applied from installed local snapshots, without web verification:

- [Playing haptics — Best practices and iOS](https://developer.apple.com/design/human-interface-guidelines/playing-haptics): consistent meanings, brief discrete cues, avoid overuse, synchronize feedback, preserve functionality when disabled, and account for supported hardware.
- [Feedback — Best practices](https://developer.apple.com/design/human-interface-guidelines/feedback): truthful contextual outcomes and actionable recovery through complementary channels.
- [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility): retain meaning without dependence on one sense and give people time to perceive feedback.
- [Privacy — Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy): minimize data use and transfers. Generic private status and no added sound/telemetry are product choices, not claims that HIG mandates this exact design.
