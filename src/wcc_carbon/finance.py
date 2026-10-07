"""Indicative carbon revenue and price sensitivity (report section 3.9).

The financial model is deliberately partial: it reports gross carbon revenue
only, before establishment, management and verification costs, grant income or
discounting.
"""

CENTRAL_PRICE_GBP = 26.85  # WCC published 2024 average PIU price, GBP per tCO2e
PRICE_LOW_GBP = 10.0
PRICE_HIGH_GBP = 30.0


def revenue(pius: float, price_gbp: float = CENTRAL_PRICE_GBP) -> float:
    """R = p * PIU."""
    if price_gbp < 0:
        raise ValueError("price must be non-negative")
    return price_gbp * pius


def sensitivity_band(
    pius: float,
    low: float = PRICE_LOW_GBP,
    central: float = CENTRAL_PRICE_GBP,
    high: float = PRICE_HIGH_GBP,
) -> dict:
    """Revenue at the low, central and high carbon price.

    Because revenue is linear in price, the high/low ratio equals
    high_price / low_price (a factor of three across the GBP 10 to 30 band).
    """
    return {
        "low": revenue(pius, low),
        "central": revenue(pius, central),
        "high": revenue(pius, high),
    }
