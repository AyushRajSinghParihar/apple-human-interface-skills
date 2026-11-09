# Transient formatting palette — revised specification

Platforms: iPadOS and iOS. The palette edits formatting for the current document selection. It remains a short contextual task; it is not a persistent inspector. No framework or deployment version is specified.

## Presentation and layout

- A Format control opens the palette and captures the selected content as its editing target. Keep that target stable while using palette controls.
- In a regular-width environment with sufficient space, present one content-sized popover. Anchor its arrow directly to the visible Format control's bounds, updating the anchor as the window changes. Keep the control and essential selected-content reference visible; never point into empty space.
- Show primary formatting choices together. Reveal secondary formatting options inside the same surface with disclosure and an internal detail view. Back returns to the primary choices without saving, discarding, or closing. Never cascade a second popover. Animate content-size changes as one continuing surface.
- In compact width, use a modal sheet occupying the available width instead of tiny floating geometry. Start expanded at the large detent, with a scrollable body and fixed, reachable completion controls. Use standard centered sheet sizing on iPad when this fallback is needed. Do not offer a medium detent in this initial specification; therefore no resize grabber is needed.
- Select the surface from the current size class and usable space, not the device name. If a regular-width popover cannot fit its content while retaining the anchor and essential reference, use the sheet fallback. Keep controls inside safe areas; wrap/stack content rather than shrinking it. Short heights and enlarged text must retain access to every choice and completion action through scrolling.
- Resize or rotation transfers the active session between surfaces without a second presentation, commit, rollback, or reset. Preserve target, selected choices, draft, internal route, and scroll position where applicable. If the source control becomes unavailable, use the sheet rather than retain a detached arrow.

## Editing and exits

Maintain an opening baseline, a working formatting draft, and a stable target. Choices update a preview of that draft on the target; a preview is not yet a document commit. Each choice stays selected visibly. Both single and multiple choices leave the palette open so people can make a sequence of adjustments.

| Event | Required outcome |
|---|---|
| Done | Commit the draft to the target, dismiss, and return focus to Format. |
| Cancel | Explicitly discard this session's draft, restore the baseline preview, dismiss, and return focus to Format. Previously committed changes remain intact. |
| Tap outside wide popover | Commit the draft before dismissing. Never discard work. The dismissing tap must not also edit underlying document content. |
| Activate another contextual popover trigger | Commit and close the current popover, then open the replacement in the same activation. At most one popover is visible. |
| Back within detail options | Return within the same palette; retain all draft choices. |
| Tap outside compact modal sheet | No dismissal or parent interaction. |
| Swipe down to dismiss compact sheet | Commit the draft before dismissal. This task has no unsaved draft after automatic dismissal; never interpret the gesture as Cancel. |
| Other automatic dismissal, including Escape if supported | Commit before closing; only explicit Cancel discards. |
| App interruption | Retain session state and preview for resumption; do not treat backgrounding as Cancel. If the session must close, commit first. |
| Width/orientation change | Transfer the session as described above; no exit semantics. |

At the root, show leading Cancel and trailing Done; these clarify rollback versus commit. In detail views show Back and Done, without a simultaneous Cancel. Returning to the root exposes Cancel again. Done works from either route. On dismissal restore editor selection and focus to Format unless a replacement control deliberately takes focus.

Compact parent content is unavailable for editing while the modal sheet is open. On wide layouts the palette must not hide essential preview context. Changes committed by Done or automatic dismissal form one undoable formatting operation per session (product decision). If persistence fails, retain the draft and show an explicit failure state with retry; never silently dismiss or claim it was saved.

## Guidance basis

These are local design decisions informed by the installed HIG snapshot, not verified SDK behavior. Anchoring, no cascades, retaining multi-selection, saving on automatic dismissal, and compact adaptation follow [Popovers — Best practices and iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/popovers). Sheet sizing and action placement follow [Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets). Saving on sheet swipe is a deliberate adaptation of the palette's automatic-save contract: there is no pending unsaved work to discard after that exit. [Layout — Adaptability and Size classes](https://developer.apple.com/design/human-interface-guidelines/layout) supports environment-based adaptation and state preservation. Platform context follows [Designing for iPadOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados) and [Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios).
