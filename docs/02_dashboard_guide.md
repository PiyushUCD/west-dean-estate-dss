# Dashboard guide

[← Back to README](../README.md) · [Methodology](01_methodology.md) · [Results](03_results.md) · [Species palette](04_species_palette.md) · [Data & governance](05_data_and_governance.md) · [Limitations](06_limitations_and_future_work.md) · [References](07_references.md)

<p align="center">
  <a href="https://public.tableau.com/app/profile/piyush.patil6025/viz/WestDeanEstateDSS/LandingPage">
    <img src="https://img.shields.io/badge/Open_the_live_tool-Tableau_Public-E97627?style=for-the-badge&logo=tableau&logoColor=white" alt="Open the live tool on Tableau Public">
  </a>
</p>

The workbook is a **five-dashboard funnel** that follows the order an estate planner makes decisions in. Each dashboard's choices feed the next, and every screen carries the same navigation panel so you can move back and forth freely.

```mermaid
flowchart LR
    L[Landing page] --> O[Overview<br/><i>how much land, where</i>]
    O --> M[Mix Configuration<br/><i>which species, how planted</i>]
    M --> C[CO₂<br/><i>how much carbon</i>]
    M --> F[Financials<br/><i>what it is worth</i>]
    C <--> F
```

> Screenshot values come from a sample configuration used while building the tool, not from Scenario A or B. The tool's default carbon price is £27; the report quotes the more precise WCC average of £26.85.

| | |
|---|---|
| **Parameters** | 166 in total: 4 soil-area parameters, 160 species parameters (32 species × area, spacing, yield class, management, layout), plus carbon price and analysis year |
| **Data sources** | `Base` (WCC lookup + per-species calculated fields), `sites` (384 parcels with soil and ESC attributes), `estate_boundary`, `soil_base_map`, `Sankey_Species_Detail` |
| **Guard-rails** | Soil areas are capped at each zone's plantable ceiling; spacing and yield-class menus only offer values that exist in the species' WCC growth model, so no impossible configuration can be entered |

---

## 1 · Landing page

<img src="../assets/dashboards/01_landing_page.jpg" alt="Landing page with the West Dean estate photograph and an Enter the Dashboard button" width="100%">

**Purpose:** orient and route. It carries no controls or results, only the tool's identity over a photograph of the estate and one call to action, **Enter the Dashboard**, which opens the Overview.

---

## 2 · Overview · estate map & sites

<img src="../assets/dashboards/02_overview.jpg" alt="Overview dashboard: satellite base map with selectable parcels, soil-area sliders, species suitability Sankey and a ranked list of selected sites" width="100%">

**Purpose:** decide how much of each soil zone to plant, and where. *(Owner: Piyush Patil)*

| Element | What it does |
|---|---|
| Header tiles | Available planting area (1,982.8 ha), number of selected sites, planned area |
| Estate map | The 384 plantable parcels over satellite imagery. Click a parcel, or Ctrl + click several, to add them to the scenario. Selections are pushed to the four soil-area parameters through Parameter Actions |
| Soil sliders | Optional manual area for Acid Loam, Chalk, Floodplain and Lime Loam, each capped at its ceiling |
| Trees Suitability Sankey | Flows from each soil to ESC suitability class, previewing what grows well before you configure species |
| Selection Sites | The selected parcels ranked by area, grouped by soil |

---

## 3 · Mix Configuration

<img src="../assets/dashboards/03_mix_configuration.jpg" alt="Mix Configuration dashboard: per-species rows for area, spacing, layout, yield class and thinning, with trees needed and a map of the selected chalk sites" width="100%">

**Purpose:** turn an area budget into a planting design. *(Owner: Dheeraj Chavan)*

| Element | What it does |
|---|---|
| Selected Soil Type | Switches between the four soils, so you configure 8 species at a time rather than 32 |
| Species rows | For each locked species: area (ha), spacing, layout (square / triangular), yield class, thinning (thinned / unthinned). Growth model and native status are shown under the name |
| Trees Needed | Live seedling count from area, spacing and layout (10,000 / s² or 20,000 / (s²√3) per hectare) |
| Area allocation bar | Shows how much of the soil's budget is still unallocated, or by how much it is over |
| Distribute Equally | Resets the eight species to an even split as a neutral starting point |
| Selected sites map | The parcels of the chosen soil, for spatial context |

---

## 4 · CO2 dashboard

<img src="../assets/dashboards/04_co2.jpg" alt="CO2 dashboard: estate cumulative sequestration curve, species treemap, per-species and per-soil sequestration curves with an analysis-year marker" width="100%">

**Purpose:** show the physical carbon outcome of the configured design. *(Shared build)*

| Element | What it does |
|---|---|
| Header tiles | Total trees planted, total CO₂ at the analysis year, % native species |
| Estate CO₂ curve | Gross cumulative sequestration across all soils and species |
| Treemap | Each species' share of sequestration at the analysis year |
| Per-soil species curves | The selected soil's eight species, one line each |
| CO₂ by soil type | The estate total split into the four soils |
| Analysis Year | Moves the dashed marker; default year 65 (after the steep growth phase, well inside the 100-year crediting period) |

---

## 5 · Financial outcomes

<img src="../assets/dashboards/05_financials.jpg" alt="Financials dashboard: total revenue, total PIUs and revenue per hectare tiles, cumulative PIU and buffer area chart, vintage table and claimable revenue bar chart with a carbon price slider" width="100%">

**Purpose:** convert carbon into indicative Pending Issuance Units and revenue. *(Owner: Mrunmayee Bhavsar)*

| Element | What it does |
|---|---|
| Header tiles | Total revenue, total PIUs to the project, revenue per hectare |
| Cumulative chart | PIUs plus buffer versus PIUs in vintage, over 100 years |
| Vintage table | PIUs and buffer at each of the 11 WCC verification years |
| Claimable revenue at year | Revenue released at each vintage, showing the year-25 / year-35 peak |
| Carbon price slider | £10 to £30 per tCO₂e; every figure on the page recomputes live |

---

## Using the tool in five minutes

1. Open the [live workbook](https://public.tableau.com/app/profile/piyush.patil6025/viz/WestDeanEstateDSS/LandingPage) and press **Enter the Dashboard**.
2. On **Overview**, Ctrl + click a handful of parcels, or drag a soil slider.
3. On **Configuration**, pick a soil, press **Distribute Equally**, then change one species' yield class and watch Trees Needed update.
4. Open **CO₂** and move **Analysis Year** to see how the curve flattens after year 50.
5. Open **Financial** and drag the **carbon price** from £10 to £30: revenue scales by exactly three.
