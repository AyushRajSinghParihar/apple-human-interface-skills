# Haptic feedback repair

Patched `interface.md` in place, replacing its three-sentence problem description with an implementable iPhone feedback contract. This is a specification repair; no app implementation was supplied or executed.

## Decisions and patch summary

- Removed app-generated heavy keystroke impacts and routine autosave/retry vibration. Apple advises avoiding overuse and matching impact to physical metaphors; removing typing cues is this app's design choice.
- Mapped explicit upload completion to standard Success and failure to standard Error, synchronized with truthful status. Added capability, preference, foreground, deduplication, and overlap gates; background events remain quiet.
- Added persistent local-save, uploading, uploaded, and failure text, with Retry and retained drafts. Haptic-off and unsupported hardware preserve the complete flow. Local write and exact-revision server acknowledgment are separate truth sources.
- Defined late callbacks, edits during upload, interruption, local-save failure, and rapid outcomes. No cue is queued or replayed.
- Kept private content out of outcome copy and added accessible status and recovery requirements. No new telemetry or permission flow is introduced.

Source support: [Playing haptics](https://developer.apple.com/design/human-interface-guidelines/playing-haptics) supports standard meanings, restraint, synchronization, and disabled functionality; [Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback) supports complementary channels and contextual recovery; [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) supports sensory alternatives; [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy) supports data minimization. Specific copy, local retention requirements, revision rules, and event gating are product decisions, not quoted Apple mandates.

## Worked before/after

Before: A person types a private entry, receiving a heavy impact for each character. Upload fails and only vibration conveys the failure. With haptics off, confirmation information disappears.

After: Typing generates no app haptic. Once the local write succeeds, the entry reads “Saved on this iPhone.” An explicit upload shows “Uploading…”. A network failure leaves the entry intact and shows “Couldn’t upload. Saved on this iPhone. Check your connection and retry,” with Retry. A supported, permitted foreground event adds one Error cue. With haptics off or unavailable, the same text and action remain. Retry shows “Uploading…” and only a server acknowledgment of that revision produces “Uploaded,” optionally paired with one Success cue. If the person edited meanwhile, the status identifies the uploaded earlier version instead of falsely claiming current changes uploaded.

## Acceptance checks

Passed — static specification inspection:

- Every original defect has an explicit replacement requirement in `interface.md`.
- Success depends on confirmed remote completion; local save and remote state are distinct.
- Every upload outcome has nonhaptic text; failure has persistent recovery.
- Haptic-off, unsupported hardware, rapid events, interruption, and background events have defined behavior.

Failed: No static specification checks identified as failed. This does not imply implementation passes.

Not executed — required implementation/device checks:

| Scenario | Acceptance criterion |
|---|---|
| Sustained typing and autosave | Zero app-generated keystroke/autosave cues; no repeated-impact distraction |
| Explicit successful, rejected, delayed, and failed upload | Correct persistent state; no premature Success; failure retains entry and enables Retry |
| Haptics on/off; capability absent; system suppression | Identical content/recovery, with zero app cues when ineligible; pending outcome respects changed preference |
| Rapid retry, duplicate callbacks, overlapping outcomes | No duplicate or overlapping tactile flood; truthful latest state; no replay |
| Edit during upload; background/return; relaunch | Revision-specific confirmation; no false Uploaded or delayed tactile cue |
| Local save failure | Draft retained in editor; no false local safety claim; Retry save available |
| Sound muted and haptics disabled | Complete upload/recovery task remains understandable from accessible text |
| VoiceOver and other supported assistive inputs; enlarged text | Status and Retry perceivable and operable; no disruptive focus jump or hidden recovery at 200% text |
| Physical iPhone evaluation with people | Brief cues align with outcomes and are comfortable at realistic frequency |
| Camera/microphone/motion tasks, if the app supports them | Cues do not interfere with recording or sensing; suppress during conflicting work if needed |

## Evidence limits and audit trail

Read the installed root `apple-hig/SKILL.md` explicitly, inspected `interface.md`, and searched the local topic index for haptics, feedback, accessibility, and privacy. Read Patterns and Foundations family procedures, then the Playing haptics, Feedback, Accessibility, and Privacy topic procedures before their respective source guides. All paths resolved under `.agents/skills/apple-hig/`; each read used a separate single-file command.

Only supplied local files and installed instructions were used. Official links above are attribution from local guides, not browsed sources. No web, device, SDK build, GUI, Accessibility Inspector, assistive-technology, physical-comfort, synchronization, sensor, or security execution occurred. Hardware support, persistence, upload acknowledgment, and actual preference behavior remain implementation requirements requiring evidence. The supplied artifact does not establish the app's framework, storage guarantees, upload consent model, or security protections.
