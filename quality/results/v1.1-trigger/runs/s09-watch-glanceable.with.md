Replace the eight-number grid with **one primary metric and two supporting metrics**. For a running workout, I’d use:

```text
       CURRENT PACE
          5′24″
          /km

   ELAPSED       HEART RATE
    24:18         148 bpm
```

These are proposed starting sizes, not Apple requirements:

| Element | Treatment |
|---|---|
| Primary value | 36–40 pt, semibold |
| Supporting values | 22–24 pt, semibold |
| Labels and units | 14–16 pt, system font |

Choose the primary metric by workout goal: pace for running, remaining interval time for intervals, elapsed time for an open workout. Keep positions stable as values update.

Move the other five metrics to a secondary view reachable with the Digital Crown. Keep Pause, Resume, and End on a separate controls page with generous targets. This follows Apple’s guidance for [prioritized workout metrics](https://developer.apple.com/design/human-interface-guidelines/workouts) and [brief watchOS glances](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos).

Use high-contrast text on a simple background, retain explicit labels and units, and show “Paused” or “Unavailable” when appropriate. Support Dynamic Type; at larger sizes, stack supporting metrics instead of shrinking text. Apple’s [accessibility guidance](https://developer.apple.com/design/human-interface-guidelines/accessibility) lists 16 pt default text and 12 pt minimum for watchOS—10 pt is too small for these essential readings.

Validate on the smallest supported Watch while moving: can someone identify the primary value in a brief wrist raise, and read everything at 140% text size without clipping?

No app source was available here, so this is a screen specification; device readability and accessibility remain untested.