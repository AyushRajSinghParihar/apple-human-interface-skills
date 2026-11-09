---
description: Specify a visionOS alert with an accessory view.
tags: [task, hard]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

Specify the alert that our visionOS photo app shows before it deletes a shared album. The current design:

- The alert has an accessory view with album thumbnails. It is 220 pt tall with 8 pt rounded corners.
- In the Shared Space, the alert opens in the center of the room, away from the album window, and it stays there when the person moves the window.
- In a Full Space, the alert opens at the side of the person's view.
- The buttons are OK and Cancel.

Give me the corrected alert specification.
