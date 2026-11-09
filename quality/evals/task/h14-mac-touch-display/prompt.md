---
description: Support a Mac with a touch display.
tags: [task, hard]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

Our macOS drawing app must work well on a Mac with a touch display. Our designer proposes this:

- Make every toolbar button and control 44 pt tall so that fingers can hit them, and space the toolbar out.
- Change the layout to a larger "touch mode" when the person touches the screen.
- Add a new "Smart Erase" feature that works only with a two-finger touch gesture.
- Some tools need Shift-drag or a hover menu, and we have no touch alternative for them.
- Our small stepper and the brush-size slider stay as they are.

What should we do instead?
