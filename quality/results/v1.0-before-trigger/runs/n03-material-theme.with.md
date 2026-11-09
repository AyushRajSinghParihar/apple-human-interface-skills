Here’s a custom Material 3 theme with **#0B6E4F as the exact light-theme primary**, mint accents for dark mode, muted green secondary colors, and a blue tertiary accent.

| Color role | Light | Dark |
|---|---|---|
| Primary | `#0B6E4F` | `#75DBAE` |
| On primary | `#FFFFFF` | `#003825` |
| Primary container | `#91F5C8` | `#005138` |
| On primary container | `#002114` | `#91F5C8` |
| Secondary | `#4D6358` | `#B3CCBC` |
| On secondary | `#FFFFFF` | `#20352A` |
| Secondary container | `#CFE9D8` | `#364C40` |
| On secondary container | `#0B2116` | `#CFE9D8` |
| Tertiary | `#3D6373` | `#A5CDDF` |
| On tertiary | `#FFFFFF` | `#073543` |
| Tertiary container | `#C0E9FC` | `#244B5B` |
| On tertiary container | `#001F29` | `#C0E9FC` |

Paste this into your Compose theme file:

```kotlin
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val LightColors = lightColorScheme(
    primary = Color(0xFF0B6E4F),
    onPrimary = Color(0xFFFFFFFF),
    primaryContainer = Color(0xFF91F5C8),
    onPrimaryContainer = Color(0xFF002114),
    inversePrimary = Color(0xFF75DBAE),

    secondary = Color(0xFF4D6358),
    onSecondary = Color(0xFFFFFFFF),
    secondaryContainer = Color(0xFFCFE9D8),
    onSecondaryContainer = Color(0xFF0B2116),

    tertiary = Color(0xFF3D6373),
    onTertiary = Color(0xFFFFFFFF),
    tertiaryContainer = Color(0xFFC0E9FC),
    onTertiaryContainer = Color(0xFF001F29),

    background = Color(0xFFF5FBF5),
    onBackground = Color(0xFF171D19),
    surface = Color(0xFFF5FBF5),
    onSurface = Color(0xFF171D19),
    surfaceVariant = Color(0xFFDCE5DD),
    onSurfaceVariant = Color(0xFF404943),
    surfaceTint = Color(0xFF0B6E4F),
    inverseSurface = Color(0xFF2C322D),
    inverseOnSurface = Color(0xFFEDF2EC),

    surfaceDim = Color(0xFFD6DBD5),
    surfaceBright = Color(0xFFF5FBF5),
    surfaceContainerLowest = Color(0xFFFFFFFF),
    surfaceContainerLow = Color(0xFFEFF5EF),
    surfaceContainer = Color(0xFFE9EFE9),
    surfaceContainerHigh = Color(0xFFE3E9E3),
    surfaceContainerHighest = Color(0xFFDDE4DE),

    outline = Color(0xFF707973),
    outlineVariant = Color(0xFFC0C9C1),
    scrim = Color(0xFF000000),

    error = Color(0xFFBA1A1A),
    onError = Color(0xFFFFFFFF),
    errorContainer = Color(0xFFFFDAD6),
    onErrorContainer = Color(0xFF410002),
)

private val DarkColors = darkColorScheme(
    primary = Color(0xFF75DBAE),
    onPrimary = Color(0xFF003825),
    primaryContainer = Color(0xFF005138),
    onPrimaryContainer = Color(0xFF91F5C8),
    inversePrimary = Color(0xFF0B6E4F),

    secondary = Color(0xFFB3CCBC),
    onSecondary = Color(0xFF20352A),
    secondaryContainer = Color(0xFF364C40),
    onSecondaryContainer = Color(0xFFCFE9D8),

    tertiary = Color(0xFFA5CDDF),
    onTertiary = Color(0xFF073543),
    tertiaryContainer = Color(0xFF244B5B),
    onTertiaryContainer = Color(0xFFC0E9FC),

    background = Color(0xFF0F1511),
    onBackground = Color(0xFFDDE4DE),
    surface = Color(0xFF0F1511),
    onSurface = Color(0xFFDDE4DE),
    surfaceVariant = Color(0xFF404943),
    onSurfaceVariant = Color(0xFFC0C9C1),
    surfaceTint = Color(0xFF75DBAE),
    inverseSurface = Color(0xFFDDE4DE),
    inverseOnSurface = Color(0xFF2C322D),

    surfaceDim = Color(0xFF0F1511),
    surfaceBright = Color(0xFF353B36),
    surfaceContainerLowest = Color(0xFF0A100C),
    surfaceContainerLow = Color(0xFF171D19),
    surfaceContainer = Color(0xFF1B211D),
    surfaceContainerHigh = Color(0xFF252B27),
    surfaceContainerHighest = Color(0xFF303631),

    outline = Color(0xFF8A938C),
    outlineVariant = Color(0xFF404943),
    scrim = Color(0xFF000000),

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

Use the matching `on…` role for text and icons on each color, following [Android’s Material 3 guidance](https://developer.android.com/develop/ui/compose/designsystems/material3). The accent pairs above were checked: primary, secondary, and tertiary text contrasts exceed **6:1** in both themes.

This keeps your brand palette consistent; enabling wallpaper-based dynamic color would replace it.