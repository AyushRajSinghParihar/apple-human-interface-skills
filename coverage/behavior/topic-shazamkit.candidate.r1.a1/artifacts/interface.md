# iPhone museum companion — sound recognition specification

Platform: iOS on iPhone. Sound recognition helps visitors find exhibit information; it is optional and complementary to manual browsing. Preserve the existing recognition stack. The brief supplies no framework, catalog, accuracy data, or implementation. ShazamKit guidance informs sampling behavior; adopting ShazamKit is not required.

## Entry and permissions

Launch into Ready, never recording or requesting microphone access. Show “Identify an exhibit” and “Listen briefly to find a possible exhibit. You can also browse exhibits.” Primary: **Identify Exhibit**. Secondary: **Browse Exhibits**, opening the museum catalog without microphone permission. Catalog entries include exhibit name, gallery and exhibit number so a visitor can select using a physical label without hearing the exhibit audio.

On Identify Exhibit, inspect current authorization and capability:

- Undetermined: invoke the system microphone request in this action's context, without an extra custom pre-alert. Purpose string: “Use the microphone to recognize exhibit audio and find its museum information.” No capture before authorization. If granted while this action remains active and foregrounded, start one sample; otherwise return to Ready.
- Granted and available: start one sample.
- Denied: show Permission Denied; do not request again, including after relaunch or retry taps. Offer **Open Settings** as a secondary, explicit action and **Browse Exhibits** as primary. Copy: “Microphone access is off. Browse exhibits, or change microphone access in Settings.” Returning from Settings rechecks permission but never starts capture automatically; granted returns to Ready.
- Restricted: show “Microphone access is restricted on this iPhone.” Offer Browse Exhibits; do not suggest Settings can necessarily remove the restriction.
- Unavailable (for example capture cannot start or catalog service is unavailable): use Unavailable below. Check prerequisites before capture where possible.

## State and transition contract

One attempt has a unique ID. Starting an attempt clears the previous recognition candidate and invalidates prior callbacks. Keep manually opened exhibit pages intact in navigation history, never as the current recognition outcome. Only the active attempt can update the recognition screen.

The 10-second capture cap and 15-second processing cap below are initial product choices, not HIG timings or measured performance guarantees. Revisit against representative museum tests; never ship unbounded waits.

| State | Visible content and actions | Transition and capture behavior |
| --- | --- | --- |
| Ready | Entry copy; Identify Exhibit; Browse Exhibits | Capture off. Only Identify Exhibit can initiate permission/sample flow. |
| Listening | “Listening for exhibit audio…”; activity indication in the initiating button, now labeled “Listening”; separate **Cancel**; Browse Exhibits | Start only with access. Ignore duplicate Identify taps. Stop capture immediately when the recognizer has the needed sample, or at 10 seconds at the latest. If sample is usable, enter Processing; otherwise No Match. An early usable result stops capture and resolves directly. |
| Processing | “Finding a possible exhibit…”; same in-button activity indication labeled “Finding Exhibit”; Cancel; Browse Exhibits | Capture off. Resolve within 15 seconds from entry; processing timeout enters Unavailable. |
| Possible Match | “Possible match: [exhibit name]”; gallery and exhibit number; “Check the exhibit label before opening.” Primary **Open Exhibit**; secondary **Try Again**, **Choose Another Exhibit** | Capture off. Never say “This is…” or announce certainty. Opening is explicit and leads to the chosen exhibit details; no automatic navigation or narration. Choose Another Exhibit opens manual catalog. |
| Ambiguous | “Several exhibits may match. Check the exhibit label.” Show up to three distinct candidates with name, gallery and number, each labeled **Open [name]**; Try Again; Browse Exhibits | Capture off. No preselected candidate. Use catalog order until ranking quality is validated. More candidates remain available through browsing. |
| No Match | “No exhibit matched this attempt. Try again near the exhibit's audio, or browse exhibits.” Primary **Try Again**; Browse Exhibits | Capture off. Clear prior candidate, title, image, detail link and any spoken result; do not present an earlier exhibit as a current match. No automatic retries. |
| Unavailable | “Sound recognition is unavailable right now. You can browse exhibits.” Add a specific cause only when known, such as “The recognition service could not be reached.” Primary Browse Exhibits; **Try Again** when a fresh attempt is meaningful | Capture off. Distinguish service/capture failure from a completed search with no match. No guessed cause, repeated background retries or permission requests. |
| Permission Denied / Restricted | Copy and actions above | Capture off. Recheck status on return to foreground without prompting. |

Cancel stops capture and processing, invalidates the attempt, clears transient recognition content and returns to Ready without an error message. Browse Exhibits, leaving the recognition screen, backgrounding, locking, interruption or access revocation likewise stops capture and invalidates pending work. Return to Ready on reentry, except that revoked access shows the applicable permission state. A user must explicitly start again. Stop/release the capture resource on every exit path, including errors. Late, out-of-order and cancelled callbacks cannot restore candidates or start narration.

## Result quality and correction

Accept only catalog-backed candidates for the current sample. A recognizer's resolved single candidate becomes Possible Match, multiple plausible candidates become Ambiguous, and no useful candidates become No Match. Any internal filtering thresholds need representative validation; no numeric confidence, accuracy claim or confidence-ranked UI is justified by the supplied evidence. All candidates remain tentative, even a single one.

Choose Another Exhibit lets the visitor immediately replace a mistaken suggestion with a catalog selection. Show the selected details as “Selected by you”; retain that choice in navigation history and allow choosing again. Do not silently substitute the rejected suggestion on return. This is a navigation correction, not a promise to retrain the model. Browsing/opening an exhibit is not inferred approval or training consent. No calibration questionnaire blocks the task.

## Data-purpose contract

| Data | Purpose and boundary |
| --- | --- |
| Microphone sample | Only the visitor-initiated recognition attempt. No background or continuous recording, raw-audio history, analytics attachment or model-training reuse. Release transient sample buffers when an attempt ends or is cancelled. |
| Recognition query / derived signature | Only current catalog lookup. Prefer local matching where the existing stack supports it. Transfer, provider retention and deletion behavior are unknown: audit these before release and document the actual destination/use in privacy information. Do not claim on-device-only processing. |
| Selected exhibit | Navigate to museum information; preserve ordinary navigation history. No behavioral profiling or model-feedback transmission is introduced by this specification. |

If the existing service requires raw audio transfer or retention outside these boundaries, resolve that architecture and accurate disclosure before enabling recognition; manual browsing remains usable. Align App Store privacy disclosures with verified behavior.

## Presentation and accessible operation

Use persistent inline text for every state and outcome, with no timed dismissal. Sound, color or animation never carries the only status or result; optional spoken feedback must use the same tentative wording and never autoplay exhibit narration. Use system text buttons and styles with clear press/disabled states; preserve the initiating button's context during work. Only the current state's primary action receives prominent emphasis. Cancel abandons the active attempt and is not destructive. Candidate opening and Settings changes always require explicit activation.

Specify at least 44 × 44 pt activation areas for iPhone controls, separated without overlap; this is the chosen default, not a claim that the source's smaller accessibility minimum is prohibited. Labels and state text must remain readable and operable at 200% text enlargement, reflowing vertically and scrolling when needed. Expose visible button labels as accessible names, button roles and pending/disabled states; task reading order is state heading, explanation/candidates, primary action, recovery alternatives. Test assistive navigation rather than inferring it from system controls. Keep a static text status sufficient without the activity animation.

## Guidance basis

These links identify official articles underlying the installed local snapshot; no online verification was performed.

- [ShazamKit — Best practices](https://developer.apple.com/design/human-interface-guidelines/shazamkit#Best-practices): explain/request microphone access and stop after the needed sample.
- [Privacy — Requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission) and [Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices): contextual permission, precise purpose, minimum collection and preference for on-device processing.
- [Machine learning — Mistakes, Corrections, Confidence and Limitations](https://developer.apple.com/design/human-interface-guidelines/machine-learning): recoverable errors, alternatives and validated confidence. The exact state names, caps, catalog fallback and wording above are product decisions.
- [Buttons — iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS) and [Style](https://developer.apple.com/design/human-interface-guidelines/buttons#Style): in-button activity feedback and system styles.
- [Accessibility — Vision, Hearing, Mobility and Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility): enlarged text, multiple sensory paths, comfortable targets and persistent outcomes.
