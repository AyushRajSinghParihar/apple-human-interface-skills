**Let the row grow and reflow as text gets larger.** One line is a useful default layout, but shouldn’t be a constraint at accessibility sizes. Apple’s [Dynamic Type guidance](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type) specifically recommends stacking inline timestamps when space becomes tight.

For this cell, I’d use:

- **Regular sizes:** icon → title → trailing timestamp, with title and timestamp aligned by their first baselines.
- **Accessibility sizes:** icon beside a vertical stack containing the wrapping title and timestamp below it. Top-align the icon.
- Reflow earlier if narrow widths or localized content require it.

Configure both labels with semantic fonts and automatic updates:

```swift
titleLabel.font = .preferredFont(forTextStyle: .body)
timestampLabel.font = .preferredFont(forTextStyle: .caption1)

for label in [titleLabel, timestampLabel] {
    label.adjustsFontForContentSizeCategory = true
    label.numberOfLines = 0
}
timestampLabel.textColor = .secondaryLabel
```

In the layout code, use this as a starting breakpoint:

```swift
let shouldStack =
    traitCollection.preferredContentSizeCategory.isAccessibilityCategory
```

Apply that on initial configuration and whenever the content-size-category trait changes. Switch between constraint sets, or change a title/timestamp stack view’s axis. Font updates alone don’t rearrange your layout.

Make the cell self-sizing:

```swift
tableView.rowHeight = UITableView.automaticDimension
tableView.estimatedRowHeight = 60
```

Provide an unbroken chain of top-to-bottom constraints inside `contentView`, constrain the labels’ available width, and avoid fixed row or label heights. Use leading/trailing constraints for right-to-left support.

For an SF Symbol icon, configure it with a text style and enable scaling:

```swift
iconView.preferredSymbolConfiguration =
    UIImage.SymbolConfiguration(textStyle: .body)
iconView.adjustsImageSizeForAccessibilityContentSizeCategory = true
```

Avoid fixed icon constraints that prevent it growing. For custom fonts or meaningful custom icons, use `UIFontMetrics` to scale them.

Don’t use `adjustsFontSizeToFitWidth` to squeeze the row back onto one line. Preserve the requested text size and allow wrapping.

Verify all text sizes, especially the largest accessibility size, with long titles, localized timestamps, narrow widths, and Bold Text. Also change text size while the screen is open to check that both the arrangement and row height update. This is a recommended implementation pattern; runtime behavior still needs testing in your app.