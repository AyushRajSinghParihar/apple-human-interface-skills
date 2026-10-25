# Charts

Source: [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/charts)  
Snapshot: 2026-10-25. Original implementation guidance derived from the source.

A chart should answer a specific question about data, such as whether conditions are changing, how categories compare, or whether a goal is within reach. Choose the question before choosing its visual form.

<a id="Anatomy"></a>
## Anatomy

A mark represents a value; a series groups related values; the plot area contains the marks. A scale maps numbers, dates, or categories to properties such as position, height, and color. Axes establish the variables and frame of reference. Ticks identify reference values; grid lines extend those references into the plot. Titles, subtitles, annotations, visible labels, accessibility labels, and legends explain the representation. A legend is useful for encodings such as color or shape that position alone cannot explain.

<a id="Marks"></a>
## Marks

- Use bars to compare categories, proportions, or accumulated quantities such as daily steps.
- Use a line to connect a series across time and reveal the direction and magnitude of change.
- Use points when individual observations, relationships, outliers, or clusters matter.
- Combine marks deliberately: points over a line can expose individual observations while retaining a readable overall trend.

<a id="Axes"></a>
## Axes

Choose a fixed range when its limits have stable meaning: battery charge spans 0–100%. Choose a dynamic range when values vary widely and filling the plot helps inspection, such as step totals for different periods. Set the baseline with the mark and task in mind: a zero baseline makes bar lengths comparable; a zero baseline can hide meaningful heart-rate variation far above zero.

Use familiar tick sequences such as 0, 5, 10 rather than 1, 6, 11. Balance grid density and label weight against the task and available interactions. If direct inspection reveals exact values, lighter and fewer grid lines can keep the data prominent.

<a id="Descriptive-content"></a>
## Descriptive content

Explain what the chart measures and why it matters before requiring exploration. A clear title and short takeaway help everyone, especially VoiceOver users and people with cognitive disabilities. Supply the main conclusion directly; a precipitation chart should communicate the expected rain in words as well as displaying values.

<a id="Best-practices"></a>
## Best practices

- Put data first in the visual hierarchy; axes and explanatory text provide supporting context.
- In narrow spaces, preserve useful plot width. Shorten vertical-axis labels without losing meaning, move units to the title when helpful, or put long category labels inside the plot only where they cannot cover important data.
- Supply accessibility descriptions and consider Audio Graphs. Interactive exploration supplements the primary message; it must not be the only route to critical facts.
- Enlarge interaction beyond tiny marks when needed. Scrubbing anywhere in the plot can make selection easier for touch, pointers, and reduced motor control.
- Design predictable keyboard, full keyboard access, and Switch Control navigation. Use accessibility APIs to establish a logical traversal, such as progressing along the X axis, or navigate groups of observations when a dataset is large.
- Expose meaningful updates to assistive technologies and people using Reduce Motion. Animation can draw attention to changed marks or axes, but an accessible change notification or another cue must also communicate the update.
- Align charts with adjacent content. Placing vertical-grid labels on the trailing side, or moving the Y axis to the trailing edge, can preserve a clean leading edge. Attach a tick to a label that would otherwise seem unconnected.

<a id="Color"></a>
## Color

Color can identify series and emphasize meaningful facts, but pair it with shape, pattern, or another encoding. Blood-pressure series, for example, can use different mark shapes in addition to different colors. Insert visible separation between adjacent colored segments in a stacked bar so segment boundaries remain distinguishable.

<a id="Enhancing-the-accessibility-of-a-chart"></a>
## Enhancing the accessibility of a chart

Swift Charts supplies accessibility elements for marks or mark groups and a default Audio Graphs implementation. Customize its spoken title and summary to explain purpose and the main pattern. Without Audio Graphs, explicitly describe chart type, axis meanings, and axis bounds.

Choose the descriptive granularity that serves the question. A route-elevation chart can summarize terrain over segments; a step chart may need each period's exact count. A small chart used as a button can have one concise overview, with detail available after opening it. Unlike a single image, a chart often needs several accessible elements.

Write objective labels with enough context to identify the value, followed by its details. Avoid repeating an axis name already supplied by the overview or Audio Graphs. State actual quantities instead of subjective speed or magnitude claims. Prefer explicit dates and units, such as June 6, 60 minutes, or 60 meters, over ambiguous shorthand. Describe the meaning of a series rather than its visible color, and refer to axes consistently. Hide purely visual axis and tick labels from assistive technology when accessible marks and Audio Graphs already provide the information.

<a id="Platform-considerations"></a>
## Platform considerations

The source adds no separate rules for iOS, iPadOS, macOS, tvOS, or visionOS.

<a id="watchOS"></a>
### watchOS

Prioritize useful information at a glance and simple interactions. Put detailed exploration in a companion platform when available: a watch can show today's heart-rate trend while an iPhone supports multiple periods and individual readings.

<a id="Resources"></a>
## Resources

Official implementation links and revision metadata follow.

<a id="Related"></a>
#### Related

[Charting data](https://developer.apple.com/design/human-interface-guidelines/charting-data)

<a id="Developer-documentation"></a>
#### Developer documentation

<https://developer.apple.com/documentation/Charts>

<a id="Videos"></a>
#### Videos

<https://developer.apple.com/videos/play/wwdc2025/313>
  <https://developer.apple.com/videos/play/wwdc2022/110342>
  <https://developer.apple.com/videos/play/wwdc2022/110340>

<a id="Change-log"></a>
## Change log

Revision dates recorded by Apple: September 23, 2022.
