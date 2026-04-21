"""hwostyle: Matplotlib styles, palettes, and colormaps for HWO.

Usage::

    import hwostyle

    hwostyle.use("light")
    hwostyle.use("dark", palette_family="biosignature")

    hwostyle.palette.o2
    hwostyle.cmaps.intensity

    # Color utilities
    from hwostyle.colors import wavelength_to_rgb, contrast_ratio
"""

from . import colors, core
from .core import barbie, dark, light, paper, use

try:
    from ._version import __version__
except ModuleNotFoundError:
    __version__ = "0.0.0.dev"


def __getattr__(name):
    """Forward ``palette`` and ``cmaps`` to the live core state."""
    if name in ("palette", "cmaps"):
        return getattr(core, name)
    raise AttributeError(f"module 'hwostyle' has no attribute {name!r}")


__all__ = [
    "barbie",
    "cmaps",
    "colors",
    "dark",
    "light",
    "palette",
    "paper",
    "use",
]
