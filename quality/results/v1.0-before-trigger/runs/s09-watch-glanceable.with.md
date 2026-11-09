Replace the eight-number grid with **one dominant metric and two supporting metrics**. Apple recommends large, high-contrast workout values that people can read while moving. [Workout guidance](https://developer.apple.com/design/human-interface-guidelines/workouts)

For a running workout, I’d use this hierarchy:

| Position | Content | Suggested starting size |
|---|---|---|
| Top | Elapsed time: 24:18 | 20 pt |
| Center | Current pace: **5′32″** with min/km label | 36 pt, semibold |
| Bottom | Heart rate: **152 bpm** | 24 pt |

These sizes are design starting points. Choose the dominant metric by workout type: pace for running, remaining interval time for intervals, elapsed time for strength training.

- Move the other five metrics to a secondary detail view. Keep the main view stable; don’t automatically rotate values.
- Use system text styles, clear units, and monospaced digits so updates don’t shift the layout. Replace fixed 10 pt text; Apple lists 16 pt as the watchOS default and 12 pt as its general minimum guidance. [Typography](https://developer.apple.com/design/human-interface-guidelines/typography)
- Use a black background and bright text, with one accent for the dominant value. Pair zone colors with a written zone label.
- Keep Pause/Resume and End on an easily reached controls page, separate from metrics. Show “Paused” clearly when appropriate.
- At larger text sizes, move supporting metrics into a vertical layout rather than shrinking everything.

Validate on the smallest supported Watch while moving: can someone identify the primary value in a brief glance? Also check enlarged text, Bold Text, and missing sensor readings.

No app files were available here, so this is a proposed screen specification; device readability remains untested.