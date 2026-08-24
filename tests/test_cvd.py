"""Color-vision-deficiency simulation, so palette safety is measured not asserted."""

import pytest

from hwostyle import colors, palettes
from hwostyle.colors import cvd_safety_report, perceptual_distance, simulate_cvd


def test_severity_zero_is_the_identity():
    """A severity of zero must leave every color untouched."""
    for color in ("#C2185B", "#0097A7", "#F9A825"):
        assert simulate_cvd(color, "deuteranopia", 0.0).lower() == color.lower()


def test_red_and_green_converge_under_deuteranopia():
    """The defining property: the red-green axis collapses."""
    red = simulate_cvd("#FF0000", "deuteranopia")
    green = simulate_cvd("#00FF00", "deuteranopia")
    assert perceptual_distance(red, green) < perceptual_distance("#FF0000", "#00FF00")


def test_blue_survives_deuteranopia_but_not_tritanopia():
    """Deuteranopia spares the blue-yellow axis; tritanopia is the one that hits it."""
    blue, yellow = "#0000FF", "#FFFF00"
    normal = perceptual_distance(blue, yellow)
    deut = perceptual_distance(
        simulate_cvd(blue, "deuteranopia"), simulate_cvd(yellow, "deuteranopia")
    )
    trit = perceptual_distance(
        simulate_cvd(blue, "tritanopia"), simulate_cvd(yellow, "tritanopia")
    )
    assert deut > 0.5 * normal
    assert trit < deut


def test_unknown_deficiency_raises_naming_the_options():
    """An unknown deficiency names the valid ones rather than failing bare."""
    with pytest.raises(ValueError, match="deuteranopia"):
        simulate_cvd("#FFFFFF", "quadranopia")


def test_report_covers_normal_and_all_three_deficiencies():
    """The report is only useful if it covers every deficiency at once."""
    report = cvd_safety_report(["#0097A7", "#C2185B", "#F9A825"])
    assert set(report) == {"normal", "protanopia", "deuteranopia", "tritanopia"}
    assert all(isinstance(v, float) for v in report.values())
    # a deficiency can only merge colors, never separate them further
    assert all(report[k] <= report["normal"] + 1e-9 for k in report if k != "normal")


def test_a_deliberately_safe_palette_scores_better_than_a_red_green_one():
    """The report has to rank palettes, or it cannot be used to choose one."""
    red_green = ["#D62728", "#2CA02C", "#8C564B"]
    blue_yellow = ["#0173B2", "#DE8F05", "#000000"]
    assert min(cvd_safety_report(blue_yellow).values()) > min(
        cvd_safety_report(red_green).values()
    )


def test_unsafe_pairs_names_the_pair_not_just_a_minimum():
    """A minimum distance does not tell you which pair to retire; this does."""
    rows = colors.unsafe_pairs(["#000000", "#ffffff"], ["black", "white"])
    assert rows == []
    rows = colors.unsafe_pairs(["#2E7D32", "#D32F2F"], ["green", "red"])
    assert any(r["kind"] == "grayscale" for r in rows)


def test_light_palette_green_red_is_retired_for_paired_use():
    """The paper palette's worst pair, pinned so a repalette cannot hide it.

    green and red differ by 0.006 in relative luminance, so they are one gray
    in print, and they are also the worst protanopia pair. Any two-series
    comparison reaching for both is the commonest way to lose a figure to a
    photocopier. The rule is a redundant second channel, not a new palette.
    """
    light = palettes.CYBERPUNK_LIGHT
    rows = colors.unsafe_pairs(
        [light["green"], light["red"]], ["green", "red"], contrast_floor=3.0
    )
    gray = [r for r in rows if r["kind"] == "grayscale"]
    assert gray, "green/red must still register as grayscale-colliding"
    assert gray[0]["value"] < 1.1


def test_model_and_reference_roles_collide_in_the_light_palette():
    """Model (pink) against reference (green) is the commonest comparison made.

    Recorded rather than fixed: retiring the collision means a second channel
    on every model-vs-reference figure, not a role remap, because remapping
    would break every figure already built against these roles.
    """
    light = palettes.CYBERPUNK_LIGHT
    pink = light[palettes.ROLE_COLOR_NAMES["model"]]
    green = light[palettes.ROLE_COLOR_NAMES["reference"]]
    rows = colors.unsafe_pairs([pink, green], ["model", "reference"])
    assert any(r["kind"] == "grayscale" for r in rows)
