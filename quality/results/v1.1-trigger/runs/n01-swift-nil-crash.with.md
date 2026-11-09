That error means an implicitly unwrapped optional (`SomeType!`) was `nil` when your code tried to use it. In `viewDidLoad`, common causes are:

- **Disconnected `IBOutlet`:** An outlet is declared, but it isn’t connected to a view in the storyboard or XIB.
- **Loading the view controller incorrectly:** Calling `MyViewController()` when its views and outlets are defined in a storyboard. Instantiate it through that storyboard instead.
- **Incorrect storyboard setup:** The scene has the wrong custom class or module, or you’re loading a different scene than intended.
- **Missing injected data:** A property such as `var user: User!` wasn’t assigned before the view loaded. Accessing `controller.view` can trigger `viewDidLoad` earlier than expected.
- **Another optional used on that line:** An implicitly unwrapped property, or an explicit force unwrap (`!`), may be nil even if the outlet is connected.

For example:

```swift
@IBOutlet weak var titleLabel: UILabel!
var user: User!

override func viewDidLoad() {
    super.viewDidLoad()
    titleLabel.text = user.name // Either titleLabel or user could be nil
}
```

Start with the **exact crashing line in Xcode’s stack trace**, then inspect each optional on that line. Outlets should already be connected by `viewDidLoad` when the controller is loaded correctly.

Share the crashing line and the relevant property declarations, and I can help narrow it down.