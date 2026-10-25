# Revised lunch-poll interaction specification

Design contract for an iOS Messages extension; framework agnostic. The only product evidence is `interface.md`: the initial view is an unrelated social feed, selecting a sticker immediately sends it with private notes, expansion loses poll selection, and recipients may lack the app. No screens, implementation, backend, assets, or SDK are supplied. All behavior below is proposed unless explicitly identified as observed.

## Decisions and rationale

| Observed behavior or need | Revised decision | Source and scope |
|---|---|---|
| Full unrelated feed at entry | Open the selected conversation poll, otherwise the last poll used in this conversation, otherwise a small empty state with “Create Lunch Poll.” Remove the feed from this extension. | [iMessage best practices](https://developer.apple.com/design/human-interface-guidelines/imessage-apps-and-stickers#Best-practices): one quickly understood experience and frequent functions in compact view. |
| Expansion loses selection | Compact and expanded are presentations of one persistent task model; expansion never constructs a fresh poll. | [iOS best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices): preserve context and adapt presentation. |
| Sticker selection sends immediately | Remove stickers from the core poll flow. Selecting a poll opens it; preparing a poll produces a reviewable message draft. Only the person's explicit Messages Send action sends that message. | This send boundary is a product correction, informed by clear action outcomes in [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Content). It is not a claim that the local HIG specifies composer APIs. |
| Private notes travel with shared content | Store notes separately and exclude them from every shared representation, link, preview, update, and telemetry payload. | [Privacy best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices): minimize data and explain its use. |
| Recipients may lack the extension | Always include readable poll text; offer a browser participation destination if implemented, with plain-message replies as a fallback. Never require installation to understand the invitation. | Product fallback; [Collaboration and sharing](https://developer.apple.com/design/human-interface-guidelines/collaboration-and-sharing#Best-practices) supports distinguishing copies from access and providing representations and management. HIG alone does not establish no-app voting capability. |

## Surface and action contract

Compact view contains, in reading order: poll title and time, “Open” or “Closed,” last-updated status, option names with counts, the person's current vote, and immediate vote commands. Example:

```text
Lunch today · 12:30
Open · Updated just now
Ramen — 2 votes · Your vote
[Vote for Tacos]   Tacos — 1 vote
[Vote for Salad]   Salad — 0 votes
[Remove My Vote]
[Details]  [Prepare Update]
```

Actual layout uses full-width vertical rows, not the illustrative inline alignment. Each unchosen option has an immediate “Vote for {option}” button. The chosen option shows “Your vote”; there is no separate uncommitted selection. Changing a vote replaces the prior vote after server acknowledgement. Supporting copy says “Your vote and display name are visible to poll participants.” Voting updates the shared poll; it does not silently send a new conversation message.

“Details” expands the same poll for editing and management. “Prepare Update” stages a reviewed snapshot in the Messages composer; it is secondary to voting. For a new poll, “Create Lunch Poll” expands to title, lunch time, and 2–6 option fields (product limits). “Review Poll” is enabled only when required fields are valid; inline errors name the missing or duplicate value. Review shows exactly the public title, time, options, access summary, and fallback text. “Add to Message” stages the draft, then Messages owns Send. Cancelling review preserves the editable draft; cancelling the composer does not publish or announce a poll.

Expanded details expose full option text, participants, counts, “Prepare Update,” and “Back to Poll.” The creator also gets “Manage Poll”: close/reopen voting, remove a participant, and revoke the invitation link. Options and time become immutable after first publication to avoid changing the meaning of existing votes; create a new poll for changed choices. “Private Note — Only on this device” is a separate local editor, initially empty. Back saves that local note without sharing it. No keyboard appears in compact view; editing requests expanded presentation first. Keep focused fields and completion controls reachable above the keyboard by scrolling.

Buttons have explicit accessible names matching their labels, normal press feedback, and at least 44 × 44 pt nonoverlapping activation regions on iOS. Use one primary action per task: create in the empty state, Review Poll in the editor, Add to Message in review. Vote commands are peer controls with equal geometry. Pending commands show an activity indication within the initiating button and suppress duplicates; failures retain context and show a persistent inline Retry. These choices follow [Buttons: style and iOS behavior](https://developer.apple.com/design/human-interface-guidelines/buttons#Style).

## Identity, access, and data contract

This is asynchronous collaboration on one poll ID. A message contains a snapshot and a reference to that poll; it is not a new independent poll each time it is shared. “Prepare Text Copy” in details instead stages a clearly labeled static text copy, with no access-granting link and no promise of live counts.

Proposed custom-service policy: anyone holding the invitation link can request to join and vote once approved by the creator. Review explicitly says “Link holders can request access. Approved participants can view names and votes and change their own vote. Only you can manage the poll.” Do not claim that a link is restricted to Messages conversation membership. Recipients can forward it. A join request contains a chosen display name; creator approval binds a stable participant credential, rather than using names as identity. The creator sees pending requests in Manage Poll. Removed credentials lose read/write access; revocation disables the old invitation link while approved members retain access. Closing the poll preserves readable results and prevents votes. No participant may change another person's vote or add members.

| Data | Purpose and destination | Boundary |
|---|---|---|
| Public title, time, option IDs/labels | Poll service and explicitly staged message snapshot | Allowlisted fields only |
| Participant credential, display name, own vote | Service authorization and shared participant list | No address-book or conversation-member scraping |
| Invitation token | Join destination; shared only in reviewed collaborative invitation | Never a management credential; revoke server-side |
| Private note | Local personal reminder | Separate storage; never serialized into public model, analytics, link query, or message metadata |
| Local draft and presentation state | Resume interrupted work | Partition by conversation context and poll/draft ID; do not assume an SDK exposes a particular identifier |

The basic task requests no contacts, location, photos, microphone, or tracking permissions. Protect participant and management credentials using established secure storage in the eventual platform implementation. “Only on this device” excludes cloud sync and backup export of the note; implementation must verify that storage behavior before shipping that copy. Existing leaked notes cannot be recalled by this redesign.

## State and transition model

```text
Task = {conversationContext, pollOrDraftID, revision,
        route, editorDraft, localNoteKey, scrollAnchor,
        focusedField, pendingOperationID, stagedSnapshotRevision}
Presentation = compact | expanded  // not the owner of Task

openMessage(reference): restore referenced poll, then refresh authorization/data
openExtension(context): restore that context's task, otherwise show empty state
expand/collapse/rotate: persist Task; change Presentation; keep poll and draft
background/terminate: persist local task; reconcile unfinished operations on resume
vote(option): require authorized && open; submit own-vote replacement with operationID
ack: replace confirmed model with authoritative revision; show “Vote saved”
failure: keep confirmed vote; retain attempted operation for explicit Retry
retry: reuse operationID; server deduplicates and returns authoritative result
prepareMessage: allowlist public fields into immutable snapshot; show review
addToMessage: stage snapshot; never call an implicit send operation
```

Create a provisional poll reference before staging an invitation if the implementation requires one. It must contain no private notes and must not notify participants. Publication/send reconciliation requires a verified host integration contract: if send status cannot be known, say “Message prepared,” never “Sent.” Cancelled drafts retain local work and provisional references expire without becoming discoverable. Reopening a staged draft retains the same poll identity.

Refresh never replaces unsaved editor text. If the service closes the poll during a vote, reject the vote, refresh results, and show “This poll has closed.” Resolve concurrent votes from different people independently; serialize one person's operations to avoid older retries overriding newer votes. Opening an old message goes to the current poll and labels the embedded counts “Snapshot,” rather than presenting them as live. Offline shows cached results with their timestamp, disables unconfirmed voting, and offers Retry; no optimistic “saved” state. A missing/revoked poll shows “Poll unavailable” and Back, without exposing cached protected details to a removed participant.

## Recipient contract

The invitation's plain text must stand alone:

```text
Lunch today, 12:30
1. Ramen  2. Tacos  3. Salad
Open poll — counts are a snapshot from 11:40.
Open poll / request access: <poll-specific link>
No app? Open the link in your browser, or reply with your choice.
Replies are not counted automatically.
```

With the extension available, the reference opens the exact poll. Without it, the proposed HTTPS destination shows that poll's join request and, after approval, the same voting rules. It has no mandatory installation detour. Link preview exposes no private note, participant names, or protected live results. A browser route, universal-link association, authentication, approval service, and backend are implementation dependencies, not supplied capabilities. Until those exist, use text-copy mode with “Reply with your choice”; do not ship a nonfunctional “Vote” link. The organizer must reconcile replies explicitly with the group; do not silently count them as authenticated votes.

## Worked before/after

Before (supplied): Sam opens the extension and gets a social feed. Selecting a sticker immediately sends it with a private note. Expanding then loses the selected poll.

After (illustrative data): Sam creates “Lunch today · 12:30” with Ramen, Tacos, and Salad in expanded view. Sam writes “Ask Jo privately about allergies” in the device-only note. Review contains only the public invitation and access policy. Add to Message stages it; Sam cancels, reopens the extension, and finds the same draft and note. Sam stages again and explicitly sends using Messages. The outgoing allowlist contains no note. Lee has no extension and reads the three options in the message, opens the browser destination, requests access, and votes for Tacos after approval. Sam opens the message's poll, votes for Ramen, expands Details, and collapses: the poll ID, confirmed vote, note, and position survive. If browser participation is unavailable, Lee replies “Tacos”; the message accurately warns this is not automatically counted.

## Acceptance checks and evidence status

**Passed — document inspection:** the specification removes the feed, separates staging from sending, excludes notes from public serialization, preserves task identity across presentations, distinguishes live collaboration from text copies, defines permissions and management, and gives a no-app fallback. Root skill, topic-index matches, owning families, topic procedures, and corresponding local source guides were read in that order. These are specification checks only.

**Failed — supplied behavior against the revised contract:** unrelated initial feed; immediate send on sticker selection; attached private notes; lost poll selection on expansion. These failures are reported in the brief, not independently reproduced. Recipient compatibility is unknown rather than a confirmed failure.

**Not executed — implementation acceptance:**

| Scenario | Required observable result |
|---|---|
| Launch, select poll, expand/collapse, rotate, background, terminate and resume | Same conversation-scoped poll, draft, note and confirmed vote; no unrelated task or lost edits |
| Select content, review, stage, cancel composer | No outgoing message or participant notification; draft remains recoverable |
| Insert a unique secret in every private-note field | Secret absent from message text, metadata, previews, links, public storage, logs and analytics; inspect actual serialized payloads |
| Double-tap vote; timeout then retry; concurrent participants | One vote per credential, no duplicates, no stale retry overwrite, no false success |
| Close during submission; remove member; revoke invitation | Server rejects unauthorized writes and reads; old invitation cannot admit new members; UI explains recovery |
| Open without app; expired or invalid link; send text copy | Readable invitation; exact poll destination when supported; clear unavailable state; copy never appears live |
| Keyboard visible in expanded editor | Fields and Review Poll reachable; compact voting needs no keyboard |
| Portrait/landscape, 200% text and every supported accessibility text size, Bold Text | Titles/options wrap, counts stack, controls grow; vertical scrolling retains all actions; no required label clipping |
| Accessibility traversal and alternate input | Order: heading/status, options/counts/vote commands, result, secondary actions; names state action and target, pending/disabled reasons perceivable; full task works with VoiceOver, Switch Control and Full Keyboard Access |
| Light/dark and Increase Contrast | Measure actual text/background contrast; color never alone communicates vote/status; 44 × 44 pt targets remain separate |

Use semantic headline/body/supporting text roles, with iOS body at the default 17 pt scale; support text growth rather than shrinking to fit. Provide persistent text feedback instead of sound-only or timed success. These requirements follow [Typography: Dynamic Type](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type) and [Accessibility: vision and mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility). At enlarged sizes compact content may scroll or offer Details; it must not remove voting. No custom motion is required.

## Evidence limits

Only local supplied files and installed guidance were used; no web browsing occurred. Official links above are source attribution from those local guides, not evidence of visiting current pages. The local package is an independent derived HIG snapshot dated 2026-10-25, not an SDK reference or proof of platform availability. Sticker artwork/export checks are inapplicable to the revised scope because no sticker pack is retained; none was supplied for inspection.

This deliverable is a proposed interaction and service contract. No app was built or run, and no Messages send, device, GUI, SDK compilation, backend authorization, browser fallback, physical comfort, contrast measurement, native rendering, or assistive-technology execution was performed. No API or automatic message-update capability is assumed. Release requires verifying the host's actual staging/send lifecycle, durable context mapping, secure storage and link behavior with the chosen implementation. Source citations and static reasoning do not establish those results.
