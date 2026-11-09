---
description: Audit the alerts of a Mac research archive app.
tags: [task]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

Audit the alerts in our Mac research archive app. Rank the problems you can verify from this description and show the corrected behavior. There is no screenshot or build.

- A routine successful save always shows an alert.
- The irreversible archive deletion alert is titled "Error" with the body "Something happened". Its buttons are Yes and No.
- The harmless save alert makes Cancel the default button.
- When sync fails, a second alert appears on top of the first one.
