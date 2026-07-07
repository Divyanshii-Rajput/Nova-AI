# Nova AI Desktop Assistant
# SVG Icon Assets

This directory contains SVG assets used by the Nova AI Desktop Assistant UI.

## Design Guidelines

All icons should follow:

- SVG format
- Vector based
- Transparent background
- 24x24 default viewport
- Consistent stroke width
- Minimal visual complexity
- Dark/light theme compatibility


## Directory Structure
icons/

├── navigation/
│ ├── home.svg
│ ├── chat.svg
│ ├── browser.svg
│ ├── files.svg
│ ├── music.svg
│ ├── history.svg
│ ├── settings.svg
│ └── about.svg
│
├── actions/
│ ├── search.svg
│ ├── send.svg
│ ├── copy.svg
│ ├── close.svg
│ ├── refresh.svg
│ └── download.svg
│
├── assistant/
│ ├── robot.svg
│ ├── microphone.svg
│ ├── speaker.svg
│ └── brain.svg
│
└── system/
├── success.svg
├── warning.svg
├── error.svg
└── info.svg



## Naming Convention

Use:
lowercase-name.svg


Examples:


microphone.svg
window-close.svg
arrow-left.svg



## Color Rules

Avoid hardcoded colors whenever possible.

Preferred:

```svg
currentColor

Example:

<path
    fill="currentColor"
    d="..."
/>

This allows:

Dark theme support
Light theme support
Dynamic recoloring
Optimization

Before adding icons:

Remove unnecessary metadata
Minify paths
Keep file size small
Preserve accessibility attributes
Usage

Icons are loaded through:

app/ui/resources.py

Never load SVG files directly inside widgets.
