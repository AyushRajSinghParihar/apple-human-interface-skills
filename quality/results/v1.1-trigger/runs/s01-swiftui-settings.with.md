Let `Form` supply more of the appearance. Based on your description, I’d change three things:

1. **Remove the custom grey rectangles.** Group related rows with `Section` and keep the system row backgrounds, separators, and insets. The section becomes the visual group, instead of every setting looking like a separate card. See Apple’s [lists and tables guidance](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables).
2. **Move “Settings” into the navigation title.** Use `.navigationTitle("Settings")`, with a large title for the main settings screen or an inline title for a deeper page. A fixed 28 pt title isn’t inherently wrong, but native navigation handles placement and scrolling; semantic text styles support Dynamic Type. See [toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars) and [typography](https://developer.apple.com/design/human-interface-guidelines/typography).
3. **Choose Save behavior deliberately.** For ordinary preferences, I’d apply and persist changes immediately and remove Save. If users are editing a draft that needs explicit commitment, keep Save in the top trailing toolbar, with Cancel when changes can be discarded. That follows Apple’s [toolbar action placement](https://developer.apple.com/design/human-interface-guidelines/toolbars).

For simple preferences, this is a native starting point:

```swift
struct SettingsView: View {
    @AppStorage("soundsEnabled") private var soundsEnabled = true
    @AppStorage("useCellularData") private var useCellularData = false

    var body: some View {
        NavigationStack {
            Form {
                Section("Playback") {
                    Toggle("Sounds", isOn: $soundsEnabled)
                }

                Section {
                    Toggle("Use Cellular Data", isOn: $useCellularData)
                } header: {
                    Text("Downloads")
                } footer: {
                    Text("Allow downloads when Wi-Fi is unavailable.")
                }
            }
            .navigationTitle("Settings")
            .navigationBarTitleDisplayMode(.large)
        }
    }
}
```

If this screen is already inside a `NavigationStack`, omit the extra stack.

Check the result in Dark Mode and at the largest accessibility text size: labels should wrap and rows should grow. This is a recommendation from your description; rendering and accessibility haven’t been tested.