Use a native visionOS confirmation alert with this specification:

- **Trigger:** After the person chooses to delete a shared album, before deletion occurs.
- **Title:** `Delete “[Album Name]”?`
- **Message:** Briefly state the actual consequences for participants and photos, including whether deletion is reversible.
- **Accessory:** Album thumbnails in a view **no taller than 154 pt**, with a **16 pt corner radius**.
- **Shared Space:** Present slightly in front of the album’s parent window. Keep the alert attached as the window moves.
- **Full Space:** Present centered in the person’s field of view.
- **Buttons:** **Delete Album** and **Cancel**. Cancel dismisses without changes; Delete Album performs deletion. Place Delete Album trailing in a row or first in a stack.
- **Default behavior:** Because this confirms explicitly requested deletion, Delete Album may be the normal default action; destructive styling isn’t automatically required. Consider no default if the consequences require deliberate reading. Support Escape and Command-Period cancellation with an attached keyboard.

Source: [Apple HIG — Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts).