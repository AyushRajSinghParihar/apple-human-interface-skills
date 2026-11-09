# Recognition-state repair

Patched [interface.md](interface.md) in place from its original one-paragraph brief into an implementable iPhone interaction contract. Launch is now idle; recognition requires an explicit action, consent, a bounded sample, and cancellable processing. Results are suggestions, ambiguity requires visitor choice, no match clears current results, and denied permission leads to manual lookup or Settings without repeated prompts. Failures, interruptions, stale callbacks, and repeated taps have explicit handling.

Decisions follow the installed apple-hig root, the topic-index search, and the owning family → topic procedure → source-guide routes for ShazamKit, Privacy, Accessibility, Progress indicators, and Buttons. Each instruction/source file was read individually using cat; the index was searched using rg. The source links and product-specific qualifications are included in interface.md. No web sources were fetched. No framework migration is prescribed.

## Worked before/after

Before: launch starts indefinite listening; a guessed “Roman Gallery” is announced as certain. A later unsuccessful attempt still shows Roman Gallery. Denying access repeatedly triggers another permission attempt.

After: launch shows Ready with the microphone off. Identify Sound requests permission only if undetermined. With access, Listening captures at most 10 seconds, stopping earlier when sufficient; Matching has a separate 10-second ceiling with capture already stopped. Two plausible candidates, “Roman Gallery — 12” and “Greek Gallery — 13,” produce Ambiguous, with neither selected. The visitor may view a suggestion and explicitly choose it, retry, or browse. Retrying clears those candidates immediately. If the new sample returns no eligible candidates, No match replaces them; a delayed callback from the previous session cannot restore Roman Gallery. Denial instead shows Access Off; opening Settings and granting permission returns to Ready without automatic recording.

## Acceptance checks

Passed — specification inspection only:

- Ready has no launch-time recording; every capture path requires authorization and an explicit initiating action.
- Listening and Matching have finite bounds, safe cancellation, separate microphone states, and no fabricated completion percentage.
- Possible match, Ambiguous, No match, Access Off, Unavailable, and Cancelled define copy, actions, and transitions.
- Retry clears current results; session invalidation prevents stale restoration after cancel, navigation, interruption, or completion.
- Browse Exhibits provides an end-to-end alternative without microphone access; permission denial does not gate museum information.
- Text preserves uncertainty and status without sound or color; action names, reading order, enlargement, and target requirements are specified.

Failed: none identified in the revised document during static inspection. This does not establish an implemented pass.

Not executed — required implementation acceptance:

1. Launch and relaunch with each permission state; verify zero capture before consent, one contextual system request when undetermined, no repeated request after denial, restricted-state recovery, and explicit restart after Settings.
2. Instrument microphone lifecycle: sufficient early sample, 10-second capture limit, processing-only interval, result, cancellation, backgrounding, revocation, and capture/service failures must all release capture. Verify matching timeout and absence of automatic retry.
3. Inject single, multiple, empty, malformed, unknown-catalog, delayed, and out-of-order results. Verify conservative labels, correct exhibit opening, clearing on retry/no match, and rejection of invalidated callbacks. Rapid taps must create one session.
4. Exercise Browse Exhibits through a numbered selection with denied access, unavailable recognition, and an active session. Verify capture stops and the correct detail opens.
5. On supported iPhone builds, test VoiceOver and other supported assistive inputs for reachable actions, status uncertainty, order, and no repeated score announcements. Verify at least 200% text enlargement, 44 × 44 pt targets, separation, and light/dark contrast with actual measurements. No geometry or contrast measurements are available here.
6. Validate real museum recordings, noise, catalog coverage, eligibility thresholds, ambiguity signals, and session durations. Audit audio transfers, transient-buffer deletion, logging, purpose text, and privacy disclosures against implementation.

## Evidence limits

The supplied artifact contained only a behavioral brief: no code, screenshots, SDK configuration, recognition backend, catalog, device logs, or data-flow evidence. This work repairs the specification; it does not demonstrate microphone control, permission behavior, recognition accuracy, native UI rendering, SDK compilation, GUI execution, or accessibility execution. The installed guides are a dated local HIG-derived snapshot, not SDK API documentation or proof of independent source review. The 10-second limits and conservative result policy are proposed product choices requiring validation. Processing location and actual audio retention/transfer remain unknown; the revised specification sets release requirements rather than making claims about the existing app.
