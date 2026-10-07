"""Planting density from spacing and layout (report section 3.8.3).

Layout is informational in the tool: the Woodland Carbon Code lookup table is
indexed by spacing, so layout changes the number of seedlings to procure but
not the per-hectare carbon figure.
"""

import math

HECTARE_M2 = 10_000


def trees_per_hectare(spacing_m: float, layout: str = "square") -> int:
    """Return trees per hectare for a given spacing (metres) and layout.

    square:      N = 10,000 / s^2
    triangular:  N = 10,000 / (s^2 * sqrt(3) / 2) = 20,000 / (s^2 * sqrt(3))
    """
    if spacing_m <= 0:
        raise ValueError("spacing must be positive")
    layout = layout.lower()
    if layout == "square":
        area_per_tree = spacing_m**2
    elif layout == "triangular":
        area_per_tree = spacing_m**2 * math.sqrt(3) / 2
    else:
        raise ValueError("layout must be 'square' or 'triangular'")
    return round(HECTARE_M2 / area_per_tree)
