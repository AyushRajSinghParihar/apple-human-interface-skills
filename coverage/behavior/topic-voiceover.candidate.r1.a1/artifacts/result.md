# Revised iPhone departure-list interaction specification

## Scope and evidence

This is a framework-agnostic design contract for iOS on iPhone. `interface.md` reports four separate unlabeled row elements in random order, a favorite button named “Star,” and countdown announcements interrupting speech every second. Those are supplied descriptions, not independently observed runtime defects. The task is to compare departures, identify destination/platform/time/status, and change a favorite without losing reading position.

Assumptions: rows are informational; no row navigation is specified. Favorites apply to the service represented by a row, using a stable `favoriteKey` rather than a countdown or list position. The product must supply that key and its human-readable scope (for example, destination plus route/direction if needed). The sample below uses distinct destinations. No route, stop selector, refresh control, or detail screen is invented.

## Decisions and semantic structure

Use a text list with a short page title, “Departures,” exposed as a heading. If an existing stop name is available, include it in the page title. Do not create a heading for every departure. The heading rotor reaches the page heading and any genuine existing section headings; ordinary rows remain ordinary content. This expresses hierarchy without making the rotor a duplicate list. [VoiceOver — Navigation](https://developer.apple.com/design/human-interface-guidelines/voiceover#Navigation), [Lists and tables — Content](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables#Content).

Each row is a nonfocusable structural group containing exactly two sequential focus stops:

| Stop | Role | Name | Value/state | Activation |
| --- | --- | --- | --- | --- |
| Departure summary | Static text, one combined accessible element | Destination, including existing service qualifiers needed to distinguish it | “Platform {platform}. {departure phrase}. {status}.” | None; no button, link, selected state, or disclosure |
| Favorite | Switch-style toggle in the list row | “Favorite, {service scope}” | Off or On, reflecting committed favorite state | Toggle favorite for that key |

The page order is heading, first summary, its favorite, second summary, its favorite, and so on. Within each summary the information order is destination → platform → departure time/countdown → status. Preserve the visible row sequence in accessibility traversal and locale reading direction; do not order by individual field type. Use stable departure IDs, never row indices, for focus identity. Text children composing the summary, decorative separators, and redundant icons are not additional focus stops. The favorite remains a reachable sibling, not a hidden child of the combined text element. [VoiceOver — Descriptions and Navigation](https://developer.apple.com/design/human-interface-guidelines/voiceover).

Replace the standalone star button with a labeled switch because the favorite is a persistent binary state in a list row. “Favorite” must identify the affected service even when reached directly. On/Off is semantic state; do not put “switch” into the name. A decorative star may remain but must not announce “Star” separately. This follows the local guide’s iOS list-row switch guidance rather than treating all persistent states as command buttons. [Toggles — Best practices and iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/toggles).

Choose a 44 × 44 pt or larger selectable region for the favorite, with no overlap with the summary region; allow row height to grow. Keep destination, platform, time, status, and favorite usable with at least 200% text enlargement. Do not depend on star color or status color to convey state. The local accessibility guide gives 44 × 44 pt as the iOS default and 28 × 28 pt as a smaller minimum; this design chooses the default. [Accessibility — Vision and Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility).

### Content rules

- Expand ambiguous display abbreviations for speech: “Platform 4,” “Departs in 3 minutes,” “Delayed.” Do not read an isolated “4” or “03:00.” Use localized number, duration, and time formatting.
- For a positive duration below one minute, say “Departs in less than a minute”; for longer durations, use whole minutes rounded up. Never speak negative countdowns. Use “Due now” at zero only while the feed still describes an active departure. Prefer “Cancelled” or “Departed” when the feed explicitly supplies that status, suppressing contradictory countdowns.
- If prediction is absent, say “Departure estimate unavailable”; include a scheduled clock time only if supplied, labeled “Scheduled departure …”. If platform or status is missing, say “Platform not announced” or “Status unavailable”; do not invent “On time.” Preserve relevant delay/cancellation text.
- Expose complete identifying text even if the visual layout truncates. For duplicate destinations, include existing route/direction/scheduled-time qualifiers as necessary in the summary and favorite scope.

These exact phrases, rounding, and two-stop structure are product decisions applying HIG’s meaningful names, relationships, and synchronized values; HIG does not prescribe this transit vocabulary.

## Dynamic behavior and focus contract

A clock tick updates visible and accessible values atomically, without live speech announcements, speech cancellation, or focus movement. On the next visit to a summary, read its current value. Do not restart an utterance already in progress when its countdown changes. Turning off automatic speech must not freeze accessible data.

Feed changes such as platform changes, cancellation, or loss of live data update the same stable row. For the focused departure, coalesce material changes from one feed transaction into one concise notification queued after current speech, for example “Central: platform changed to 6.” Revalidate queued information before delivery and discard superseded or duplicate events. Routine minute/second changes never enter that queue. Off-focus updates remain available on traversal without unsolicited speech. No automatic announcement moves focus. If the platform cannot deliver noninterrupting notifications reliably, retain current semantic values and a persistent visible/accessibile update message instead; never fall back to interrupting tick announcements. This is a proposed notification policy, not a verified API guarantee. HIG asks that values stay synchronized and relevant changes be communicated; it does not specify these thresholds. [VoiceOver — Navigation](https://developer.apple.com/design/human-interface-guidelines/voiceover#Navigation).

Keep rows in feed order during a reading session; countdown ticks do not resort them. When a feed transaction genuinely reorders rows, preserve focus by departure ID and subelement. If a focused departure is removed, move to the next surviving departure summary in the previous sequence, otherwise the preceding summary, otherwise the persistent empty message “No departures available.” Notify once of removal after speech; never move to a different row’s favorite by reusing an index. A newly inserted row does not steal focus. Long-list recycling must preserve these identities and allow access to every supplied departure. This focus fallback and ordering policy are product decisions.

Favorite activation commits once to durable local state, updates On/Off and visible appearance together, and keeps focus on that toggle. A second deliberate activation reverses it. Rely on the control’s state feedback rather than adding duplicate success announcements. If saving fails, retain the previous committed state and expose a persistent inline message, “Couldn’t save favorite. Try again,” associated with that control; queue it once without interrupting speech. Retry uses the same toggle. Remote synchronization, if present, must not falsely imply durable success or silently reverse the committed local preference. No confirmation dialog is needed for this reversible preference. State must remain perceivable without color. [Toggles — Best practices](https://developer.apple.com/design/human-interface-guidelines/toggles#Best-practices).

```text
departureGroup(id):                    // structure only, not an extra stop
  summary(id + '/summary'):
    name = destinationAndQualifiers
    value = compose(platform, currentDeparturePhrase, currentStatus)
    role = staticText
    children = merged; automaticSpeech = none
  favorite(id + '/favorite'):
    name = 'Favorite, ' + favoriteScope(favoriteKey)
    role = switch; state = committedFavorites[favoriteKey]
    activate = commitInverseOrRetainStateAndExposeError

onTick(now): updateValues(now); preserveFocus(); doNotAnnounce()
onFeed(transaction):
  reconcileByStableID(transaction)
  preserveFocusOrApplyRemovalFallback()
  queueOnlyRelevantMaterialChangesAfterSpeech()
```

The pseudocode names required behavior, not SDK symbols or an assumption that any framework provides these flags directly.

## Worked before/after

Illustrative data, not additional evidence: Central, platform 4, 3 minutes, delayed; Airport, platform 2, 8 minutes, on time. Central is initially not a favorite.

**Before (possible sequence consistent with the brief):** “3” → “Star” → “Delayed” → “Central” → “4”; a second passes and countdown speech interrupts. Actual utterances and random ordering have not been recorded. A rider cannot reliably associate values or identify the star’s outcome.

**After (semantic content; actual role phrasing varies by VoiceOver settings):**

1. “Departures,” heading.
2. “Central. Platform 4. Departs in 3 minutes. Delayed.”
3. “Favorite, Central. Off,” switch.
4. “Airport. Platform 2. Departs in 8 minutes. On time.”
5. “Favorite, Airport. Off,” switch.

The rider reaches Central’s summary, learns the platform and delay in one stop, moves to its favorite, and activates it. Focus remains there and the state becomes On. Countdown ticks do not interrupt that feedback. Returning to Central’s summary reads the current estimate. If Central’s platform then changes to 6 while its summary is focused, finish the current speech and deliver one concise platform update. The next summary visit also says platform 6. Heading rotor navigation returns to “Departures”; it does not land on decorative stars.

## Acceptance checks and current status

**Passed — static specification inspection:** the contract names all four supplied data fields, defines a stable order, separates the favorite from merged text, specifies both favorite directions and failure, and excludes ticks from speech. It provides empty/removed/reordered/duplicate-destination handling. These are document checks only.

**Failed — supplied baseline against this contract:** the described unlabeled/random elements fail meaningful grouping and order; “Star” fails action/state identification; second-by-second interruptions fail the proposed speech policy. These failures are based solely on `interface.md`, not execution.

**Not executed — implementation and iPhone acceptance:**

| Check | Required observable result |
| --- | --- |
| Sequential nonvisual traversal, including multiple rows | Exactly one summary and one favorite stop per departure; all values belong to the correct row; reverse traversal is coherent |
| Heading rotor and direct touch exploration | Page/real section headings available; no artificial row headings; favorite independently discoverable and operable |
| Repeated ticks while speaking, then revisit summary | Speech completes without tick interruptions or focus changes; revisited value is current, including crossing minute/zero boundaries |
| Material update burst and superseded event | One relevant, noninterrupting notification; current platform/status available; no stale queued message or off-focus chatter |
| Favorite on → off, persistence failure and retry | Correct service changes once per activation; truthful committed state; focus stays; visible and spoken state agree; failure recoverable |
| Insertion, reorder, focused removal and empty list | Stable focus where possible, specified fallback otherwise; no focus transfer to a different favorite; empty message reachable |
| Long/recycled list and duplicate destinations | Every supplied item reachable and distinguishable; recycled nodes retain correct identities and actions |
| Missing prediction/platform/status; cancellation; stale feed | No invented certainty, negative countdown, or contradictory cancellation/time; data-loss state perceivable |
| Narrow iPhone layout and 200% text, noncolor state | Essential text/actions remain available, targets do not overlap; favorite selectable region at least 44 × 44 pt |

Run those checks on an eventual iPhone implementation with VoiceOver and relevant accessibility inspection; verify framework-specific notification behavior there. No device, SDK, GUI, accessibility tool, build, or runtime test was available or executed for this work. Physical transit data can become outdated; this specification cannot guarantee boarding accuracy.

## Source and evidence limits

Only `interface.md` and the installed local apple-hig package were used. The installed root was read, the topic index searched, then owning families and topic procedures were read before their supporting guides: Foundations/Accessibility; Technologies/VoiceOver; Layout and organization/Lists and tables; Menus and actions/Buttons; Selection and input/Toggles. The buttons route led to toggles for persistent favorite state. Sources are the package’s dated application-guidance snapshots, not SDK documentation or independently validated device behavior. Official URLs above identify the cited guidance; they were not browsed. No screenshot or implementation established geometry, actual semantics, locale output, or current runtime support. Notification timing, favorite scope, and focus fallback require implementation validation; the exact contract choices are recommendations for this product, not universal Apple mandates.
