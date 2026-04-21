"""Tests for hwostyle palette and mode switching."""

import matplotlib.pyplot as plt

import hwostyle
from hwostyle.palettes import (
    BARBIE,
    BIOSIGNATURE,
    CYBERPUNK_DARK,
    CYBERPUNK_LIGHT,
    SPECTRAL,
    Palette,
)


class TestPalette:
    """Tests for the Palette class."""

    def test_dark_cyberpunk_colors(self):
        """Dark cyberpunk palette returns neon hex values."""
        p = Palette("dark")
        assert p.cyan == CYBERPUNK_DARK["cyan"]
        assert p.pink == CYBERPUNK_DARK["pink"]
        assert p.yellow == CYBERPUNK_DARK["yellow"]

    def test_light_cyberpunk_colors(self):
        """Light cyberpunk palette returns muted hex values."""
        p = Palette("light")
        assert p.cyan == CYBERPUNK_LIGHT["cyan"]
        assert p.pink == CYBERPUNK_LIGHT["pink"]

    def test_spectral_palette(self):
        """Spectral palette has emission line color names."""
        p = Palette("dark", family="spectral")
        assert p.oiii == SPECTRAL["oiii"]
        assert p.h_alpha == SPECTRAL["h_alpha"]
        assert len(p) == 6

    def test_biosignature_palette(self):
        """Biosignature palette has molecule color names."""
        p = Palette("light", family="biosignature")
        assert p.o2 == BIOSIGNATURE["o2"]
        assert p.h2o == BIOSIGNATURE["h2o"]
        assert p.ch4 == BIOSIGNATURE["ch4"]
        assert len(p) == 6

    def test_barbie_palette(self):
        """Barbie palette returns RdPu-sampled hex values."""
        p = Palette("barbie")
        assert len(p) == 5
        assert p[0] == BARBIE["blush"]
        assert p[2] == BARBIE["magenta"]

    def test_palette_length(self):
        """Palette has exactly 6 colors for cyberpunk."""
        p = Palette("dark")
        assert len(p) == 6

    def test_palette_indexing(self):
        """Palette supports integer indexing."""
        p = Palette("dark")
        assert p[0] == p.cyan

    def test_palette_string_indexing(self):
        """Palette supports string indexing."""
        p = Palette("dark", family="biosignature")
        assert p["o2"] == BIOSIGNATURE["o2"]

    def test_palette_iteration(self):
        """Palette is iterable."""
        p = Palette("dark")
        colors = list(p)
        assert len(colors) == 6

    def test_cycler_length(self):
        """Cycler contains the right number of colors."""
        p = Palette("dark")
        assert len(p.cycler) == 6

    def test_palette_names(self):
        """Palette exposes color names."""
        p = Palette("dark", family="spectral")
        assert "oiii" in p.names
        assert "h_alpha" in p.names

    def test_invalid_family_raises(self):
        """Invalid family name raises ValueError."""
        try:
            Palette("dark", family="rainbow")
            raise AssertionError("Should have raised ValueError")
        except ValueError:
            pass

    def test_invalid_attr_raises(self):
        """Accessing a nonexistent color by name raises AttributeError."""
        p = Palette("dark")
        try:
            _ = p.nonexistent_color
            raise AssertionError("Should have raised AttributeError")
        except AttributeError:
            pass

    def test_as_dict(self):
        """as_dict returns a name->hex mapping."""
        p = Palette("dark", family="biosignature")
        d = p.as_dict
        assert d["o2"] == BIOSIGNATURE["o2"]
        assert len(d) == 6


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

    def test_use_with_palette_family(self):
        """use() accepts a palette_family argument."""
        hwostyle.use("light", palette_family="spectral")
        assert hwostyle.palette.family == "spectral"
        assert hwostyle.palette.oiii == SPECTRAL["oiii"]

    def test_use_biosignature(self):
        """use() with biosignature palette sets correct colors."""
        hwostyle.use("dark", palette_family="biosignature")
        assert hwostyle.palette.family == "biosignature"
        assert hwostyle.palette.o2 == BIOSIGNATURE["o2"]
        assert len(hwostyle.palette) == 6

    def test_context_manager_restores(self):
        """Context manager restores previous mode."""
        hwostyle.use("dark")
        with hwostyle.light():
            assert plt.rcParams["figure.facecolor"] == "white"
        assert plt.rcParams["figure.facecolor"] == "black"

    def test_context_manager_restores_family(self):
        """Context manager restores previous palette family."""
        hwostyle.use("light", palette_family="spectral")
        with hwostyle.dark(palette_family="biosignature"):
            assert hwostyle.palette.family == "biosignature"
        assert hwostyle.palette.family == "spectral"

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
        assert hwostyle.palette.cyan == CYBERPUNK_DARK["cyan"]
        hwostyle.use("light")
        assert hwostyle.palette.cyan == CYBERPUNK_LIGHT["cyan"]
