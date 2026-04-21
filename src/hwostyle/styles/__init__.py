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

__all__ = ["MODE_CMAPS", "MODE_RC", "SHARED_RC"]
