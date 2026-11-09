---
description: Accessibility audit of an iPhone trip checkout.
tags: [task]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

Audit our iPhone trip checkout for accessibility, using only this specification. Give me a prioritized list of corrections and a test plan. This is the standard app, not an Assistive Access flow. We have no contrast values, focus order or screenshots.

- Body text is fixed at 12 pt and clips when the person enlarges text to 200%.
- Unavailable departure times are shown only in red text, available ones only in green.
- Pay is a custom icon with no accessible name.
- Removing a traveller needs a three-finger swipe, with no button on screen.
- A booking failure plays a sound, with no visual or text message.
