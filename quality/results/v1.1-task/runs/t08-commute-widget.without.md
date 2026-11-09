Make **“When should I leave, and has anything changed?”** the organizing principle. Give the active journey its own Live Activity.

| Surface | Useful content | Tap behavior |
|---|---|---|
| Small Home Screen | Saved route, next departure in large type, platform, delay | Open that departure |
| Medium Home Screen | Next departure prominently; two later alternatives; relevant disruption | Each departure opens its details |
| Large Home Screen | Outbound and return departures, alternatives and disruption details | Open the selected service or alert |
| Inline Lock Screen | `Train to Central · 8 min · +5 min` | One target opening that departure |
| Circular Lock Screen | Train symbol, minutes until departure; accessible destination label | Open the saved commute |
| Rectangular Lock Screen | Destination, departure time, platform and short status | Open that departure |

Use a small brand cue only where space permits. Prioritize readable information over the logo and station lists. Let people configure their route, direction and departure station through widget configuration.

**Delays and freshness**

Show the revised time and its consequence together: **“08:47 · 5 min late · Platform 4.”** Keep the scheduled time secondary. Use explicit words for cancellation, platform changes and delays; color alone must never carry the meaning. A cancellation stays visible long enough to explain what happened, with the next usable service alongside it.

Replace the every-second refresh promise with these rules:

- Use WidgetKit timelines for known departures and scheduled state changes. Request refreshes when new data becomes available; iOS controls delivery and timing.
- Use system-rendered relative dates or timers for countdowns. A moving countdown does **not** mean the service data was fetched again.
- Show “Live” only while the underlying feed meets an explicit freshness threshold based on the provider’s update cadence.
- After that threshold, show **“Updated 6 min ago”** or **“Updates unavailable.”** Distinguish scheduled times from live estimates, and stop presenting expired predictions as imminent departures.
- Include freshness-expiry entries in the timeline so the label can change even without another successful fetch.

**The 50-minute journey**

Start a **Live Activity** when the person starts tracking a particular train. Fifty minutes fits comfortably within a Live Activity’s supported duration.

On the Lock Screen, show destination, expected arrival, next stop and a simple progress indicator. In the Dynamic Island, prioritize time to arrival and a disruption indicator; expanded presentation can add the next stop and platform or transfer information.

Update through ActivityKit when meaningful events occur: departure, a confirmed stop, a changed arrival estimate, cancellation or arrival. Use push updates when available while the app is inactive. Let system timers advance between events; don’t poll every second or infer confirmed train movement from elapsed time. Set a stale date and visibly mark delayed updates. At arrival, show a brief completion state and end the activity.

**Appearance and fallback states**

Use semantic text styles, system spacing, SF Symbols and a system-managed widget background. Check Home Screen layouts in full color, dark and tinted rendering; preserve hierarchy through typography and shape when route colors disappear. For StandBy, make the primary departure readable at a distance and allow the system’s night treatment. Test reduced-luminance presentation without relying on bright colors or animation.

Signed-out people should see a useful setup state: **“Choose your commute”**, with a tap opening setup. If authentication is required, say **“Sign in to see your commute.”** Also design explicit states for no service, unavailable data and an unconfigured route. Respect privacy redaction for saved commute details on locked surfaces.