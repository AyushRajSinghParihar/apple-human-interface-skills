Use **#0B6E4F** as your primary color, with sage secondary tones and blue tertiary accents. This Material 3 theme keeps the brand’s green prominent and provides coordinated light and dark palettes.

```kotlin
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val LightColors = lightColorScheme(
    primary = Color(0xFF0B6E4F),
    onPrimary = Color(0xFFFFFFFF),
    primaryContainer = Color(0xFFA5F2CD),
    onPrimaryContainer = Color(0xFF002116),

    secondary = Color(0xFF4D6358),
    onSecondary = Color(0xFFFFFFFF),
    secondaryContainer = Color(0xFFD0E8DA),
    onSecondaryContainer = Color(0xFF092017),

    tertiary = Color(0xFF3D6373),
    onTertiary = Color(0xFFFFFFFF),
    tertiaryContainer = Color(0xFFC1E8FB),
    onTertiaryContainer = Color(0xFF001F2A),

    background = Color(0xFFF5FBF5),
    onBackground = Color(0xFF171D19),
    surface = Color(0xFFF5FBF5),
    onSurface = Color(0xFF171D19),
    surfaceVariant = Color(0xFFDCE5DD),
    onSurfaceVariant = Color(0xFF404943),

    outline = Color(0xFF707973),
    outlineVariant = Color(0xFFC0C9C1),
    inverseSurface = Color(0xFF2C322E),
    inverseOnSurface = Color(0xFFEDF2EC),
    inversePrimary = Color(0xFF89D5B2),

    error = Color(0xFFBA1A1A),
    onError = Color(0xFFFFFFFF),
    errorContainer = Color(0xFFFFDAD6),
    onErrorContainer = Color(0xFF410002),
)

private val DarkColors = darkColorScheme(
    primary = Color(0xFF89D5B2),
    onPrimary = Color(0xFF003825),
    primaryContainer = Color(0xFF005139),
    onPrimaryContainer = Color(0xFFA5F2CD),

    secondary = Color(0xFFB4CCBE),
    onSecondary = Color(0xFF20352B),
    secondaryContainer = Color(0xFF364B41),
    onSecondaryContainer = Color(0xFFD0E8DA),

    tertiary = Color(0xFFA5CCDF),
    onTertiary = Color(0xFF073544),
    tertiaryContainer = Color(0xFF244C5B),
    onTertiaryContainer = Color(0xFFC1E8FB),

    background = Color(0xFF0F1511),
    onBackground = Color(0xFFDFE4DE),
    surface = Color(0xFF0F1511),
    onSurface = Color(0xFFDFE4DE),
    surfaceVariant = Color(0xFF404943),
    onSurfaceVariant = Color(0xFFC0C9C1),

    outline = Color(0xFF8A938C),
    outlineVariant = Color(0xFF404943),
    inverseSurface = Color(0xFFDFE4DE),
    inverseOnSurface = Color(0xFF2C322E),
    inversePrimary = Color(0xFF0B6E4F),

    error = Color(0xFFFFB4AB),
    onError = Color(0xFF690005),
    errorContainer = Color(0xFF93000A),
    onErrorContainer = Color(0xFFFFDAD6),
)

@Composable
fun BrandTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit,
) {
    MaterialTheme(
        colorScheme = if (darkTheme) DarkColors else LightColors,
        content = content,
    )
}
```

Use `primary` for key actions, `primaryContainer` for selected states, and `surface` for page backgrounds. Pair each color with its corresponding `on…` color for text and icons.

This is a curated palette; dark mode uses a lighter brand green for readability. Keep wallpaper-based dynamic color disabled if you want these brand colors to remain consistent.