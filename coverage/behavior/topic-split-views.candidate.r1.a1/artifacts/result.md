# Adaptive iPad mail archive interaction specification

## Scope and decisions

The supplied `interface.md` reports an always-visible three-column iPadOS interface that leaves 70 pt for the message, loses selection when a column hides, and sometimes sends Back to account settings. This revision specifies mailbox → message list → message detail as one hierarchy. It is a framework-agnostic design contract, not an SDK implementation. “Archive” means the mail browsing workspace; moving or deleting mail is outside the supplied brief.

1. **Adapt visibility, preserve identity.** Use three coordinated panes when useful, two at intermediate widths, and one at compact widths. A hidden pane retains its selected object and scroll position. This follows [Split views — Best practices and iPadOS](https://developer.apple.com/design/human-interface-guidelines/split-views#Platform-considerations) and [iPadOS — Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados#Best-practices).
2. **Keep the mailbox sidebar.** Accounts group mailboxes in at most two visible levels; selecting a mailbox populates the middle list, selecting a message populates detail. Tabs were considered but would flatten a parent/child mailbox relationship and consume content space without solving the detail route. Hide the sidebar before sacrificing reading width; retain a visible restoration control and leading-edge swipe restoration. See [Sidebars — Best practices](https://developer.apple.com/design/human-interface-guidelines/sidebars#Best-practices). This hierarchy and rejection of tabs are product decisions, not universal HIG requirements.
3. **Back means parent.** It traverses message → mailbox message list → mailboxes, never settings. A sidebar restoration control changes visibility; it is not Back. Account Settings is an explicitly labeled separate destination. See [Toolbars — Navigation and Item groupings](https://developer.apple.com/design/human-interface-guidelines/toolbars#Navigation).
4. **Retain selected-row feedback.** Visible mailbox and message rows remain highlighted while their content is current. Message rows show sender, subject and date; body text belongs in detail. See [Lists and tables — Best practices and Content](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables#Best-practices).

## Layout contract

Let W be the available content width in logical points after safe-region insets. Pane widths include their own padding. For an initial implementation use mailbox minimum 240 pt, list minimum 300 pt, detail minimum 360 pt, and two 1 pt separators. These are **proposed product values**, not Apple-prescribed iPad dimensions; tune them with representative messages and text settings.

| Mode | Initial fit rule | Visible content | Context and restoration |
|---|---|---|---|
| Wide | W ≥ 902 pt and all three panes fit | Mailboxes 240 pt; list 300 pt; detail receives remainder | Both parent selections remain visible. “Hide Mailboxes” can opt into two panes. |
| Intermediate | 661 ≤ W < 902 pt, or sidebar manually hidden | List 300 pt; detail receives remainder | Leading “Show Mailboxes” reveals the mailbox view, replacing the list temporarily while retaining detail. “Messages” restores the list without changing selection. |
| Compact | W < 661 pt, or environment reports compact width, or two panes cannot fit | One full-width hierarchy level | Detail Back returns to the selected mailbox's list; list Back returns to Mailboxes. |

Use the least dense arrangement required by fit and environmental constraints; compact width overrides numeric fit. Determine fit again when text metrics, localization, safe regions, or controls change. Increase pane minima if necessary and collapse earlier. No rule shrinks detail to a 70 pt sliver. Below 360 pt, the single view uses all available width and reflows; the minimum is a multipane fit criterion, not a promise to lock the window width. Avoid a transient blank detail or horizontal page clipping during resizing.

In intermediate mode, Mailboxes and Messages are alternate leading panes, not a modal sheet. Selecting a mailbox restores the message list. Its detail becomes the remembered message for that mailbox if still valid, otherwise “Select a message.” When Mailboxes is showing, its leading “Messages” restoration control returns to the prior list even without a new selection. Leading-edge swipe shows Mailboxes; explicit controls remain available without gestures.

In wide mode “Show Mailboxes” restores three panes when they fit. A manual hide preference persists while wide; automatic collapse does not set that preference. Expansion therefore restores automatically hidden panes but respects deliberate hiding. Intermediate and compact modes always retain their explicit navigation routes.

Keep essential content and navigation inside safe regions. Rows grow and wrap when text requires it; detail body reflows with vertical scrolling. Preserve long sender/subject information in full in detail. Available width and text fit, rather than orientation or an iPad model name, determine arrangement. See [Layout — Adaptability, Size classes, and Guides and safe areas](https://developer.apple.com/design/human-interface-guidelines/layout#Adaptability).

## State and transitions

Store stable IDs independently of view instances:

```text
Workspace:
  selectedMailboxID
  rememberedMessageID[mailboxID]   // nullable; scoped to its mailbox
  routeLevel = mailboxes | messages | detail
  listAnchor[mailboxID]            // stable row ID + offset
  detailAnchor[messageID]
  wideSidebarHiddenByUser
  intermediateLeading = messages | mailboxes

resize(environment):
  save visible scroll anchors
  mode = chooseLeastDenseRequiredMode(environment, measuredPaneMinima)
  render projection(mode, routeLevel, selection, visibilityPreferences)
  // No selection mutation, navigation push, or settings navigation.

selectMailbox(id):
  save current anchors
  selectedMailboxID = id
  restore valid rememberedMessageID[id], else null
  routeLevel = messages
  intermediateLeading = messages

selectMessage(id):
  require id belongs to selectedMailboxID
  rememberedMessageID[selectedMailboxID] = id
  routeLevel = detail

back():
  if routeLevel == detail: routeLevel = messages
  else if routeLevel == messages: routeLevel = mailboxes
  else: no hierarchical Back is shown
  // Retain both selection IDs and anchors.
```

Projection rules: compact shows `routeLevel`. Wide shows all three panes unless deliberately hidden; intermediate normally shows messages + detail. Entering `mailboxes` reveals the mailbox pane in either wider mode. In wide mode selecting a mailbox leaves all panes visible; in intermediate mode it restores list + detail. A detail Back control is shown only when its parent list is hidden; a message-list Back control is shown only when Mailboxes is hidden. When parents are already visible, use their rows directly. Collapse after opening a message shows detail; collapse after Back to Messages shows messages, even though the remembered message remains selected. Expanding never manufactures a new navigation entry.

The list heading names the mailbox and account, disambiguating identical mailbox names. Detail shows its subject and mailbox/account context when the parents are hidden. Leading navigation controls have recognizable Back/sidebar appearances and destination-specific accessible names such as “Back to Archive messages.” Reserve their space before titles; truncate a title before hiding navigation. Account Settings must be reached through its own labeled entry and retain a return snapshot; returning restores the workspace, rather than adding settings to the mailbox hierarchy. Its internal settings design is out of scope.

Empty mailbox: show “No messages” in the list and neutral detail; do not invent a selected message. No selected mailbox: prompt “Choose a mailbox.” A loading/error detail stays tied to its requested message ID, with loading/error text and retry on failure; an outdated asynchronous response must not replace a newer selection. If a selected message disappears externally, clear only that invalid message ID and show “Message no longer available”; preserve mailbox and list anchor using the nearest surviving row. If a mailbox disappears, clear its invalid child selection and return to Mailboxes. Resizing alone never triggers either invalidation rule.

Touch tap and pointer click activate the same rows and controls; no essential route depends on hover. Existing platform keyboard activation must invoke the same transitions. No new shortcuts, drag/drop, editing mode, search, or mail mutations are introduced by this revision. Keyboard traversal and assistive behavior require implementation validation.

## Worked before/after

Example fixture, not observed execution: Work account → Archive → message M42 (“Quarterly review”), list anchored on M40, body at paragraph 6.

**Before, per brief:** three columns remain visible in compact width, leaving 70 pt for the body. Hiding a column loses selection. Back can open account settings.

**After, specified trace:**

1. At W = 1100 pt, show 240 / 300 / 558 pt panes with two 1 pt separators. Archive and M42 are highlighted.
2. Resize to 800 pt: show list 300 pt and detail 499 pt. M42 and paragraph 6 survive. “Show Mailboxes” reveals Archive selected; “Messages” restores the same list anchor.
3. Resize to 500 pt while reading: show M42 full-width, with mailbox/account context. Back returns to Archive's message list at M40, with M42 still selected. Back again shows Mailboxes with Archive selected. Neither step enters settings.
4. Select Archive, then M42: restore paragraph 6. Expand to 1100 pt: restore three panes and both selections, without changing the navigation history. If Mailboxes had been manually hidden at wide width, retain two panes with a visible restoration control.

## Acceptance checks and status

The following are executable acceptance scenarios for the eventual implementation. “Not executed” is deliberate: a specification cannot establish runtime results.

| Check | Required result | Status |
|---|---|---|
| Resize 1100 → 800 → 500 → 1100 with M42 open | Same mailbox/message IDs and anchors; 3 → 2 → 1 → 3 panes | Not executed |
| Cross 660/661 and 901/902 pt in both directions | Correct fit, no clipped controls, selection loss, duplicate route entries, or blank flash | Not executed |
| Back twice at 500 pt | Detail → messages → Mailboxes; settings never opens | Not executed |
| Collapse while route is Messages after Back | Messages stays foreground; remembered detail does not force itself open | Not executed |
| Hide/restore sidebar manually; then resize | Restore control and edge gesture reach every mailbox; deliberate hide is respected on expansion | Not executed |
| Choose different mailbox with/without remembered message | Correct parent/detail relationship or neutral placeholder; no stale message from previous mailbox | Not executed |
| Empty/long mailbox, long identifiers, message removed, delayed loading responses | All expected rows reachable; no misleading selection or wrong detail identity | Not executed |
| Larger text, long localized labels, short window and narrow single pane | Earlier collapse/reflow as needed; controls reachable, safe regions respected | Not executed |
| Touch, pointer, keyboard and assistive traversal | Equivalent routes, meaningful control names, visible selection, no focus stranded in hidden panes | Not executed |

**Passed — static specification review:** all three supplied problems have explicit replacement rules; wide/intermediate/compact states and hidden-pane restoration are defined; resize does not mutate selection; the worked width arithmetic meets the proposed minima; Back has no transition to settings. Root, selected families, topic procedures and supporting guides were read locally in that order, with each file read by its own command.

**Failed — supplied baseline only:** `interface.md` reports cramped detail, lost selection and incorrect Back routing. These are reported defects, not independently reproduced failures. No revised runtime check has been marked passed or failed.

## Evidence limits

Only `interface.md` and the installed skill package informed this design. Read routes: Getting started → Designing for iPadOS; Layout and organization → Split views and Lists and tables; Navigation and search → Sidebars; Foundations → Layout; Menus and actions → Toolbars. The topic index was searched before finalizing the route. Each procedure preceded its supporting reference. No screenshot-specific media route applied because no screenshot or animation was supplied.

Official links above identify the articles/sections attributed by the local snapshot; they were not opened or checked on the web. The package describes itself as independent application guidance based on a dated English HIG snapshot (2026-10-25), not a verbatim manual or SDK reference. No conflicting rule was found in the selected local guides. Guidance about macOS dividers, menu parity, or other platforms was not promoted into iPad requirements.

No source implementation, representative mailbox dataset, device, Apple SDK, rendered GUI, physical gesture, keyboard/focus runtime, or accessibility execution was available or performed. Proposed minima, text fit, selection styling and scroll restoration remain to be validated. SDK support, native rendering, physical comfort, contrast and assistive traversal are not established by this document. The specification requires no Apple framework and makes no compilation claim.
