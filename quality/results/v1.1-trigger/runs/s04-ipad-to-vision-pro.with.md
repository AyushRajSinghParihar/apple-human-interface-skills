Keep the thumbnail grid, but give navigation and controls their native visionOS presentation. Start with a movable window in Shared Space; ordinary photo browsing works well alongside other apps. ([Designing for visionOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos))

I’d adapt your layout this way:

| Current iPad design | Recommended Vision Pro design |
|---|---|
| Bottom tab bar | A native vertical tab bar at the window’s leading edge. Supply an SF Symbol and short label for each destination; the system reveals labels when the bar expands. |
| Thumbnail grid | A resizable grid with comfortably separated targets and system hover feedback. Adjust column count as the window changes size. |
| Actions mixed into navigation | Keep destinations in tabs; put actions on the current photo in a standard toolbar. |
| Photo detail | Open the selected photo in a large, focused view, with an explicit return that restores the grid’s scroll position and selection. |

The leading tab bar is the [visionOS convention](https://developer.apple.com/design/human-interface-guidelines/tab-bars). If an Albums tab needs deeper navigation, add a sidebar *inside that tab*.

Make each thumbnail one stable target. Looking should show hover feedback; looking and pinching should open it. Avoid tiny favorite or overflow buttons on every thumbnail—put those actions in the detail view or a selection toolbar. Apple’s [eye-input guidance](https://developer.apple.com/design/human-interface-guidelines/eyes) recommends generous target separation and keeping hover effects from interfering with neighboring targets.

For photo actions, prefer a system toolbar, which gets the platform’s ornament presentation. This keeps tools near the window without covering the image. If you hide controls during focused viewing, provide a clear way to restore them. ([Ornaments](https://developer.apple.com/design/human-interface-guidelines/ornaments))

Keep the grid and controls at a coherent depth. Let users position and resize the window, and support browsing with hands resting in their lap. A room full of floating thumbnails would make routine browsing require more scanning and movement. ([Spatial layout](https://developer.apple.com/design/human-interface-guidelines/spatial-layout))

For a first release, prioritize this flow: **choose a tab → browse → open a photo → act on it → return to the same place**. Treat immersive viewing as a later, deliberately chosen feature with a clear return path.

Validate on a worn Vision Pro: thumbnail targeting, narrow-window layouts, extended browsing comfort, and VoiceOver navigation. Those checks remain unverified from your description alone.