"""Gross-to-net-to-PIU crediting chain (report sections 3.8.4 to 3.8.6).

Notation follows the report:

    Q(t)  gross cumulative sequestration of the planting design, tCO2e
    C(t)  = 0.80 * Q(t)          model-precision reduction
    F(t)  = C(t) - L_b           net sequestration after the lumped
                                 baseline-and-leakage deduction L_b
    G(t)  = 0.20 * F(t)          cumulative buffer contribution
    PIU(v) = [F(v) - F(v-)] - [G(v) - G(v-)] = 0.80 * [F(v) - F(v-)]

Summed over the eleven WCC verification years this gives

    PIU_total = 0.80 * F(100) = 0.64 * Q(100) - 0.80 * L_b
"""

from typing import Mapping

MODEL_PRECISION_FACTOR = 0.80
BUFFER_RATE = 0.20
DEFAULT_BASELINE_LEAKAGE_TCO2E = 60.0  # from the certified Phase 1 record (-60.45, rounded)

VINTAGES = (5, 15, 25, 35, 45, 55, 65, 75, 85, 95, 100)


def net_sequestration(q_gross: float, l_b: float = DEFAULT_BASELINE_LEAKAGE_TCO2E) -> float:
    """F = 0.80 * Q - L_b."""
    return MODEL_PRECISION_FACTOR * q_gross - l_b


def piu_total(q_gross_100: float, l_b: float = DEFAULT_BASELINE_LEAKAGE_TCO2E) -> float:
    """Total claimable Pending Issuance Units over the 100-year duration."""
    return (1 - BUFFER_RATE) * net_sequestration(q_gross_100, l_b)


def buffer_total(q_gross_100: float, l_b: float = DEFAULT_BASELINE_LEAKAGE_TCO2E) -> float:
    """Total buffer contribution withheld over the 100-year duration."""
    return BUFFER_RATE * net_sequestration(q_gross_100, l_b)


def piu_by_vintage(
    q_cumulative: Mapping[int, float],
    l_b: float = DEFAULT_BASELINE_LEAKAGE_TCO2E,
) -> dict:
    """Split claimable PIUs and buffer across the WCC verification years.

    ``q_cumulative`` maps each vintage year to gross cumulative sequestration
    Q(v) in tCO2e. The one-off deduction L_b is taken at the first vintage, so
    the net value before the first verification is zero.

    Returns {vintage: {"piu": ..., "buffer": ...}}.
    """
    missing = [v for v in VINTAGES if v not in q_cumulative]
    if missing:
        raise KeyError(f"q_cumulative is missing vintages {missing}")

    schedule = {}
    previous_net = 0.0
    for v in VINTAGES:
        net = net_sequestration(q_cumulative[v], l_b)
        increment = net - previous_net
        schedule[v] = {
            "piu": (1 - BUFFER_RATE) * increment,
            "buffer": BUFFER_RATE * increment,
        }
        previous_net = net
    return schedule
