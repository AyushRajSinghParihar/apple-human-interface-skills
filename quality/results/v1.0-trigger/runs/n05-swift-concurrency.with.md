Both `async let` and `TaskGroup` create **child tasks that run concurrently** using structured concurrency. Their main difference is how you define the work.

| | `async let` | `TaskGroup` |
|---|---|---|
| Best for | A fixed set of concurrent operations | A runtime-determined set of operations |
| Result types | Each operation can return a different type | All children return the same type |
| Getting results | Await named values | Iterate results as tasks finish |
| Adding work | Declare each task explicitly | Add tasks dynamically, including while processing results |

Use **`async let`** when you know the operations upfront:

```swift
async let profile = fetchProfile()
async let settings = fetchSettings()

let screen = try await ScreenData(
    profile: profile,
    settings: settings
)
```

Both fetches start concurrently. Their return types can differ, and you access each result by name.

Use **a task group** when the number of operations depends on runtime data:

```swift
let images = try await withThrowingTaskGroup(
    of: Image.self,
    returning: [Image].self
) { group in
    for url in urls {
        group.addTask {
            try await downloadImage(from: url)
        }
    }

    var results: [Image] = []
    for try await image in group {
        results.append(image)
    }
    return results
}
```

The images arrive in **completion order**, so this array may have a different order from `urls`. A group also lets you implement bounded concurrency by adding new tasks as earlier tasks finish.

Both forms keep children within their enclosing scope: the scope cannot finish until its child tasks finish. Cancellation is cooperative; neither mechanism forcibly stops a running task.

Choose `async let` for a few named operations. Choose `TaskGroup` for dynamically managed collections of work.