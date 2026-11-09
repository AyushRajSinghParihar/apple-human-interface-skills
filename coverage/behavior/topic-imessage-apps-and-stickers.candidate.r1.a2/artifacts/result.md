# Revised lunch-poll interaction specification

## Scope and evidence

Design for an iOS Messages extension, using framework-agnostic state and action contracts. The only product evidence is `interface.md`: entry shows an unrelated social feed; choosing a sticker immediately sends it with private notes; expanding loses the selected poll; recipients may lack the app. There is no supplied implementation, screenshot, backend, asset inventory, or device evidence. Proposed behavior below is a product decision unless explicitly attributed to HIG.

## Decisions and source support

| Observed behavior or requirement | Revised decision | Local guidance basis |
|---|---|---|
| Unrelated feed at entry | Open the poll associated with the tapped message; otherwise restore the current conversation's poll draft, or show “Plan lunch” and “New Poll.” Remove the social feed from the extension. | HIG recommends one quickly understood experience and lightweight collaborative decisions in [iMessage apps: Best practices](https://developer.apple.com/design/human-interface-guidelines/imessage-apps-and-stickers#Best-practices). |
| Compact experience | Compact view contains poll title, open/closed status, choices with counts, explicit vote actions, and “Details.” Creation and text editing use expanded view. | HIG places frequent functions in compact view and generally text editing in expanded view, avoiding keyboard obstruction; same source above. |
| Sticker selection sends immediately | Remove stickers from this core flow. Choosing a poll template only creates a local draft. “Preview Poll” prepares an exact public representation; “Add to Message” stages it for the host's explicit Send action. No selection sends a message. | Separating draft, preview and send is our correction; [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Content) supports labels that describe outcomes. No sticker assets are proposed, so sticker export checks are inapplicable. |
| Private notes attached | Keep private notes in a separate local-only record and out of every share serializer. Do not offer attachment of private notes in this version. Preview says “Shared: question, choices, vote totals and poll link. Your private notes stay on this device.” | Data minimization and precise usage disclosure: [Privacy: Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices). The local-only boundary is our product policy. |
| Expansion loses poll | Change presentation without recreating task state. Preserve poll ID, selected option, draft fields, pending operation and logical focus across compact/expanded, orientation changes and interruptions. | [Designing for iOS: Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices) calls for adaptation without breaking context. |
| Recipients without app | Include a readable message snapshot plus a link to the same poll. Specify a browser fallback without installation; also allow a plain-text reply if the link cannot be used. | [Collaboration and sharing](https://developer.apple.com/design/human-interface-guidelines/collaboration-and-sharing#Best-practices) distinguishes copies from shared access and calls for relevant-object links and clear permissions. Browser voting is a proposed dependency, not proven platform behavior. |

## Surfaces and actions

**Compact, open poll:** heading “Lunch today?”, status “Open · 3 votes”, then up to four options, each with name, numeric count, and a button such as “Vote for Tacos.” Below: persistent “Your vote: Tacos” when confirmed, “Details,” and “New Poll.” These option buttons immediately request a vote; they are commands, not ambiguous persistent toggles. Every participant has one vote and may change it. Choosing a different option replaces the prior vote only after confirmation from the service. The current option's button reads “Voted for Tacos” and is unavailable with its selected state exposed.

**Expanded:** retain the same poll header and voting controls; show full option labels, access explanation and “Copy Summary.” Draft creation/editing provides a question and two to four nonempty, distinct option names. “Preview Poll” becomes available when valid; show the validation reason otherwise. Editing sent questions/options is excluded from this version to avoid changing the meaning of existing votes. “Done” returns to compact and retains edits. No keyboard Return action sends or stages content.

**Preview:** show the exact public question, choices, snapshot timestamp and link representation, plus the privacy/access explanation. “Edit Poll” returns to the preserved draft. “Add to Message” stages this representation in Messages; it does not claim delivery. Sending remains an explicit host-owned action. If staging is unavailable or fails, retain the draft and show “Couldn't add poll. Try Again.” Do not fall back to automatic sending.

**Incoming message:** show question, numbered options, counts labelled “Snapshot at [time],” and “Open Poll” link. Text fallback: “Can't open it? Reply with your choice.” A reply is not automatically counted: the creator can record an explicitly attributed manual vote from Details, labelled “Recorded by organizer,” and the respondent can correct it. Never claim a snapshot is live.

**Details / collaboration:** show access policy, total participants, current results, “Copy Summary,” and creator-only “Close Poll” / “Reopen Poll.” Closing stops new votes but preserves results and can be reversed; it does not delete messages. “Copy Summary” produces a static plain-text copy labelled as such and excludes the access link and private notes. Returning from Details restores the same poll.

Buttons use short outcome labels, one prominent action per editing/preview surface, equal geometry for peer vote controls, and visible press feedback. Delayed actions show activity inside their activating button with an operation label; block repeat activation while pending. These choices follow [Buttons: Style and iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS).

## Collaboration, data and fallback contract

This design uses custom shared poll storage; it does not assume Messages exposes conversation membership or supplies identity, authorization, persistence or live updates.

| Data | Purpose and boundary |
|---|---|
| Public poll ID, question, options, counts, revision, open/closed state | Shared poll service; rendered into the preview and message snapshot. |
| Opaque participant credential and vote | Service enforces one vote per credential. No contacts or conversation-history access required. Identity assurance and cross-device recovery require implementation design. |
| Creator credential | Authorizes closing, reopening and manual vote recording; protect through established secure credential storage in implementation. Never serialize into a message. |
| Access link | Bearer access: anyone with the link may view and vote while open, including forwarded recipients. State this before staging. Do not label it “conversation members only.” Closing disables writes through every copy; readable snapshots remain. |
| Private notes and unsent edits | Local private storage keyed separately from public poll data. Never included in links, service requests, copied text, previews, message metadata or diagnostics. Retention is until explicit local draft removal; removing a draft does not delete a published poll. |

No permission prompts for contacts, photos, location or microphone belong in this task. Browser fallback must open the exact poll, explain bearer access, accept an explicit vote, show confirmed results and honor closure. If that infrastructure is unavailable, ship a clearly labelled static poll with numbered replies and organizer-recorded counts; do not promise browser voting or live collaboration. The installed HIG supports custom infrastructure/universal-link requirements but supplies no SDK availability or no-install voting guarantee.

## State and transition contract

```text
Task = {conversationScope, pollId?, draft, privateRecordKey,
        presentation, route, focusKey, confirmedVote?, revision,
        pendingOperation?}
PublicPoll = {id, question, options, counts, revision, status, accessLink}

serializeMessage(publicPoll):
    return allowlisted public fields + timestamped text snapshot
    // Never serialize Task or private records.

on presentationChange / orientationChange:
    change layout only; retain Task and restore logical focus
on textEditRequested:
    persist Task; request expanded layout; then focus field/show keyboard
on PreviewPoll:
    validate draft; create stable draft operation ID; show public-only preview
on AddToMessage:
    publish/reuse poll using same operation ID; stage public representation
    retain poll identity and draft until host outcome is known
on hostCancel / outcomeUnknown:
    retain draft and poll identity; do not claim sent or duplicate the poll
on hostSendConfirmed:
    mark shared only when host supplies reliable confirmation
on Vote(option):
    retain confirmedVote; submit idempotent operation against poll revision
    success -> replace confirmedVote and counts; show “Vote saved”
    failure -> retain prior vote; show persistent error and Retry
    stale/closed -> refresh exact poll; explain change; never silently reapply
on interruption / dismissal:
    save private Task by conversation scope; resume exact poll and pending op
```

Do not retry an uncertain write with a new operation ID. Resolve its status first. Merge concurrent votes server-side; a client must not overwrite aggregate counts. On refresh, keep options stable while someone is activating a button; announce results without moving focus. A link to another poll switches explicitly to that poll and preserves the previous draft in its conversation scope. Missing or expired links show “Poll unavailable” with the readable snapshot and reply fallback.

## Worked before → after

**Before, as supplied:** Alex opens the extension, sees a social feed, selects a sticker and immediately sends private notes. Expanding loses the lunch poll. Sam lacks the app.

**After, illustrative:** Alex opens “Plan lunch,” creates “Lunch today?” with Tacos and Sushi in expanded view, and adds a local note “Budget concern.” Preview shows only the question, options and bearer-link explanation. Alex returns to compact, expands again, and finds the same poll and note. “Add to Message” stages the public poll; Alex presses Messages Send. Sam reads the snapshot without the extension and opens the proposed browser fallback to vote for Tacos. A confirmed response shows “Your vote: Tacos.” If browser voting is unavailable, Sam replies “Tacos”; Alex records the reply with organizer attribution. Alex's note never crosses the public boundary. A failed vote retains Sam's previous confirmed state and offers Retry.

## Acceptance checks and status

**Passed — specification inspection only:** the written flow removes the unrelated feed; separates selection, staging and sending; explicitly excludes private notes; defines compact/expanded restoration, recipient fallback, permissions, copy semantics, closure, concurrency and retry behavior. These are properties of this document, not implemented behavior.

**Failed:** no executed implementation checks exist, so none are reported as failed. The supplied brief's three adverse behaviors are reported observations requiring correction, not independently reproduced failures.

**Not executed — implementation acceptance gates:**

1. Open from a message and from the extension entry point; reach the relevant poll or creation state without the social feed. Compact voting must remain usable without a keyboard; editing must expand before text entry.
2. Enter a question, options and a unique private-note sentinel. Expand/collapse, rotate, dismiss/reopen and interrupt. Restore the same poll, edits and confirmed vote without duplicate writes or another conversation's draft.
3. Selecting a template and opening preview must send nothing. Cancel staging and repeat it: preserve the same poll ID. Only explicit host Send may deliver. Inspect every payload, link, clipboard value, request and diagnostic for absence of the private sentinel.
4. Exercise installed-app and no-app recipients, forwarded links, unavailable links, offline use and closed polls. Links must target the same poll. Verify bearer access matches the disclosure and closure is enforced server-side. Static copies must remain distinguishable from current results.
5. Submit concurrent votes, repeat a pending tap, simulate lost acknowledgments, stale revisions and failures. Count one vote per participant credential, preserve prior confirmed votes on failure, and expose persistent recovery. Verify organizer attribution on manual votes.
6. Use at least 44 × 44 pt nonoverlapping activation regions for iOS buttons. The accessibility guide lists a smaller 28 × 28 pt minimum, but this design chooses its 44 pt default and the Buttons guide's general target recommendation. Measure actual hit regions separately from visible artwork.
7. Start with iOS's 17 pt default body text; preserve full labels/actions at 200% enlargement through wrapping and scrolling, without reducing hit regions. Test compact and expanded, portrait and landscape, keyboard visible, light/dark and Increase Contrast. Measure actual contrast; no palette or rendering exists to assess here.
8. Expose action names, button roles, unavailable states and persistent confirmed/pending/error text. Keep task order: question → status → options/actions → personal vote → secondary actions. Complete voting and editing with VoiceOver, Switch Control and Full Keyboard Access; no gesture or speech-only action. Selection and status must not rely on color or sound. Avoid decorative animation and preserve meaning under Reduce Motion.

Checks 6–8 apply [Accessibility: Vision, Mobility, Speech and Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). Layout overflow may scroll or offer expanded view, but must not hide the only primary action or discard context.

## Evidence limits and route audit

Read the installed root `.agents/skills/apple-hig/SKILL.md`, inspected `interface.md`, and searched the installed topic index. Then read each owning family SKILL.md, each selected `.topics/.../SKILL.md`, and finally its matching reference: Getting started → Designing for iOS; Technologies → iMessage apps and stickers; Patterns → Collaboration and sharing; Foundations → Privacy and Accessibility; Menus and actions → Buttons. Each file was read with an individual `cat` command; topic-index searches used `rg`.

All Apple links above identify the official articles represented by the local snapshots; they were not browsed. Local references are application guidance derived from HIG, dated 2026-10-25, not SDK documentation or independently verified current Apple pages. No source conflict was found; the control-size distinction is retained above. No graphical session, device, Messages host, browser fallback, SDK build, backend enforcement, accessibility tool, contrast measurement or physical comfort test was executed. Universal-link routing, host staging/send callbacks, credential handling and cross-device identity remain implementation dependencies. The specification does not certify accessibility, security or App Store eligibility.
