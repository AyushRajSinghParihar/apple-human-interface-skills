Replace the eight equal numbers with **one primary metric and two supporting metrics**. Move the other five to a secondary detail view.

For a running workout, the main screen could look like:

```text
          PACE
        5:24 /km

   ELAPSED       HEART RATE
    24:18         152 bpm
```

- **Primary value:** start around 36–40 pt, semibold.
- **Supporting values:** around 22–24 pt.
- **Labels and units:** around 16 pt. Use system text styles, Dynamic Type, and stable-width digits so updates don’t shift the layout.
- Use a black background with high-contrast text. Keep labels visible; color can reinforce meaning.
- Keep metric positions stable throughout the workout. Choose the primary metric by activity—for example, remaining interval time during intervals.
- Put large Pause/Resume and End controls on a separate, readily accessible controls page. Show a clear “Paused” state when applicable.
- If a sensor reading is unavailable, show “—” instead of presenting an old value as live.

These sizes are design starting points. Apple’s [typography guidance](https://developer.apple.com/design/human-interface-guidelines/typography) lists **16 pt as the watchOS default and 12 pt as the minimum**; your current 10 pt is below that guidance. Its [workout guidance](https://developer.apple.com/design/human-interface-guidelines/workouts) recommends large, high-contrast, prioritized metrics.

Before shipping, verify a quick wrist glance while moving, the smallest supported Watch, and enlarged text. At larger text sizes, reduce visible supporting metrics instead of shrinking text. Device readability and runtime behavior remain untested; no app code was supplied.