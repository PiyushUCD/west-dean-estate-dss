"""Rebuild the README result charts from the tables in data/.

Usage:  python scripts/make_charts.py
Output: assets/charts/*.png
"""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "assets" / "charts"
OUT.mkdir(parents=True, exist_ok=True)

# Palette validated for colour-vision deficiency (two-slot categorical, light surface).
GREEN = "#1b6e34"   # Scenario A / single-series default
GOLD = "#d9a21f"    # Scenario B
SURFACE = "#fcfcfb"
INK = "#1d2420"
INK_2 = "#55605a"
GRID = "#e4e7e2"

plt.rcParams.update(
    {
        "font.family": ["Inter", "DejaVu Sans"],
        "font.size": 11,
        "axes.edgecolor": GRID,
        "axes.labelcolor": INK_2,
        "axes.titlecolor": INK,
        "axes.titlesize": 14,
        "axes.titleweight": "semibold",
        "axes.titlelocation": "left",
        "axes.titlepad": 14,
        "xtick.color": INK_2,
        "ytick.color": INK_2,
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "legend.frameon": False,
    }
)


def read(name):
    with open(DATA / name, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def tidy(ax, grid_axis="y"):
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.grid(axis=grid_axis, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)


def subtitle(fig, text):
    fig.text(0.012, 0.015, text, color=INK_2, fontsize=9)


# 1. Plantable area by soil zone ----------------------------------------------
def soil_chart():
    rows = read("soil_zones.csv")
    names = [r["soil_zone"] for r in rows][::-1]
    areas = [float(r["area_ha"]) for r in rows][::-1]
    shares = [float(r["share_of_plantable_pct"]) for r in rows][::-1]

    fig, ax = plt.subplots(figsize=(8, 3.6), dpi=200)
    bars = ax.barh(names, areas, color=GREEN, height=0.56)
    for bar, a, s in zip(bars, areas, shares):
        ax.text(bar.get_width() + 18, bar.get_y() + bar.get_height() / 2,
                f"{a:,.1f} ha  ·  {s:.1f}%", va="center", color=INK, fontsize=10.5)
    ax.set_xlim(0, 2250)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.set_xlabel("Plantable area (hectares)")
    ax.set_title("Chalk is 92.9% of the 1,982.8 ha plantable inventory")
    tidy(ax, grid_axis="x")
    subtitle(fig, "Source: capstone report Table 4.2 (NATMAP series consolidated into four ESC soil zones).")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(OUT / "plantable_area_by_soil.png")
    plt.close(fig)


# 2. Share of 100-year PIUs issued at each verification year -------------------
def vintage_chart():
    a = read("scenario_a_vintages.csv")
    b = read("scenario_b_vintages.csv")
    years = [r["vintage_year"] for r in a]
    a_tot = sum(int(r["piu_tco2e"]) for r in a)
    b_tot = sum(int(r["piu_tco2e"]) for r in b)
    a_share = [100 * int(r["piu_tco2e"]) / a_tot for r in a]
    b_share = [100 * int(r["piu_tco2e"]) / b_tot for r in b]

    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=200)
    x = range(len(years))
    w = 0.38
    gap = 0.02
    ax.bar([i - w / 2 - gap for i in x], a_share, width=w, color=GREEN,
           label="Scenario A · full area, equal split")
    ax.bar([i + w / 2 + gap for i in x], b_share, width=w, color=GOLD,
           label="Scenario B · 200 ha, top-4 by ESC")
    i25 = years.index("25")
    ax.text(i25 - w / 2 - gap, a_share[i25] + 0.8, f"{a_share[i25]:.1f}%", ha="center",
            color=INK, fontsize=9.5)
    ax.text(i25 + w / 2 + gap, b_share[i25] + 0.8, f"{b_share[i25]:.1f}%", ha="center",
            color=INK, fontsize=9.5)
    ax.set_xticks(list(x), [f"Yr {y}" for y in years], fontsize=9.5)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.set_ylim(0, 40)
    ax.set_ylabel("Share of 100-year claimable PIUs")
    ax.set_title("Carbon income is back-loaded: years 25 and 35 carry about half")
    ax.legend(loc="upper right", fontsize=9.5)
    tidy(ax)
    subtitle(fig, "Source: report Tables 5.6 and 5.7. Only ~13% of Scenario A revenue arrives in the first 15 years.")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(OUT / "piu_vintage_profile.png")
    plt.close(fig)


# 3. Revenue per hectare across the carbon-price band --------------------------
def price_chart():
    rate_a = 629_636 / 1_982.76   # claimable tCO2e per ha
    rate_b = 51_841 / 200
    prices = [p / 2 for p in range(20, 61)]  # GBP 10 to 30
    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=200)
    ax.plot(prices, [p * rate_a for p in prices], color=GREEN, linewidth=2.2)
    ax.plot(prices, [p * rate_b for p in prices], color=GOLD, linewidth=2.2)
    ax.axvline(26.85, color=INK_2, linewidth=1, linestyle=(0, (3, 3)))
    ax.text(26.6, 300, "WCC 2024 average\n£26.85 / t", ha="right", va="bottom", color=INK_2, fontsize=9)
    for rate, colour in ((rate_a, GREEN), (rate_b, GOLD)):
        y = 26.85 * rate
        ax.plot([26.85], [y], marker="o", markersize=7, color=colour,
                markeredgecolor=SURFACE, markeredgewidth=2)
    ax.text(30.3, 30 * rate_a, f"Scenario A\n{rate_a:.1f} t/ha", va="center", color=INK, fontsize=9.5)
    ax.text(30.3, 30 * rate_b, f"Scenario B\n{rate_b:.1f} t/ha", va="center", color=INK, fontsize=9.5)
    ax.text(26.85 - 0.3, 26.85 * rate_a + 250, "£8,528 / ha", ha="right", color=INK, fontsize=9.5)
    ax.text(26.85 + 0.3, 26.85 * rate_b - 650, "£6,960 / ha", ha="left", color=INK, fontsize=9.5)
    ax.set_xlim(10, 33.5)
    ax.set_ylim(0, 10_500)
    ax.set_xticks([10, 15, 20, 25, 30])
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"£{v:.0f}"))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"£{v:,.0f}"))
    ax.set_xlabel("Carbon price (£ per tCO₂e)")
    ax.set_ylabel("100-year revenue per hectare")
    ax.set_title("Curating for ecology costs 18% per hectare; price moves revenue 3×")
    tidy(ax)
    subtitle(fig, "Gross, undiscounted carbon revenue before costs or grants. Source: report Tables 5.3 and 5.5.")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(OUT / "revenue_per_ha_vs_price.png")
    plt.close(fig)


if __name__ == "__main__":
    soil_chart()
    vintage_chart()
    price_chart()
    print("Charts written to", OUT)
