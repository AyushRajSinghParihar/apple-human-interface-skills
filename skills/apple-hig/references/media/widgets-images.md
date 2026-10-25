# Widget visual examples

Source: [Apple HIG Widgets](https://developer.apple.com/design/human-interface-guidelines/widgets). Snapshot: 2026-10-25.

These original notes describe the inspected primary images and their alternate appearances. The [main guide](../../subskills/apple-hig-system-experiences/references/widgets.md) contains exact size/context tables, rendering behavior, and platform guidance. Names, dates, prices, temperatures, and artwork in the samples illustrate content rather than mandatory values.

## Family size and information hierarchy

The Calendar examples increase useful scope with size. Small shows the current day and a few upcoming items. Medium adds adjacent upcoming context. Large presents a time grid for two days. Extra-large landscape expands the calendar across several days, while preserving event color and date hierarchy. They demonstrate a family of purposeful layouts rather than a stretched small design.

The spatial extra-large portrait example acts like an album poster: artwork dominates the upper region, with a readable title, artist, and restrained footer below. It uses the portrait surface as a distinct media object.

Accessory examples compress content differently. Circular combines one event time with a calendar symbol; corner curves time and event name along a watch-face edge; inline fits day, symbol, event count, and time into one line; rectangular provides a short vertical stack of meeting details. Select the hierarchy for the family rather than shrinking the same paragraph into every shape.

## The same content in different contexts

| Inspected presentation | What changes and what remains recognizable |
| --- | --- |
| Stocks full color | Green direction/graph and a large price remain clearly ranked on a dark surface. |
| Stocks clear | Translucent material and pale foreground replace the solid color treatment while preserving identifiers, graph, change, and price. |
| Stocks tinted | A chosen purple surface and monochrome foreground preserve the same data hierarchy. |
| Stocks spatial frame | A physical outer frame surrounds the information; content must still fit comfortably within that object. |
| Stocks Lock Screen | Background removal and restrained foreground give the wallpaper room while retaining graph and price. |
| Stocks StandBy | Large background-free information remains visible against black. Night Mode makes the same content red. |
| Calendar on a watch face | A colored leading rule and compact text identify the appointment against the watch face. |
| Calendar in Smart Stack | A rounded card and changed text colors adapt the same appointment to a standalone surface. |

## Glanceable purpose and direct actions

The Weather example emphasizes the current temperature, with location and supporting conditions in smaller text. The Stocks medium example aligns each security's name, small chart, and values on a row; selecting a row should open that security rather than an unrelated starting screen.

The Reminders pair changes individual circular controls from empty to selected while leaving the list in place. This demonstrates a simple action within the widget. It does not turn the entire list into a required multistep workflow.

## Appearance, loading, and discovery

Notes light/dark examples keep the yellow identity header and content hierarchy while adapting the body and text contrast. The Tips placeholder retains the yellow background and the approximate arrangement of three text lines as translucent blocks. The loaded version replaces those blocks with real words in the same area.

The Notes and Weather gallery examples show realistic previews plus short names and descriptions. Their Add Widget buttons use the respective yellow and blue identity colors. The Lock Screen composition places inline information above the clock and compact circular/rectangular information below it, with the same relationships retained across appearance changes.

## StandBy and spatial distance

The correct StandBy Weather example removes the blue card background so its information shares the black surface with the adjacent clock. The incorrect comparison keeps an isolated blue rounded card. The low-light version renders both clock and weather information in red; meaning must survive without the ordinary palette.

The spatial near/far poster pair preserves the same artwork and title. Nearby content adds smaller secondary description; the distant version simplifies and emphasizes the primary title. Preserve identity across the threshold while reducing detail people cannot read from farther away.
