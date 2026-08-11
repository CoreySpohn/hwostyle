"""Style registry: maps mode names to merged rcParams and colormap dicts."""

from . import barbie, dark, light, paper
from ._shared import SHARED_CMAPS, SHARED_RC

MODE_RC = {
    "dark": dark.RC,
    "light": light.RC,
    "paper": paper.RC,
    "barbie": barbie.RC,
}

MODE_CMAPS = {
    "dark": {**SHARED_CMAPS, **dark.CMAPS},
    "light": {**SHARED_CMAPS, **light.CMAPS},
    "paper": {**SHARED_CMAPS, **paper.CMAPS},
    "barbie": {**SHARED_CMAPS, **barbie.CMAPS},
}

# Per-mode savefig policy as plain data. Downstream save helpers fetch this
# at call time; hwostyle itself never saves anything.
SAVE_DEFAULTS = {
    "dark": {
        "dpi": 300,
        "facecolor": "black",
        "transparent": False,
        "bbox_inches": "tight",
    },
    "light": {
        "dpi": 300,
        "facecolor": "white",
        "transparent": False,
        "bbox_inches": "tight",
    },
    "paper": {
        "dpi": 300,
        "facecolor": "white",
        "transparent": False,
        "bbox_inches": "tight",
    },
    "barbie": {
        "dpi": 300,
        "facecolor": "white",
        "transparent": False,
        "bbox_inches": "tight",
    },
}

__all__ = ["MODE_CMAPS", "MODE_RC", "SAVE_DEFAULTS", "SHARED_RC"]
