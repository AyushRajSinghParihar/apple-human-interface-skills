I’d make it answer one question: **“What habit should I do next?”**

Start with a **rectangular Lock Screen widget** below the clock. Example content:

```text
📖 Read
10 minutes · Today
2 of 3 habits complete
```

- **Primary:** one habit name, chosen by the person or automatically selected from today’s remaining habits.
- **Secondary:** its target, such as “10 minutes” or “Walk 2 km.”
- **Supporting:** today’s overall progress. Keep streaks in the app unless the person explicitly chooses a streak-focused widget.

Tapping opens that habit’s check-in screen. For a simple yes/no habit, you could offer a native completion button; habits requiring quantities or notes should open the app.

Define these states:

| Situation | Widget shows |
|---|---|
| All habits complete | “All done today” with a checkmark |
| Nothing scheduled | “Rest day · Next habit tomorrow” |
| No habits configured | “Choose a habit” → setup |
| Older cached data | A dated summary, so yesterday’s completion never looks like today’s |

Use system typography and SF Symbols, with clear text and shapes that remain readable in monochrome and dimmed Always On mode. Offer a generic “Daily habit” label for sensitive habits, and respect system privacy redaction.

An optional **circular version** can show a progress ring with “2/3”; an **inline version** could read “Read · 10 min” with one tap destination.

This follows Apple’s [widget guidance](https://developer.apple.com/design/human-interface-guidelines/widgets): focused, timely information and precise actions. Before shipping, verify long habit names, larger text, VoiceOver, and Lock Screen rendering on a device using Apple’s [accessibility guidance](https://developer.apple.com/design/human-interface-guidelines/accessibility).