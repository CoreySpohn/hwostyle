"""hwostyle: Matplotlib style sheets and utilities for HWO figures.

Provides a dual-mode (dark/light/barbie) visual style with consistent colors,
colormaps, and rcParams for talks and papers.

Usage::

    import hwostyle

    # Switch to paper mode
    hwostyle.use("light")

    # Switch to talk mode
    hwostyle.use("dark")

    # Access colors and colormaps
    hwostyle.palette.cyan
    hwostyle.cmaps.intensity
"""

from contextlib import contextmanager

import matplotlib.pyplot as plt
from cycler import cycler

from .colormaps import Colormaps
from .palette import Palette

try:
    from ._version import __version__
except ModuleNotFoundError:
    __version__ = "0.0.0.dev"

# Global state
_current_mode = "dark"
palette = Palette("dark")
cmaps = Colormaps("dark")

# --- rcParams definitions ---

_SHARED_RC = {
    "font.family": "sans-serif",
    "font.sans-serif": ["Inter", "Helvetica", "Arial"],
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 13,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 10,
    "figure.titlesize": 16,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.figsize": (7, 5),
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
}

_DARK_RC = {
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

_LIGHT_RC = {
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": "#333333",
    "axes.labelcolor": "black",
    "text.color": "black",
    "xtick.color": "black",
    "ytick.color": "black",
    "grid.color": "#cccccc",
    "legend.facecolor": "white",
    "legend.edgecolor": "#999999",
    "legend.labelcolor": "black",
    "lines.linewidth": 1.5,
}

_BARBIE_RC = {
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": "#333333",
    "axes.labelcolor": "black",
    "text.color": "black",
    "xtick.color": "black",
    "ytick.color": "black",
    "grid.color": "#cccccc",
    "legend.facecolor": "white",
    "legend.edgecolor": "#999999",
    "legend.labelcolor": "black",
    "lines.linewidth": 1.0,
    "font.family": "serif",
    "font.size": 12,
    "axes.labelsize": 16,
    "axes.titlesize": 16,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 14,
    "image.cmap": "RdPu",
}


def use(mode):
    """Switch the global style mode.

    Args:
        mode: Either "dark" (talks, posters) or "light" (papers, print).

    Raises:
        ValueError: If mode is not "dark" or "light".
    """
    global _current_mode, palette, cmaps

    if mode not in ("dark", "light", "barbie"):
        msg = f"Mode must be 'dark', 'light', or 'barbie', got '{mode}'"
        raise ValueError(msg)

    _current_mode = mode
    palette = Palette(mode)
    cmaps = Colormaps(mode)

    rc = {**_SHARED_RC}
    mode_rc = {"dark": _DARK_RC, "light": _LIGHT_RC, "barbie": _BARBIE_RC}
    rc.update(mode_rc[mode])

    rc["axes.prop_cycle"] = cycler(color=palette.as_list)
    plt.rcParams.update(rc)


@contextmanager
def dark():
    """Context manager for dark mode. Restores previous mode on exit.

    Usage::

        with hwo_style.dark():
            fig, ax = plt.subplots()
            ax.plot(x, y)
    """
    previous = _current_mode
    use("dark")
    try:
        yield
    finally:
        use(previous)


@contextmanager
def light():
    """Context manager for light mode. Restores previous mode on exit.

    Usage::

        with hwo_style.light():
            fig, ax = plt.subplots()
            ax.plot(x, y)
    """
    previous = _current_mode
    use("light")
    try:
        yield
    finally:
        use(previous)


@contextmanager
def barbie():
    """Context manager for barbie mode. Restores previous mode on exit.

    Usage::

        with hwo_style.barbie():
            fig, ax = plt.subplots()
            ax.plot(x, y)
    """
    previous = _current_mode
    use("barbie")
    try:
        yield
    finally:
        use(previous)


__all__ = [
    "barbie",
    "cmaps",
    "dark",
    "light",
    "palette",
    "use",
]
