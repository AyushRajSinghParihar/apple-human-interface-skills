Use a system confirmation alert with this specification:

- **Title:** “Delete shared album ‘[Album Name]’?”
- **Message:** Briefly explain the actual consequences, including the effect on other participants and whether deletion can be undone.
- **Accessory view:** Album thumbnails, if useful for identifying the album; **maximum height 154 pt** and **corner radius 16 pt**.
- **Shared Space:** Present slightly in front of the album window along the z-axis. Keep the alert anchored to that window as it moves.
- **Full Space:** Present centered in the person’s field of view.
- **Buttons:** **Delete Album** and **Cancel**. Place Delete Album on the trailing side of a row or at the top of a stack; Cancel goes on the leading side or at the bottom. Since the person explicitly initiated deletion, don’t automatically apply destructive styling. If they need to read the consequences before proceeding, leave both buttons without default status.

These corrections follow [Apple’s alert guidelines](https://developer.apple.com/design/human-interface-guidelines/alerts).