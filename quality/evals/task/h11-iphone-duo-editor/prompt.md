---
description: Adapt an iPhone photo editor for iPhone Duo.
tags: [task, hard]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

We are adapting our iPhone photo editor for iPhone Duo. Please review our plan and tell me what to change.

- We will design a separate fixed layout for each display: 375 pt wide outside, and two fixed 375 pt panels inside.
- On the outer display we will move all toolbars and the tab bar to the top edge, to keep them where they are on other iPhones.
- In Arabic and Hebrew we will mirror the side toolbar to the other physical side of the device.
- Toolbar items are icon-only, with no titles, to save space.
- Our full-screen custom canvas ignores the hinge area when the inner display is partly folded.
- When the inner camera turns on for the video-call feature, our controls stay on top of the camera area.
