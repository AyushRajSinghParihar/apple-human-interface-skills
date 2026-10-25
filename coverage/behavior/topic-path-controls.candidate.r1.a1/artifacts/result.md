# Mac archive path-control review

Decision: revise the contract before implementation. Ancestor activation must navigate without deleting anything. Use a standard, noneditable path control with recognizable icon/name segments and recoverable ancestry. This is a framework-agnostic specification, not SDK code.

## Evidence and route

The entire supplied interface is the one-paragraph `interface.md`: macOS; cryptic database IDs only; ancestor clicks delete intervening folders; items do not identify hierarchy; long paths truncate the current item while preserving the root in full; files may be unavailable. These are reported behaviors, not independently executed observations.

Read from the installed `.agents/skills/apple-hig/` package, in route order: root `SKILL.md`; navigation-and-search family; relevant `references/topic-index.md` rows; `.topics/apple-hig-path-controls/SKILL.md` under that family; then `references/path-controls.md`. For preservation and unavailable-file handling, also read the patterns family, file-management index row, its file-management topic procedure, and supporting guide. Each file was read with its own command. No web sources were fetched.

Source keys below link to the official articles identified in those local snapshots:

- **P:** [Path controls](https://developer.apple.com/design/human-interface-guidelines/path-controls), including [Best practices](https://developer.apple.com/design/human-interface-guidelines/path-controls#Best-practices). The local guide describes root/parent/item icon/name segments, hiding intermediate names under width pressure, pop-up ancestry, and body placement.
- **F:** [File management — Saving work](https://developer.apple.com/design/human-interface-guidelines/file-management#Saving-work). Preserve work unless explicitly canceled or deleted. The local topic also calls for preserving identity and avoiding false saved state; this is supporting application advice, not a path-control-specific deletion rule.

## Ranked verified findings

“Verified” here means explicitly established by the supplied brief. Severity is this review's judgment.

| Rank | Finding and consequence | Correction and basis |
|---|---|---|
| 1 — Critical | Clicking an ancestor deletes intervening folders. Ordinary navigation can destroy archive contents. | Navigate to the ancestor without filesystem or database deletion. Keep folder identities and descendants intact. P defines location presentation/navigation; F supports preservation absent explicit deletion. Removing segments from the displayed trail is allowed when changing location; deleting the represented folders is not. |
| 2 — High | Only cryptic database IDs are displayed. People cannot recognize their location or reliably choose an ancestor. | Resolve IDs to user-facing folder/file names, keeping IDs internal for identity. P specifies icon/name segments. If metadata is unavailable, show an honest fallback rather than inventing a filename. |
| 3 — High | Path items do not identify hierarchy. People cannot distinguish root, parents, and the current item. | Present ordered root → ancestors → current item, with distinguishable segments and file/folder icons. P describes this structure. Separators are structural and never actionable. |
| 4 — Medium | Long paths sacrifice the current item while displaying the root in full. The most relevant location becomes difficult to identify. | Hide intermediate names first and expose hidden ancestry on demand; prioritize the current item's name. P explicitly describes intermediate-name hiding; current-name priority and recoverable overflow are the local topic's application advice. Full root text is not a priority at the expense of the current item. |

## Decisions and corrected contract

1. **Purpose and placement.** Treat the control as a location display with ancestor navigation, not a destination editor. Place it in the window body (P). Placement is unspecified in the brief, so this is a requirement, not a verified placement violation. No Choose action or path-changing drops in this mode. If later made editable, re-review supported locations and validation; P describes drop support for editable controls and Choose for editable pop-ups.
2. **Data.** Resolve each segment as `{stableID, parentID, displayName, kind, availability}`. The displayed chain must correspond to the actual current location. Use real filesystem names when representing filesystem locations. Whether archive IDs actually map to filesystem objects is unknown; if they represent only a virtual taxonomy, label it as an archive hierarchy and do not claim native filesystem-path semantics. The naming and identity rules still apply.
3. **Width.** Keep the current item visible; collapse intermediate segments into an ancestry affordance before shortening the root. Opening the affordance reveals the full ordered hierarchy with full names and stable targets. At extremely narrow widths, use the P-described pop-up form showing the current item, with full hierarchy on opening; if even its name cannot fit, elide it visually while retaining the full name in the opened presentation. No fabricated minimum width is prescribed.
4. **Unavailable items — proposed product policy.** Retain last-known identity, name, and path, qualified as unavailable; do not imply the location still resolves. Revalidate a target before navigating. If it cannot be resolved, keep the current selection and contents, explain that the location is unavailable, and permit retry or navigation to a resolvable ancestor. Do not silently substitute another path, delete missing entries, or create folders. This recovery policy is a design choice informed by the topic's stale-location checks, not a quoted Apple requirement. The brief establishes possibility of unavailability, not existing failure behavior.

### Transition pseudocode

```text
activateSegment(targetID):
    assert targetID belongs to the displayed chain or revealed ancestry
    previous = currentLocation
    outcome = resolveLocation(targetID)  // may complete asynchronously
    if this request is no longer the latest navigation request: return
    if outcome is unavailable or invalid:
        retain(previous, currentContents)
        presentUnavailable(targetID, retryAllowed=true)
        return
    currentLocation = outcome.location
    displayChain = ancestorsThrough(outcome.location)
    loadContents(outcome.location)
    // Navigation has no delete, move, or rename side effects.

resize(width):
    render currentLocation using full segments or recoverable compact ancestry
    // Never modify the location, stable IDs, or stored folders.
```

The transition policy, including stale-request handling, is proposed implementation guidance. No new delete command is specified by this review.

## Worked before/after

Illustrative names and IDs, not additional supplied evidence:

- Actual chain: `Archive [1] → Projects [28] → 2026 [903] → Spring [4172]`.
- Before: `1 → 28 → 903 → 41…`; activating `28` deletes the intervening folders as described in the brief.
- After at ordinary width: `Archive → Projects → 2026 → Spring`, with folder icons and clear segment boundaries. At narrow width: `Archive → … → Spring`; opening `…` reveals the hidden ancestors in order.
- Activate Projects: the control becomes `Archive → Projects`, and the contents view shows Projects. Both 2026 and Spring remain stored, retain their parent relationships, and can be revisited.
- If Projects becomes unavailable before activation completes: keep the prior location and contents, qualify the stale location, and show “Projects is unavailable. Try again.” No deletion occurs. A resolvable Archive ancestor remains navigable.

## Acceptance checks and status

**Passed — static review only:** platform and supplied behaviors identified; all four findings tied to explicit brief statements; installed root/family/topic/source sequence read; corrected contract covers identity, navigation, narrow width, and stale locations. These passes do not establish implementation compliance.

**Failed — supplied behavior against the contract:** destructive ancestor activation; ID-only labels; missing hierarchy; current-item truncation priority. These failures are specification-level observations from `interface.md`, not runtime test results.

**Not executed — implementation acceptance checks:**

| Scenario | Required observable result |
|---|---|
| Root only | One recognizable current/root item; activation does not mutate storage. |
| Deep path | Names and icons represent the exact ordered ancestry; duplicate names still target distinct stable IDs. |
| Ancestor activation | Location and contents change to that ancestor; before/after storage comparison shows no folder or relationship deletion. |
| Narrow, then wide | Current identity persists; hidden full ancestry remains reachable; expansion restores segments without changing location. |
| Unavailable current item or ancestor | Last-known identity is qualified; failed navigation preserves context; retry and resolvable ancestor navigation work. |
| Target disappears during resolution | No silent fallback or storage mutation; stale asynchronous results cannot override a newer request. |
| Editing routes | Choose is absent and drops cannot replace the location in the chosen noneditable mode. Editable Choose/drop selection tests are not applicable unless that decision changes. |
| Body placement and interaction | Control is in the window body; segment and overflow activation can be operated and identified with keyboard and assistive technology. This is a proposed usability check, not an accessibility compliance finding. |

## Evidence limits

No implementation, screenshots, archive model, layout dimensions, permissions, or unavailable-state flow were supplied. There is no evidence of device, GUI, SDK, filesystem durability, drag, keyboard, or accessibility execution. No Apple SDK is assumed or needed for this specification. Only the report was produced; the interface was not implemented. The installed references identify a 2026-10-25 snapshot; official links are attribution, not claims of live verification. No unsupported finding is made about toolbar placement, editability, accessibility, or existing unavailable-file recovery.
