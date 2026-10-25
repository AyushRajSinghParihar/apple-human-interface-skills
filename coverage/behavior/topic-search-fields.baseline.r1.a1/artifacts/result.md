# Mac people-directory audit

## Scope and decisions

This is a specification audit of `interface.md`, which explicitly describes macOS and five behaviors. “Verified” below means confirmed by that supplied text, not reproduced in an application. No implementation or screenshot was supplied. Use framework-independent search semantics; an Apple SDK is not required.

Treat this as a persistent directory window: search finds people, Clear resets the query, and Return submits without dismissing the window. Default to **All People**, with an explicit **Favorites** scope. All People means every record available in this directory, subject to the same access rules as browsing. These are product decisions chosen to correct the described behavior, not claims that HIG mandates these exact strings or architecture.

## Ranked verified findings

Severity reflects consequence, not an Apple severity scale. Fix all five before accepting the search flow.

| Rank | Finding and supplied evidence | Effect | Correction and guidance |
| --- | --- | --- | --- |
| 1 — Critical | “Clear deletes directory records” | A routine search action destroys directory data. Reversibility and deletion extent are unknown. | Clear must only empty query text and refresh results within the current scope. Give it the accessible name “Clear Search.” Never dispatch a record mutation from search controls. HIG describes search-field clearing and requires button meaning to explain its action. If record deletion exists elsewhere, give it a separate explicit action; warnings apply to unexpected irreversible loss, not every ordinary deletion. [Search fields](https://developer.apple.com/design/human-interface-guidelines/search-fields), [Buttons — Content and Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Content), [Feedback — Best practices](https://developer.apple.com/design/human-interface-guidelines/feedback#Best-practices). |
| 2 — High | “a query returning zero results leaves stale matches” | People can mistake unrelated records for matches to their current query. | Replace previous rows with an empty result set and contextual text: “No people found for ‘…’ in All People.” Retain query and scope so people can revise them. Do not use an alert for this routine outcome. This correction applies HIG's contextual state/outcome feedback; the exact empty-state wording is a product choice. [Feedback — Best practices](https://developer.apple.com/design/human-interface-guidelines/feedback#Best-practices). |
| 3 — High | “the scope indicator says All while only searching favorites” | A person outside Favorites appears absent from the directory. | Make All People search all available people; Favorites searches favorites only. Derive indicator, placeholder, and filtering from the same scope value. Begin broadly and let people narrow deliberately. [Search fields — Scope bars and tokens](https://developer.apple.com/design/human-interface-guidelines/search-fields#Scope-bars-and-tokens), [Searching — Best practices](https://developer.apple.com/design/human-interface-guidelines/searching#Best-practices). |
| 4 — High | “submitting closes the window” | Submission removes the place where people need to inspect results. | Route Return in the field to search; preserve the directory window, query, scope, and field focus. Opening a selected person is a separate explicit action. HIG allows a primary action to close a temporary view; that does not establish that a directory search should close its window. This correction is a task-based decision supported by search results remaining usable and contextual. [Search fields — iPadOS, macOS](https://developer.apple.com/design/human-interface-guidelines/search-fields#iPadOS-macOS), [Buttons — Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Role). |
| 5 — Medium | “Search field has no label or placeholder” | Search purpose and searchable scope are unexplained. | Add a visible associated label “Search People,” placeholder “Search All People” or “Search Favorites,” and a programmatic accessible name “Search People.” Keep scope separately exposed. The missing visual explanation is verified; absence of an accessible name is not established by this text. HIG recommends scope-explaining placeholders and meaningful accessible descriptions. [Search fields — Best practices](https://developer.apple.com/design/human-interface-guidelines/search-fields#Best-practices), [Accessibility — Vision and Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision). |

## Corrected behavior specification

Prefer updating results as people type where practical; this is a HIG preference, not a universal requirement. Return also requests the current search. Matching fields and normalization need product agreement; for the worked example, use case-insensitive display-name substring matching.

```text
state = {query: "", scope: ALL_PEOPLE, phase: READY,
         rows: [], selectedPersonID: none, requestVersion: 0}

scopeDescription = scope == ALL_PEOPLE ? "All People" : "Favorites"
placeholder = "Search " + scopeDescription
accessibleFieldName = "Search People"

onQueryEdit(text):
    state.query = text
    refresh()
onScopeChange(scope):
    state.scope = scope
    refresh()
onClearSearch():
    state.query = ""
    refresh()                 // preserve scope; no directory write
    focus(searchField)
onReturnInSearchField():
    refresh()                 // consume search submission; no close-window action

refresh():
    version = ++state.requestVersion
    snapshot = (state.query, state.scope)
    state.rows = []            // never present old rows as current matches
    state.selectedPersonID = none
    state.phase = LOADING
    readDirectory(snapshot.scope, snapshot.query).then(result):
        if version != state.requestVersion: return
        state.rows = result    // including []
        state.phase = result.isEmpty ? EMPTY : READY
    .catch(error):
        if version != state.requestVersion: return
        state.rows = []
        state.phase = ERROR    // distinct from no matches; offer Retry

render:
    LOADING -> contextual "Searching…"; old results unavailable for activation
    EMPTY   -> no result rows; query + scope in no-matches message
    READY   -> only current matching rows; current result count
    ERROR   -> contextual failure and Retry; preserve query and scope
```

An empty query lists people within the chosen scope. Search completion must not steal focus. Announce settled result count, no matches, or error through the host platform's accessible status mechanism without moving focus or announcing every keystroke. All field, scope, Clear, Retry, and result actions must be keyboard reachable with visible focus. These are acceptance requirements; they have not been executed. HIG supports complete keyboard navigation and accessible feedback: [Accessibility — Speech](https://developer.apple.com/design/human-interface-guidelines/accessibility#Speech), [Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback).

## Worked before/after

Illustrative fixture, not supplied production data: Ada Chen is a favorite; Ben Ortiz is not. Both are available directory records.

| Step | Before, following the supplied defects | Corrected behavior |
| --- | --- | --- |
| Open directory | Field has no label or placeholder; indicator says All but searches favorites. | Label Search People; scope All People; placeholder Search All People; both fixture records visible. |
| Search “Ben” | Ben is excluded by the hidden favorites restriction. The zero-result behavior can leave earlier rows displayed. | Only Ben appears; count is 1; directory window remains open. |
| Submit “Ben” with Return | Window closes. | Same query and scope; Ben remains available; focus stays in search. |
| Change query to “Zzz” | Previous matches remain despite no matches. | Zero rows and “No people found for ‘Zzz’ in All People.” No stale selection can open. |
| Activate Clear | Directory records are deleted. | Query becomes empty; both records return; directory data is unchanged. |
| Choose Favorites, search “Ben” | Scope behavior is misleading when labeled All. | Indicator and placeholder say Favorites; zero rows. Switching to All People returns Ben. |

## Acceptance checks

These checks are specified, not run. Use a deterministic fixture and a framework-independent state/handler harness first; use the Mac client for later interaction and assistive-technology validation.

1. **Data integrity:** Snapshot record IDs and values. Search, submit, change scope, and Clear repeatedly. Assert no write/delete calls and identical records afterward. Clear with empty query is harmless.
2. **Scope truth:** With Ada favorited and Ben not favorited, All People + “Ben” returns Ben; Favorites + “Ben” returns zero. Indicator, placeholder, accessible scope value, and request scope agree after every scope change.
3. **Empty transition:** Find Ada, then search “Zzz.” Assert zero rows, no selected person, and a query/scope-specific empty message. No previous row is actionable.
4. **Submission:** Return while focus is in search executes search and leaves the window open with query, scope, and focus preserved. It cannot invoke a default close or destructive command.
5. **Clear semantics:** In Favorites, enter a query, then Clear. Assert empty query, Favorites preserved, all favorite records shown, and field focus retained.
6. **Request ordering:** Delay an old matching response until after a newer zero-result response. Assert the late response cannot restore stale matches. Repeat across a scope change and Clear. For synchronous implementations, verify equivalent atomic state transitions.
7. **Failure handling:** Force a read failure. Assert error rather than empty-success text, zero stale rows, preserved query/scope, and a working Retry.
8. **Mac interaction/accessibility:** Inspect accessible name, search semantics, scope value, Clear name, result status, and focus order. Manually verify keyboard-only use, visible focus, and VoiceOver feedback on a Mac. A placeholder alone must not supply the only field identity. Record actual outcomes before claiming support.

## Evidence limits and instruction trail

Read the installed root `apple-hig/SKILL.md` first, then the navigation-and-search and patterns family procedures before their selected source guides (`search-fields.md`, `searching.md`, and `feedback.md`). Also read the foundations and menus-and-actions family procedures before `accessibility.md` and `buttons.md`. All paths resolved within `.agents/skills/apple-hig/`; each file was read in a separate shell command. No additional topic procedure was routed by these family files.

The local guides identify a 2026-10-25 snapshot/retrieval date. Official links above attribute those installed guides; they were not opened or checked online. This audit used only `interface.md` and installed instructions. No source code, GUI, SDK, device, screen reader, Accessibility Inspector, test harness, or runtime execution was available or performed. Async races, loading/error handling, keyboard behavior, and accessible announcements are proposed requirements, not additional verified defects. There is no evidence to judge visual placement, contrast, sizing, typography, resizing, actual data recovery, or existing deletion safeguards. No platform-wide compliance claim is made.
