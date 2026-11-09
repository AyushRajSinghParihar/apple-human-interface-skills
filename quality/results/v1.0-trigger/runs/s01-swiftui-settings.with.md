Based on your description, the biggest improvement is to **let `Form` supply the visual structure**.

- **Remove the per-row grey rounded rectangles.** Group related rows with `Section`, and keep the system backgrounds, separators, and insets. That matches Apple’s [grouped-list guidance](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables#Style).
- **Move “Settings” into the navigation bar.** Use `.navigationTitle("Settings")`; choose `.large` for a main settings destination or `.inline` for a compact detail screen. Avoid hard-coding a 28 pt content title. System titles provide the expected hierarchy and scrolling behavior ([toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars#Titles), [typography](https://developer.apple.com/design/human-interface-guidelines/typography)).
- **Reconsider Save based on behavior.** For ordinary preferences, I’d apply and persist changes immediately and remove Save. If users need to review a batch of edits, put **Save** in the trailing navigation toolbar and **Cancel** on the leading side of a modal editor; Cancel should discard the draft. A large bottom button gives routine settings the emphasis of a submission flow.

For simple preferences, this is a useful starting point:

```swift
struct SettingsView: View {
    @AppStorage("playSounds") private var playSounds = true
    @AppStorage("useHaptics") private var useHaptics = true

    var body: some View {
        NavigationStack {
            Form {
                Section {
                    Toggle("Sounds", isOn: $playSounds)
                    Toggle("Haptics", isOn: $useHaptics)
                } header: {
                    Text("Feedback")
                } footer: {
                    Text("Choose how the app responds to your actions.")
                }
            }
            .formStyle(.grouped)
            .navigationTitle("Settings")
            .navigationBarTitleDisplayMode(.large)
        }
    }
}
```

If the screen is already inside a `NavigationStack`, reuse that stack.

I haven’t seen or run your screen. Check the result on a small iPhone with larger Dynamic Type and in Dark Mode, then reopen settings to verify persistence.