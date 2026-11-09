Use a standard visionOS confirmation alert with this specification:

- **Title:** “Delete shared album ‘[Album Name]’?”
- **Message:** Briefly explain the actual consequences, including effects on other participants and whether deletion can be undone.
- **Accessory view:** Show album thumbnails only if they help identify the album. Limit the view to **154 pt maximum height**, with a **16 pt corner radius**.
- **Shared Space placement:** Present slightly forward of the album window along the z-axis. Keep the alert anchored to that window as it moves.
- **Full Space placement:** Present centered in the wearer’s field of view.
- **Buttons:** **Delete Album**, using the destructive role, and **Cancel**, using the cancel role. Cancel dismisses without deleting.

These sizing and placement requirements follow [Apple’s alert guidelines](https://developer.apple.com/design/human-interface-guidelines/alerts).