---
description: Adapt an iPad invoice editor for Arabic, compact width, keyboard and 200% text.
tags: [task]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

Please adapt our iPad invoice editor for Arabic, a compact resizable window, a hardware keyboard and 200% text size. Keep the totals and the editing state. Give me the revised layout and behavior specification, the decisions, and acceptance checks.

Current state:
- iPadOS. The compact width is 420 pt.
- Fixed left-aligned columns. Labels clip at 200% text.
- Payment state is shown only with red or green.
- Sample data: vendor name مؤسسة النور, invoice ID INV-2026-04, email accounts@example.test, amount 1,240.50 SAR.
- The app currently mirrors all numerals and all icons mechanically for Arabic.
- Tab cannot reach the Add line button.
- Resizing the window resets the quantities that the person entered.
