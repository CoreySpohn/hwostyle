"""Core style engine for hwostyle.

Manages rcParams, mode switching, and global palette/colormap state.
"""

from contextlib import contextmanager

import matplotlib.pyplot as plt
from cycler import cycler

from .colormaps import Colormaps
from .palettes import Palette
from .styles import MODE_RC, SHARED_RC

# Global state
_current_mode = "dark"
_current_family = None
palette = Palette("dark")
cmaps = Colormaps("dark")


def use(mode, palette_family=None):
    """Switch the global style mode and optionally the palette family.

    Args:
        mode: One of "dark" (talks), "light" (papers), "paper" (tol-colors),
            or "barbie".
        palette_family: Palette family name. One of "cyberpunk", "spectral",
            "biosignature", "tol", or "barbie". Defaults to "cyberpunk" for
            dark/light, "tol" for paper, and "barbie" for barbie mode.

    Raises:
        ValueError: If mode or palette family is invalid.
    """
    global _current_mode, _current_family, palette, cmaps

    if mode not in MODE_RC:
        msg = f"Mode must be 'dark', 'light', or 'barbie', got '{mode}'"
        raise ValueError(msg)

    _current_mode = mode
    _current_family = palette_family
    palette = Palette(mode, family=palette_family)
    cmaps = Colormaps(mode)

    rc = {**SHARED_RC}
    rc.update(MODE_RC[mode])
    rc["axes.prop_cycle"] = cycler(color=palette.as_list)
    plt.rcParams.update(rc)


@contextmanager
def dark(palette_family=None):
    """Context manager for dark mode. Restores previous mode on exit."""
    prev_mode, prev_family = _current_mode, _current_family
    use("dark", palette_family)
    yield
    use(prev_mode, prev_family)


@contextmanager
def light(palette_family=None):
    """Context manager for light mode. Restores previous mode on exit."""
    prev_mode, prev_family = _current_mode, _current_family
    use("light", palette_family)
    yield
    use(prev_mode, prev_family)


@contextmanager
def barbie():
    """Context manager for barbie mode. Restores previous mode on exit."""
    prev_mode, prev_family = _current_mode, _current_family
    use("barbie")
    yield
    use(prev_mode, prev_family)


@contextmanager
def paper(palette_family=None):
    """Context manager for paper mode (tol-colors). Restores previous mode on exit."""
    prev_mode, prev_family = _current_mode, _current_family
    use("paper", palette_family)
    yield
    use(prev_mode, prev_family)
