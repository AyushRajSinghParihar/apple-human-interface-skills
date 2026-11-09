That error means Swift tried to use an implicitly unwrapped optional (`SomeType!`) whose value was `nil`. In `viewDidLoad`, the usual causes are:

- **A disconnected `@IBOutlet`.** The property exists in code, but its storyboard or XIB connection is missing or broken.
- **Creating the controller without its storyboard or XIB.** For example, `MyViewController()` won’t load storyboard outlet connections. Instantiate it through the storyboard instead.
- **Incorrect storyboard setup.** Check the scene’s custom class and module, and verify that you’re loading the intended scene.
- **A dependency wasn’t assigned.** A property such as `var model: Model!` must be set before the view loads. Accessing `controller.view` or calling `loadViewIfNeeded()` can trigger `viewDidLoad` earlier than expected.
- **Accessing another controller’s outlets too early.** Its outlets remain `nil` until its view has loaded.

For example:

```swift
@IBOutlet private weak var titleLabel: UILabel!
var model: Model!

override func viewDidLoad() {
    super.viewDidLoad()
    titleLabel.text = model.title // Either property could be nil
}
```

Start with the **exact crashing line** in Xcode. If it contains several expressions, split them into separate lines and inspect each optional in the debugger. Fix the missing connection or initialization; changing `!` to `?` may simply hide the underlying problem.

If you paste the crashing line and how you create the view controller, I can help pinpoint it.