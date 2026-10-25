# First-run revision

Patched `interface.md` in place. The revised contract opens a usable canvas, replaces eight forced pages with optional inline learning, persists dismissal and completion across updates, supplies a later Help route, and moves each permission to the action that needs it. It also specifies interruption, refusal, migration, offline use, and save-failure behavior.

## Decisions and rationale

The original file explicitly required eight tutorial pages before a blank canvas, simultaneous camera/microphone/location requests for later optional features, and tutorial replay after every update. Those are the observed specification problems; no running interface was supplied.

- Start with drawing because the brief establishes no indispensable setup. Apple recommends quick, optional learning and deferring optional requests: [Onboarding — Best practices / Additional requests](https://developer.apple.com/design/human-interface-guidelines/onboarding).
- Remember learning outcomes independently of release versions; keep guidance available through Help. This applies the onboarding skip-memory guidance and [Offering help — Creating tips](https://developer.apple.com/design/human-interface-guidelines/offering-help) to an explicit eligibility model.
- Request camera, microphone, or one-time location access only for the selected attachment action. Specific purpose copy and denial recovery apply [Privacy — Requesting permission / Location button](https://developer.apple.com/design/human-interface-guidelines/privacy).

The exact attachment features, local draft model, hint wording, state names, and conservative migration fallback are proposed product decisions. Apple guidance supports the direction; it does not mandate these exact choices or establish the app’s current capabilities.

## Worked before/after

Before: a fresh-install user wanting to sketch must pass eight tutorial pages and encounters three unrelated permission requests before reaching a blank canvas. After an update, the tutorial returns.

After: the same user reaches an editable canvas with the default pen selected, makes a mark without dismissing anything, and gets a locally saved entry. The hint disappears and learning state becomes completed. Later, Add photo → Take photo requests only camera access. If refused, the sketch stays editable and saved. After an update, the last entry reopens without tutorial replay. Help → Sketching basics remains available on demand.

The revised design has zero mandatory tutorial pages and zero permission prompts before a first mark. This is a specification-level comparison, not a measured reduction in task time or abandonment.

## Acceptance checks and status

Passed — static specification inspection:

- Fresh-install path reaches drawing without a tutorial or optional permission gate.
- Dismissal, skip, completion, first-stroke persistence, update migration, and later help access have explicit transitions.
- Each protected resource has an action, minimum purpose, request moment, proposed copy, and denial/cancellation path.
- Offline essentials, unavailable optional capabilities, current-entry preservation, and save failure are specified.

Failed: no unresolved failure found in this document-level check. This does not report an application test pass.

Not executed — implementation acceptance checks:

1. Fresh install offline: make and save a stroke with no tutorial dismissal or authorization prompt; relaunch and recover the entry.
2. Dismiss the hint or skip guidance, terminate and relaunch, then update the app: no automatic guidance returns. Repeat for Done and first-stroke completion.
3. Migrate prior-used installations, including ambiguous legacy history: preserve entries and avoid tutorial replay. Confirm a genuinely fresh install still receives its inline hint.
4. Open Help on an existing draft, close and reopen guidance: strokes and editor context remain intact; dismissal does not reset eligibility.
5. Exercise each optional action with undetermined, authorized, denied, and restricted states. Verify only the selected resource is requested; refusal never blocks drawing or saving. Check cancellation and Settings return without automatic capture.
6. Verify one-time location behavior, approximate location, absent hardware, service failure, and interrupted recording. Verify no background tracking or unauthorized capture occurs.
7. Simulate missing optional assets and storage failure: basic drawing remains available; failed saves retain work and Retry works without false success.
8. Check localized help and system location-control text for truncation, native authorization rendering, and accessibility behavior on the implemented iPhone interface.

## Evidence and limits

Read the installed root `apple-hig/SKILL.md`, searched `references/topic-index.md`, then read the Patterns and Foundations family procedures. Read Onboarding and Privacy topic procedures before their supporting source guides; followed the onboarding route to Offering help and read its procedure before its guide. All paths resolve within `.agents/skills/apple-hig/`; each read used a separate command for one file. The supplied `interface.md` was the sole product evidence.

The local guides identify a 2026-10-25 snapshot/retrieval date. Official links above are attribution only; no web browsing occurred. No device, SDK, build, GUI, accessibility, permission-persistence, security, storage, or usability execution was performed. No code or runnable application was supplied. Real API availability, state durability, data transfers, privacy disclosures, and measured first-run outcomes remain unverified.
