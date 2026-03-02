"""Color palette definitions for hwo-style."""

from cycler import cycler

# Dark mode: cyberpunk neons for talks, posters, animations
DARK_COLORS = {
    "cyan": "#08F7FE",
    "pink": "#FE53BB",
    "yellow": "#F5D300",
    "green": "#00FF41",
    "red": "#FF0000",
    "purple": "#9467BD",
}

# Light mode: de-saturated variants for papers and print
LIGHT_COLORS = {
    "cyan": "#0097A7",
    "pink": "#C2185B",
    "yellow": "#F9A825",
    "green": "#2E7D32",
    "red": "#D32F2F",
    "purple": "#7B1FA2",
}

# Barbie mode: RdPu-sampled pinks for a collaborator's visual style
BARBIE_COLORS = {
    "blush": "#FAA6B7",
    "rose": "#F768A1",
    "magenta": "#D42A92",
    "berry": "#9A017B",
    "plum": "#5E006F",
}


class Palette:
    """Mode-aware color palette.

    Provides named color access and a matplotlib cycler for the current mode.

    Attributes:
        cyan: Primary color.
        pink: Secondary color.
        yellow: Tertiary color.
        green: Quaternary color.
        red: Error / alert color.
        purple: Sixth series color.
    """

    def __init__(self, mode="dark"):
        """Initialize palette for the given mode.

        Args:
            mode: Either "dark", "light", or "barbie".
        """
        self._mode = mode
        color_map = {
            "dark": DARK_COLORS,
            "light": LIGHT_COLORS,
            "barbie": BARBIE_COLORS,
        }
        self._colors = color_map[mode]

    @property
    def mode(self):
        """Current mode name."""
        return self._mode

    @property
    def cyan(self):
        """Primary color."""
        return self._colors["cyan"]

    @property
    def pink(self):
        """Secondary color."""
        return self._colors["pink"]

    @property
    def yellow(self):
        """Tertiary color."""
        return self._colors["yellow"]

    @property
    def green(self):
        """Quaternary color."""
        return self._colors["green"]

    @property
    def red(self):
        """Error / alert color."""
        return self._colors["red"]

    @property
    def purple(self):
        """Sixth series color."""
        return self._colors["purple"]

    @property
    def as_list(self):
        """All colors as a list in canonical order."""
        return list(self._colors.values())

    @property
    def cycler(self):
        """Matplotlib color cycler for the current palette."""
        return cycler(color=self.as_list)

    def __getitem__(self, idx):
        """Access color by index."""
        return self.as_list[idx]

    def __iter__(self):
        """Iterate over colors."""
        return iter(self.as_list)

    def __len__(self):
        """Number of colors in the palette."""
        return len(self._colors)

    def __repr__(self):
        """String representation."""
        return f"Palette(mode='{self._mode}', colors={self.as_list})"
