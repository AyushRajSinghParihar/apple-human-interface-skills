# Mac people directory audit

## Basis and decisions

Evidence: `interface.md`, a one-line behavioral description for macOS. “Verified” below means explicitly stated in that supplied description, not reproduced in an application. No implementation, screenshot, dataset, or executable interface was supplied. Preserve the people-directory task and its window; specify behavior independently of any SDK.

The installed apple-hig root was explicitly read, then the topic index was searched. Routes consumed in order: each owning family → topic procedure → supporting reference, under `.agents/skills/apple-hig/subskills/`:

- `apple-hig-navigation-and-search` → `apple-hig-search-fields` → `references/search-fields.md`.
- `apple-hig-patterns` → `apple-hig-searching` → `references/searching.md`.
- `apple-hig-menus-and-actions` → `apple-hig-buttons` → `references/buttons.md`.
- `apple-hig-foundations` → `apple-hig-accessibility` → `references/accessibility.md`.

Control mapping: search entry, clearing, submission, and scope indicator belong to Search fields; Clear also belongs to Buttons; result freshness and corpus coverage belong to Searching; field naming belongs to Accessibility. The indicator's interactive form is unknown: do not assume a menu, segmented control, or sidebar. Result rows and window chrome are not described sufficiently to audit their control designs.

## Ranked verified findings

Ranking is this audit's judgment, based on harm and task interruption, rather than an Apple severity scale.

| Rank | Supplied observation | Effect | Correction and support |
|---|---|---|---|
| 1 — Critical | “Clear deletes directory records” | A search action unexpectedly destroys underlying people data. Reversibility and extent are unknown. | Make Clear a nondestructive query reset, labeled/named “Clear Search.” It must never call record deletion. Button meaning must describe its outcome ([Buttons, Content and Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Content)); clearing belongs to the search field ([Search fields](https://developer.apple.com/design/human-interface-guidelines/search-fields)). Do not add a deletion-confirmation flow to search. |
| 2 — High | “a query returning zero results leaves stale matches” | People can mistake earlier matches for current results and act on the wrong people. | Replace previous matches with an empty result set and a persistent no-results message naming the current query and scope. This concrete state rule follows the installed Search fields procedure's explicit stale-results failure check; it applies the result-updating guidance in [Search fields, Best practices](https://developer.apple.com/design/human-interface-guidelines/search-fields#Best-practices). |
| 3 — High | “the scope indicator says All while only searching favorites” | Nonfavorite people are silently excluded, producing false negatives. | Default to All and actually search the entire available directory. Favorites must be a deliberate narrower scope whose display and predicate agree. [Search fields, Scope bars and tokens](https://developer.apple.com/design/human-interface-guidelines/search-fields#Scope-bars-and-tokens) recommends starting broad; [Searching, Best practices](https://developer.apple.com/design/human-interface-guidelines/searching#Best-practices) calls for communicating scope. |
| 4 — High | “submitting closes the window” | Search submission interrupts finding and inspecting people. | Submit evaluates the current query and displays results in the same window, preserving query and scope. Keep window closing a separate explicit command. This is a task-specific correction supported by search-result continuity, not a universal prohibition on buttons closing temporary views ([Search fields, iPadOS/macOS](https://developer.apple.com/design/human-interface-guidelines/search-fields#iPadOS-macOS); [Buttons, Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Role)). |
| 5 — Medium | “Search field has no label or placeholder” | Search purpose and searchable content lack textual cues. | Add visible label “Search People,” placeholder “Search all people” or “Search favorites,” and a programmatically associated name “Search People.” The missing visible cues are verified; an absent accessible name is **not** established. Placeholder scope is supported by [Search fields, Best practices](https://developer.apple.com/design/human-interface-guidelines/search-fields#Best-practices); semantic naming by [Accessibility, Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility). |

## Corrected behavior contract

These are proposed product decisions, not evidence of implemented behavior. Use a clearly visible field associated with the directory results. Exact toolbar/sidebar placement requires the missing window structure; the Mac guidance permits different placements for different scopes.

- Initial state: scope All; empty query; all available people shown. All means the available directory corpus, not records outside the user's access.
- Scope text and predicate derive from the same state. If a scope chooser exists, offer All and Favorites; if only an indicator exists, keep All truthful without inventing a chooser.
- Clear Search resets query only, retains the selected scope, recomputes its unfiltered results, and returns focus to the field. It is a normal nondestructive action, not the window's default action. Disable it for an empty query. A custom button needs press feedback and a meaningful accessible name.
- Submit evaluates search without closing the window, deleting records, or opening an arbitrary match. Keep keyboard focus in the field. Result activation, if supported, is a separate action on a stable person ID; preserve query/scope on return from detail. Existing selection survives only if that ID remains in the current results.
- Prefer results while typing where feasible, as HIG recommends. Latency is unknown; explicit submission must work regardless. For asynchronous search, invalidate earlier requests, remove old matches from the current-result presentation, show a pending state, and accept only the latest response. Errors must show failure/retry, never “No people found.”
- Successful zero matches: show no rows and “No people found for ‘{query}’ in {scope},” retaining the field and scope so the person can refine or clear. An empty corpus with an empty query instead says “No people available” or “No favorites yet.”
- Accessible semantics expose the field's name/value, Clear Search as a button, scope as text or the actual chooser's selected value, and results/empty status as readable content. Preserve complete keyboard access and system accessibility shortcuts. Exact spoken order and announcements require runtime verification.

Pseudocode (query matching policy must be agreed against real directory metadata; illustrative matching below uses display name):

```text
state = { query: "", scope: All, requestVersion: 0,
          rows: [], selectedID: none, phase: idle }

refresh():
    version = ++state.requestVersion
    request = immutableSnapshot(state.query, state.scope)
    state.rows = []                 // never present old matches as current
    state.phase = pending
    candidates = directory.readOnlyPeople()
    candidates = request.scope == Favorites
                 ? candidates.where(person.isFavorite) : candidates
    search(candidates, request.query).complete(outcome =>
        if version != state.requestVersion: return
        if outcome.failed:
            state.phase = error; state.selectedID = none
        else:
            state.rows = outcome.people  // assign even when empty
            state.selectedID = retainOnlyIfPresent(state.selectedID, state.rows)
            state.phase = state.rows.empty ? empty : results
    )

onSubmit(): refresh()               // no closeWindow
onClearSearch():
    state.query = ""
    refresh()
    focus(searchField)
onScopeChange(scope):
    state.scope = scope
    refresh()
renderScopeAndPlaceholder(): deriveFrom(state.scope)
```

Every search handler has read-only access to directory data. No deletion capability is required. New edits invalidate outstanding requests immediately, even if evaluation is debounced. The matcher treats an empty query as matching all candidates. These implementation safeguards are audit recommendations, not prescribed Apple APIs.

## Worked before/after

Illustrative fixture, not supplied production data: Ada Chen (favorite), Maya Patel (not favorite), and no person named Zqx.

| Step | Before, applying the supplied description | Corrected behavior |
|---|---|---|
| Search “Maya” while scope says All | Favorites-only filtering excludes Maya; zero matches can leave an earlier result visible. | All includes Maya. The window remains open, showing only Maya. |
| Submit “Zqx” after Maya | Submission closes the window; zero-result handling is also specified to retain stale matches. The brief does not establish the order of those effects. | The window stays open. Rows become empty; status reads “No people found for ‘Zqx’ in All.” |
| Activate Clear | Directory records are deleted; exact affected set is unspecified. | Query becomes empty, All remains selected, and Ada and Maya appear. Both records remain unchanged. Focus returns to Search People. |
| Deliberately choose Favorites, if supported, and search “Maya” | Existing indicator falsely says All despite favorites filtering. | Scope says Favorites and the field says “Search favorites.” No matches appear. Switching to All finds Maya. |

## Acceptance checks and status

**Passed — document inspection only:** platform established as macOS; all five supplied defects mapped to ranked findings and explicit corrected transitions; installed root, selected families, procedures, and local references read. Framework-agnostic specification produced. No network browsing performed.

**Failed — supplied behavior only:** clear preserves records; zero matches replace stale rows; displayed scope matches searched corpus; submit retains the directory window; search has visible purpose/scope cues. Each fails according to `interface.md`, without runtime reproduction.

**Not executed — implementation acceptance:**

1. With the fixture above, search Maya under All: exactly Maya appears. Under Favorites: zero rows. Changing scope preserves query and immediately reevaluates; text and actual corpus agree.
2. After a positive match, search Zqx: no stale rows or selected person remain; current query/scope and empty feedback remain visible. Empty-directory and error states are distinguishable from zero matches.
3. Snapshot record IDs, attributes, favorites, and count; activate Clear Search and submit via pointer and keyboard. All data stays identical; clear resets only query, retains scope, and restores field focus. Empty-query Clear is disabled; Return in the field never closes the window or deletes records.
4. Resolve request A after newer request B, including when B has zero matches: A cannot replace B's rows/status. Clear or scope change during a pending request invalidates its response.
5. Navigate the whole search/clear/scope/result workflow with keyboard and macOS Full Keyboard Access. Verify associated field name, values, scope, button name, empty/error feedback, and useful reading order with VoiceOver and Accessibility Inspector on the Mac. Ensure system shortcuts still work.
6. If result activation exists, activate a named person and verify exact person ID; return retains query/scope. Resize the window and enlarge text to 200%: field, scope, empty feedback, and actions remain usable without clipping essential content. Measure actual target separation and light/dark contrast rather than inferring them from this brief.

## Evidence limits

This is a specification audit, not an application patch or test run. No device, GUI, SDK compilation, assistive-technology execution, native rendering, hit-region measurement, contrast calculation, or search relevance testing occurred. Source links identify official articles represented in the installed local snapshot (dated 2026-10-25); those URLs were not opened. No newer-source verification or independent source-review claim is made.

Unknowns include matching fields, data size/latency, deletion persistence and recovery, accessible names, keyboard/default bindings, result activation, window structure, and whether scope is interactive. Suggestions, history, tokens, Spotlight indexing, and deletion UI are not established requirements; their absence is not a finding. No new record-deletion action or alert is specified. If deletion is later designed, route separately through Alerts and Undo and redo before deciding confirmation and recovery.

The local Buttons guide gives a general 44×44 pt hit-region recommendation while Accessibility lists macOS default 28×28 pt and minimum 20×20 pt. This audit makes no dimensional violation claim from missing geometry; measure actual controls and retain platform-standard sizing and sufficient separation, documenting any custom sizing decision against both passages.
