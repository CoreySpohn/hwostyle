"""Domain-specific colormap registry for HWO figures."""

from matplotlib.colors import LinearSegmentedColormap

from .palette import DARK_COLORS, LIGHT_COLORS

# --- Custom colormaps built from the brand palette ---

_hwo_intensity_dark = LinearSegmentedColormap.from_list(
    "hwo_intensity_dark",
    ["#000000", DARK_COLORS["cyan"], "#FFFFFF"],
    N=256,
)

_hwo_intensity_light = LinearSegmentedColormap.from_list(
    "hwo_intensity_light",
    ["#FFFFFF", LIGHT_COLORS["cyan"], "#000000"],
    N=256,
)

_hwo_diverging_dark = LinearSegmentedColormap.from_list(
    "hwo_diverging_dark",
    [DARK_COLORS["pink"], "#000000", DARK_COLORS["cyan"]],
    N=256,
)

_hwo_diverging_light = LinearSegmentedColormap.from_list(
    "hwo_diverging_light",
    [LIGHT_COLORS["pink"], "#FFFFFF", LIGHT_COLORS["cyan"]],
    N=256,
)


class Colormaps:
    """Mode-aware colormap registry with semantic names.

    Access colormaps by their intended use rather than by name. The returned
    colormap depends on the current mode (dark or light).

    Colormap categories:
        - **intensity**: PSF images, focal plane count rates, throughput maps.
          Perceptually uniform, monotonic lightness.
        - **high_dynamic_range**: Stellar intensity, coronagraph images spanning
          5+ decades. High contrast over extreme ranges.
        - **residual**: Difference images, signed error maps. Diverging with
          a clear zero crossing.
        - **phase**: Wavefront error, position angles. Cyclic/periodic, wraps
          smoothly at boundaries.
        - **mask**: Aperture masks, boolean maps, sky transmission.
          Two-tone, high contrast.
        - **probability**: Completeness, detection probability, SNR maps.
          Intuitive (0 = bad, 1 = good), print-safe.
        - **brand_intensity**: Custom sequential cmap built from the brand
          palette colors.
        - **brand_diverging**: Custom diverging cmap (pink-to-cyan) through
          black (dark) or white (light).
    """

    def __init__(self, mode="dark"):
        """Initialize colormaps for the given mode.

        Args:
            mode: Either "dark", "light", or "barbie".
        """
        self._mode = mode

    @property
    def intensity(self):
        """Sequential cmap for PSF images and focal plane intensities."""
        cmap_map = {"dark": "magma", "light": "viridis", "barbie": "RdPu"}
        return cmap_map[self._mode]

    @property
    def high_dynamic_range(self):
        """Sequential cmap for data spanning many decades."""
        cmap_map = {"dark": "inferno", "light": "cividis", "barbie": "RdPu"}
        return cmap_map[self._mode]

    @property
    def residual(self):
        """Diverging cmap for difference images and signed errors."""
        return "RdBu_r"

    @property
    def phase(self):
        """Cyclic cmap for phase maps and wavefront error."""
        return "twilight"

    @property
    def mask(self):
        """Two-tone cmap for binary masks and apertures."""
        if self._mode == "dark":
            return LinearSegmentedColormap.from_list(
                "hwo_mask_dark", ["#000000", DARK_COLORS["cyan"]], N=2
            )
        if self._mode == "barbie":
            return LinearSegmentedColormap.from_list(
                "hwo_mask_barbie", ["#FFFFFF", "#D42A92"], N=2
            )
        return LinearSegmentedColormap.from_list(
            "hwo_mask_light", ["#FFFFFF", LIGHT_COLORS["cyan"]], N=2
        )

    @property
    def probability(self):
        """Sequential cmap for probabilities, completeness, SNR."""
        cmap_map = {"dark": "plasma", "light": "YlOrRd_r", "barbie": "RdPu"}
        return cmap_map[self._mode]

    @property
    def brand_intensity(self):
        """Custom sequential cmap from the brand palette."""
        if self._mode == "dark":
            return _hwo_intensity_dark
        return _hwo_intensity_light

    @property
    def brand_diverging(self):
        """Custom diverging cmap (pink-to-cyan) from the brand palette."""
        if self._mode == "dark":
            return _hwo_diverging_dark
        return _hwo_diverging_light

    def __repr__(self):
        """String representation."""
        return f"Colormaps(mode='{self._mode}')"
