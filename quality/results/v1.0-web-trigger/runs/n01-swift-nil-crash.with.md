That error means an implicitly unwrapped optional (`SomeType!`) was `nil` when your code tried to use it. In `viewDidLoad`, common causes are:

- **A disconnected `@IBOutlet`.** The outlet exists in code but isn’t connected to a view in the storyboard or XIB. Check the Connections inspector.
- **Creating a storyboard controller with `MyViewController()`.** This bypasses the storyboard, so its outlets aren’t connected. Instantiate it through the storyboard instead.
- **The wrong storyboard/XIB configuration.** Check the controller’s custom class, module, storyboard identifier, and which resource you’re actually loading.
- **A missing dependency.** A property such as `var user: User!` wasn’t assigned before the controller’s view loaded.
- **An outlet whose view was removed or never loaded.** For example, a weak outlet can become `nil` if nothing retains its view.

For example:

```swift
@IBOutlet private weak var titleLabel: UILabel!
var user: User!

override func viewDidLoad() {
    super.viewDidLoad()
    titleLabel.text = user.name // Either property could be nil
}
```

When the debugger stops, inspect the highlighted line and each optional on it. Split complex expressions into separate lines to identify the failing value. Calling `super.viewDidLoad()` is correct, but won’t repair missing outlet connections.

Share the crashing line and the related property declarations, and I can help pinpoint the cause.