# Data sources and governance

[← Back to README](../README.md) · [Methodology](01_methodology.md) · [Dashboards](02_dashboard_guide.md) · [Results](03_results.md) · [Species palette](04_species_palette.md) · [Limitations](06_limitations_and_future_work.md) · [References](07_references.md)

## Datasets used in the project

| Dataset | Provider | Purpose | Vintage / scale | Licence |
|---|---|---|---|---|
| Estate boundary (GeoJSON) & cartographic map | West Dean Estate (sponsor) | Outer extent; digitisation guide | Supplied 2026 | Sponsor, commercially sensitive |
| Phase 1 Carbon Calculator V3.0 | West Dean Estate (sponsor) | Lookup table source; validation benchmark | Certified project | Sponsor, commercially sensitive |
| National Forest Inventory | Forestry Commission | Existing woodland extent | Current annual release | OGL |
| OS Open Map Local (Buildings, Roads) | Ordnance Survey | Built-structure exclusions | 2024 release | OGL |
| OS Open Greenspace / OpenStreetMap farmland | OS / OpenStreetMap | Agricultural parcels | Current release | OGL / ODbL |
| NATMAP National Soil Map | Cranfield University (LandIS) | Soil type, drainage, fertility | 1:250,000 | Academic licence, no redistribution |
| Ecological Site Classification | Forest Research | Species suitability scoring | 1961–1990 baseline | Public web tool |
| Woodland Carbon Code pricing | Scottish Forestry | Central carbon price £26.85 / t | 2024 data | Publicly published |
| England Woodland Creation Offer | Forestry Commission / Defra | Consulted for grant rates; excluded from model | 2024 rates | OGL |
| Defra Farm Business Survey | Defra | Consulted for opportunity cost; excluded | 2023 release | OGL |

## What this repository contains, and what it does not

| Included | Not included, and why |
|---|---|
| Dashboard screenshots, already public on Tableau Public | **Raw sponsor files** (boundary, cartographic map, Carbon Calculator): commercially sensitive, used solely for the project |
| Derived maps of the plantable inventory | **NATMAP soil polygons**: Cranfield's academic licence allows derived analysis, not redistribution. Only the four-zone derived product appears |
| Result tables transcribed from the report (`data/*.csv`) | **The WCC biomass lookup table**: published by Scottish Forestry for certification use; obtain it from the Code directly |
| The A1 poster | **The full capstone report**: contains sponsor-supplied material. Available from the authors on request |
| A tested reference implementation of the formulas (`src/`) | **The production Python scripts and `.twbx`**: they read the restricted inputs above |

## Ethics

The project used no personal data and involved no human participants. External datasets were used within their licence terms, and the tool's outputs are described throughout as indicative projections, not certified figures. Only a WCC-accredited validator can issue certified numbers.

## Licences in this repository

* **Code** (`src/`, `scripts/`, `tests/`): MIT, see [LICENSE](../LICENSE).
* **Report-derived content** (docs, data tables, figures, poster): © 2026 the authors, shared for reference and portfolio purposes. Please cite the project (see [CITATION.cff](../CITATION.cff)).
* **Third-party marks and imagery** (estate photograph, Mapbox / OpenStreetMap basemap tiles inside screenshots) remain with their owners.
