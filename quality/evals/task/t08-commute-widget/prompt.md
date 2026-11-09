---
description: Design a train-commute widget set for iPhone.
tags: [task]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

Design a useful train-commute widget set for the iPhone Home Screen and Lock Screen, and decide how delays and an active journey should update.

The current proposal:
- Every widget is the app logo plus a tiny list of stations.
- The inline Lock Screen accessory has three separate tap targets.
- The widget promises a refresh every second.
- Stale departures still say "Live".
- Signed-out people see a blank rectangle.
- The Home Screen widget must work in tinted mode, dark appearance and StandBy night mode.
- An active train journey can last 50 minutes.
