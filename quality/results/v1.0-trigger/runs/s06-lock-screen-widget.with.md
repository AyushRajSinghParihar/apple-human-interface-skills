I’d make it answer one question: **“What’s my next habit today?”**

Start with a **rectangular widget below the clock**, showing one habit and a little context. Example content:

```text
◯ Read 10 pages
   Next at 8 pm · 2 of 3 done
```

- **Primary:** the next scheduled, unfinished habit. Let people pin a specific habit instead.
- **Secondary:** its scheduled time and today’s completed/total count.
- **Tap:** open that habit’s check-in screen directly.

When everything is complete, switch to **“✓ All done today”** with “3 of 3 habits complete.” On rest days, show **“Nothing scheduled today.”** Keep the tone encouraging; leave missed-day warnings and detailed streak history inside the app.

For smaller options:

| Format | Content |
|---|---|
| Circular | Progress ring with **2/3** and a checkmark symbol |
| Inline, above the clock | **“Read at 8 pm · 2/3 done”**, with one tap destination |

Use system typography and SF Symbols, with text or shapes carrying meaning when color disappears. Offer a summary-only setting for people who prefer to hide habit names on their Lock Screen. Refresh after check-ins and scheduled changes; don’t imply continuous live updates.

This follows [Apple’s widget guidance](https://developer.apple.com/design/human-interface-guidelines/widgets): focused, glanceable content and precise navigation. Before shipping, preview long habit names, monochrome and Always On appearances, and unavailable data; device validation is still needed.