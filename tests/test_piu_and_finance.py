"""Check the reference implementation against the figures published in the report."""

import csv
from pathlib import Path

import pytest

from wcc_carbon import (
    VINTAGES,
    buffer_total,
    piu_by_vintage,
    piu_total,
    revenue,
    sensitivity_band,
    trees_per_hectare,
)

DATA = Path(__file__).resolve().parents[1] / "data"


def read(name):
    with open(DATA / name, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


# --- Planting density (Table 3.2) -------------------------------------------

@pytest.mark.parametrize("row", read("planting_density.csv"))
def test_density_table(row):
    s = float(row["spacing_m"])
    assert trees_per_hectare(s, "square") == int(row["square_trees_per_ha"])
    assert trees_per_hectare(s, "triangular") == int(row["triangular_trees_per_ha"])


def test_triangular_is_about_15_5_percent_denser():
    ratio = trees_per_hectare(2.5, "triangular") / trees_per_hectare(2.5, "square")
    assert ratio == pytest.approx(1.155, abs=0.001)


# --- PIU chain (section 3.8.6 worked example) ---------------------------------

def test_scenario_a_piu_total_matches_report():
    # 0.64 * 983,882 - 0.80 * 60 = 629,636
    assert round(piu_total(983_882)) == 629_636


def test_scenario_a_buffer_total_matches_report():
    assert round(buffer_total(983_882)) == 157_409


def test_scenario_b_totals_within_one_tonne():
    # Report figures are rounded to whole tonnes.
    assert piu_total(81_078) == pytest.approx(51_841, abs=1)
    assert buffer_total(81_078) == pytest.approx(12_961, abs=1)


def test_vintage_split_sums_to_total():
    # Synthetic monotone curve: Q(v) = 10,000 * v
    q = {v: 10_000.0 * v for v in VINTAGES}
    schedule = piu_by_vintage(q)
    assert sum(x["piu"] for x in schedule.values()) == pytest.approx(piu_total(q[100]))
    assert sum(x["buffer"] for x in schedule.values()) == pytest.approx(buffer_total(q[100]))


@pytest.mark.parametrize("name", ["scenario_a_vintages.csv", "scenario_b_vintages.csv"])
def test_published_vintages_keep_the_80_20_split(name):
    for row in read(name):
        piu, buf = int(row["piu_tco2e"]), int(row["buffer_tco2e"])
        # PIU and buffer columns are rounded independently in the Tableau export,
        # so a single row can sit up to ~2 t off the exact 80/20 split.
        assert buf == pytest.approx(piu / 4, abs=2)
        assert buf / (piu + buf) == pytest.approx(0.20, abs=0.001)


def test_published_vintage_totals():
    a = read("scenario_a_vintages.csv")
    b = read("scenario_b_vintages.csv")
    assert sum(int(r["piu_tco2e"]) for r in a) == 629_636
    assert sum(int(r["piu_tco2e"]) for r in b) == 51_841


# --- Phase 1 validation (Table 4.5) -------------------------------------------

def test_phase1_validation_within_one_tonne_every_vintage():
    rows = read("phase1_validation.csv")
    assert [int(r["vintage_year"]) for r in rows] == list(VINTAGES)
    for r in rows:
        # Table values are rounded to whole tonnes; the largest gap is 1 t at year 15.
        assert abs(int(r["tool_piu_tco2e"]) - int(r["certified_piu_tco2e"])) <= 1
    assert sum(int(r["certified_piu_tco2e"]) for r in rows) == 6_309


# --- Finance (section 3.9 and Table 5.5) -------------------------------------

def test_scenario_a_revenue_at_central_price():
    assert round(revenue(629_636)) == 16_905_727


def test_price_band_is_factor_of_three():
    band = sensitivity_band(629_636)
    assert band["high"] / band["low"] == pytest.approx(3.0)
    assert round(band["low"]) == 6_296_360
    assert round(band["high"]) == 18_889_080


def test_per_hectare_gap_and_cost_of_curation():
    a_rate = 629_636 / 1_982.76
    b_rate = 51_841 / 200
    assert round(a_rate, 1) == 317.6
    assert round(b_rate, 1) == 259.2
    assert 1 - b_rate / a_rate == pytest.approx(0.184, abs=0.001)
    extrapolated_b = revenue(b_rate * 1_982.76)
    assert extrapolated_b / 1e6 == pytest.approx(13.80, abs=0.01)
    assert (revenue(629_636) - extrapolated_b) / 1e6 == pytest.approx(3.11, abs=0.01)
