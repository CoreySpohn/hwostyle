"""Tests for hwostyle palette and mode switching."""

import matplotlib.pyplot as plt

import hwostyle
from hwostyle.palette import BARBIE_COLORS, DARK_COLORS, LIGHT_COLORS, Palette


class TestPalette:
    """Tests for the Palette class."""

    def test_dark_palette_colors(self):
        """Dark palette returns neon hex values."""
        p = Palette("dark")
        assert p.cyan == DARK_COLORS["cyan"]
        assert p.pink == DARK_COLORS["pink"]
        assert p.yellow == DARK_COLORS["yellow"]

    def test_light_palette_colors(self):
        """Light palette returns muted hex values."""
        p = Palette("light")
        assert p.cyan == LIGHT_COLORS["cyan"]
        assert p.pink == LIGHT_COLORS["pink"]
        assert p.yellow == LIGHT_COLORS["yellow"]

    def test_barbie_palette_colors(self):
        """Barbie palette returns RdPu-sampled hex values."""
        p = Palette("barbie")
        assert len(p) == 5
        assert p[0] == BARBIE_COLORS["blush"]
        assert p[2] == BARBIE_COLORS["magenta"]

    def test_palette_length(self):
        """Palette has exactly 6 colors."""
        p = Palette("dark")
        assert len(p) == 6

    def test_palette_indexing(self):
        """Palette supports integer indexing."""
        p = Palette("dark")
        assert p[0] == p.cyan

    def test_palette_iteration(self):
        """Palette is iterable."""
        p = Palette("dark")
        colors = list(p)
        assert len(colors) == 6

    def test_cycler_length(self):
        """Cycler contains the right number of colors."""
        p = Palette("dark")
        assert len(p.cycler) == 6


class TestModes:
    """Tests for mode switching."""

    def test_use_dark(self):
        """use('dark') sets dark rcParams."""
        hwostyle.use("dark")
        assert plt.rcParams["figure.facecolor"] == "black"
        assert plt.rcParams["text.color"] == "white"

    def test_use_light(self):
        """use('light') sets light rcParams."""
        hwostyle.use("light")
        assert plt.rcParams["figure.facecolor"] == "white"
        assert plt.rcParams["text.color"] == "black"

    def test_use_barbie(self):
        """use('barbie') sets barbie rcParams."""
        hwostyle.use("barbie")
        assert plt.rcParams["figure.facecolor"] == "white"
        assert plt.rcParams["font.family"] == ["serif"]
        assert plt.rcParams["image.cmap"] == "RdPu"

    def test_context_manager_restores(self):
        """Context manager restores previous mode."""
        hwostyle.use("dark")
        with hwostyle.light():
            assert plt.rcParams["figure.facecolor"] == "white"
        assert plt.rcParams["figure.facecolor"] == "black"

    def test_barbie_context_manager(self):
        """Barbie context manager restores previous mode."""
        hwostyle.use("dark")
        with hwostyle.barbie():
            assert plt.rcParams["font.family"] == ["serif"]
            assert len(hwostyle.palette) == 5
        assert plt.rcParams["figure.facecolor"] == "black"
        assert len(hwostyle.palette) == 6

    def test_invalid_mode_raises(self):
        """Invalid mode raises ValueError."""
        try:
            hwostyle.use("neon")
            raise AssertionError("Should have raised ValueError")
        except ValueError:
            pass

    def test_palette_updates_on_mode_switch(self):
        """Global palette object updates when mode switches."""
        hwostyle.use("dark")
        assert hwostyle.palette.cyan == DARK_COLORS["cyan"]
        hwostyle.use("light")
        assert hwostyle.palette.cyan == LIGHT_COLORS["cyan"]
