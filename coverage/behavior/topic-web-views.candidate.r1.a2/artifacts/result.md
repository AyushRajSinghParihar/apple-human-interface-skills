# Mac Help web-view audit

## Scope and evidence

The sole interface evidence is the one-paragraph behavioral description in [interface.md](interface.md). “Verified” below means explicitly stated in that brief, not reproduced in a running app. No implementation, screenshot, destination URLs, network traces, or authentication configuration was supplied. Priorities are audit judgments based on consequence, not measured incident frequency.

This is a framework-agnostic correction specification. It preserves embedded web content for Help and assigns navigation and trust boundaries to the host. It does not require an Apple SDK.

## Ranked findings and decisions

| Rank | Verified observation | Effect and decision | Guidance and qualification |
|---|---|---|---|
| 1 — Critical | An unexpected authentication redirect captures credentials in Help. | The reading surface unexpectedly becomes a credential-entry surface. Stop unexpected authentication before rendering or accepting submission; retain the last safe article. Offer an explicit route to the app’s established account flow only when genuinely needed. Help must not collect passwords. | [Privacy: Protecting data](https://developer.apple.com/design/human-interface-guidelines/privacy#Protecting-data) favors established authentication and protected secrets; [Managing accounts](https://developer.apple.com/design/human-interface-guidelines/managing-accounts#Best-practices) defers sign-in until needed. Blocking redirects and isolating Help are application security decisions, not a quoted universal HIG rule. The brief does not establish malicious intent, exfiltration, or storage. |
| 2 — High | External payment links masquerade as local buttons. | Users cannot predict the destination or transaction context. Present them as explicit external links with purpose and actual destination, for example “Manage billing on provider.example — opens in browser.” Open only after deliberate activation; retain Help. | [Buttons: Content](https://developer.apple.com/design/human-interface-guidelines/buttons#Content) supports outcome-specific labels; [Web views: Best practices](https://developer.apple.com/design/human-interface-guidelines/web-views#Best-practices) bounds browsing to the immediate task. Browser handoff and destination disclosure are product decisions. External payments themselves are not established as prohibited; no payment-policy or legal conclusion is possible. |
| 3 — High | Web content supplies the entire app navigation, without Back controls. | A linked page can strand the user and mix app navigation with document history. Keep app destinations and return-to-task access in the host; bound the web pane to Help. Add working Back and Forward for multipage Help, distinct from Close Help. | [Web views: Best practices](https://developer.apple.com/design/human-interface-guidelines/web-views#Best-practices) explicitly calls for enabled history and corresponding controls for multiple pages. It does not ban all web-based app navigation; the bounded Help design is the audit’s correction for this context. |
| 4 — High | Zoom and text selection are disabled. | Readers cannot enlarge help or select instructions to copy. Enable text enlargement through at least 200% with usable reflow, selection, and Copy. Preserve zoom choice through article navigation. | [Accessibility: Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision) supports at least 200% enlargement. [Typography: macOS](https://developer.apple.com/design/human-interface-guidelines/typography#macOS) says macOS has no Dynamic Type: provide explicit resizing. Selection/Copy is a task-based recommendation here, not an asserted blanket HIG mandate. No font-size or contrast defect is established. |
| 5 — Medium | Load failures leave a blank white view. | The user receives neither explanation nor recovery. Preserve useful prior content, show a persistent failure message and Retry, and keep history and Close usable. | [Loading](https://developer.apple.com/design/human-interface-guidelines/loading#Best-practices) favors useful content and continued interaction; [Showing progress](https://developer.apple.com/design/human-interface-guidelines/loading#Showing-progress) calls for truthful wait feedback. Exact error copy, retry, and timeout policy are application decisions. White itself is not the finding. |

## Corrected navigation and control contract

Assume general Help is readable without an account; account-specific assistance may explicitly require sign-in. Confirm this product assumption before implementation. Do not silently gate general Help on authentication.

```text
Host app task (preserve selection, edits, and focus origin)
  -> Open Help -> Help home -> Article A -> Article B
                              <- Back      <- Back
                              -> Forward when history exists
  <- Close Help from any Help state

Help -> explicit external link -> default browser
     -> return to unchanged Help history, article, scroll, and zoom
Help -> unexpected auth redirect -> blocked notice + last safe article
     -> optional explicit Open Account Sign-In -> established account flow
```

Back traverses document history; at its boundary it is disabled, never repurposed to close Help. Forward is enabled only when forward history exists. A successful new navigation after Back truncates forward history. Failed, blocked, and external navigation do not enter article history. Preserve scroll positions for history entries. Close Help restores the host task and its focus origin. Keep a later Help entry available. This exit follows [Offering help](https://developer.apple.com/design/human-interface-guidelines/offering-help#Best-practices), which recommends dismissible help tied to the task.

Place Back/Forward together at the leading side of the host’s Help toolbar, title the surface “Help” or the current article, and keep Close Help distinct from history. Preserve essential navigation at narrow widths. Every toolbar action also has a menu-bar command, so hiding the toolbar does not remove access. These placement decisions follow [Toolbars: Navigation, Item groupings, and macOS](https://developer.apple.com/design/human-interface-guidelines/toolbars#Navigation).

| Control or candidate | Contract and inspection boundary |
|---|---|
| Existing payment “buttons” → external links | Show action, real destination, and browser transition in visible text and accessible name. No automatic purchase or external opening on load. Existing labels, roles, geometry, and handlers are unknown. Candidate procedure: Buttons, alongside Web views. |
| Back / Forward | Named history commands, accurate disabled states; activation never dismisses Help. Candidate procedures: Web views and Toolbars. |
| Close Help | Host command available during loading, failure, and blocked navigation; restores app task. No claim that the original lacks dismissal, only that the corrected design requires it. Candidate procedures: Buttons and Offering help. |
| Retry | Enabled after failure, retries the failed approved article once per activation; duplicate activation while pending is ignored. Does not reload the entire app. Candidate procedures: Buttons and Loading. |
| Larger Text / Smaller Text / Actual Size | Explicit reading controls and menu commands; support at least 100–200% text scale, retain hierarchy, wrap essential text, and grow containers. Ordinary article text remains selectable and copyable. Candidate procedures: Typography and Accessibility. |
| Unexpected credential fields | No credential fields or submit path in Help; legitimate sign-in is an explicit separate task. Candidate procedures: Managing accounts and Privacy. Actual field semantics are unknown. |

All commands need keyboard activation, visible focus, semantic names/roles/states, and press feedback where custom controls are used. Link semantics identify navigation. Do not assign external payment or sign-in as an implicit Return/default action. No target dimensions are verified. The local Buttons guide gives a general 44 × 44 pt target, while Accessibility gives macOS 28 × 28 pt default and 20 × 20 pt minimum; this audit uses standard Mac control sizing as the platform baseline and does not silently impose the general value on every Mac toolbar item. Actual activation regions and spacing require measurement.

## Framework-agnostic navigation policy

This policy requires real approved origins/routes supplied by the product; none are invented from the brief. An origin allowlist alone is insufficient if a permitted route can serve sign-in content.

```text
beforeNavigation(request):  // applies to initial loads, every redirect, frames,
                            // form submissions, and new-window requests
  destination = parseAndNormalize(request.url)
  if isAuthRoute(destination) or request.isCredentialSubmission:
    cancelBeforeContentOrSubmission()
    showBlockedNotice("Sign-in is unavailable in Help.")
    retainLastSafeArticleAndHistory()
  else if isApprovedReadOnlyHelpRoute(destination):
    beginArticleLoad(destination, newRequestId())
  else if request.isExplicitUserLinkActivation
          and isApprovedExternalDestination(destination):
    cancelEmbeddedNavigation()
    openDefaultBrowser(destination)  // already disclosed by the link
    if handoffFails: showRecoverableNotice("Couldn’t open the browser.")
  else:
    cancelEmbeddedNavigation()
    showBlockedNotice("This destination can’t open in Help.")

beginArticleLoad(url, id):
  keepHostControlsUsable()
  retainLastSafeArticleIfAvailable()
  showStatus("Loading help…")  // no invented percentage or completion estimate
  onSuccess(id, approvedDocument):
    if id != currentRequestId: ignoreStaleResult()
    else: commitArticleAndHistory(); clearStatus()
  onFailureOrConfiguredTimeout(id):
    if id == currentRequestId:
      showPersistentError("Couldn’t load this help article.", Retry, CloseHelp)
      retainLastSafeArticleOrShowHelpScaffold()
```

For unexpected credential forms served at an otherwise approved URL, URL checks alone cannot provide the promised boundary. Serve controlled read-only Help documents, prohibit credential forms and submission paths, and enforce the boundary before interaction. Do not depend on detecting a password field after credentials have already been entered. Isolate Help from credential/session storage and privileged host bridges. These are implementation requirements proposed by this audit and need security validation.

Data-purpose decision: Help needs article identifiers and reading state, not passwords or payment details. The established account flow owns authentication; the external billing destination owns payment entry. Do not log credentials, tokens, or sensitive redirect query strings in Help telemetry. Retention and actual transfers remain unknown; no privacy certification is implied.

## Worked before/after

Illustrative article names and steps below demonstrate the contract; they are not additional observed screens.

**Before:** A person opens Help from an unfinished task, follows “Billing,” then activates a payment-looking local button. An unexpected sign-in page takes credentials inside Help. There is no Back route. A subsequent load failure leaves white space, and the person cannot enlarge or copy the instructions.

**After:** Opening Help preserves the unfinished task. Help home → Billing enables Back and disables Forward. The billing link says “Manage billing on [actual provider domain] — opens in browser”; activating it opens that destination externally without changing Help history. Any unexpected sign-in redirect is canceled before credential entry, leaving Billing visible with the blocked notice. Back returns home and enables Forward; Forward restores Billing and its scroll position. A failed related article leaves Billing visible with “Couldn’t load this help article,” Retry, and Close Help. Retry success commits the article; repeated failure preserves recovery. Text can be enlarged to 200%, selected, and copied. Close Help returns to the unfinished task without saving, discarding, or submitting it.

## Acceptance checks and current results

| Check | Required observable result | Current status |
|---|---|---|
| Evidence and route inspection | Root skill → selected families → topic procedures → source guides; topic-index concepts searched | Passed: local instruction inspection only |
| Original navigation | Multipage history and return routes exist | Failed by supplied description: no Back controls; Forward and host dismissal unknown |
| Original trust boundary | Authentication is expected and external actions disclose destination | Failed by supplied description |
| Original reading and recovery | Enlargement/selection available; failure has recovery | Failed by supplied description |
| Corrected history | Home → A → B → Back → Forward restores correct pages/scroll; boundary disables Back; new branch drops forward history | Not executed; specification walkthrough only |
| Corrected exit | Close during load, failure, or block returns to original task and focus; Help can reopen | Not executed |
| Redirect and submission isolation | Test initial URL, multi-hop redirects, frames, forms, script navigation, and new-window requests; blocked authentication never renders or submits; no secrets in logs/storage | Not executed; requires implementation and security instrumentation |
| External links | Visible/accessible text matches actual host; one deliberate activation opens browser; handoff failure is recoverable; return retains Help | Not executed |
| Slow/offline/retry | First load shows scaffold/status; refresh retains useful content; failure offers Retry; partial content is identified; stale responses cannot overwrite newer navigation | Not executed; no timings measured |
| Reading | At 100%, 150%, and 200%, essential text/actions remain available; text selects and copies; history retains zoom | Not executed |
| Keyboard and assistive access | Reach and activate all routes without pointer; names/states are accurate; focus survives transitions; toolbar-hidden/menu and narrow-width paths work | Not executed; requires Mac keyboard and assistive-technology evaluation |
| Visual behavior | Measure actual contrast/targets; check light/dark and increased contrast, localization, and text wrapping | Not executed; no visual evidence |

The proposed state model has been manually traced for success, history boundary, failure, retry, blocked authentication, external handoff, and exit. This establishes specification coverage only. It does not establish corrected runtime behavior.

## Guidance provenance and limits

Read the installed `.agents/skills/apple-hig/SKILL.md`, then Content/Web views; Foundations/Accessibility, Typography, Privacy; Patterns/Loading, Managing accounts, Offering help; and Menus and actions/Buttons, Toolbars, each topic procedure before its reference. The local topic index was searched for relevant concepts. Official links above identify the source sections; no web browsing occurred. Local references are dated snapshots, not SDK documentation or proof of independent source review.

No GUI, device, Apple SDK, native web engine, VoiceOver, Accessibility Inspector, browser handoff, network, or accessibility execution was performed. No code build or runtime test was possible from this brief. The audit cannot establish authentication provider trust, credential storage, transaction behavior, App Store payment compliance, actual focus order, visual fidelity, timing, or security effectiveness. These findings and the proposed corrections are reviewable specifications, not a claim that the app has been fixed.
