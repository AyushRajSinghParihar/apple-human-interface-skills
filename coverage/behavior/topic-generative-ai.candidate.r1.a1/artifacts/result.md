# AI-assisted reply: revised interaction specification

This is a proposed macOS interaction contract, independent of framework or Apple SDK. AI is an optional drafting aid for a support agent; manual composition and sending remain available when it is unavailable. The only supplied product evidence is `interface.md`: Generate sends all account notes without disclosure, inserts fabricated commitments into outgoing mail, lacks cancel/edit/undo, and can fail or produce unsafe answers. No screens, implementation, service contract, or model results were supplied.

## Decisions and source rationale

| Observed problem | Revised decision | Local HIG basis, with official source link |
|---|---|---|
| All account notes leave without disclosure | Review exact context before every request; exclude account notes by default; explicitly authorize the current transfer | [Generative AI — Privacy](https://developer.apple.com/design/human-interface-guidelines/generative-ai#Privacy), [Privacy — Best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices) recommend minimization, clear use, and appropriate permission |
| Fabricated commitments enter outgoing mail | Separate editable, labeled AI preview; constrain factual claims to approved current evidence; explicit insertion followed by separate send review | [Generative AI — Inputs and Outputs](https://developer.apple.com/design/human-interface-guidelines/generative-ai#Inputs) advises narrowing factual generation and generally confirming significant actions |
| No cancel, edit, or undo | Cancel generation, edit preview, adjust/retry, discard, and undo insertion | [Generative AI — Outputs](https://developer.apple.com/design/human-interface-guidelines/generative-ai#Outputs), [Undo and redo — macOS](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#macOS) |
| Failure or unsafe answer | Persistent actionable status; preserve draft; block known unsafe suggestions; manual fallback | [Generative AI — Best practices and Outputs](https://developer.apple.com/design/human-interface-guidelines/generative-ai#Best-practices) |
| Mac editing task | Resizable workspace, adjacent review area, shared menu/control commands, keyboard completion, preserved context across app switches | [Designing for macOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos#Best-practices), [Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards#Best-practices) |
| Required actions must remain perceivable and operable | Text status, labeled controls, keyboard route, enlargement and assistive-input checks | [Accessibility — Vision, Mobility, Speech, Cognitive](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision) |

Exact labels, per-request authorization, validation gates, preview placement, and send review below are product decisions applying this guidance; they are not asserted to be verbatim Apple requirements. No Apple Intelligence or Foundation Models availability is assumed. Server generation is a provisional design choice reflecting the brief's transfer behavior; assess local processing feasibility before implementation.

## Workspace and entry

Keep ticket, customer message, and editable reply visible. Add a labeled **Draft with AI…** action beside the reply editor and the same command in the app's Reply menu. It opens a nonmodal review area in the current ticket window. At narrow widths stack the area below the reply, with scrolling and persistent access to actions. Do not cover the reply with a blocking onboarding flow.

Heading: **AI reply suggestion**. Introduction: “Draft a reply from the context you choose. AI can make mistakes. Check facts and commitments before sending.” Example instructions: “Acknowledge the delay and explain the next step” and “Make this reply shorter without adding promises.” Manual reply editing never requires AI consent.

## Context and transfer contract

Before any request, show **Review context** with the actual text to be submitted, not merely category names. Defaults: current customer message selected; existing draft included only when the agent selects **Use my draft**; account notes and attachments excluded. Each account note has an unchecked inclusion control, title/date, and readable content. Allow selection of relevant excerpts and removal/redaction in this request without changing the source record. Exclude unrelated tickets and hidden account history.

| Data | Purpose and permitted scope | Persistence/use contract |
|---|---|---|
| Selected customer message text | Understand the current question | Included in explicitly authorized request only |
| Optional draft and instruction | Transform the agent's wording or guide tone | Same request authorization; no background uploads while typing |
| Explicitly selected note excerpts | Supply relevant verified facts | Default off; identify each excerpt in the preview |
| Current approved support policy excerpts | Ground policy statements | Show source, version/date, and exact included text |
| Secrets, credentials, payment details, unrelated personal notes | No drafting need | Exclude; visibly identify redactions before submission |

Disclosure immediately above **Send context and generate**: “Send the context shown here to [actual provider] to draft this reply.” Also display actual processing location, retention period, training use, and deletion/access policy in plain language, with details available before the action. These are required configuration facts, not values to invent. If they cannot be established, disable server generation with “AI drafting is unavailable because its data handling has not been confirmed. You can write your reply here.” Do not ship bracketed placeholder copy.

The button authorizes only this immutable context snapshot and stated use. **Cancel** closes review without transfer. No training or improvement reuse is authorized by generation; any future optional reuse requires a separate explicit choice, default off. Revoking future AI use does not pretend to retract an already transferred request. Any real system permission needed by the eventual implementation remains distinct from this ordinary app-level transfer choice; do not imitate an OS authorization alert.

## State and action contract

| State | Display and available actions | Transition and invariant |
|---|---|---|
| Idle | Editable reply; Draft with AI… | Open context review; preserve draft and selection |
| Context review | Exact payload, disclosure, instruction; Cancel; Send context and generate | Submit only after valid provider disclosure and authorization |
| Generating | “Drafting a reply from your selected context…”; Cancel | Reply stays editable; no outgoing-mail mutation; do not show invented progress percentages |
| Cancelled | “Generation cancelled. Your reply is unchanged.”; Try again; Close | Invalidate request immediately, attempt service cancellation, ignore late output; cannot guarantee recall of submitted data |
| Preview | “AI-generated suggestion — review before use”; editable text; source evidence; Adjust; Generate again; Discard; Insert into reply / Replace reply… | Output never inserts automatically; no send action within AI area |
| Failed | “Couldn’t generate a reply. Your reply is unchanged.”; Retry; Review context; Close | No automatic retry or additional transfer; retry reauthorizes shown context |
| Blocked | “This suggestion couldn’t be used because it may contain unsafe or unsupported content.”; Adjust request; Review context; Write manually | Do not expose blocked text as ready-to-insert content; insertion disabled |
| Unavailable | Explain known cause and recovery, e.g. “AI drafting is offline. Reconnect to try again.” | Manual editing and ordinary send remain usable |
| Inserted | Focus reply; reveal and select inserted text; persistent AI-origin review marker | One reversible draft edit; ordinary editing continues |

Adjust edits instructions/context without changing the current reply. Generate again keeps the existing preview until a valid replacement is ready; cancellation/failure preserves that preview and any edits. Context changes always require authorization of a new snapshot. Closing the AI area discards its transient preview but preserves the reply. Switching apps or resizing preserves both; switching tickets isolates request, preview, selection, and history by ticket. Never display one ticket's late result in another.

## Factual and safety boundaries

Use current approved records as evidence, with source identifiers beside proposed factual claims. A generated source identifier must resolve to a supplied record and supporting passage; a model's citation alone is not verification. The model receives an instruction to treat customer messages and notes as data, never as instructions to send mail, reveal records, or override policy. The service has no send, refund, or account-change capability.

Never invent approval, refund amount, deadline, legal promise, or completed action. If evidence is absent, omit the promise and show “No approved resolution is included. Add verified details or write a reply without a commitment.” Mark ambiguous claims for review and disable insertion until removed or supported by approved evidence. Block detected unsafe content, sensitive-data leakage, malicious instruction following, and unsupported commitments. Validation is defense in depth, not a guarantee: an agent still reviews wording and evidence. A safe fallback acknowledges the issue and asks for a next step without promising an outcome.

Feedback is optional: **Report suggestion…** opens a review of exactly what would be submitted; preview text and customer records are excluded by default. Reporting never happens automatically on dismissal or failure.

## Insert, undo, and send

For an empty reply, **Insert into reply** inserts the reviewed preview. For a nonempty reply, **Replace reply…** first shows the existing reply and proposed replacement with **Replace reply** and **Keep editing**. No selection captured before a long request may silently determine the replacement target. Check the current draft revision again at insertion; if it changed during review, refresh the comparison and require another explicit choice.

Insertion/replacement records one transaction: ticket ID, prior reply text/formatting, new text, prior selection, and AI-origin metadata. Undo restores that ticket's exact prior content and selection and reveals the change. Redo reapplies the accepted suggestion; it never regenerates or retransmits. Preview typing uses its own editing history while focused there. In the reply editor, later manual edits undo before the insertion transaction. New edits after undo clear the redo branch. Preserve meaningful history across draft saves in the open session; closing/reopening restores saved content but does not promise a persisted undo stack. Changing windows targets only the active editor's history.

At the top of Edit use **Undo Insert AI Reply** (or **Undo Replace Reply**) with Command-Z and corresponding **Redo…** with Shift-Command-Z. Undoing text does not reverse data transfer or completed email delivery.

**Send…** opens a final review of the current recipient, subject, and exact current body, with **Send reply** and **Back to editing**. Include “This reply includes AI-assisted text. Check facts and commitments.” when AI-origin text remains. Any edit after review invalidates that reviewed revision. Sending requires an explicit activation against the reviewed revision, independently of generation or insertion. Prevent duplicate sends; an ambiguous delivery failure requires checking delivery status before retry. AI cannot invoke this command. Send review is a deliberate product safeguard for customer commitments, applying HIG's qualified recommendation to confirm significant actions.

## Keyboard and accessibility contract

All visible commands share enabled states and targets with menu commands. No custom generation shortcut is assigned until conflict/localization review. Preserve standard copy, paste, selection, Undo, and Redo. Escape or Command-period cancels active generation; Escape closes the context/review area when idle. In multiline editors Return inserts a newline; it never sends or accepts an AI suggestion. A labeled Cancel/Close action always provides the same exit.

Keyboard path: Reply menu → Draft with AI… → context controls → instruction → Send context and generate → preview → Edit/Insert or Discard → reply → Send… → Back to editing or Send reply. Support Tab/Shift-Tab navigation under macOS keyboard navigation settings and Full Keyboard Access without trapping focus. Opening context review focuses its heading/first context control; generation completion announces status without stealing focus; insertion focuses the inserted reply text; closing restores the invoking control.

Specify accessible names, roles, checked/disabled states, and validation descriptions for controls. Associate preview and evidence labels with their text. Status is persistent text and exposed as a status announcement, once per transition, without reading token-by-token output. Risk meaning never relies on color alone. Support at least 200% text enlargement with reflow and reachable actions; use the local guide's macOS 13 pt default text and 28 × 28 pt default control activation area as starting points. Measure actual layout, spacing, and contrast in implementation. These are design targets, not measured results.

## Worked before/after

Illustrative fixture, not an observed model run: customer asks, “My parcel is late. Can you refund me?” Reply currently reads “Thanks for contacting us.” Account notes include “Refund request pending; no approval,” an unrelated private account note, and an old delivery estimate. Current approved policy says refunds need review.

**Before (brief behavior, illustrated):** Generate sends every note and immediately adds “Your refund is approved and will arrive tomorrow” to outgoing mail. The agent cannot cancel, edit, or undo the insertion.

**After:** The agent opens Draft with AI…, reviews the customer message and policy, selects only “Refund request pending; no approval,” and excludes the private note and stale estimate. The disclosure identifies the real service and its actual data handling. After explicit transfer authorization the preview reads:

> Thanks for contacting us. I’m sorry your parcel is late. Your refund request is awaiting review; it has not yet been approved.

The pending-review statement links to the selected note; no payment timing is asserted. The agent edits the opening to “Thanks for letting us know,” compares against the current reply, and explicitly replaces it. Command-Z restores “Thanks for contacting us.” Redo restores the edited suggestion without another service request. Send… shows the exact recipient and body; Back to editing preserves the draft. Only Send reply sends it. If the model instead promises a refund tomorrow, the unsupported-commitment gate blocks insertion and offers adjustment/manual writing; its detection remains to be tested.

## Acceptance checks and evidence status

**Passed — static specification checks:** Each problem stated in `interface.md` has a concrete replacement above; transfer precedes generation only after explicit authorization; preview, insertion, and send are separate transitions; cancellation, unsafe output, failure, and manual fallback have defined exits; undo has a target, inverse, and external-effect boundary. These are document checks, not runtime passes.

**Failed — supplied baseline description:** Undisclosed full-note transfer, direct fabricated commitment insertion, and missing cancel/edit/undo conflict with this contract. This conclusion rests on the supplied description, not executed software.

**Not executed — implementation acceptance scenarios:**

1. Open context review and cancel: capture zero generation requests. Submit with notes unchecked: capture only the displayed authorized payload, with no excluded note, attachment, identifier, or hidden history. Unknown retention/provider facts prevent submission. Verify actual provider retention/training behavior separately.
2. Edit reply during generation, then cancel; deliver a late success and failure. Neither mutates reply or resurrects a preview. Switch tickets/windows during requests: all results remain scoped to origin. Change source context after authorization: no silent payload expansion.
3. Retry after failure requires explicit action and correct disclosure; no automatic request. Unavailable generation leaves manual reply and send operational. Failed regeneration retains edited prior preview.
4. Insert, type, undo typing, undo insertion, redo, undo, then type: correct text/selection/metadata restore; redo clears after new work. Test replacement revision race, offscreen restoration, save, and reopen policy. No undo claims to recall mail or transferred data.
5. Test refund/deadline fabrication, stale policy, invalid citations, prompt injection, data leakage, ambiguous requests, unsafe and out-of-scope output. Block detected unsafe results and unsupported commitments; permit grounded safe drafts. Evaluate representative languages, customer groups, underrepresented cases, stereotypes, misinformation, and copying risks using licensed/provenance-known fixtures. Record false positives and missed hazards; define release thresholds with support-policy owners before release. Reevaluate model/prompt/policy changes.
6. Insert without sending; cancel final review; edit after final review; double-activate send; simulate ambiguous delivery. Verify only an explicit current-revision Send reply causes a single delivery and uncertain delivery does not prompt a blind resend.
7. On a Mac, complete the entire path by keyboard and Full Keyboard Access, then with relevant assistive input. Verify status announcements, focus restoration, correct menu targets, no shortcut collisions, international layouts, app switching, resizing, and 200% text. Measure light/dark and Increase Contrast rendering and control activation areas.

## Evidence limits and audit route

Read from the installed package: root `apple-hig/SKILL.md`; searched `references/topic-index.md`; read owning family SKILL.md files for getting-started, technologies, foundations, patterns, and inputs; then read each selected topic procedure before its source guide: Designing for macOS, Generative AI, Privacy, Undo and redo, Keyboards, Accessibility. Each file was read in its own shell command. Paths were resolved under `.agents/skills/apple-hig/`, not another installation.

Official links above identify the guidance underlying the local snapshot; they were not fetched. Local guides report a 2026-10-25 snapshot/retrieval date and describe themselves as derived application guidance. Their existence does not establish independent source review or current SDK support. No web access, GUI/device session, Apple SDK compilation, accessibility execution, service inspection, model evaluation, privacy verification, or delivery test was performed. No implementation is supplied or certified. Provider identity, processing location, retention, training policy, approved factual sources, detection quality, and release evaluation thresholds remain implementation dependencies, with explicit unavailable behavior where necessary.
