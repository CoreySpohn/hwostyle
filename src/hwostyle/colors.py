"""Color utilities for hwostyle.

Wavelength-to-color conversions, perceptual color manipulation,
hex/RGB interop, and contrast helpers for building astronomy-aware
color palettes.
"""

import colorsys

import numpy as np

# ---------------------------------------------------------------------------
# Wavelength <-> RGB
# ---------------------------------------------------------------------------


def wavelength_to_rgb(wavelength_nm, gamma=0.8):
    """Convert a wavelength in nanometers to an sRGB (r, g, b) tuple.

    Uses Dan Bruton's piecewise-linear approximation of the CIE 1931
    color matching functions, with intensity roll-off at the edges of
    the visible range.

    Args:
        wavelength_nm: Wavelength in nanometers (380-780 for visible).
        gamma: Display gamma correction exponent.

    Returns:
        Tuple of (r, g, b) floats in [0, 1].  Returns (0.3, 0.3, 0.3)
        for wavelengths outside the visible range.
    """
    wl = float(wavelength_nm)

    if 380 <= wl < 440:
        r = -(wl - 440) / (440 - 380)
        g = 0.0
        b = 1.0
    elif 440 <= wl < 490:
        r = 0.0
        g = (wl - 440) / (490 - 440)
        b = 1.0
    elif 490 <= wl < 510:
        r = 0.0
        g = 1.0
        b = -(wl - 510) / (510 - 490)
    elif 510 <= wl < 580:
        r = (wl - 510) / (580 - 510)
        g = 1.0
        b = 0.0
    elif 580 <= wl < 645:
        r = 1.0
        g = -(wl - 645) / (645 - 580)
        b = 0.0
    elif 645 <= wl <= 780:
        r = 1.0
        g = 0.0
        b = 0.0
    else:
        return (0.3, 0.3, 0.3)

    # Intensity falloff at spectrum edges
    if 380 <= wl < 420:
        factor = 0.3 + 0.7 * (wl - 380) / (420 - 380)
    elif 645 < wl <= 780:
        factor = 0.3 + 0.7 * (780 - wl) / (780 - 645)
    else:
        factor = 1.0

    r = (r * factor) ** gamma
    g = (g * factor) ** gamma
    b = (b * factor) ** gamma
    return (r, g, b)


def wavelength_to_hex(wavelength_nm, gamma=0.8):
    """Convert a wavelength in nanometers to a hex color string.

    Convenience wrapper around :func:`wavelength_to_rgb`.

    Args:
        wavelength_nm: Wavelength in nanometers.
        gamma: Display gamma correction exponent.

    Returns:
        Hex color string like ``'#e84855'``.
    """
    return rgb_to_hex(wavelength_to_rgb(wavelength_nm, gamma=gamma))


# ---------------------------------------------------------------------------
# Format conversions
# ---------------------------------------------------------------------------


def rgb_to_hex(rgb):
    """Convert an (r, g, b) float tuple to a hex color string.

    Args:
        rgb: Tuple of floats in [0, 1].

    Returns:
        Hex string like ``'#4a90d9'``.
    """
    r, g, b = (max(0.0, min(1.0, c)) for c in rgb)
    ri, gi, bi = int(r * 255), int(g * 255), int(b * 255)
    return f"#{ri:02x}{gi:02x}{bi:02x}"


def hex_to_rgb(hex_color):
    """Convert a hex color string to an (r, g, b) float tuple.

    Args:
        hex_color: String like ``'#4a90d9'`` or ``'4a90d9'``.

    Returns:
        Tuple of (r, g, b) floats in [0, 1].
    """
    h = hex_color.lstrip("#")
    return tuple(int(h[i : i + 2], 16) / 255.0 for i in (0, 2, 4))


# ---------------------------------------------------------------------------
# Perceptual color manipulation
# ---------------------------------------------------------------------------


def adjust_saturation(hex_color, factor):
    """Scale a color's saturation while preserving hue and lightness.

    Args:
        hex_color: Input color as hex string.
        factor: Multiplicative factor.  ``0.5`` halves saturation,
            ``1.5`` boosts it by 50%.

    Returns:
        Adjusted hex color string.
    """
    r, g, b = hex_to_rgb(hex_color)
    h, lit, s = colorsys.rgb_to_hls(r, g, b)
    s = max(0.0, min(1.0, s * factor))
    r2, g2, b2 = colorsys.hls_to_rgb(h, lit, s)
    return rgb_to_hex((r2, g2, b2))


def adjust_lightness(hex_color, factor):
    """Scale a color's lightness while preserving hue and saturation.

    Args:
        hex_color: Input color as hex string.
        factor: Multiplicative factor.  ``0.7`` darkens, ``1.3`` lightens.

    Returns:
        Adjusted hex color string.
    """
    r, g, b = hex_to_rgb(hex_color)
    h, lit, s = colorsys.rgb_to_hls(r, g, b)
    lit = max(0.0, min(1.0, lit * factor))
    r2, g2, b2 = colorsys.hls_to_rgb(h, lit, s)
    return rgb_to_hex((r2, g2, b2))


def shift_hue(hex_color, degrees):
    """Rotate a color's hue by a given number of degrees on the color wheel.

    Args:
        hex_color: Input color as hex string.
        degrees: Hue rotation in degrees (0-360).  Positive = clockwise.

    Returns:
        Adjusted hex color string.
    """
    r, g, b = hex_to_rgb(hex_color)
    h, lit, s = colorsys.rgb_to_hls(r, g, b)
    h = (h + degrees / 360.0) % 1.0
    r2, g2, b2 = colorsys.hls_to_rgb(h, lit, s)
    return rgb_to_hex((r2, g2, b2))


# ---------------------------------------------------------------------------
# Contrast and accessibility
# ---------------------------------------------------------------------------


def relative_luminance(hex_color):
    """Compute the WCAG 2.0 relative luminance of a color.

    Uses the sRGB linearization and standard luminance coefficients.

    Args:
        hex_color: Color as hex string.

    Returns:
        Luminance as a float in [0, 1].
    """
    r, g, b = hex_to_rgb(hex_color)

    def linearize(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def contrast_ratio(hex_a, hex_b):
    """Compute the WCAG 2.0 contrast ratio between two colors.

    A ratio >= 4.5 is required for normal text; >= 3.0 for large text.

    Args:
        hex_a: First color as hex string.
        hex_b: Second color as hex string.

    Returns:
        Contrast ratio as a float >= 1.0.
    """
    lum_a = relative_luminance(hex_a)
    lum_b = relative_luminance(hex_b)
    lighter = max(lum_a, lum_b)
    darker = min(lum_a, lum_b)
    return (lighter + 0.05) / (darker + 0.05)


def text_color_for_background(hex_bg, light="#ffffff", dark="#000000"):
    """Choose black or white text for maximum contrast on a background.

    Args:
        hex_bg: Background color as hex string.
        light: Color to return for dark backgrounds.
        dark: Color to return for light backgrounds.

    Returns:
        Either *light* or *dark* hex string.
    """
    return light if relative_luminance(hex_bg) < 0.4 else dark


# ---------------------------------------------------------------------------
# Palette analysis
# ---------------------------------------------------------------------------


def perceptual_distance(hex_a, hex_b):
    """Approximate perceptual distance between two colors in CIELAB space.

    Uses a simplified conversion to L*a*b* (D65 illuminant) and returns
    the Euclidean distance.  Good enough for palette design; not intended
    for colorimetric precision.

    Args:
        hex_a: First color as hex string.
        hex_b: Second color as hex string.

    Returns:
        Approximate Delta-E distance (larger = more distinguishable).
    """
    lab_a = _hex_to_lab(hex_a)
    lab_b = _hex_to_lab(hex_b)
    return float(np.sqrt(sum((a - b) ** 2 for a, b in zip(lab_a, lab_b, strict=True))))


def min_perceptual_distance(hex_colors):
    """Find the minimum pairwise perceptual distance in a color list.

    Useful for checking whether all colors in a palette are
    distinguishable.  A minimum distance below ~20 suggests
    two colors may be confused.

    Args:
        hex_colors: List of hex color strings.

    Returns:
        Tuple of (min_distance, color_a, color_b).
    """
    best = (float("inf"), None, None)
    for i, a in enumerate(hex_colors):
        for b in hex_colors[i + 1 :]:
            d = perceptual_distance(a, b)
            if d < best[0]:
                best = (d, a, b)
    return best


def pairwise_distances(hex_colors, names=None):
    """Compute pairwise perceptual distance matrix for a list of colors.

    Args:
        hex_colors: List of hex color strings.
        names: Optional list of labels (same length as hex_colors).

    Returns:
        Dict with keys: ``'matrix'`` (2D numpy array), ``'labels'``
        (list of labels), ``'min'`` (minimum off-diagonal distance).
    """
    n = len(hex_colors)
    labels = names if names is not None else hex_colors
    mat = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            d = perceptual_distance(hex_colors[i], hex_colors[j])
            mat[i, j] = d
            mat[j, i] = d
    off_diag = mat[np.triu_indices(n, k=1)]
    return {
        "matrix": mat,
        "labels": list(labels),
        "min": float(np.min(off_diag)) if len(off_diag) > 0 else 0.0,
    }


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _hex_to_lab(hex_color):
    """Convert hex to approximate CIELAB (L*, a*, b*) under D65."""
    r, g, b = hex_to_rgb(hex_color)

    # sRGB -> linear RGB
    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    rl, gl, bl = lin(r), lin(g), lin(b)

    # Linear RGB -> XYZ (D65)
    x = 0.4124564 * rl + 0.3575761 * gl + 0.1804375 * bl
    y = 0.2126729 * rl + 0.7151522 * gl + 0.0721750 * bl
    z = 0.0193339 * rl + 0.1191920 * gl + 0.9503041 * bl

    # D65 reference white
    xn, yn, zn = 0.95047, 1.0, 1.08883

    def f(t):
        delta = 6.0 / 29.0
        if t > delta**3:
            return t ** (1.0 / 3.0)
        return t / (3 * delta**2) + 4.0 / 29.0

    l_star = 116.0 * f(y / yn) - 16.0
    a_star = 500.0 * (f(x / xn) - f(y / yn))
    b_star = 200.0 * (f(y / yn) - f(z / zn))
    return (l_star, a_star, b_star)


_LMS_FROM_LINEAR_RGB = np.array(
    [
        [0.31399022, 0.63951294, 0.04649755],
        [0.15537241, 0.75789446, 0.08670142],
        [0.01775239, 0.10944209, 0.87256922],
    ]
)
_LINEAR_RGB_FROM_LMS = np.linalg.inv(_LMS_FROM_LINEAR_RGB)

# Brettel-Vienot-Mollon dichromat projections, in LMS.
_CVD_MATRICES = {
    "protanopia": np.array(
        [[0.0, 1.05118294, -0.05116099], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    ),
    "deuteranopia": np.array(
        [[1.0, 0.0, 0.0], [0.9513092, 0.0, 0.04866992], [0.0, 0.0, 1.0]]
    ),
    "tritanopia": np.array(
        [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [-0.86744736, 1.86727089, 0.0]]
    ),
}


def _srgb_to_linear(c):
    """Undo the sRGB transfer function."""
    c = np.asarray(c, float)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def _linear_to_srgb(c):
    """Apply the sRGB transfer function."""
    c = np.clip(np.asarray(c, float), 0.0, 1.0)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055)


def simulate_cvd(hex_color, kind, severity=1.0):
    """Simulate how a color appears to a viewer with a color vision deficiency.

    Between five and ten percent of readers have some deficiency, so a figure
    whose meaning rests on hue alone fails for roughly one viewer in a lecture
    room of twenty. That is checkable rather than a matter of taste, which is
    the point of having this function.

    Args:
        hex_color: Color as ``"#rrggbb"``.
        kind: One of ``"protanopia"``, ``"deuteranopia"``, ``"tritanopia"``.
        severity: 0 (unaffected) to 1 (full dichromacy). Intermediate values
            interpolate, standing in for the anomalous trichromacies.

    Returns:
        The simulated color as ``"#rrggbb"``.

    Raises:
        ValueError: If ``kind`` is not one of the three deficiencies.
    """
    if kind not in _CVD_MATRICES:
        raise ValueError(
            f"unknown deficiency {kind!r}: use one of {sorted(_CVD_MATRICES)}"
        )
    rgb = np.array(hex_to_rgb(hex_color), float)
    lms = _LMS_FROM_LINEAR_RGB @ _srgb_to_linear(rgb)
    simulated = _LINEAR_RGB_FROM_LMS @ (_CVD_MATRICES[kind] @ lms)
    out = _linear_to_srgb(simulated)
    blended = (1.0 - severity) * rgb + severity * out
    return rgb_to_hex(tuple(blended))


def cvd_safety_report(hex_colors, names=None, severity=1.0):
    """Minimum perceptual separation of a palette under each deficiency.

    Args:
        hex_colors: The palette to check.
        names: Optional names, for readable output.
        severity: Passed through to `simulate_cvd`.

    Returns:
        Dict keyed by ``"normal"`` and each deficiency, each holding the
        minimum pairwise perceptual distance (a float) over the palette.
    """
    report = {"normal": min_perceptual_distance(list(hex_colors))[0]}
    for kind in sorted(_CVD_MATRICES):
        shifted = [simulate_cvd(c, kind, severity) for c in hex_colors]
        report[kind] = min_perceptual_distance(shifted)[0]
    return report
