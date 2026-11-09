Use a **lightweight migration**: Core Data supports adding a non-optional attribute when the destination model supplies a default value.

1. **Create a new model version.** In Xcode, select your `.xcdatamodeld` file, then choose **Editor → Add Model Version**.
2. **Add the attribute** in the new version. Uncheck **Optional** and set **Default Value** in the Data Model inspector—for example, `false` for a Boolean or `0` for an integer.
3. **Make the new version current** using the model file’s File inspector.
4. **Enable automatic migration** before loading your persistent store:

```swift
let container = NSPersistentContainer(name: "MyModel")

for description in container.persistentStoreDescriptions {
    description.shouldMigrateStoreAutomatically = true
    description.shouldInferMappingModelAutomatically = true
}

container.loadPersistentStores { _, error in
    if let error {
        fatalError("Persistent store failed to load: \(error)")
    }
}
```

These options default to `true` for `NSPersistentContainer`; setting them explicitly makes the intent clear.

During migration, **existing objects receive the model’s default value** for the new attribute. New objects also receive that default. Set it in the Core Data model; a Swift property initializer or `awakeFromInsert()` does not populate existing records during migration.

Test with a store created using the previous model version, and keep that version in your model bundle. If the value must be calculated separately for each existing object, use a staged backfill or custom migration instead of a fixed default.