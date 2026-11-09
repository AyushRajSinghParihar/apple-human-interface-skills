Use a **lightweight migration** with a new model version. Core Data can infer the migration when a new non-optional attribute has a default value.

1. In Xcode, select your `.xcdatamodeld` file and choose **Editor → Add Model Version**.
2. Add the attribute to the new version.
3. In the Data Model inspector:
   - Set its type.
   - Uncheck **Optional**.
   - Set a **Default Value**, such as `0`, `false`, or `"Unknown"`.
4. Select the `.xcdatamodeld` container and set **Current Model Version** to the new version in the File inspector.
5. Enable automatic migration before loading the store:

```swift
let container = NSPersistentContainer(name: "MyModel")

for description in container.persistentStoreDescriptions {
    description.shouldMigrateStoreAutomatically = true
    description.shouldInferMappingModelAutomatically = true
}

container.loadPersistentStores { _, error in
    if let error {
        // Handle the migration or store-loading failure.
        print("Failed to load persistent store: \(error)")
    }
}
```

These migration options are enabled by default for `NSPersistentContainer`; setting them explicitly makes the intent clear.

**Existing records receive the model’s default value during migration.** Newly inserted objects also receive that default. A default set only in a Swift initializer or `awakeFromInsert()` won’t backfill existing records.

Keep the old model version bundled, and test against a copy of an actual old store. If the value must be calculated separately for each existing record, use a staged migration or a custom migration policy instead of a constant model default.