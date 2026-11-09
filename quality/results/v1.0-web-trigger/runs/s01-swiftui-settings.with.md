Let `Form` handle more of the appearance. Based on your description, I’d change three things:

- **Remove the grey rounded rectangle around each row.** Group related rows with `Section`, and let the form supply backgrounds, separators, spacing, and Dark Mode appearance. iOS forms already use grouped-list styling. [SwiftUI Form](https://developer.apple.com/documentation/swiftui/form)
- **Move “Settings” into the navigation bar.** Use `.navigationTitle("Settings")` instead of a bold, fixed 28 pt heading inside the form. Choose `.large` for a main settings screen or `.inline` for a deeper page. Use semantic styles such as `.body` and `.footnote` elsewhere so text supports Dynamic Type. [Navigation titles](https://developer.apple.com/documentation/swiftui/configure-your-apps-navigation-titles), [Typography](https://developer.apple.com/design/human-interface-guidelines/typography)
- **Reconsider Save based on behavior.** For ordinary preferences, I’d apply and persist changes immediately and remove Save. If users are editing a draft that needs explicit commitment, put Save in the trailing navigation toolbar; a modal editor can pair it with Cancel, which discards the draft. This is a design recommendation for your flow, rather than a blanket prohibition on bottom buttons. [Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars)

For simple preferences:

```swift
struct SettingsView: View {
    @AppStorage("playSounds") private var playSounds = true
    @AppStorage("showPreviews") private var showPreviews = true

    var body: some View {
        NavigationStack {
            Form {
                Section("Playback") {
                    Toggle("Play Sounds", isOn: $playSounds)
                }

                Section {
                    Toggle("Show Previews", isOn: $showPreviews)
                } header: {
                    Text("Appearance")
                } footer: {
                    Text("Show a preview alongside each item.")
                }
            }
            .navigationTitle("Settings")
            .navigationBarTitleDisplayMode(.large)
        }
    }
}
```

If the screen already lives inside a `NavigationStack`, omit the extra stack.

Before shipping, check the smallest supported iPhone, accessibility text sizes, Dark Mode, and whether changes survive leaving and reopening the screen. These suggestions are based on your description; rendering and behavior haven’t been tested.