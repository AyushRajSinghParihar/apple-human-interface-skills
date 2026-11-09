# First-run revision

Edited `interface.md` in place, replacing the original three-sentence flow with an actionable iPhone specification. It now opens directly into drawing, replaces eight mandatory pages with optional practice and a dismissible hint, persists learning choices across updates, and requests each optional permission at its feature's point of use. It also specifies cancellation, denial, interrupted learning, upgrade migration, local saving, and later Help access.

## Decisions and support

The first valuable task is making and retaining a sketch. None of the supplied optional permissions is a prerequisite. Apple's [Onboarding](https://developer.apple.com/design/human-interface-guidelines/onboarding#Best-practices) guidance supports safe interaction, optional learning, remembered skipping, and later access. Zero mandatory tutorial pages is this revision's product choice, not an Apple numerical requirement.

A short hint and disposable practice protect journal work while allowing learning. Eligibility ends after dismissal or the first stroke, and tutorials never reopen automatically. This applies [Offering help](https://developer.apple.com/design/human-interface-guidelines/offering-help#Creating-tips); the exact cadence and copy are design decisions.

Camera/photo attachment, microphone/audio note, and location/place tag are explicit proposed feature mappings because the original only says these features are optional. Each has a purpose, minimal access, cancellation, and denial route. Context replaces custom pre-alerts. The one-time system location button suits a single attachment action on supported iOS versions. These choices follow [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission) and its [Location button](https://developer.apple.com/design/human-interface-guidelines/privacy#Location-button) section. System styles, descriptive labels, and specified 44 × 44 pt iPhone hit regions follow [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices).

## Worked before/after

Before: a new user wanting to draw must pass eight tutorial pages and encounter camera, microphone, and location requests before reaching a blank canvas. After an update, the same tutorial returns. Exact taps and elapsed time are unknown.

After: launch opens an editable canvas with no permission request and no required onboarding action. The user draws a stroke; the hint disappears and a journal entry is saved locally. Later, selecting Take Photo requests only camera access. Denying it leaves the sketch intact and drawing available. After an update, the latest journal entry resumes without a tutorial. Help → Sketch Basics remains available and uses disposable practice, preserving the entry on Skip Tutorial or Done. This is a specified walkthrough, not an executed result.

## Acceptance checks

Passed — static specification inspection:

- `interface.md` was replaced with the revised specification, including entry, learning, persistence, recovery, permission, and action contracts.
- No mandatory tutorial or optional authorization gates the first stroke.
- Every original permission category has a contextual request and nonblocking unavailable/denied outcome.
- Skip/dismiss persistence, upgrade migration, interrupted practice, bundled initial tools, and Help re-entry are explicit.

Failed: no static specification checks identified as failing. This does not establish runtime success.

Not executed — implementation acceptance scenarios:

1. Fresh install, offline: draw immediately; see zero permission prompts before drawing; save and relaunch into the retained entry. No asset download is required.
2. Dismiss the hint, skip practice, relaunch, then update: neither appears automatically. Help still opens practice. Repeat with completed practice and an existing install lacking learning flags.
3. Interrupt practice or open Help mid-entry: return to the same journal content and selected tools; no practice marks or empty journal entries are added.
4. Invoke each optional action with undetermined permission: only its relevant system authorization appears. Grant, deny, restrict, revoke, cancel, and return from settings; drawing and existing content remain usable. Authorized repeat use does not prompt again unnecessarily.
5. Location: verify supported system-button behavior and one-time scope; verify typed-place fallback when unavailable. No continuous/background acquisition occurs.
6. Force a save failure: show unsaved status, retain the working canvas, retry successfully, and do not claim success before persistence. Check interruption recovery under available storage.
7. Measure iPhone hit regions and separation, test long/localized labels, and verify system control activation and assistive-technology behavior on an implemented build.

## Evidence and limits

Used only local files and installed guidance; no web requests. Explicitly read the installed root `.agents/skills/apple-hig/SKILL.md`, searched its topic index, then read the Patterns and Foundations families and the Onboarding and Privacy topic procedures before their source guides. For the Help route, read Offering help's procedure before its guide. For actions, read Menus and actions, then Buttons' procedure before its guide. Each instruction/source read used a separate single-file command. Links above identify official source sections; they were not fetched.

The package is a dated, independent HIG summary (local references dated 2026-10-25), not SDK documentation or proof of current API availability. No app code, deployment target, screenshots, measurements, or persistence implementation was supplied. No device, SDK build, GUI, permission dialog, accessibility, storage-failure, or usability test was executed. Expected reduced friction is a design rationale, not a measured retention or speed improvement. Actual feature mappings, data handling, privacy disclosures, authorization APIs, and location-button availability require implementation verification.
