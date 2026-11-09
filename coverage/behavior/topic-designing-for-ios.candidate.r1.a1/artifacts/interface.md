# iPhone maintenance task specification

Platform: iOS, handheld touch, often one free hand and intermittent connectivity. Primary flow: find a maintenance task → inspect instructions → record work → review and submit completion → return to the queue.

## Scope and data contract

The supplied desktop port has eight dense columns, hover-only row actions, a window for every detail, and a bottom action obscured by the home indicator. Replace that presentation with the flow below. No implementation framework or task schema was supplied; retain the existing stack.

Product assumptions for this specification: tasks have a stable ID, title, asset/location, priority, due date, status, instructions, and completion notes. These are proposed fields, not a recovered inventory of the eight columns. During implementation, map every existing column to either the summary or labeled detail fields; retain all original values and permissions. Retain every existing command through a visible labeled control on the relevant detail screen; inventory its consequences before assigning destructive behavior. Do not silently remove fields or commands to fit the phone. Completion records maintenance work; it does not operate machinery.

## Screens and navigation

1. **Tasks** is the root, a single vertically scrolling navigation list. Show cached tasks immediately, plus “Last updated [date/time]” and a persistent connectivity/sync message when relevant. Each row shows title and ID first, asset/location next, then textual priority, due date and status. Use a disclosure indicator; tapping anywhere in the row opens that task, never completes it. Long instructions stay in detail. Preserve recognizable identifier ends if summary truncation is necessary; show the full ID in detail.
2. Initial queue contains assigned unfinished tasks, ordered by priority, then earliest due date, then ID; missing dates sort last within priority. A visible “All Tasks” navigation row opens all tasks the technician is authorized to see, including completed tasks. “Assigned Tasks” returns to the initial scope. Keep the active scope in the title. These scopes and ordering are product decisions. Do not interpret cached subsets as the entire server dataset; show “Available offline: [count] tasks” when incomplete. Online lists load further pages while scrolling, with an explicit “Load More” fallback and retry on page failure.
3. **Task detail** pushes onto the same navigation stack. Top: title, full ID, status, asset/location, priority, due date and data freshness. Then instructions and labeled remaining desktop fields. Below, visible text buttons expose task commands. “Record Work” is the prominent bottom action. Back and system swipe-back return to the same queue scope, order and scroll position. Additional read-only details push within this stack; do not open a separate window for each item.
4. **Record Work** pushes a task-specific screen with instructions, a labeled completion-notes input and “Review Completion.” Notes are optional under this proposed schema; preserve any actual existing required fields and validate them inline before review. Save edits durably on change, associated with task ID and server revision. Back keeps the draft. Show “Draft saved on this iPhone” only after local persistence succeeds; if it fails, retain the editor and state the error, with Retry. Do not silently discard edits.
5. **Review Completion** shows task identity, completion notes and an explicit statement: “Submit marks this task complete after the server accepts it.” “Back” returns to editing. “Submit Completion” commits this reviewed draft; no row tap or keyboard Return in the notes editor submits it. On acceptance, return to detail with persistent “Completed” and confirmation time. Back returns to the queue; the assigned unfinished queue removes the accepted task and anchors to its next neighbor. All Tasks retains it. If a task is removed remotely, retain its draft, show “Task unavailable,” and offer “Back to Tasks”; never switch edits to another task.

## Touch, layout and access

Use platform navigation, list, button and text-entry components where the existing stack permits. No required command depends on hover, long press, swipe, precise dragging, sound or color. Visible text labels identify actions; state text distinguishes priority, offline, pending and completed states.

Place each screen's single prominent action in a bottom container constrained above the current system safe area. Reserve scroll-content space equal to that container's measured height so the last field can scroll fully above it. Respect side/top safe areas, home indicator, bars and keyboard; move the action above the keyboard or into reachable scroll content when vertical room is insufficient. Never use a fixed screen-bottom coordinate. Keep a visible Back control alongside system swipe-back; do not override the edge gesture.

Use activation regions at least 44 × 44 pt for this product's iPhone controls, with nonoverlapping targets and visible separation. This adopts the normal iOS target rather than the smaller accessibility reference minimum. Prefer broad, full-width primary actions in the lower display, subject to device validation for one-handed reach.

Use semantic system title, headline and body styles (body is 17 pt at the default iOS size). Support Dynamic Type through the largest accessibility sizes and at least 200% enlargement, plus Bold Text. Grow rows, wrap essential labels, and stack metadata rather than shrink fonts. Use the same navigation in portrait and landscape; adapt to available width/height. At large text or short height, allow the bottom action to participate in scrolling so it cannot consume the whole viewport. Preserve the task, draft and reading position across resizing.

Use semantic appearance-adaptive colors and explicit status words. Verify actual contrast in light/dark appearances and Increase Contrast; no contrast pass is implied by selecting system colors. Expose control names matching visible labels, roles and current states; task identity must remain available to assistive input. Test the entire flow with assistive navigation before claiming support.

## Connectivity and completion states

| State | Visible behavior and transition |
|---|---|
| Initial load, no cache | Show task-list structure and “Loading tasks”; if loading fails, show “Tasks unavailable” with Retry. Distinguish this from a successful empty queue (“No assigned unfinished tasks,” with All Tasks). |
| Refresh with cache | Keep cached content and drafts usable while refreshing. Show freshness and “Updating”; failure leaves content with “Couldn’t update” and Retry. Missing uncached instructions say “Connect to load instructions.” Do not present a placeholder as an instruction. |
| Editing offline | Cached instructions remain readable. Notes persist locally; show “Offline — draft saved on this iPhone.” Review remains available. |
| Submit offline | Button reads “Save Completion for Sync.” Activation durably stores the reviewed payload and unique operation ID, then shows “Pending sync — task is not yet confirmed complete.” Keep it in the unfinished queue with this label. Local write failure leaves the draft and Retry; it does not show pending success. |
| Sending | Online Submit, queued retry or reconnect sends the same operation ID and base revision. Show “Submitting” with activity indication in the initiating button; prevent duplicate activation for that operation. Other tasks remain usable. Reconnection retries pending operations while the app can execute; do not promise immediate background delivery. |
| Acknowledged | Only server acceptance changes confirmed status to Completed. Persist the receipt and remove the pending operation atomically. A lost response triggers reconciliation/retry with the same ID, never a second completion. |
| Retryable failure | Keep the payload and operation ID. Show “Not confirmed — Retry” on detail and in the queue; allow manual Retry. No endless blocking spinner. |
| Conflict or permission change | Stop automatic retry. Show “Needs review,” current server status and preserved submitted notes. If already completed, reconcile the receipt/status without creating another completion. Otherwise “Review Changes” opens current details beside labeled saved notes in a vertical layout; an authorized new submission requires explicit review against the latest revision. Never overwrite newer server work silently. |

Once queued, the submitted payload is locked while its outcome is unknown; details remain readable. Further completion editing becomes available only after rejection/reconciliation resolves the operation. Pending work must survive termination. On resume, restore the selected task, route, draft, queue scope and scroll position; reconcile network state without resetting the screen. A locally saved draft or pending sync is never labeled server-completed.

## Implementation gates

The completion API must support stable operation IDs, revision checks and receipt reconciliation before queued completion is enabled. If it cannot, ship offline draft saving only, label the action “Connect to Submit,” and explain that completion requires a connection. This fallback preserves work without claiming reliable offline submission. Cache availability, retention and authorization must follow existing product policy; no cache coverage or offline capability is established by this document.

Acceptance scenarios and source rationale are recorded in result.md. This is an implementable design contract, not executable UI or verified SDK code.
