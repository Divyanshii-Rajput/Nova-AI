# Nova AI Desktop Assistant
# Font Assets

This directory contains font resources used by the Nova AI Desktop Assistant UI.


## Recommended Fonts

Primary:


Segoe UI


Reason:

- Native Windows desktop font
- Excellent readability
- Supports Windows scaling
- Professional appearance


Fallback:


Inter
Roboto
Arial
Sans-serif



## Font Usage

Fonts are controlled through:


app/ui/styles/*.qss


Example:

```css
QWidget {
    font-family: "Segoe UI";
}
Font Files

If bundled fonts are required, place:

.ttf
.otf
.woff

files inside this directory.

Example:

fonts/

├── SegoeUI.ttf
├── Inter-Regular.ttf
├── Inter-Medium.ttf
└── Inter-Bold.ttf
Loading Fonts

Fonts should be registered during application startup using:

QFontDatabase.addApplicationFont()

before creating the main window.

Guidelines
Use limited font families.
Maintain consistent typography.
Avoid decorative fonts.
Ensure readability at different DPI settings.
Test with Windows display scaling:
100%
125%
150%
200%