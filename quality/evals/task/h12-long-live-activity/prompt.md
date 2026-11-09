---
description: Design a Live Activity for a long bus trip.
tags: [task, hard]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

Design the Live Activity for our long-distance bus app and fix our current plan:

- The Live Activity starts at booking and runs for the whole 10-hour trip.
- It shows a promotional banner for hotel deals and uses the full app icon.
- After arrival it stays on the Lock Screen for 8 more hours with a summary.
- The compact trailing view shows "Arrives 14:35 · Gate 12 · On time", also when the Dynamic Island has only a limited width.
- The leading and trailing compact views open two different screens in the app.
- The custom layout has Check In and Seat Map buttons that we expect to work in CarPlay too.
