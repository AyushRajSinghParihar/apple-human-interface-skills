---
description: Apple-quality settings page for a React web app.
tags: [task]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

We build a React web app, not a native Apple app, but we want our settings page to be as clear and polished as Apple's own apps. Please review it and tell me exactly what to change.

- One long page with 30 toggles in a single list, no groups or headings.
- Labels are grey placeholder text inside the inputs, and they disappear when the person types.
- Changes save only when the person presses a Save button at the very bottom. If they leave the page, the changes are lost without a warning.
- A custom toggle is a styled div that a mouse can click but the keyboard cannot reach.
- The designer wants to download Apple's SF Pro font files and SF Symbols and bundle them into our site.
