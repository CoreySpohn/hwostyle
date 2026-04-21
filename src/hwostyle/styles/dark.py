"""Dark mode: neon-on-black for talks and presentations."""

from ..palettes import CYBERPUNK_DARK

RC = {
    "figure.facecolor": "black",
    "axes.facecolor": "black",
    "axes.edgecolor": "#444444",
    "axes.labelcolor": "white",
    "text.color": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "grid.color": "#333333",
    "legend.facecolor": "#1a1a1a",
    "legend.edgecolor": "#444444",
    "legend.labelcolor": "white",
    "lines.linewidth": 2.5,
}

CMAPS = {
    "intensity": "magma",
    "probability": "plasma",
    "mask": ["#000000", CYBERPUNK_DARK["cyan"]],
    "brand_intensity": ["#000000", CYBERPUNK_DARK["cyan"], "#FFFFFF"],
    "brand_diverging": [CYBERPUNK_DARK["pink"], "#000000", CYBERPUNK_DARK["cyan"]],
}
