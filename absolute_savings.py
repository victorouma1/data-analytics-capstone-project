import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

BASE      = "C:/Users/victo/OneDrive/Documents/Cost of Living"
SES_YEARS = [2002, 2006, 2010, 2014, 2018, 2022]

NAME_TO_ISO = {
    "Austria": "AT", "Belgium": "BE", "Bulgaria": "BG", "Cyprus": "CY",
    "Czechia": "CZ", "Czech Republic": "CZ", "Denmark": "DK", "Estonia": "EE",
    "Finland": "FI", "France": "FR", "Germany": "DE", "Greece": "EL",
    "Hungary": "HU", "Iceland": "IS", "Ireland": "IE", "Italy": "IT",
    "Latvia": "LV", "Lithuania": "LT", "Luxembourg": "LU", "Malta": "MT",
    "Netherlands": "NL", "Norway": "NO", "Poland": "PL", "Portugal": "PT",
    "Romania": "RO", "Slovakia": "SK", "Slovenia": "SI", "Spain": "ES",
    "Sweden": "SE", "United Kingdom": "UK", "Croatia": "HR", "Albania": "AL",
    "Bosnia and Herzegovina": "BA", "North Macedonia": "MK", "Kosovo": "XK",
    "Serbia": "RS", "Switzerland": "CH", "Turkey": "TR", "Montenegro": "ME",
}
ISO_TO_NAME = {
    "AT": "Austria",      "BE": "Belgium",      "BG": "Bulgaria",
    "CY": "Cyprus",       "CZ": "Czechia",       "DK": "Denmark",
    "EE": "Estonia",      "EL": "Greece",         "ES": "Spain",
    "FI": "Finland",      "FR": "France",          "DE": "Germany",
    "HR": "Croatia",      "HU": "Hungary",         "IE": "Ireland",
    "IS": "Iceland",      "IT": "Italy",           "LT": "Lithuania",
    "LU": "Luxembourg",   "LV": "Latvia",          "MT": "Malta",
    "NL": "Netherlands",  "NO": "Norway",          "PL": "Poland",
    "PT": "Portugal",     "RO": "Romania",         "RS": "Serbia",
    "SE": "Sweden",       "SI": "Slovenia",        "SK": "Slovakia",
    "TR": "Turkey",       "UK": "United Kingdom",  "CH": "Switzerland",
    "AL": "Albania",      "BA": "Bosnia & Herz.",  "MK": "N. Macedonia",
}

AGGREGATES = {
    "EU","EU15","EU25","EU27_2007","EU28","EU27_2020",
    "EA","EA13","EA16","EA17","EA18","EA19","EA20",
    "EEA","EEA30","EEA31",
}

print("Loading inflation data...")
inf_raw = pd.read_csv(f"{BASE}/Inflation.csv")

hicp = (
    inf_raw[(inf_raw["unit"] == "INX_A_AVG") & (inf_raw["coicop"] == "CP00")]
    [["geo", "TIME_PERIOD", "OBS_VALUE"]]
    .rename(columns={"OBS_VALUE": "idx"})
    .dropna(subset=["idx"])
)

hicp_2022 = hicp[hicp["TIME_PERIOD"] == 2022].set_index("geo")["idx"]

defl_table = {}
for geo in hicp["geo"].unique():
    sub  = hicp[hicp["geo"] == geo].set_index("TIME_PERIOD")["idx"]
    base = hicp_2022.get(geo)
    if base is None:
        continue
    for yr in SES_YEARS:
        period = sub.get(yr)
        if period and period > 0:
            defl_table[(geo, yr)] = base / period

print("Loading Structure of Earnings Surveys...")

SES_CFG = {
    2002: dict(ind="Gross earnings", unit_col="unit",          euro_val="Euro",
               sex_col="sex",    sex_val="Total",
               size_col=None,    size_val=None,
               nace_col="nace_r1",
               broad_nace="All NACE activities (except agriculture; fishing; "
                          "activities of households and extra-territorial organizations)",
               geo_type="name"),
    2006: dict(ind="ERN",          unit_col="Unit of measure", euro_val="Euro",
               sex_col="sex",    sex_val="T",
               size_col="sizeclas", size_val="TOTAL",
               nace_col="nace_r1", broad_nace="C-O",
               geo_type="iso"),
    2010: dict(ind="ERN",          unit_col="currency",        euro_val="EUR",
               sex_col="Sex.1",  sex_val="Total",
               size_col="sizeclas", size_val="TOTAL",
               nace_col="nace_r2", broad_nace="B-S",
               geo_type="iso"),
    2014: dict(ind="ERN",          unit_col="currency",        euro_val="EUR",
               sex_col="Sex.1",  sex_val="Total",
               size_col="sizeclas", size_val="TOTAL",
               nace_col="nace_r2", broad_nace="B-S",
               geo_type="name_label"),
    2018: dict(ind="ERN",          unit_col="unit",            euro_val="EUR",
               sex_col="Sex.1",  sex_val="Total",
               size_col="sizeclas", size_val="TOTAL",
               nace_col="nace_r2", broad_nace="B-S",
               geo_type="name_label"),
    2022: dict(ind="ERN",          unit_col="unit",            euro_val="EUR",
               sex_col="Sex.1",  sex_val="Total",
               size_col="sizeclas", size_val="TOTAL",
               nace_col="nace_r2", broad_nace="B-S",
               geo_type="iso"),
}

def load_ses(year):
    cfg = SES_CFG[year]
    df  = pd.read_csv(f"{BASE}/Structure of Earnings Survey {year}.csv")

    masks = [
        df["indic_se"]       == cfg["ind"],
        df[cfg["unit_col"]]  == cfg["euro_val"],
        df[cfg["sex_col"]]   == cfg["sex_val"],
        df["cpayagr"].isin(["Total", "TOTAL"]),
        df[cfg["nace_col"]]  == cfg["broad_nace"],
    ]
    if cfg["size_col"]:
        masks.append(df[cfg["size_col"]] == cfg["size_val"])

    filt = df[np.logical_and.reduce(masks)].copy()

    if cfg["geo_type"] == "iso":
        filt["geo_iso"] = filt["geo"].astype(str)
    elif cfg["geo_type"] == "name":
        filt["geo_iso"] = filt["geo"].map(NAME_TO_ISO)
    else:  # name_label
        filt["geo_iso"] = filt["Geopolitical entity (reporting)"].map(NAME_TO_ISO)

    filt["year"]             = year
    filt["earnings_nominal"] = pd.to_numeric(filt["OBS_VALUE"], errors="coerce")
    return filt[["geo_iso", "year", "earnings_nominal"]].dropna()


ses_all = pd.concat([load_ses(yr) for yr in SES_YEARS], ignore_index=True)
ses_all = ses_all[~ses_all["geo_iso"].isin(AGGREGATES)]

for yr in SES_YEARS:
    n = (ses_all["year"] == yr).sum()
    print(f"  SES {yr}: {n} country-rows after filtering to EUR")

ses_all["defl"]          = ses_all.apply(lambda r: defl_table.get((r["geo_iso"], r["year"]), np.nan), axis=1)
ses_all["earnings_2022"] = ses_all["earnings_nominal"] * ses_all["defl"]
ses_all = ses_all.dropna(subset=["earnings_2022"])

print("Loading Purchasing Power Parities...")
ppp_raw = pd.read_csv(f"{BASE}/Purchasing Power Parities.csv")

col_df = (
    ppp_raw[
        (ppp_raw["indic_ppp"] == "EXP_EUR_HAB") &
        (ppp_raw["ppp_cat18"] == "A01")
    ]
    [["geo", "TIME_PERIOD", "OBS_VALUE"]]
    .rename(columns={"OBS_VALUE": "col_nom", "geo": "geo_iso", "TIME_PERIOD": "year"})
    .dropna(subset=["col_nom"])
)
col_df["col_nom"] = pd.to_numeric(col_df["col_nom"], errors="coerce")
col_df["defl"]    = col_df.apply(lambda r: defl_table.get((r["geo_iso"], r["year"]), np.nan), axis=1)
col_df["col_2022"] = col_df["col_nom"] * col_df["defl"]

col_survey = (
    col_df[col_df["year"].isin(SES_YEARS)][["geo_iso", "year", "col_2022"]]
    .dropna()
)

print("Computing savings...")
merged = pd.merge(ses_all, col_survey, on=["geo_iso", "year"], how="inner")
merged["savings_2022"] = merged["earnings_2022"] - merged["col_2022"]

avg = (
    merged.groupby("geo_iso")
    .agg(avg_savings=("savings_2022", "mean"),
         n_years=("year", "nunique"))
    .reset_index()
    .sort_values("avg_savings", ascending=False)
)
avg = avg[(~avg["geo_iso"].isin(AGGREGATES)) & (avg["n_years"] >= 2)]
top5 = avg.head(5).copy()
top5["country"] = top5["geo_iso"].map(ISO_TO_NAME).fillna(top5["geo_iso"])

print("\nTop 5 countries by average annual real savings (2022 euros):")
for _, row in top5.iterrows():
    print(f"  {row['country']:25s}  €{row['avg_savings']:>10,.0f}  ({row['n_years']:.0f} survey years)")

print("\nFull ranking:")
for i, (_, row) in enumerate(avg.iterrows(), 1):
    name = ISO_TO_NAME.get(row["geo_iso"], row["geo_iso"])
    print(f"  {i:2}. {name:25s}  €{row['avg_savings']:>10,.0f}")

print("\nGenerating chart...")

BG, PANEL, TEXT = "#18181A", "#22222A", "#F0EDDF"
MUTED, GRID     = "#9A9480",  "#2E2E3A"
GOLD = ["#D4A843", "#C49438", "#B4802D", "#9A6A22", "#825418"]

fig, ax = plt.subplots(figsize=(13, 7.5))
fig.patch.set_facecolor(BG)
ax.set_facecolor(PANEL)

y_pos  = list(range(len(top5) - 1, -1, -1))
vals_k = top5["avg_savings"].values / 1000

bars = ax.barh(y_pos, vals_k, color=GOLD, edgecolor="#100E08",
               linewidth=0.6, height=0.55, zorder=3)

ax.set_axisbelow(True)
ax.xaxis.grid(True, color=GRID, linewidth=0.8, linestyle="--", zorder=0)

# Value labels
for bar, v in zip(bars, vals_k):
    ax.text(
        bar.get_width() + vals_k.max() * 0.012,
        bar.get_y() + bar.get_height() / 2,
        f"€{v:,.1f}k",
        va="center", ha="left", fontsize=12.5, fontweight="bold", color=GOLD[0]
    )

medals = {1: "🥇", 2: "🥈", 3: "🥉"}
ax.set_yticks(y_pos)
ax.set_yticklabels(
    [f"  {medals.get(i+1, f'#{i+1}')}  {row['country']}"
     for i, (_, row) in enumerate(top5.iterrows())],
    fontsize=13, color=TEXT
)

ax.set_xlabel("Average Annual Real Savings (€ thousands · 2022 prices)",
              color=MUTED, fontsize=11, labelpad=10)
ax.set_xlim(0, vals_k.max() * 1.22)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"€{x:.0f}k"))
ax.tick_params(axis="x", colors=MUTED, labelsize=10)
ax.tick_params(axis="y", length=0)
for spine in ax.spines.values():
    spine.set_visible(False)

ax.set_title(
    "Top 5 Countries by Absolute Annual Savings\n"
    "Gross Earnings − Cost of Living  ·  Inflation-Adjusted to 2022 Euros  ·  2002–2022 Eurostat SES",
    color=TEXT, fontsize=14, fontweight="bold", pad=18, loc="left"
)

fig.text(
    0.01, 0.01,
    "Source: Eurostat Structure of Earnings Survey  ·  HICP all-items (INX_A_AVG, CP00)  "
    "·  PPP Actual Individual Consumption per capita (EXP_EUR_HAB, A01)\n"
    "Savings = Inflation-adjusted gross annual earnings − Inflation-adjusted per-capita consumption expenditure  "
    "·  Euro-denominated values only  ·  All sectors, total workers",
    color="#666666", fontsize=7.5, style="italic"
)

plt.tight_layout(rect=[0, 0.07, 1, 1])
plt.show()