import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

df_2022 = pd.read_csv("Structure of Earnings Survey 2022.csv")
df_ppp  = pd.read_csv("Purchasing Power Parities.csv")
df_ppp.columns = df_ppp.columns.str.strip()

salary_2022 = (
    df_2022
    .groupby("Geopolitical entity (reporting)")[["OBS_VALUE"]]
    .median()
    .rename(columns={"OBS_VALUE": "monthly_salary_eur"})
)

salary_2022["annual_salary_eur"] = salary_2022["monthly_salary_eur"]

indicator = "Nominal expenditure per inhabitant (in euro)"
category  = "Actual individual consumption"

ppp_2022 = df_ppp[
    (df_ppp["TIME_PERIOD"] == 2022) &                                   
    (df_ppp["Purchasing power parities indicator"] == indicator) &
    (df_ppp["Analytical categories for purchasing power parities (PPPs) calculation (based on COICOP18)"] == category)
].groupby("Geopolitical entity (reporting)")[["OBS_VALUE"]].median()
ppp_2022 = ppp_2022.rename(columns={"OBS_VALUE": "annual_cost_eur"})

merged = salary_2022.merge(ppp_2022, on="Geopolitical entity (reporting)")
merged["annual_savings_eur"] = merged["annual_salary_eur"] - merged["annual_cost_eur"]

top5 = (
    merged[merged["annual_savings_eur"] > 0] 
    .nlargest(5, "annual_savings_eur")
    .reset_index()
)

bottom5 = (
    merged[merged["annual_savings_eur"] > 0] 
    .nsmallest(5, "annual_savings_eur")
    .reset_index()
)

print("--- TOP 5 ---")
print(top5[["Geopolitical entity (reporting)", "annual_salary_eur",
            "annual_cost_eur", "annual_savings_eur"]])

print("\n--- BOTTOM 5 ---")
print(bottom5[["Geopolitical entity (reporting)", "annual_salary_eur",
               "annual_cost_eur", "annual_savings_eur"]])

colors_salary = "#4C9BE8"
colors_cost   = "#E8734C"
colors_save   = "#4CAF50"
width = 0.25

# ==========================================
# FIGURE 1: TOP 5 COUNTRIES
# ==========================================
fig1, ax1 = plt.subplots(figsize=(10, 6))

x1 = range(len(top5))

bars_v1 = ax1.bar([i + width for i in x1], top5["annual_savings_eur"],
                  width=width, label="Annual Savings", color=colors_save, zorder=3)

ax1.bar_label(bars_v1, padding=3)
ax1.set_xticks([i + width for i in x1]) # Aligned ticks with offset bars
ax1.set_xticklabels(top5["Geopolitical entity (reporting)"], fontsize=11)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"€{v:,.0f}"))
ax1.set_ylabel("EUR (Annual)", fontsize=12)
ax1.set_title("Top 5 Countries by Absolute Annual Savings (2022)", fontsize=14, fontweight="bold")
ax1.legend(fontsize=11)
ax1.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)
ax1.spines[["top", "right"]].set_visible(False)

fig1.tight_layout()

# ==========================================
# FIGURE 2: BOTTOM 5 COUNTRIES
# ==========================================
fig2, ax2 = plt.subplots(figsize=(10, 6))

x2 = range(len(bottom5))

bars_v2 = ax2.bar([i + width for i in x2], bottom5["annual_savings_eur"],
                  width=width, label="Annual Savings", color=colors_save, zorder=3)

ax2.bar_label(bars_v2, padding=3)
ax2.set_xticks([i + width for i in x2]) # Aligned ticks with offset bars
ax2.set_xticklabels(bottom5["Geopolitical entity (reporting)"], fontsize=11)
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"€{v:,.0f}"))
ax2.set_ylabel("EUR (Annual)", fontsize=12)
ax2.set_title("Bottom 5 Countries by Absolute Annual Savings (2022)", fontsize=14, fontweight="bold")
ax2.legend(fontsize=11)
ax2.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)
ax2.spines[["top", "right"]].set_visible(False)

fig2.tight_layout()

# Renders both windows simultaneously 
plt.show()

