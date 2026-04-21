"""Shared defaults applied to all style modes.

Each style file can override any key from SHARED_RC or SHARED_CMAPS.
Missing keys fall back to these defaults.
"""

SHARED_RC = {
    "font.family": "sans-serif",
    "font.sans-serif": ["Inter", "Helvetica", "Arial"],
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 13,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 10,
    "figure.titlesize": 16,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
}

SHARED_CMAPS = {
    "intensity": "viridis",
    "high_dynamic_range": "inferno",
    "residual": "RdBu_r",
    "phase": "twilight",
    "probability": "YlOrRd_r",
    "mask": ["#FFFFFF", "#0097A7"],
    "brand_intensity": ["#FFFFFF", "#0097A7", "#000000"],
    "brand_diverging": ["#C2185B", "#FFFFFF", "#0097A7"],
}
