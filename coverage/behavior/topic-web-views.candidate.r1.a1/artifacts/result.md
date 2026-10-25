# Mac embedded Help audit

## Scope and evidence

Reviewed `interface.md`, a one-paragraph behavioral description. “Verified” below means explicitly reported there, not independently reproduced. No implementation, screenshots, URL inventory, network traces, credentials, or executable app were supplied. This is an audit and corrected framework-agnostic specification; it does not implement or certify an app.

Used the installed apple-hig root, searched its topic index, then read the Content family → Web views procedure → supporting guide. Also read the Foundations family and Accessibility, Typography, Privacy procedures and guides; Patterns family and Loading, Managing accounts procedures and guides; Menus and actions family and Buttons, Toolbars procedures and guides. Each file was read in its own shell command. Official links below identify the local guides’ sources; no website was opened.

## Ranked findings and decisions

Priority reflects likely consequence, not measured frequency. P0 requires resolution before shipping this flow; P1 blocks reliable Help use; P2 impairs useful reading. These priorities are audit judgments.

| Rank | Verified evidence in brief | Effect and source basis | Corrected decision |
|---|---|---|---|
| 1 — P0 | “unexpected auth redirect captures credentials in the help pane” | Unexpected credential collection breaks the Help task’s trust boundary. HIG advises minimizing collection and using established authentication protections: [Privacy, Protecting data](https://developer.apple.com/design/human-interface-guidelines/privacy#Protecting-data). The brief does not establish exfiltration, storage, or compromise. | Stop unexpected authentication before rendering credential entry or submitting data. Keep general Help usable without authentication. A genuinely account-dependent action must explain why sign-in is needed and require deliberate entry into an established authentication flow outside Help. This boundary is an application security decision, not a HIG rule banning all embedded authentication. |
| 2 — P1 | “Web content is the entire app navigation without back controls” | People cannot reliably return through linked content. HIG explicitly calls for enabled history and corresponding Back/Forward controls for multipage web content and discourages recreating general browsing: [Web views, Best practices](https://developer.apple.com/design/human-interface-guidelines/web-views#Best-practices). | Give the host persistent app navigation and an exit from bounded Help. Keep article history separate from returning to the app task. Provide accurate Back/Forward availability. Web rendering itself is not categorically prohibited on Mac. |
| 3 — P1 | “external payment links masquerade as local buttons” | Activation conceals the destination and task change. HIG asks that labels explain actions: [Buttons, Content](https://developer.apple.com/design/human-interface-guidelines/buttons#Content). | Identify the external website and browser handoff before activation; for example, “Continue to Payment in Browser…” with the configured merchant hostname beside it. No payment occurs merely by opening the page. Actual merchant, price, billing model, and platform payment obligations are unknown. External routing is a product decision; no Apple Pay requirement is inferred. |
| 4 — P1 | “load failures leave blank white” | Help offers neither explanation nor recovery. HIG favors useful structure and honest loading feedback: [Loading](https://developer.apple.com/design/human-interface-guidelines/loading#Best-practices). | Preserve the host chrome and last usable article when possible. Show “Couldn’t Load Help” with Retry and a route to available Help content or the app task. Error copy and Retry are application recovery decisions, not verbatim HIG requirements. |
| 5 — P2 | “zoom/text selection are disabled” | People cannot enlarge reading or copy instructions. HIG supports at least 200% text enlargement: [Accessibility, Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). Mac has no Dynamic Type: [Typography, macOS](https://developer.apple.com/design/human-interface-guidelines/typography#macOS). | Enable explicit text enlargement through at least 200%, reflowing essential content and controls. Restore selection and Copy for article text. Selection is a task-specific usability correction; the cited sources do not establish a universal text-selection mandate. Disabled zoom is verified; absence of every possible alternative resizing mechanism is not. |

## Corrected behavior contract

Host/page map:

```text
App task (retain selection, edits, focus)
  → Help index → Article A → Article B
       ↑           ← Back / Forward →
  ← Return to App (separate from history)

Article → explicitly labeled external payment → default browser
        ↳ Help remains on the same article
Unexpected authentication redirect → blocked-navigation explanation
                                   → Back to Help
```

The host owns navigation controls; remote content cannot replace or hide them. Use a top navigation region with Back/Forward together, an article/location title, and a distinct Return to App action. If Help is a separate window, Close Help closes only that window. Do not introduce a blocking modal merely for Help. On Mac, mirror toolbar actions in the menu bar and keep navigation essentials available when the toolbar hides or the window narrows. This follows [Toolbars, Navigation and macOS](https://developer.apple.com/design/human-interface-guidelines/toolbars#macOS). Do not add browser tabs, an arbitrary address bar, or duplicate overflow.

| Control | Outcome and availability | Semantics/state |
|---|---|---|
| Back / Forward | Move within committed Help history; disabled at respective boundaries | Named buttons; disabled state exposed; never dismiss Help |
| Return to App / Close Help | Restore originating task and focus / close separate Help window | Separate host action; available during loading and errors |
| External payment link | Open configured merchant in default browser after explicit activation | Link semantics, destination hostname and external consequence visible; no default Return-key activation |
| Retry | Retry failed safe article request | Button, disabled while its request is pending; no duplicate requests |
| Larger Text / Smaller Text / Actual Size | Adjust Help reading scale; preserve chosen scale across articles | Menu commands and reachable controls; Larger Text supports at least 200%; expose current scale |
| Copy | Copy selected article text | Standard selection and keyboard/menu access; no selection suppression |

Original payment labels, geometry, default roles, and accessible names are unknown. The table specifies replacements, not observed properties. Custom controls need press/focus/disabled feedback; prefer existing host controls where available. No SDK dependency is assumed. The local Buttons guide gives general 44 × 44 pt targeting advice while Accessibility gives Mac-specific 28 × 28 pt default and 20 × 20 pt minimum. This audit makes no geometric violation claim; preserve standard Mac sizing and measure actual custom targets rather than silently treating either table as universal.

### Navigation and loading pseudocode

```text
state = {originTask, committedHelpHistory, cursor, lastReadablePage,
         pendingRequest, readingScale, status}

on navigationAttempt(request):  // links, redirects, scripts, forms, new windows
    classify normalized destination using configured exact origins/routes
    if unexpectedAuthRoute or credentialSubmission:
        cancel before rendering/submission
        retain lastReadablePage and history
        show host explanation: "Sign-in isn't available in Help."
        offer Back to Help
    else if safeHelpReadRequest:
        begin load; keep host controls and any lastReadablePage
        show loading status if wait persists; do not invent a percentage
    else if explicitlyActivatedApprovedExternalLink:
        cancel embedded navigation
        open destination in default browser; retain Help history and focus context
        if handoff fails: show failure and allow explicit retry
    else:
        cancel; explain unavailable destination; retain Help context

on redirect(request):
    apply navigationAttempt policy again before following

on successfulHelpLoad(requestId, page):
    ignore stale completions
    commit history only for successful new navigation
    history traversal moves cursor without creating a duplicate entry
    discard forward branch only when a new page successfully commits
    restore saved scroll position for history traversal
    retain readingScale; expose article title; status = ready

on failedHelpLoad(requestId):
    ignore stale completions
    stop loading feedback; preserve committed history and lastReadablePage
    show persistent error with Retry and Return to App
    if no readable page exists, show an error body rather than a blank view

on exitHelp:
    cancel pending load; restore originTask and originating focus
```

The destination inventory and classifier must be supplied by the product: an origin alone is insufficient if it hosts both Help and authentication. Apply the policy before navigation, including redirects, subframes, submissions, and new-window requests. Do not inspect typed secrets to discover authentication after submission. If the embedding technology cannot enforce these boundaries, keep Help to controlled local documents until an enforceable integration exists.

Data-purpose contract: general Help needs article identifiers and reading preferences, not credentials or payment details. Authentication belongs to an explicit account task; payment details belong to the disclosed merchant flow. Help must not collect or log passwords, payment fields, or sensitive redirect tokens. Actual storage and telemetry require separate inspection. General Help remains available as a guest; account-only information may explain its dependency without forcing sign-in during ordinary reading, consistent with [Managing accounts, Best practices](https://developer.apple.com/design/human-interface-guidelines/managing-accounts#Best-practices).

## Worked before/after

The following article names and sequence are illustrative; the reported failures come from the brief.

**Before:** From an unsaved app task, a person opens Help, follows “Billing,” and cannot go back. A payment-looking local action leaves the app context unclear; a later unexpected sign-in appears in Help. A failed load becomes white. The person cannot enlarge or select the instructions.

**After:** Opening Help retains the app task. At Help index, Back and Forward are disabled. Opening Billing commits a second history entry: Back enabled, Forward disabled. Back returns to the index and enables Forward; Forward restores Billing and its scroll position. A visibly external payment link opens the configured merchant in the browser only on deliberate activation; Billing stays in Help. An unexpected authentication redirect is canceled before credential entry and leaves a recoverable explanation over the retained article. A failed article load preserves Billing and offers Retry. At 200% text scale, instructions wrap and controls remain reachable; a selected instruction can be copied. Return to App restores the unsaved task and focus. These are proposed outcomes, not executed results.

## Acceptance checks and status

**Passed — document inspection:** Confirmed macOS and all five reported problem categories in `interface.md`; read routed local procedures and source guides; produced explicit action, data, state, history, recovery, and exit contracts without assuming an Apple SDK.

**Failed — supplied behavior description:** Multipage navigation lacks Back; payment handoff is disguised; failure produces a blank page; zoom and selection are disabled; unexpected authentication captures credentials in Help. These are brief-level failures, not runtime reproductions. Forward availability, alternative text resizing, keyboard behavior, and secret storage are not independently established.

**Not executed — implementation acceptance:**

| Check | Passing observation required |
|---|---|
| History and exit | Index → A → B → Back → Forward works; boundary states accurate; new successful branch clears forward history; failed load does not corrupt history; exit restores app work and focus |
| Boundary enforcement | Exercise direct links, same-origin auth routes, cross-origin redirects, frames, forms, scripts, and new windows; unexpected auth is stopped before credential entry/submission; unknown destinations cannot bypass policy |
| Payment handoff | Label and hostname disclose external destination; mouse and keyboard activation open only the configured browser destination; cancellation/handoff failure retains Help; no unintended purchase or automatic redirect handoff |
| Slow/offline/retry | Initial offline load shows recoverable error; delayed load shows truthful status; failure after a readable page retains it; retry succeeds without duplicate entries; stale completions cannot replace a newer page |
| Partial and refresh states | Available article text remains usable while independent assets fail/load; refresh does not erase useful content; missing cache is handled without fabricated offline content |
| Reading | At 100% and 200% scale and supported narrow widths, essential text/actions remain usable; selection and Copy work; no fixed-height clipping; scale persists through history |
| Mac input and access | Keyboard reaches and activates all needed actions; focus is visible and restored sensibly; VoiceOver names, roles, disabled states, content order, and status announcements identify the task without focus theft |
| Host resilience | Narrow, hidden, and customized toolbar states retain menu access and exit; remote content cannot cover navigation; enlarged/localized labels remain readable |
| Privacy | Inspect navigation handlers, network traffic, storage and logs to confirm Help never captures secrets; verify deliberate account flow and guest Help remain separate |

## Evidence limits

Only source/document inspection occurred on the headless Linux workspace. No Mac device, browser GUI, native web engine, SDK build, network behavior, accessibility tool, VoiceOver, keyboard interaction, contrast calculation, geometry measurement, or timing test was executed. Actual URLs, account requirements, payment mechanics, cache availability, layout, and authentication framework remain unknown. Nothing here certifies security, legal compliance, accessibility conformance, or App Review eligibility. Local guidance is a dated 2026-10-25 snapshot; source links are attribution, not claims of current online verification. The correction is ready for implementation review, with runtime acceptance still pending.
