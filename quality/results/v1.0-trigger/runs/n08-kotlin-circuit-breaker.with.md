Use a circuit breaker around **calls from your backend to a failing dependency**—for example, an HTTP service or database. After enough failures, it temporarily rejects calls immediately, giving that dependency time to recover.

First, check what causes the 500s. A circuit breaker helps when a dependency is failing or slow. If your own server is exhausting threads, connections, or CPU, also add concurrency limits, timeouts, and load shedding.

For a Kotlin/JVM backend, [Resilience4j](https://resilience4j.readme.io/docs/circuitbreaker) is a common choice.

Add the dependency using your project’s version catalog or a compatible pinned version:

```kotlin
implementation("io.github.resilience4j:resilience4j-circuitbreaker:<version>")
```

Create **one shared breaker per dependency**, rather than one per request:

```kotlin
import io.github.resilience4j.circuitbreaker.CallNotPermittedException
import io.github.resilience4j.circuitbreaker.CircuitBreaker
import io.github.resilience4j.circuitbreaker.CircuitBreakerConfig
import java.time.Duration

class CatalogClient(
    private val httpClient: CatalogHttpClient
) {
    private val breaker = CircuitBreaker.of(
        "catalog",
        CircuitBreakerConfig.custom()
            .slidingWindowSize(20)
            .minimumNumberOfCalls(10)
            .failureRateThreshold(50f)
            .waitDurationInOpenState(Duration.ofSeconds(15))
            .permittedNumberOfCallsInHalfOpenState(3)
            .build()
    )

    fun getProduct(id: String): Product =
        breaker.executeSupplier {
            httpClient.getProduct(id)
        }
}
```

This configuration:

- Measures the most recent 20 calls, after at least 10 calls.
- Opens the circuit when at least 50% fail.
- Rejects calls for 15 seconds with `CallNotPermittedException`.
- Then allows a few probe calls to check recovery.

**Make sure your HTTP client throws for relevant upstream failures.** A returned HTTP 500 response won’t count as a failure unless you translate it into an exception or configure a result predicate. Exclude expected business errors, such as “product not found,” from breaker failures.

At your API boundary, translate an open circuit into **503 Service Unavailable**, or serve a valid cached response. Avoid returning fake success data.

Also configure:

- **Connect and request timeouts:** a circuit breaker does not cancel slow calls.
- **A bulkhead/concurrency limit:** caps simultaneous dependency calls and protects your server during spikes.
- **Metrics:** track breaker state, rejected calls, dependency latency, and connection/thread pool saturation.
- **Careful retries:** retries can amplify overload; start without them.

If your client uses Kotlin `suspend` functions, use `resilience4j-kotlin` and its `executeSuspendFunction` extension instead of wrapping asynchronous work in `executeSupplier`.

Which framework are you using—Spring Boot, Ktor, or something else—and where do the 500s originate?