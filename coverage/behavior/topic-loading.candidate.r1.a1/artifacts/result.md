# Loading and retry audit — iPhone route planner

## Scope and evidence

The sole interface evidence is `interface.md`, a behavioral brief for iOS. Findings below are verified against that description, not reproduced in a running app. No screenshot, implementation, request logs, backend contract, or timing trace was supplied. The five-second delay is reported by the brief, not measured here.

Guidance was read locally from the installed `apple-hig` package: root `SKILL.md`; relevant rows of `references/topic-index.md`; Patterns → Loading, Status → Progress indicators, and Menus and actions → Buttons, each in family → topic procedure → supporting guide order. References carry a 2026-10-25 snapshot date. Official links below identify the guidance; no web access was used or freshness independently verified.

## Ranked verified findings

Severity is an audit judgment based on task impact, not an Apple severity scale. All five findings have direct textual evidence; their implementation causes remain unknown.

| Rank | Finding and evidence from interface.md | Effect | Correction and basis |
| --- | --- | --- | --- |
| 1 — High | “retry creates overlapping requests and duplicates results” | Repeated recovery can corrupt the route choices presented to the person. | Admit one active attempt for the current route query; ignore superseded responses; replace results with a unique snapshot. This concurrency policy is an engineering decision supporting reliable recovery, not an Apple-prescribed algorithm. Buttons guidance calls for meaningful waiting feedback; the topic procedure calls for duplicate-activation handling. |
| 2 — High | “failure leaves no retry” | A failed search reaches a dead end. | Stop activity, retain available routes and inputs, explain failure inline, and offer **Retry Routes**. Progress guidance calls for useful recovery when work stalls. |
| 3 — High | “Cached routes disappear behind an indefinite spinner” | Available information becomes inaccessible while fresh results are unavailable. | Show matching cached routes during refresh and failure, labeled as saved results with their known update time. Keep available interaction usable. Loading guidance favors useful content and background loading. |
| 4 — Medium | “a fake 90% bar never advances” | The UI promises unsupported completion and disguises a stall. | Remove invented percentages. Use indeterminate activity for unknown whole-operation duration; terminate it on success, failure, cancellation, or timeout. Progress guidance requires honest whole-operation estimates. |
| 5 — Medium | “no initial acknowledgment appears for five seconds” | People cannot tell whether the action registered and may activate it again. | On activation, immediately enter pending state and show activity within the initiating button. Do not wait for the network response to acknowledge the action. This follows the iOS delayed-completion button guidance. |

Material source sections: [Loading — Best practices](https://developer.apple.com/design/human-interface-guidelines/loading#Best-practices), [Loading — Showing progress](https://developer.apple.com/design/human-interface-guidelines/loading#Showing-progress), [Progress indicators — Best practices](https://developer.apple.com/design/human-interface-guidelines/progress-indicators#Best-practices), and [Buttons — iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS).

## Decisions and corrected behavior

### Content and progress

- Keep origin, destination, options, navigation context, and selected route identity through refresh and retry. Only show cached routes that match the current query. Never present results from an old query as current results.
- Render matching saved routes promptly and keep them inspectable while fetching. Use “Saved routes · Updated {known time}”; if the time is unknown, omit it rather than inventing freshness. Saved route information must not imply live traffic or availability.
- Without cache, show the route-results structure and “Finding routes…” rather than fake route values. Independent decorative assets must not gate route results; none are documented in the supplied brief.
- Unknown duration uses a spinner in a stable status location. For button-initiated requests, place it within that button, preserving its label/context; avoid redundant competing indicators. Automatic refresh uses the results status area. Do not switch the spinner into a bar mid-attempt.
- There is no evidence of a measurable whole-operation denominator, so this specification does not use determinate progress. If one is later proven, select a compatible progress presentation deliberately and test stage boundaries; completed subrequests alone do not establish whole-task percentage.
- A timeout ends the UI wait and offers recovery. Proposed product default: 30 seconds per attempt, configurable after real latency evidence. This is not a HIG timing requirement. Timeout says “Routes are taking too long. Try again.” A generic failure says “Couldn’t update routes. Try again.” With cache, add “Showing saved routes.” With no cache, say “Couldn’t load routes. Try again.” Do not infer an offline cause without evidence.
- Success publishes the validated result snapshot atomically, removes temporary progress/error, and records freshness. A successful empty snapshot says “No routes found” and permits editing the query; it is not a transport error. Invalid or unusable responses produce recoverable failure. If incremental delivery is later supported, keep valid partial results with explicit incomplete status; this brief establishes no streaming contract.

### Control contract

| Control | Scope, role, and placement | Availability and outcome |
| --- | --- | --- |
| Existing initiating command (label unknown) | Candidate: immediate-action button; supplied visual design and hit region unknown. Proposed label **Find Routes**, normal nondestructive role, prominent near route inputs. | Idle: starts current query. Pending: immediate press feedback and in-button spinner with “Finding Routes…”; duplicate activation does nothing. Success/failure removes activity. |
| Retry mechanism (surface/label unknown in brief) | Candidate: button. Corrected **Retry Routes**, normal nondestructive role, prominent beside the inline error in the results area. | Failed/timed out: starts the same query with one new attempt. Pending: “Retrying Routes…” with in-button activity; unavailable for further activation while the guard remains active. Repeated failure restores Retry Routes. |
| Proposed **Cancel** | Secondary button adjacent to pending status; abandons the refresh only. | Pending only. Stops waiting, invalidates the attempt, preserves inputs and saved results. It does not delete routes. No pause or confirmation is needed for this proposed read-only fetch; revisit if cancellation later discards useful work. |

Use clearly separated hit regions of at least 44 × 44 pt on iPhone and perceivable press feedback for custom controls. Prefer system styles when available; no SDK is assumed. “Finding Routes…” explains why the initiating action is unavailable during work. These are proposed specifications, not verified properties of the supplied controls. Source: [Buttons — Best practices, Style, Content, Role](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices).

No alert or sheet is evidenced or needed for the proposed routine inline recovery. The apparent tension between “failure leaves no retry” and “retry creates overlapping requests” is retained: these may describe different states or an external retry path. The brief does not establish how retry is currently reached. Neither finding proves a particular control is visible.

### Framework-agnostic state contract

States: `idle`, `pending`, `ready`, `empty`, `failed`. Matching cached results are independent of request state. A failed refresh can still display saved routes.

```text
All state transitions run serially (or under one atomic lock).
queryKey = canonical(origin, destination, routingOptions)
generation = 0
active = none
visibleRoutes = matchingCache(queryKey) or []

start(query):
    key = canonical(query)
    if active exists and active.key == key:
        return                         // synchronous guard, before rendering/network
    invalidateActive()                 // abort if possible; logical invalidation always
    generation += 1
    token = generation
    queryKey = key
    visibleRoutes = matchingCache(key) or []
    active = {token, key, deadline: now + 30 seconds}
    state = pending
    clear error; publish pending UI immediately
    launch fetch(query) tagged with token and key
    schedule timeout(token, key)

isCurrent(token, key):
    return active exists and active.token == token
           and active.key == key and queryKey == key

onSuccess(token, key, payload):
    if not isCurrent(token, key): return
    if payload is invalid: onFailure(token, key, invalidResponse); return
    snapshot = uniqueByStableRouteIdentity(payload.routes)
    // Validate a backend route identity or documented canonical route key;
    // never deduplicate solely by display name or travel time.
    visibleRoutes = snapshot          // replace, never append retry responses
    saveCache(key, snapshot, now)
    active = none; cancel deadline
    state = empty if snapshot is empty else ready
    clear error; remove progress; publish

onFailure(token, key, reason):
    if not isCurrent(token, key): return
    abort transport if possible
    active = none; cancel deadline
    state = failed
    keep matching saved routes and query; remove progress
    show reason-appropriate message and Retry Routes

onTimeout(token, key):
    onFailure(token, key, timeout)

cancel():
    invalidateActive(); generation += 1
    state = idle; remove progress and error
    keep query and matching saved routes

onQueryChanged(newQuery):
    cancel()
    queryKey = canonical(newQuery)
    visibleRoutes = matchingCache(queryKey) or []
    // Start only on the product's normal submit/refresh trigger.

retry(): start(currentQuery)
```

`invalidateActive` clears ownership and cancels the timer before requesting transport abort. Aborting a transport may not stop server work; token checks protect the UI even then. A new query may supersede an old transport, but at most one attempt owns current-query UI state. Timeout followed by retry can likewise leave obsolete server work; this specification does not claim backend cancellation. Completion, failure, and timeout racing each other accept only the first current terminal event. Cache writes also require a current token, preventing old responses from overwriting newer data. Preserve selection by route identity when it survives replacement; otherwise clear it explicitly rather than silently selecting another route.

## Worked before/after

Scenario: saved routes A and B exist for the current query. A refresh fails; the person taps retry twice quickly.

**Before, as described:** A and B disappear behind a spinner. For five seconds there is no acknowledgment. A fabricated 90% bar stalls. Failure offers no recovery. If retry is reached, two requests overlap and append duplicate results.

**After, proposed:** A and B remain visible as saved routes. The initial activation immediately shows in-button activity. No percentage appears. On failure, the spinner disappears and an inline message says “Couldn’t update routes. Showing saved routes. Try again.” Retry Routes becomes available. The first tap claims a new attempt synchronously and shows “Retrying Routes…”. The second tap starts nothing. A late response from the failed attempt changes nothing. When the current attempt returns A, A, and C, the validated snapshot becomes A and C once each; saved freshness updates and activity disappears. If the attempt instead times out, A and B remain and retry returns. Cancel preserves those routes and ignores subsequent late responses.

## Acceptance checks and status

### Passed — static audit/specification inspection

- All five ranked findings are directly traceable to `interface.md`; source-backed experience guidance is distinguished from engineering choices.
- The proposed model covers cached/uncached loading, success, empty success, failure, timeout, retry, query change, cancellation, and stale responses.
- The proposed unknown-duration path has no fabricated percentage and defines removal of progress on every terminal transition.

These passes concern the written artifact only.

### Failed — supplied behavior, as reported

- Useful cached content remains visible during refresh: failed.
- Activation receives prompt acknowledgment: failed; brief reports five seconds.
- Progress reflects real whole-task completion: failed; brief calls the 90% bar fake.
- Failure offers a recovery path: failed.
- Retry prevents overlapping current attempts and duplicate results: failed.

### Not executed — implementation acceptance checks

| Test input | Required observable result |
| --- | --- |
| Slow fetch, matching cache | Saved routes stay inspectable; immediate pending feedback; inputs/context retained; no invented estimate. |
| Cold fetch, no cache | Useful structure and honest activity appear promptly; no fabricated route rows. |
| Network failure/offline, with and without cache | Activity ends, accurate error and Retry Routes appear; available matching data persists. No unsupported claim about the cause. |
| Frozen request | Configured 30-second deadline ends pending state; timeout message and retry appear; late completion is ignored. |
| Ten rapid retry activations | One attempt owns current query; one transport launch for that activation burst; controls acknowledge pending state. |
| Failure → retry → success | Exactly one unique result snapshot; error and progress disappear; success is distinct from request acceptance. |
| Old query responds after a new query | Old payload changes neither visible routes nor current cache/selection. |
| Success races timeout/failure; response repeats | Only the first current terminal event wins; no duplicate application. |
| Cancel, then late completion, then restart | Inputs and saved routes persist; no post-cancel update; restart works. |
| Empty/invalid/duplicate-containing response | Empty state is distinct from failure; invalid payload permits retry; valid duplicates collapse by route identity. |
| Stage boundary / unknown-to-known duration | No fake stage percentage or spinner-to-bar jump. Any future determinate design must prove a whole-operation denominator. |
| Button layout and interaction | Measure at least 44 × 44 pt hit regions and separation; verify press/pending feedback, label fit, disabled state, naming, and focus on the actual implementation. |

Partial delivery and pause/resume are not established capabilities; if introduced, add corresponding acceptance cases rather than treating them as tested. No measured performance, backend completion, SDK compilation, device rendering, GUI interaction, VoiceOver/accessibility execution, haptics, or physical target testing occurred. Linux file inspection cannot establish those results. No application implementation was supplied or changed; this artifact is the requested audit and correction specification.
