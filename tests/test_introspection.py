"""Tests for mode introspection and save defaults."""

import subprocess
import sys

import hwostyle
from hwostyle.styles import MODE_RC, SAVE_DEFAULTS


def test_current_mode_none_before_use():
    """current_mode() is None in a fresh interpreter that never called use()."""
    code = "import hwostyle; print(hwostyle.current_mode())"
    out = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, check=True
    )
    assert out.stdout.strip() == "None"


def test_current_mode_tracks_use():
    """current_mode() reflects the most recent use() call."""
    hwostyle.use("light")
    assert hwostyle.current_mode() == "light"
    hwostyle.use("dark")
    assert hwostyle.current_mode() == "dark"


def test_context_manager_restores_mode():
    """A mode context manager restores the prior mode on exit."""
    hwostyle.use("dark")
    with hwostyle.light():
        assert hwostyle.current_mode() == "light"
    assert hwostyle.current_mode() == "dark"


def test_save_defaults_keys_and_modes():
    """SAVE_DEFAULTS covers every mode with the expected policy keys."""
    assert set(SAVE_DEFAULTS) == set(MODE_RC)
    for mode in SAVE_DEFAULTS:
        d = hwostyle.save_defaults(mode)
        assert set(d) == {"dpi", "facecolor", "transparent", "bbox_inches"}


def test_save_defaults_follows_active_mode():
    """save_defaults() with no argument follows the active mode."""
    hwostyle.use("dark")
    assert hwostyle.save_defaults()["facecolor"] == "black"
    hwostyle.use("light")
    assert hwostyle.save_defaults()["facecolor"] == "white"


def test_save_defaults_light_fallback_before_use():
    """save_defaults() falls back to light before any use() call."""
    code = "import hwostyle; print(hwostyle.save_defaults()['facecolor'])"
    out = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, check=True
    )
    assert out.stdout.strip() == "white"


def test_save_defaults_returns_copy():
    """save_defaults() returns a copy; mutating it does not alter the policy."""
    d = hwostyle.save_defaults("dark")
    d["dpi"] = 1
    assert hwostyle.save_defaults("dark")["dpi"] != 1
