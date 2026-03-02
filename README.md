# hwostyle

Matplotlib style sheets and utilities for HWO direct imaging figures.

## Installation

```bash
pip install hwostyle
```

For development:
```bash
git clone https://github.com/CoreySpohn/hwostyle.git
cd hwostyle
pip install -e ".[dev,test]"
```

## Quick Start

```python
import hwostyle

# Switch to paper mode (white background, muted colors)
hwostyle.use("light")

# Switch to talk mode (black background, neon colors)
hwostyle.use("dark")

# Access the palette
colors = hwostyle.palette
colors.cyan   # '#08F7FE' in dark, '#0097A7' in light

# Use domain-specific colormaps
cmap = hwostyle.cmaps.intensity   # PSF images
cmap = hwostyle.cmaps.residual    # difference maps
cmap = hwostyle.cmaps.phase       # wavefront error
```

## Modes

| Feature | Dark (Talks) | Light (Papers) | Barbie |
|---------|-------------|----------------|--------|
| Background | Black | White | White |
| Colors | Neon (high saturation) | Muted (print-safe) | RdPu pinks |
| Line width | 2.5 | 1.5 | 1.0 |
| Font | Sans-serif | Sans-serif | Serif |
| Image cmap | `magma` | `viridis` | `RdPu` |

## Color Palette

| Name   | Dark         | Light       |
|--------|-------------|-------------|
| Cyan   | `#08F7FE`   | `#0097A7`   |
| Pink   | `#FE53BB`   | `#C2185B`   |
| Yellow | `#F5D300`   | `#F9A825`   |
| Green  | `#00FF41`   | `#2E7D32`   |
| Red    | `#FF0000`   | `#D32F2F`   |
| Purple | `#9467BD`   | `#7B1FA2`   |

### Barbie Palette

| Name    | Hex       |
|---------|-----------|
| Blush   | `#FAA6B7` |
| Rose    | `#F768A1` |
| Magenta | `#D42A92` |
| Berry   | `#9A017B` |
| Plum    | `#5E006F` |
