# Haptic feedback repair

Patched `interface.md` in place, replacing its three-sentence brief with an implementable iPhone feedback contract. Removed app-added typing impacts, made confirmation/error text independent of the haptic preference, and mapped confirmed upload success/failure to optional standard Success/Error cues. Added local-save truth conditions, revision-aware upload states, retry/reconciliation behavior, hardware/configuration fallback, deduplication, foreground timing, and privacy/accessibility requirements.

## Decisions and rationale

- Typing and autosave stay tactually quiet. Heavy impact has no specified physical metaphor here; repeating it on every keystroke overuses feedback. No custom pattern is warranted.
- Upload status persists next to the entry. A failed upload retains text and a retry action even with haptics disabled, unsupported, or imperceptible. Local save and remote acceptance are separate facts.
- An explicit foreground upload may emit one standard notification outcome cue when its result becomes visible. Automatic retries, duplicate callbacks, background completion, and history replay stay silent. The exact frequency policy is a product decision requiring hardware validation.
- Quiet, generic feedback avoids disclosing journal content. No new permissions, audio, telemetry, or notifications are introduced. Existing storage and transfer security are outside the supplied evidence.

The revised specification links the official HIG articles for [haptics](https://developer.apple.com/design/human-interface-guidelines/playing-haptics), [feedback](https://developer.apple.com/design/human-interface-guidelines/feedback), [accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility), and [privacy](https://developer.apple.com/design/human-interface-guidelines/privacy). Recommendations were derived only from installed local article snapshots; those links were not fetched.

## Worked before / after

Before: someone writes a paragraph and receives heavy impacts for every keystroke. They attempt an upload, which fails with only a vibration. With haptics off, confirmation information disappears, leaving no dependable outcome.

After: the same paragraph produces no app typing haptics. Once persistence confirms the revision, status reads “Saved on this iPhone.” Upload changes the status to “Uploading…”. A confirmed network failure changes it to “Couldn’t upload. Saved on this iPhone.” with “Retry upload” and a verified connection reason if available. An eligible foreground attempt emits one Error cue. With haptics off or unavailable, the identical text and recovery remain. Retry shows Uploaded and optionally one Success cue only after remote acceptance; newer edits remain separately identified. This is a specified walkthrough, not an executed app test.

## Acceptance checks

Static specification checks — passed by inspection of the revised file:

- No per-keystroke app feedback; no false Success cue for failure or upload initiation.
- Every listed outcome has nonhaptic status, and disabling haptics retains confirmation and recovery.
- Capability/configuration absence and failed playback have a silent fallback.
- Local safety claims require confirmed persistence; upload claims require accepted revisions.
- Duplicate, rapid, automatic, interrupted, stale, and background outcomes have explicit rules.
- Private journal content is unnecessary for feedback; no extra data collection is specified.

Runtime checks — not executed; required before shipping:

| Scenario | Acceptance condition |
| --- | --- |
| Write, paste, delete, and rapidly edit a long entry | No app-added typing or autosave haptics; editor remains usable. |
| Confirmed upload success, rejection, delay, and unknown outcome | Text matches actual revision/result; only confirmed success says Uploaded; appropriate recovery stays available. |
| Haptics off, unsupported hardware, system suppression, playback failure | Same status and functionality; no app-requested tactile output where suppressed; no blocking or substitution. |
| Duplicate callbacks, rapid retries, background/foreground, reopen | No duplicate/queued burst or replay; unresolved state survives and reconciles. |
| Local save failure and edits during upload | Text preserved; no false local-safety claim; old revision completion cannot mark new text uploaded. |
| Nonvisual use and assistive activation | Status and named recovery are discoverable and operable; updates preserve editing focus and avoid repeated keystroke announcements. |
| Physical iPhone comfort and synchronization | Brief appropriate outcome cues align with status, remain comfortable during repeated use, and do not interfere with any camera/microphone/motion feature if present. |

Failed checks: none observed in static inspection of the revised specification. The original brief explicitly failed the typing-frequency, tactile-only failure, and haptic-off information checks. Runtime results remain unknown.

## Evidence and audit limits

Read the installed root `.agents/skills/apple-hig/SKILL.md` explicitly, then searched `references/topic-index.md`. Followed the Patterns family to Playing haptics and Feedback, and Foundations to Accessibility and Privacy. Read each selected topic procedure before its supporting reference. Every instruction/source read used a separate `cat` or `rg` command for one file, resolved within that installed package.

Evidence consists of the original interface brief and installed guidance only. No app source, build target, SDK documentation, hardware capability report, rendered interface, or runtime trace was supplied. No web browsing, SDK compilation, device playback, GUI inspection, Accessibility Inspector, VoiceOver, or other assistive-technology execution occurred. Static specification checks establish coverage of the requested design changes, not implementation correctness, physical comfort, security, or accessibility conformance. API selection and availability remain implementation verification work.
