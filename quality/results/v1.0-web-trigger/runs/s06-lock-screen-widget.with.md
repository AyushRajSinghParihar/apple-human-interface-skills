I’d make it answer one question: **“What’s my next habit, and have I done it today?”**

Start with a **rectangular widget below the clock**, showing one habit the person chooses:

```text
📖 Read
10 of 20 min today
```

Use a small progress indicator beside the text. For a yes/no habit, show “Not yet today” or “Done today.” Keep streaks secondary—today’s action deserves the most attention.

My proposed behavior:

- **Tap:** Open that habit’s check-in screen.
- **Completed:** Show a checkmark and “Done today.” Keep the chosen habit visible so the result feels stable.
- **Rest day:** Show “Next: Tomorrow.”
- **No habit configured:** Show “Choose a habit,” opening setup.
- **Data unavailable:** Show “Open to update,” avoiding an incorrect zero.

Offer two compact alternatives:

| Format | Content |
|---|---|
| Circular | Progress ring with “3/5” and “Today” for daily habit completion |
| Inline, above the clock | “Habits: 3 of 5 done” |

Use readable system text and symbols that retain meaning in monochrome and dimmed Always On presentation. Keep content focused and deep-link to the relevant habit, following [Apple’s widget guidance](https://developer.apple.com/design/human-interface-guidelines/widgets).

Let people choose a neutral label such as “Daily habit” for sensitive routines. Avoid motivational quotes, tiny calendars, and overdue warnings competing with the main action.

This is a design proposal; device rendering, long habit names, VoiceOver, and refresh behavior still need validation.