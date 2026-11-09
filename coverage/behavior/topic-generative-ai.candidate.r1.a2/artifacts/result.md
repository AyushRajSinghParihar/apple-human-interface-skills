# AI-assisted replies: revised interaction specification

## Scope and decisions

This specifies a complementary drafting tool for a macOS customer-support editor. It is framework agnostic; no Apple SDK, Apple Intelligence integration, or local model availability is assumed. `interface.md` supplies behavior only, with no implementation or screenshots.

The supplied flow sends all account notes without disclosure, inserts fabricated commitments directly into outgoing mail, and offers no cancel, edit, or undo. The revision keeps manual composition available throughout and separates **approve context → generate suggestion → edit/review → apply to draft → review actual message → send**. Generation never sends mail or performs refunds, account changes, or other external actions.

These are product decisions applying HIG advice, rather than claims that Apple mandates this exact workflow:

| Decision | Concrete contract | Source basis |
|---|---|---|
| Make AI optional and recognizable | Label the workspace “AI Reply”; label output “AI-generated suggestion — check facts and commitments.” Manual typing and sending work when AI is unavailable or declined. | [Generative AI: best practices and transparency](https://developer.apple.com/design/human-interface-guidelines/generative-ai#Transparency) |
| Minimize and approve transfer | No generation request or AI-service prefetch occurs before approval of the exact context. Account notes are excluded by default. | [Generative AI: privacy](https://developer.apple.com/design/human-interface-guidelines/generative-ai#Privacy), [Privacy: best practices](https://developer.apple.com/design/human-interface-guidelines/privacy#Best-practices) |
| Keep factual commitments under human control | Use verified source material; unsupported commitments block application until removed or verified. Preview and explicit send review remain necessary because detection is imperfect. | [Generative AI: inputs and outputs](https://developer.apple.com/design/human-interface-guidelines/generative-ai#Inputs) |
| Preserve desktop editing | Use an inline AI workspace beside/below the reply in the existing resizable window, with persistent ticket context and equivalent menu commands. Switching apps preserves edits and selection. | [Designing for macOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos#Best-practices) |
| Make changes recoverable | Apply is one reversible draft edit. Standard Undo/Redo restores the correct draft and selection; sending is separately consequential. | [Undo and redo: macOS](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#macOS) |

## Surfaces, copy, and data scope

The reply area retains recipients, subject, multiline editable body, and manual Send. “AI Reply…” opens the inline workspace for further input. It does not transfer data. The workspace begins with: “Draft a reply using the context you choose. AI can invent facts or commitments. Review before sending.” Examples: “Summarize the next steps” and “Acknowledge the issue without promising a resolution date.”

Show full, selectable context text with its title, source ID, and last-updated time. Never silently add related records, attachments, prior tickets, hidden notes, or retrieval results. “Include Context” adds an explicitly chosen excerpt to the request; “Remove Context” removes it. These are immediate commands, not persistent permission toggles. Display included and excluded state in words. Allow redaction by editing the request copy without modifying the original record.

| Data | Default and purpose | Handling contract |
|---|---|---|
| Current customer message | Proposed context for understanding this request | Agent can remove/redact it before transfer. Include only the displayed message, not the entire thread. |
| Current reply text | Excluded; optional for rewriting | Include only an explicitly chosen excerpt. No background transmission while typing. |
| Account notes | Excluded | Individually include relevant excerpts; never send all notes automatically. |
| Approved policy text | Optional, chosen current excerpt | Show version/source. Missing or outdated policy cannot justify a promise. |
| Agent instructions | Locally composed multiline text | Show in the final request preview; no inferred sensitive traits. |
| Routing metadata | Minimum needed for service operation | Enumerate actual fields in disclosure. No account identity or unrelated identifiers by default. |
| Outputs and feedback | Local working suggestion | No feedback transfer by default. “Report Problem…” opens a preview with a separate submission action. |

Before each request, display the complete frozen payload and this disclosure template with **verified values substituted**: “Send the displayed context to [operator/service] to draft this reply. Processing: [locations]. Retention: [duration and purpose]. Training use: [actual practice].” Provide accessible details for subprocessors and deletion practices where applicable. Templates are specification placeholders, never shippable copy. If these facts are unknown, show “AI replies are unavailable because data-handling details are not configured. You can write a reply manually.” Disable transfer and offer “Back to Reply.” Do not promise no training, deletion, confidentiality, or local processing without evidence.

“Send Context and Generate” grants permission for this snapshot and purpose only; “Back to Reply” transfers nothing. A scope, service, policy, or payload change invalidates approval. Retry requires a fresh preview and explicit approval. Declining AI does not restrict manual work. This is application consent, not an imitation of a macOS system permission alert; no system permission API is assumed. Update distribution privacy disclosures when applicable. See [Privacy: requesting permission](https://developer.apple.com/design/human-interface-guidelines/privacy#Requesting-permission).

## Interaction and state contract

| State | Visible content/actions | Transitions and invariants |
|---|---|---|
| Manual / unavailable | Existing draft; AI Reply… or unavailable explanation | Manual editor remains usable. Opening AI saves ticket ID, draft revision, and selection. |
| Configure | Instructions, selected context, Preview Request, Back to Reply | Preview Request freezes exact payload plus service policy version. No transfer yet. |
| Approve | Complete payload and disclosure; Send Context and Generate; Back to Reply | Approval starts one request. Editing scope returns to Configure. |
| Generating | Small indeterminate spinner, persistent Cancel Generation | No invented percentage. Disable duplicate generation. Keep reply editable. Status details distinguish actual stages only when instrumented. |
| Slow / failed | “The service is taking longer than expected” or “Couldn’t generate a reply. Your draft is unchanged.” | Product timeout: 30 seconds, configurable after measurement. Stop waiting at timeout; offer Retry…, Change Context, Back to Reply. No automatic retry or duplicate transfer. |
| Cancelled | “Generation cancelled. Your draft is unchanged.” | Invalidate request token immediately; attempt service cancellation. Explain that already transmitted data cannot be recalled by cancellation. Ignore late completions. |
| Review | AI label, editable suggestion, source evidence, verification issues, Apply to Draft, Retry…, Discard Suggestion | No streaming text enters the outgoing draft. Empty/malformed output is failure. Retrying keeps current suggestion until explicit replacement; edited text is recoverable through local history. |
| Blocked | “This suggestion was blocked. Try a narrower request or write the reply manually.” | Unsafe output is not rendered as usable reply text; Apply unavailable. Keep original draft and chosen context. Retry… returns to approval. |
| Applied | Changed draft, provenance label “Contains AI-assisted text; review before sending” | Apply replaces the whole reply body with the reviewed suggestion. Label is explicit about this replacement. One undo transaction records old/new bodies and selection. No automatic send. |
| Send review | Read-only exact recipients, subject, body; Back to Editing; Send Message | Invoked by Send for all replies. Explicit Send Message sends only that reviewed revision. Any message/recipient change invalidates review. Never auto-send after generation, Return, or completion. |

Cancellation and completion remove the spinner. Status persists until the next deliberate action, without timed dismissal. The editor may continue operating during generation. If its body revision changes, Apply becomes unavailable with “Your draft changed. Compare it with this suggestion before replacing it.” An explicit “Review Replacement…” shows old/new text and binds replacement to the current revision. A further edit invalidates that binding.

Each ticket/window owns its request and undo history. Ticket switch invalidates/cancels an in-flight request; results cannot land in another ticket. App deactivation preserves draft, suggestion, and approved context, and completion does not steal focus. Closing a workspace cancels pending work and preserves its local working text for that editing session; no cloud retention is implied.

Framework-agnostic guards:

```text
start(snapshot, approval):
  require configuredDisclosure && approval.hash == hash(snapshot, servicePolicy)
  require noActiveRequest(ticket)
  token = uniqueToken(ticket, session)
  request(snapshot, token)  // generation service has no mail/account-action capability

complete(token, output):
  if token != activeToken || token.ticket != currentTicket: ignore
  stopProgress()
  if error/empty/malformed: showFailure(); return
  if safetyCheckBlocks(output): showBlocked(); return
  showEditableSuggestion(output, evidence, issues) // draft is unchanged

apply(suggestion, targetRevision):
  require currentRevision == targetRevision && noUnresolvedCommitments
  atomicUndoableReplace(ticket, oldBody, suggestion, oldSelection)

send(reviewedMessage):
  require explicitSendMessageActivation
  require hash(currentMessage) == reviewedMessage.hash
  sendExactly(reviewedMessage) // never callable by generation completion
```

## Facts, unsafe answers, and recovery

Treat customer text and notes as data, never as executable instructions. Request output constrained to selected evidence. Do not infer refunds, deadlines, eligibility, completed actions, or promises from tone or probability. A claim/evidence list identifies each policy or commitment and its actual supporting excerpt. Never invent citations or display a confidence percentage as proof.

Mark unsupported claims “Needs verification”; Apply is disabled until the agent removes the claim or supplies a current authoritative excerpt and explicitly marks that claim verified. Editing reruns checks and invalidates verification for changed claims. A missing checker or evidence service fails closed for application, with manual composition available. This proposed check cannot reliably identify every false or unsafe statement; the agent must review the full text. Customer-facing copy must not say “safe” or “verified” merely because automated checks passed.

Offer voluntary “Report Problem…” beside the suggestion. Its report preview excludes customer context and raw reply text by default; submission separately approves any included excerpts. Evaluate misinformation, stereotyping, privacy leakage, malicious prompt injection, abusive requests, copying, ambiguity, and policy conflicts before release and after model changes. These are release checks, not completed evaluations. See [Generative AI: outputs and continuous improvement](https://developer.apple.com/design/human-interface-guidelines/generative-ai#Outputs).

## Commands, editing, and access

All commands are labeled text buttons with visible pressed, focus, and unavailable states; unavailable actions explain their reason nearby. Use one prominent action per current stage. Cancel Generation is always available while waiting. Apply to Draft and Send Message have no global default Return binding. Return inside text inserts a newline; a focused button may activate through the platform’s normal keyboard behavior. Escape or Command-Period cancels the current generation, not the ticket or draft. Preserve Command-C/X/V/A and conventional text selection. At the top of Edit, expose “Undo Apply AI Reply” / “Redo Apply AI Reply” with Command-Z / Shift-Command-Z; later text edits undo before the application transaction. New edits after Undo clear the redo branch. Undo reveals restored text and restores selection. Autosave does not erase session history; reopening starts a new history baseline. Undo cannot retract transmitted context or delivered mail.

Expose equivalent Reply menu commands and standard Edit commands through the host’s command system, with the same ticket target and availability as buttons. No new generation shortcut is assigned until the host command inventory and international layouts are checked. A framework without native menu integration must still supply a keyboard-reachable command surface; native Mac integration remains an implementation requirement to resolve, not an assumed capability. See [Buttons: macOS](https://developer.apple.com/design/human-interface-guidelines/buttons#macOS), [Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards#Best-practices).

Keyboard order follows the displayed task: entry → instructions → context text/actions → request preview/approval → status/cancel → suggestion/evidence/issues → apply/retry/discard → draft → send review. Backward navigation reverses it. Moving focus never includes context or activates an action. User-invoked opening moves focus to the workspace heading; returning restores the invoking control. Asynchronous completion announces a concise status without moving focus or reading the entire suggestion. Keep Cancel Generation mounted through resolution as a status/return location so focused controls do not vanish unexpectedly. Semantics specify button names, editor labels, included/excluded context state, unavailable reasons, issue associations, and reading order. See [Focus and selection](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Best-practices).

Suggestion, request preview, and evidence support selection/copy, multiline reading, wrapping, and scrolling; only the suggestion and instructions are editable. Long identifiers remain fully accessible. At narrow widths stack workspace beneath reply without hiding completion/cancel actions. Preserve content at 200% text enlargement; do not rely on color for issues or sound for completion. Use adaptive light/dark colors and visible focus. No decorative motion; Reduce Motion retains textual progress without unnecessary animation. See [Text views](https://developer.apple.com/design/human-interface-guidelines/text-views#Best-practices), [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility), [Writing](https://developer.apple.com/design/human-interface-guidelines/writing#Best-practices).

Source qualification: the installed Buttons article gives a general 44 × 44 pt hit-region recommendation; Accessibility lists macOS defaults of 28 × 28 pt and minima of 20 × 20 pt. This specification conservatively uses at least 44 × 44 pt activation regions for new AI actions, with no overlap, while retaining normal Mac visual control sizing. That is a product choice, not a claim that all Mac controls require 44 pt. No geometry or contrast has been measured. Unknown-duration generation uses indeterminate progress, following [Progress indicators: macOS](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#macOS).

## Worked before/after

Illustrative fixture, not an observed customer record: customer asks “Can you refund order 42 today?” Existing draft: “Thanks for contacting us.” Notes contain “Refund not yet approved” plus an unrelated private medical detail. No policy guarantees a date.

**Before (illustrates the supplied defect):** Generate silently sends both notes and inserts “Your refund is approved and will arrive today” into outgoing mail. No review or recovery exists.

**After:** Agent opens AI Reply…, selects the customer question and only “Refund not yet approved,” and previews the exact payload. The medical detail is absent. Verified service disclosures appear; agent chooses Send Context and Generate. A candidate saying “Your refund will arrive today” is marked unsupported and cannot be applied. The agent edits it to “Thanks for contacting us about order 42. Your refund has not yet been approved.” After reviewing evidence and the full text, Apply to Draft replaces the original body. Command-Z restores exactly “Thanks for contacting us.” Redo restores the reviewed candidate. Send opens a review of recipients and actual body; only Send Message transmits it. If generation fails or the agent cancels, the original draft remains and can be sent manually through the same review step.

## Acceptance checks and evidence limits

**Passed — document inspection only:** Read `interface.md`; identified each supplied defect and specified a correction. Explicitly read installed root skill, searched the topic index, then read owning family and topic procedures before supporting guides for macOS, generative AI, privacy, accessibility, writing, buttons, keyboards, focus/selection, progress, text views, and undo/redo. The document contains decisions, state guards, a worked example, and checkable outcomes. No web access was used. Official links above identify source sections; they were not fetched.

**Failed — supplied baseline, as described in the brief:** disclosure/minimization, separation of suggestion from outgoing text, control over fabricated commitments, cancellation, editability, and undo. Service failure and unsafe-output recovery are unresolved in the supplied description. These are brief-based findings, not runtime observations.

**Not executed — implementation acceptance scenarios:**

1. Capture all generation traffic: opening/configuring/declining AI produces no AI-service payload; approval sends exactly the displayed snapshot, excluding unchosen notes and redacted text. Unknown service practices prevent transfer. Service/payload changes require new approval.
2. Double-activate Generate: exactly one active request. Cancel, time out, switch tickets, and inject late success: no draft mutation or cross-ticket result. Confirm backend cancellation behavior separately from client invalidation.
3. Simulate offline, unavailable, empty, malformed, blocked, and slow service results: progress ends, remedy appears, original draft survives, and manual reply remains usable. Retry never starts without fresh approval.
4. Inject unsupported refund/deadline claims, fabricated evidence, prompt injection, and private details: unsupported commitments block Apply; hard-blocked text cannot be applied. Run a representative, provenance-documented model evaluation and record misses, false blocks, and residual risks. A single fixture cannot establish safety.
5. Edit the draft while waiting, then apply: stale replacement is rejected. Compare/rebind, edit again, and verify the second revision also invalidates consent to replacement.
6. Apply → type → Undo → Undo → Redo; verify exact text, ticket identity, selection, transaction grouping, and visible restoration. New edits invalidate Redo; autosave preserves session history. Never present Undo as mail recall.
7. Generate/apply/press Return in every editor: no send. Review a message, change recipients/body, then try Send Message: review invalidates. Verify exactly one delivery of the exact reviewed revision; generation service cannot invoke delivery.
8. Complete entry, context approval, cancel, retry, edit, apply, undo, and send using keyboard and supported assistive input. Check semantic names, issue associations, announcements, no unsolicited focus jumps, Full Keyboard Access, VoiceOver, and Switch Control on a Mac.
9. Resize, enlarge text to 200%, switch light/dark and Increase Contrast/Reduce Motion, and switch away/back: all content/actions remain usable and edits survive. Measure actual contrast, targets, separation, and focus visibility; test long localized labels and unbroken identifiers.

Only a specification was produced. No device, SDK compilation, GUI, accessibility execution, network privacy validation, model-quality evaluation, service retention audit, or mail delivery test occurred. Local guides are dated application-guidance snapshots, not SDK documentation or independent certification. Service identity, model capability, retention/training practices, authoritative policy sources, host menu integration, and persistence/security implementation remain release dependencies. The flow guards describe required behavior; they do not prove it exists.
