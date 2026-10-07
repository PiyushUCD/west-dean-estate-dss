# Data tables

Result tables transcribed from the capstone report so the numbers can be checked and re-plotted. None of these files contain raw sponsor data, NATMAP polygons or the WCC lookup table.

| File | Report source | Contents |
|---|---|---|
| `polygon_inventory.csv` | Table 4.1 | Parcels by category after cleaning and deduplication |
| `soil_zones.csv` | Tables 4.2, §3.6 | Area per soil zone, NATMAP series, ESC grid reference, SMR/SNR |
| `species_palette.csv` | Table 4.3 | The 32 locked species with growth model, native status, ESC score |
| `growth_model_ranges.csv` | Table 4.4 | Valid spacing and yield class per WCC growth model |
| `planting_density.csv` | Table 3.2 | Trees per hectare by spacing, square vs triangular |
| `phase1_validation.csv` | Table 4.5 | Tool vs certified PIUs per vintage for the Phase 1 project |
| `scenario_summary.csv` | Tables 5.1–5.4 | Headline metrics for Scenarios A and B |
| `scenario_a_vintages.csv` | Table 5.6 | Scenario A PIUs, buffer and revenue by vintage |
| `scenario_b_vintages.csv` | Table 5.7 | Scenario B PIUs, buffer and revenue by vintage |
| `price_sensitivity.csv` | Table 5.5 | 100-year revenue at £10, £26.85 and £30 per tCO₂e |

Units: areas in hectares, carbon in tCO₂e, money in GBP. Figures are rounded as published; PIU and buffer columns were rounded independently, so a row can sit up to about 2 t off an exact 80/20 split.
