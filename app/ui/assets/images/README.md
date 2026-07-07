# Nova AI Desktop Assistant
# Image Assets

This directory contains raster image assets used by the Nova AI Desktop Assistant UI.


## Purpose

Images are used for:

- Application branding
- Splash screen
- Empty states
- Illustrations
- Background visuals
- Promotional graphics


## Directory Structure


images/

├── branding/
│ ├── nova_logo.png
│ ├── nova_logo_dark.png
│ └── nova_logo_light.png
│
├── splash/
│ └── splash_screen.png
│
├── empty_states/
│ ├── empty_chat.png
│ ├── empty_files.png
│ └── empty_history.png
│
└── backgrounds/
└── gradient_background.png



## Image Guidelines

Supported formats:


PNG
WEBP
JPG


Preferred:


PNG
WEBP



## Resolution Guidelines

### Logos

Recommended:


256x256
512x512



### Splash Screen

Recommended:


1920x1080



### Empty State Illustrations

Recommended:


600x400



## Optimization

Before adding images:

- Compress assets
- Remove unnecessary metadata
- Keep transparent backgrounds where required
- Avoid oversized files


## Loading

Images should be accessed through:


app/ui/resources.py


Do not load image paths directly inside widgets.


## Theme Support

Provide separate assets when required:


dark/
light/


Example:


nova_logo_dark.png
nova_logo_light.png



## Packaging

All image assets must be included in:


PyInstaller
.spec


during production packaging.