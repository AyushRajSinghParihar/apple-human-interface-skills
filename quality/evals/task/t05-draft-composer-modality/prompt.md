---
description: Repair a modal draft composer for iPhone and iPad.
tags: [task]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

Fix the state specification of our draft composer. The same flow runs on iPhone and iPad. Keep unfinished writing safe and stop the stacked presentations. Give me the revised specification, a before and after, and acceptance checks.

- States: browse, then a composer sheet, then an attachment modal, then a settings modal.
- The composer has no title.
- The only exit is a downward swipe.
- Any swipe or Done deletes the unsaved draft without a warning.
- Tapping an upload error can open two alerts at the same time.
- There is no back action inside the attachment flow.
