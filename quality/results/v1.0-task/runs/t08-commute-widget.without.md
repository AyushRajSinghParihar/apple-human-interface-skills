Make the set answer three questions: **When do I leave? Is my train disrupted? Where am I on this journey?** Give the departure time and status priority over the app logo.

| Surface | Recommended design | Tap behavior |
|---|---|---|
| Home Screen, small | One saved commute: “Central → Riverside,” **08:24**, “In 6 min,” platform and delay status. | Open that departure. |
| Home Screen, medium | Emphasize the next departure; show two alternatives beneath it. Include route, platform and data freshness. | Each departure opens its details. |
| Home Screen, large | Next departure, alternatives and a useful disruption summary, such as “Platform changed to 4.” Avoid filling space with station names. | Link departures and disruption details separately. |
| Lock Screen, inline | One concise line: “Central 08:24 · +5 min.” | **One tap target** for the entire accessory; remove the three separate targets. |
| Lock Screen, circular | Train symbol and “6 min.” Replace with a clear disruption symbol when necessary. | Open the selected commute. |
| Lock Screen, rectangular | Route, next departure, platform and short status: “08:24 · Platform 4 / Delayed 5 min.” | Open departure details. |

Let people choose their saved route, direction and departure station when configuring the widget. Use a small identifying symbol only where it helps recognition.

**Handle departures and delays honestly.**

- Use WidgetKit timelines for known changes, such as advancing to the next departure. Request reloads when new information arrives, subject to system scheduling and budgets.
- Remove the promise of a refresh every second. A system-rendered countdown can advance without fetching new train data; its movement does **not** mean the service information was refreshed.
- Show the revised time prominently: **08:29 · Delayed 5 min**, with “Scheduled 08:24” in larger layouts. Give cancellations and platform changes priority over routine information.
- Define freshness using the train provider’s expected reporting interval. Show “Updated 2 min ago”; after the freshness threshold, replace “Live” with **“Updates unavailable · Last checked 08:18.”** Label timetable-only data “Scheduled.”
- Once a cached departure time passes without confirmation, show “Check departure status” or the next clearly labeled scheduled service. Don’t infer that a train departed from the clock alone.

**Use a Live Activity for the active 50-minute journey.**

Start it when the person explicitly starts tracking a journey. Fifty minutes fits comfortably within a Live Activity’s supported lifetime; there’s no need to keep the widget extension running.

On the Lock Screen, show destination, expected arrival, next stop and any delay. In the Dynamic Island, prioritize remaining time and a train symbol; use the expanded view for next stop, arrival and disruption details.

Update through ActivityKit from the app and server push notifications as information changes. Use system-rendered timers between updates, without promising per-second network updates. Set a stale date so missed updates produce an honest “Awaiting update” state. Don’t animate estimated progress as though it were confirmed train location.

At confirmed arrival, show “Arrived at Riverside,” end the activity and leave a brief completion state before dismissal. If arrival cannot be confirmed, say so rather than declaring success from the estimated arrival time.

**Make every appearance and account state intentional.**

- **Tinted Home Screen:** Use the accented rendering mode, clear text hierarchy and symbols. Delay meaning must survive removal of route colors.
- **Dark appearance:** Use adaptive system colors and widget backgrounds; check text, symbols and contrast independently.
- **StandBy and night mode:** Favor large departure or arrival information. Let the system apply its night treatment; don’t depend on green/red distinctions or hard-coded white backgrounds.
- **Signed out:** Show “Sign in to see your commute” with a clear tap destination. For signed-in people without a saved route, show “Choose your commute.”
- **Privacy and accessibility:** Support privacy redaction for commute details, readable type and VoiceOver descriptions such as “08:29, delayed five minutes, platform four.”