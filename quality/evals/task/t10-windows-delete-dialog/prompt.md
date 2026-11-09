---
description: Apple-quality delete confirmation in a Windows app.
tags: [task]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

Our Windows desktop app (WinUI 3) should feel as clear as an Apple app. Review this delete confirmation and tell me what to change:

- When the person deletes a project (40 files, it cannot be undone), a ContentDialog says "Are you sure?" with the buttons Yes and No.
- Our designer wants to copy the macOS layout: Cancel on the left, Delete on the right, with Delete as the default button, so Enter deletes.
- Sometimes a second dialog opens on top of the first to show a sync warning.
