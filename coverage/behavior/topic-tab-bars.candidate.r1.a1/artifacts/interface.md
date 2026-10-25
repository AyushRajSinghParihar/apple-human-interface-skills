# iPhone museum app: primary navigation

Platform: iOS on iPhone. Use standard iOS tab/navigation components in the existing framework, with the supported OS's system appearance. No framework or deployment target was supplied.

## Persistent destinations

Use two bottom tabs in fixed logical order. Collections is established by the brief; Visit and the content ownership below are explicit product assumptions adopted to make this revision concrete.

| Order | Label/icon concept | Content | State retained independently |
|---|---|---|---|
| 1 | Collections / collection-stack symbol | Museum collections and objects, including user-created collections | Navigation path by stable IDs, selected collection/object, scroll anchors and offsets at each level |
| 2 | Visit / map symbol | Museum visit information | Navigation path by stable IDs and scroll anchors/offsets at each level |

First launch selects Collections. Switching tabs restores each tab's navigation depth, selection and scroll position for the current session. Reselecting the active tab leaves context intact. Cross-launch persistence is outside this repair's guarantee. Tabs never execute commands or reorder based on usage. No More destination or badges are needed.

Keep both tabs visible and enabled through root/detail navigation, loading, refresh, empty, offline and error states. Temporary modals may cover the bar; dismissal restores the prior destination and context. Do not implement app-driven scroll minimization or automatic tab switching.

Loading affects destination content only: retain cached content when available, otherwise show an inline loading explanation. Empty Collections says “No collections available.” Empty Visit says “Visit information is unavailable.” Loading failure shows an inline explanation and Retry. Retry reloads that destination without clearing its context or blocking the other tab. Late responses must not steal the current tab selection.

Restore scroll after layout using stable content anchors and offsets. If an anchor disappears, use the nearest surviving neighbor and clamp its offset. If a selected item disappears, return to the nearest surviving parent with an inline explanation; do not reset the whole destination.

## Current-content commands

Share and Delete are commands, never tabs. Keep standard Back at the leading top edge and title each view with its content name. Back pops one level within the active tab; it does not switch tabs.

On loaded, shareable detail content, place Share in the trailing top toolbar with accessible name “Share”. It opens the app's sharing flow for that exact item. Completion or cancellation restores the same detail and scroll position. Until shareable content exists, Share is unavailable and the content area explains loading/error state.

Assumption: Delete applies only to a user-created collection, never museum-owned catalog objects. Place a labeled “Delete Collection” destructive button at the end of that collection's detail content, separated from Share. It remains reachable by scrolling at narrow widths and enlarged text sizes; it is not a prominent primary action.

For this specification deletion is irreversible. Delete Collection opens a standard confirmation alert: title “Delete Collection?”, message “This permanently deletes ‘{name}’. Museum objects are not deleted.” Provide Delete (destructive role) and Cancel (cancel role), with no default. Use adaptive system ordering: Delete trailing in a row or first in a stack; Cancel leading or last respectively. Return without explicitly focused action must not delete. Cancel and supported keyboard dismissal preserve data and restore the triggering control. Choosing no default is a product safeguard, not a universal HIG restriction on destructive defaults.

After explicit confirmation, prevent duplicate requests and show pending status in the initiating control. Success returns to the parent list, preserves its surviving scroll anchor, and clears only references to the deleted collection. Failure retains detail and shows inline failure with Retry. Tabs remain available during the request; completion must not navigate away from a different tab the person has since selected. If Assistive Access is supported, provide its two confirmations for difficult-to-reverse deletion.

## Selection and access

Every tab has a persistent short label and scalable recognizable icon. Use a visible enclosing shape/selection indicator as well as tint, with semantic selected state. Prefer system selection styling where it supplies this distinction. Selection must remain identifiable in grayscale.

Expose destination names, tab roles and selected state, plus action names and button roles. Provide iPhone activation regions of at least 44 × 44 pt without overlap. Preserve all destinations and essential actions at text enlargement of at least 200%. Test narrow supported widths and long localized labels without clipping essential text; retain stable logical tab order. Use adaptive system colors and check light, dark and Increase Contrast appearances. Color alone must not communicate selection or destruction.

## Acceptance contract

1. Collections → scroll → open item → Visit → Collections restores the item, navigation depth and scroll context. Repeat in both directions; reselecting the current tab does not reset it.
2. Exercise loading, refresh, empty, offline and error states in each destination. Both tabs stay visible, enabled and ordered; Retry and late responses do not clear state or steal selection.
3. Share then cancel/complete returns to the same item and scroll position. Share/Delete never appear as tabs. Back and all commands remain reachable at narrow width and enlarged text.
4. Delete cancellation and keyboard dismissal preserve data; unfocused Return does not commit; explicit Delete commits once. Exercise pending, failure and success while switching tabs. Only deleted-item references are invalidated.
5. Remove a retained item during refresh: restore the nearest surviving parent/anchor with an explanation. Delete the last collection: Collections stays available with its empty state.
6. Verify non-color selection in grayscale, readable localized/enlarged labels, target geometry and measured contrast in supported appearances. On an Apple environment verify semantic names, roles, selected state and complete activation paths with assistive input and keyboard navigation.

## Guidance basis

Stable destinations and retained state follow [Tab bars — Best practices](https://developer.apple.com/design/human-interface-guidelines/tab-bars#Best-practices). Command placement and Back follow [Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars). Action semantics and targets follow [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons). Non-color selection and access checks follow [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility). Irreversible confirmation and cancellation follow [Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts). Decisions use the installed local snapshot; these official attribution links were not browsed.
