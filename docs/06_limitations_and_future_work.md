# Limitations and future work

[← Back to README](../README.md) · [Methodology](01_methodology.md) · [Dashboards](02_dashboard_guide.md) · [Results](03_results.md) · [Species palette](04_species_palette.md) · [Data & governance](05_data_and_governance.md) · [References](07_references.md)

The tool is a foundation, not a finished product. Every limitation below is stated in the report and each maps to a concrete extension.

## Limitations

| Limitation | Effect | Origin |
|---|---|---|
| **18 of 32 species share the generic SAB growth model** | Those species cannot be told apart on per-hectare carbon | WCC publishes no species-specific curves for them |
| **ESC uses the 1961–1990 climate baseline** | Suitability reflects past, not future, climate; the palette is not yet certification-ready under WCC v3.0 | Default of the free ESC web tool |
| **Locking rule trades suitability for diversity** | Some species sit on a soil where they score lower (e.g. Beech) | Deliberate design choice |
| **Establishment emissions fixed at the Phase 1 value (60 t)** | Under-states establishment emissions at scale by about 0.4 % of gross for Scenario A | Only validated estimate available for the estate |
| **Polygon inventory partly rests on visual judgement** | A second digitiser would get a similar but not identical parcel set | Manual digitisation in Google Earth |
| **Revenue only** | No costs, grants or discounting; figures are gross | Deliberate scoping |
| **Validated against one certified project** | Highest confidence lies within Phase 1's envelope (native broadleaves) | Only certified project on the estate |
| **Time-stamped inputs** | Prices and climate scenarios update; outputs are as of August 2026 | Nature of the data |

## Future work

### Before any Phase 2 WCC validation
* **Climate-adjusted ESC.** Re-query the four soil zones under UKCP18 medium- and high-emissions pathways and revise the locked palette.
* **Area-scaled establishment emissions.** Replace the fixed 60 t with a per-hectare rate (≈ 1.97 t/ha from Phase 1), or species-differentiated rates for broadleaves and conifers.

### Near term
* **Richer constraint mask:** protected areas, biodiversity priority zones, heritage exclusions, Agricultural Land Classification.
* **Power BI migration** of the visual layer, reading the same analytical tables, so the estate can edit it within its Microsoft licences.
* **A second validation** against a different WCC-certified project with conifers and different management.

### Longer term
* **Biodiversity net-gain module** using the Defra biodiversity metric, so designs compare on nature as well as carbon.
* **Cost module** (establishment, management, maintenance, verification) to report net return rather than gross revenue.
* **Prescriptive optimisation** that formalises the estate's own weights across carbon, ecology, cost and cash-flow timing.
