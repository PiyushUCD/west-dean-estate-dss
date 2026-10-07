"""Reference implementation of the West Dean afforestation decision-support arithmetic.

This package restates, in small tested functions, the formulas documented in
Chapter 3 of the capstone report:

* ``density``  - planting density from spacing and layout (section 3.8.3)
* ``piu``      - gross-to-net-to-PIU crediting chain and vintage schedule (3.8.4 to 3.8.6)
* ``finance``  - indicative revenue and price sensitivity (3.9)
* ``dedup``    - greedy non-maximum suppression for polygon deduplication (Algorithm 3.1)

It exists so readers can check the arithmetic behind the headline results. The
original analysis ran on the estate's own spatial data and the Woodland Carbon
Code biomass lookup table, neither of which is redistributed in this repository.
"""

from .density import trees_per_hectare
from .piu import (
    MODEL_PRECISION_FACTOR,
    BUFFER_RATE,
    VINTAGES,
    net_sequestration,
    piu_total,
    buffer_total,
    piu_by_vintage,
)
from .finance import revenue, sensitivity_band

__all__ = [
    "trees_per_hectare",
    "MODEL_PRECISION_FACTOR",
    "BUFFER_RATE",
    "VINTAGES",
    "net_sequestration",
    "piu_total",
    "buffer_total",
    "piu_by_vintage",
    "revenue",
    "sensitivity_band",
]
