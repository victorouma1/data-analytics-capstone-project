import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import plotly.express as px

st.set_page_config(
    page_title="European Earnings Explorer",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ─── Global ─────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ─── Background ─────────────────────────────── */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #1a1040 40%, #24243e 100%);
    color: #f0ecff;
}

/* ─── Hero title ─────────────────────────────── */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: clamp(2.4rem, 5vw, 4rem);
    background: linear-gradient(90deg, #f9c74f, #f3722c, #f94144, #90be6d, #4cc9f0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    letter-spacing: -1px;
    margin-bottom: 0.2rem;
}
.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-weight: 300;
    font-size: 1.05rem;
    color: #a89ed0;
    letter-spacing: 0.05em;
    margin-bottom: 1.8rem;
}

/* ─── Divider ────────────────────────────────── */
.fancy-divider {
    height: 3px;
    background: linear-gradient(90deg, #f9c74f, #f3722c, #4cc9f0, transparent);
    border-radius: 99px;
    margin-bottom: 1.8rem;
}

/* ─── Tabs ────────────────────────────────────── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 5px 8px;
    gap: 6px;
    border-bottom: none !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    font-size: 0.85rem;
    letter-spacing: 0.04em;
    color: #a89ed0;
    background: transparent;
    border-radius: 10px;
    padding: 8px 18px;
    border: none !important;
    transition: all 0.25s;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: linear-gradient(135deg, #f9c74f22, #f3722c33) !important;
    color: #f9c74f !important;
    border: 1px solid #f9c74f55 !important;
}
[data-testid="stTabs"] [data-baseweb="tab"]:hover {
    color: #f0ecff !important;
    background: rgba(255,255,255,0.08) !important;
}

/* ─── Cards ──────────────────────────────────── */
.metric-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 1.1rem 1.4rem;
    backdrop-filter: blur(10px);
}
.metric-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #a89ed0;
    margin-bottom: 0.3rem;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.7rem;
    font-weight: 700;
    color: #f9c74f;
}

/* ─── Section headers ────────────────────────── */
.section-header {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.4rem;
    color: #f0ecff;
    margin-bottom: 0.6rem;
}

/* ─── Selectbox / widgets ─────────────────────── */
[data-testid="stSelectbox"] label,
[data-testid="stSlider"] label {
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    color: #d0c8f0 !important;
    font-size: 0.9rem;
    letter-spacing: 0.03em;
}
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(249,199,79,0.35) !important;
    border-radius: 10px !important;
    color: #f0ecff !important;
}

/* ─── Spinner / info boxes ────────────────────── */
[data-testid="stInfo"] {
    background: rgba(76,201,240,0.12);
    border-left: 3px solid #4cc9f0;
    border-radius: 8px;
    color: #cde8ff;
}

/* ─── Plot backgrounds: make transparent ─────── */
.stPlotlyChart, .stPyplot {
    border-radius: 14px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

matplotlib.rcParams.update({
    "figure.facecolor": "#1a1040",
    "axes.facecolor":   "#1a1040",
    "axes.edgecolor":   "#3d3460",
    "axes.labelcolor":  "#d0c8f0",
    "xtick.color":      "#a89ed0",
    "ytick.color":      "#a89ed0",
    "text.color":       "#f0ecff",
    "grid.color":       "#2e2755",
    "legend.facecolor": "#24243e",
    "legend.edgecolor": "#3d3460",
    "font.family":      "DejaVu Sans",
    "axes.titlecolor":  "#f9c74f",
    "axes.titlesize":   13,
})

EUROPEAN_COUNTRIES = sorted([
    'Albania', 'Andorra', 'Austria', 'Belarus', 'Belgium',
    'Bosnia And Herzegovina', 'Bulgaria', 'Croatia', 'Cyprus',
    'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France',
    'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy',
    'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Moldova', 'Monaco',
    'Montenegro', 'Netherlands', 'North Macedonia', 'Norway', 'Poland',
    'Portugal', 'Romania', 'Russia', 'San Marino', 'Serbia', 'Slovakia',
    'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Ukraine', 'United Kingdom',
])

SURVEY_FILES = {
    2002: {"path": "Structure of Earnings Survey 2002.csv", "country_col": "geo",
           "indicator_col": "indic_se", "sex_col": "sex", "unit_col": "unit", "euro_value": "Euro"},
    2006: {"path": "Structure of Earnings Survey 2006.csv", "country_col": "Geopolitical entity (reporting)",
           "indicator_col": "Structure of earnings indicator", "sex_col": "Sex.1", "unit_col": "Unit of measure", "euro_value": "Euro"},
    2010: {"path": "Structure of Earnings Survey 2010.csv", "country_col": "Geopolitical entity (reporting)",
           "indicator_col": "Structure of earnings indicator", "sex_col": "Sex.1", "unit_col": "Currency.1", "euro_value": "Euro"},
    2014: {"path": "Structure of Earnings Survey 2014.csv", "country_col": "Geopolitical entity (reporting)",
           "indicator_col": "Structure of earnings indicator", "sex_col": "Sex.1", "unit_col": "Currency.1", "euro_value": "Euro"},
    2018: {"path": "Structure of Earnings Survey 2018.csv", "country_col": "Geopolitical entity (reporting)",
           "indicator_col": "Structure of earnings indicator", "sex_col": "Sex.1", "unit_col": "Unit of measure", "euro_value": "Euro"},
    2022: {"path": "Structure of Earnings Survey 2022.csv", "country_col": "Geopolitical entity (reporting)",
           "indicator_col": "Structure of earnings indicator", "sex_col": "Sex.1", "unit_col": "Unit of measure", "euro_value": "Euro"},
}

st.markdown('<div class="hero-title"> European Earnings Explorer</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Salaries · Cost of Living · Savings Across Europe</div>', unsafe_allow_html=True)
st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)


tab_map, tab_trend, tab_pie, tab_topbot = st.tabs([
    "  Cost of Living Map",
    "  Salary vs Cost Trend",
    "  Income Breakdown",
    "  Top & Bottom Cities",
])

with tab_map:
    st.markdown('<div class="section-header">Cost of Living Across Europe (2022)</div>', unsafe_allow_html=True)
    st.caption("Nominal expenditure per inhabitant in euros — Actual Individual Consumption category.")

    @st.cache_data
    def load_map_data():
        ppp = pd.read_csv("Purchasing Power Parities.csv")
        ppp["TIME_PERIOD"] = pd.to_datetime(ppp["TIME_PERIOD"], format="%Y")
        df_2022 = ppp[ppp["TIME_PERIOD"] == "2022-01-01"]
        filtered = df_2022[
            (df_2022["Purchasing power parities indicator"] == "Nominal expenditure per inhabitant (in euro)") &
            (df_2022["Analytical categories for purchasing power parities (PPPs) calculation (based on COICOP18)"] == "Actual individual consumption")
        ]
        return filtered.groupby("Geopolitical entity (reporting)")[["OBS_VALUE"]].median()

    try:
        ppp_grouped = load_map_data()
        import geopandas as gpd
        countries = gpd.read_file("CNTR_RG_20M_2024_4326.geojson")

        fig_map = px.choropleth(
            ppp_grouped,
            geojson=countries,
            locations=ppp_grouped.index,
            color="OBS_VALUE",
            color_continuous_scale="Plasma",
            range_color=(5000, 50000),
            scope="europe",
            featureidkey="properties.NAME_ENGL",
            labels={"OBS_VALUE": "Cost of Living (€)"},
        )
        fig_map.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            geo=dict(bgcolor="rgba(0,0,0,0)", lakecolor="#1a1040", landcolor="#2e2755"),
            coloraxis_colorbar=dict(title=dict(text="€ / year", font=dict(color="#f9c74f")), tickfont=dict(color="#d0c8f0")),
            margin=dict(l=0, r=0, t=10, b=0),
            height=520,
        )
        st.plotly_chart(fig_map, use_container_width=True)
    except FileNotFoundError as e:
        st.error(f"Missing data file: {e}")

    st.markdown("""
    <div style="margin-top:1.5rem; display:grid; grid-template-columns:1fr 1fr; gap:1rem;">

      <div class="metric-card" style="border-left:3px solid #f9c74f">
        <div class="metric-label"> The Expensive Tier</div>
        <p style="color:#d0c8f0; font-size:0.9rem; margin:0.5rem 0 0">
          <b style="color:#f9c74f">Switzerland</b> consistently ranks as the most expensive country in Europe,
          driven by exceptional wages, a strong franc, and costly services.
          <b style="color:#f9c74f">Norway & Iceland</b> follow due to high labour wages and the necessity of
          importing many goods.
        </p>
      </div>

      <div class="metric-card" style="border-left:3px solid #90be6d">
        <div class="metric-label"> Western & Northern Core</div>
        <p style="color:#d0c8f0; font-size:0.9rem; margin:0.5rem 0 0">
          <b style="color:#90be6d">Germany, France & the UK</b> maintain a high-middle cost of living — housing
          in London, Paris, and Munich keeps averages elevated.
          <b style="color:#90be6d">Denmark, Sweden & Finland</b> balance high consumer prices with extensive
          social safety nets.
        </p>
      </div>

      <div class="metric-card" style="border-left:3px solid #4cc9f0">
        <div class="metric-label"> Mediterranean & Central Divide</div>
        <p style="color:#d0c8f0; font-size:0.9rem; margin:0.5rem 0 0">
          <b style="color:#4cc9f0">Italy & Spain</b> have affordable rural regions that pull national averages
          below their expensive city centres. <b style="color:#4cc9f0">Czechia</b> is rapidly catching up to
          Western prices due to its central economic role in the former Eastern Bloc.
        </p>
      </div>

      <div class="metric-card" style="border-left:3px solid #a89ed0">
        <div class="metric-label"> Lower-Cost East</div>
        <p style="color:#d0c8f0; font-size:0.9rem; margin:0.5rem 0 0">
          <b style="color:#a89ed0">The Balkans</b> (Bulgaria, Serbia, Albania, etc.) are often 60–70% cheaper
          than Switzerland for housing, dining, and local services.
          <b style="color:#a89ed0">Poland & Hungary</b> remain relatively affordable despite recent inflation.
        </p>
      </div>

    </div>
    """, unsafe_allow_html=True)

with tab_trend:
    st.markdown('<div class="section-header">Salary vs Cost of Living Over Time</div>', unsafe_allow_html=True)

    selected_country = st.selectbox(
        "Choose a European Country",
        options=EUROPEAN_COUNTRIES,
        index=EUROPEAN_COUNTRIES.index("Germany"),
        key="trend_country",
    )

    @st.cache_data
    def load_ppp_trend(country: str):
        df = pd.read_csv("Purchasing Power Parities.csv")
        df["OBS_VALUE"] = pd.to_numeric(df["OBS_VALUE"], errors="coerce")
        mask = (
            (df["Purchasing power parities indicator"] == "Nominal expenditure per inhabitant (in euro)") &
            (df["Analytical categories for purchasing power parities (PPPs) calculation (based on COICOP18)"] == "Actual individual consumption") &
            (df["Geopolitical entity (reporting)"].str.lower() == country.lower())
        )
        return df[mask].dropna(subset=["OBS_VALUE", "TIME_PERIOD"]).copy()

    @st.cache_data
    def load_salary_trend(country: str):
        records = []
        for year, schema in SURVEY_FILES.items():
            try:
                df = pd.read_csv(schema["path"])
                df["OBS_VALUE"] = pd.to_numeric(df["OBS_VALUE"], errors="coerce")
                mask = (
                    (df[schema["country_col"]].str.lower() == country.lower()) &
                    (df[schema["indicator_col"]] == "Gross earnings") &
                    (df[schema["sex_col"]] == "Total") &
                    (df[schema["unit_col"]] == schema["euro_value"]) &
                    (df["OBS_VALUE"] > 1000)
                )
                filtered = df[mask]
                if not filtered.empty:
                    records.append({"TIME_PERIOD": year, "median_salary": filtered["OBS_VALUE"].median()})
            except FileNotFoundError:
                pass
        if not records:
            return pd.DataFrame(columns=["TIME_PERIOD", "median_salary"])
        return pd.DataFrame(records).sort_values("TIME_PERIOD")

    try:
        cost_df   = load_ppp_trend(selected_country)
        salary_df = load_salary_trend(selected_country)

        if cost_df.empty and salary_df.empty:
            st.info(f"No data found for **{selected_country}**. Try another country.")
        else:
            cost_df["TIME_PERIOD"] = cost_df["TIME_PERIOD"].astype(int)

            fig_trend, ax = plt.subplots(figsize=(11, 5))

            if not cost_df.empty:
                sns.lineplot(data=cost_df, x="TIME_PERIOD", y="OBS_VALUE",
                             marker="o", linewidth=2.5, color="#4cc9f0",
                             label="Cost of Living (€/yr)", ax=ax)

            if not salary_df.empty:
                sns.lineplot(data=salary_df, x="TIME_PERIOD", y="median_salary",
                             marker="s", linewidth=2.5, color="#f9c74f",
                             linestyle="--", label="Median Gross Salary (€)", ax=ax)

            ax.set_xlabel("Year", fontsize=11)
            ax.set_ylabel("Value (€)", fontsize=11)
            ax.set_title(f"Cost of Living vs Median Salary — {selected_country}", fontsize=14, color="#f9c74f")
            ax.legend(framealpha=0.3)
            ax.grid(True, linestyle="--", alpha=0.4)
            fig_trend.tight_layout()
            st.pyplot(fig_trend)
            plt.close(fig_trend)

            if not salary_df.empty and not cost_df.empty:
                latest_salary = salary_df["median_salary"].iloc[-1]
                latest_cost   = cost_df["OBS_VALUE"].iloc[-1]
                gap = latest_salary - latest_cost
                col1, col2, col3 = st.columns(3)
                for col, label, val, colour in [
                    (col1, "Latest Median Salary", f"€{latest_salary:,.0f}", "#90be6d"),
                    (col2, "Latest Cost of Living", f"€{latest_cost:,.0f}",  "#f3722c"),
                    (col3, "Estimated Savings",     f"€{gap:,.0f}",          "#f9c74f"),
                ]:
                    with col:
                        st.markdown(f"""
                        <div class="metric-card">
                          <div class="metric-label">{label}</div>
                          <div class="metric-value" style="color:{colour}">{val}</div>
                        </div>""", unsafe_allow_html=True)

    except FileNotFoundError as e:
        st.error(f"Missing data file: {e}")

with tab_pie:
    st.markdown('<div class="section-header">How Europeans Spend Their Income</div>', unsafe_allow_html=True)
    st.caption("Average split between rent and all other expenses across European cities.")

    @st.cache_data
    def load_pie_data():
        df = pd.read_csv("cost-of-living in euros.csv", index_col=0)
        euro_cities = [col for col in df.columns
                       if any(col.strip().endswith(c) for c in EUROPEAN_COUNTRIES)]
        df_euro = df[euro_cities]

        avg_rent = (
            df_euro.loc["Apartment (1 bedroom) in City Centre"].dropna().mean() +
            df_euro.loc["Apartment (1 bedroom) Outside of Centre"].dropna().mean()
        ) / 2
        avg_salary = df_euro.loc["Average Monthly Net Salary (After Tax)"].dropna().mean()
        other = avg_salary - avg_rent
        return avg_rent, avg_salary, other, len(euro_cities)

    try:
        avg_rent, avg_salary, other, n_cities = load_pie_data()

        col_pie, col_stats = st.columns([3, 2], gap="large")
        with col_pie:
            fig_pie, ax_pie = plt.subplots(figsize=(7, 7))
            wedges, texts, autotexts = ax_pie.pie(
                [avg_rent, other],
                labels=["Rent\n(1-Bed Apt)", "Remaining Income"],
                autopct="%1.1f%%",
                startangle=140,
                colors=["#f3722c", "#4cc9f0"],
                explode=(0.06, 0),
                wedgeprops=dict(linewidth=2, edgecolor="#1a1040"),
                textprops=dict(color="#f0ecff", fontsize=11),
            )
            for at in autotexts:
                at.set_fontsize(13)
                at.set_fontweight("bold")
                at.set_color("#1a1040")
            ax_pie.set_title("Monthly Net Income Distribution", color="#f9c74f", fontsize=14)
            fig_pie.patch.set_facecolor("#1a1040")
            st.pyplot(fig_pie)
            plt.close(fig_pie)

        with col_stats:
            st.markdown("<br><br>", unsafe_allow_html=True)
            for label, val, colour in [
                ("Cities Analysed",        str(n_cities),             "#f9c74f"),
                ("Avg Monthly Salary",     f"€{avg_salary:,.0f}",     "#90be6d"),
                ("Avg Monthly Rent",       f"€{avg_rent:,.0f}",       "#f3722c"),
                ("Remaining after Rent",   f"€{other:,.0f}",          "#4cc9f0"),
                ("Rent as % of Salary",    f"{avg_rent/avg_salary*100:.1f}%", "#f94144"),
            ]:
                st.markdown(f"""
                <div class="metric-card" style="margin-bottom:0.8rem">
                  <div class="metric-label">{label}</div>
                  <div class="metric-value" style="color:{colour}">{val}</div>
                </div>""", unsafe_allow_html=True)

    except (FileNotFoundError, KeyError) as e:
        st.error(f"Data error: {e}")

    st.markdown("""
    <div class="metric-card" style="margin-top:1.5rem; border-left:3px solid #f3722c">
      <div class="metric-label"> Why is Rent So High Across Europe?</div>
      <p style="color:#d0c8f0; font-size:0.93rem; margin:0.6rem 0 0; line-height:1.7">
        Rent is high across Europe due to a severe imbalance between <b style="color:#f3722c">high demand and low supply</b>,
        compounded by rapid urbanisation, the growth of short-term tourist lets, and rising costs for landlords.
        As more people move to cities for work, competition for limited housing stock intensifies — pushing rents
        upward even in countries where overall wages have not kept pace.
      </p>
    </div>
    """, unsafe_allow_html=True)

with tab_topbot:
    st.markdown('<div class="section-header">Cheapest & Priciest European Cities</div>', unsafe_allow_html=True)
    st.caption("Based on a standardised monthly basket of goods, services, and housing.")

    EXTENDED_EUROPEAN_COUNTRIES = EUROPEAN_COUNTRIES + [
        'Armenia', 'Azerbaijan', 'Georgia', 'Kazakhstan', 'Kosovo',
        'Liechtenstein', 'Macedonia', 'Turkey', 'Vatican City',
    ]

    @st.cache_data
    def load_topbot_data():
        df = pd.read_csv("cost-of-living in euros.csv")
        cities = df.columns[1:]
        euro_cities = [c for c in cities
                       if c.split(",")[-1].strip() in EXTENDED_EUROPEAN_COUNTRIES]
        df.set_index("Unnamed: 0", inplace=True)
        df_europe = df[euro_cities].T

        basket = {
            "Apartment (1 bedroom) Outside of Centre": 1,
            "Basic (Electricity, Heating, Cooling, Water, Garbage) for 85m2 Apartment": 1,
            "Internet (60 Mbps or More, Unlimited Data, Cable/ADSL)": 1,
            "Monthly Pass (Regular Price)": 1,
            "Fitness Club, Monthly Fee for 1 Adult": 1,
            "Milk (regular), (1 liter)": 10,
            "Loaf of Fresh White Bread (500g)": 15,
            "Eggs (regular) (12)": 2,
            "Local Cheese (1kg)": 1,
            "Chicken Breasts (Boneless, Skinless), (1kg)": 4,
            "Beef Round (1kg) (or Equivalent Back Leg Red Meat)": 2,
            "Apples (1kg)": 3,
            "Oranges (1kg)": 3,
            "Potato (1kg)": 5,
            "Lettuce (1 head)": 4,
            "Rice (white), (1kg)": 3,
            "Tomato (1kg)": 3,
            "Banana (1kg)": 3,
            "Onion (1kg)": 2,
            "Water (1.5 liter bottle)": 15,
            "Meal, Inexpensive Restaurant": 4,
            "Meal for 2 People, Mid-range Restaurant, Three-course": 1,
            "Cappuccino (regular)": 10,
            "Domestic Beer (0.5 liter draught)": 4,
            "Cinema, International Release, 1 Seat": 2,
        }
        valid = {k: v for k, v in basket.items() if k in df_europe.columns}
        df_europe["Total_Monthly_Spending"] = sum(
            pd.to_numeric(df_europe[k], errors="coerce").fillna(0) * v
            for k, v in valid.items()
        )
        spending = df_europe[["Total_Monthly_Spending"]].dropna().sort_values("Total_Monthly_Spending")
        return spending

    try:
        spending = load_topbot_data()
        top5    = spending.tail(5).iloc[::-1]
        bottom5 = spending.head(5)

        col_top, col_bot = st.columns(2, gap="large")

        with col_top:
            st.markdown("####  Most Expensive Cities")
            fig_top, ax_top = plt.subplots(figsize=(6, 4))
            palette_top = sns.color_palette("YlOrRd", len(top5))[::-1]
            sns.barplot(x=top5["Total_Monthly_Spending"], y=top5.index,
                        palette=palette_top, hue=top5.index, legend=False, ax=ax_top)
            ax_top.set_xlabel("Monthly Spending (€)")
            ax_top.set_ylabel("")
            ax_top.set_title("Highest Typical Monthly Spend", color="#f94144")
            ax_top.bar_label(ax_top.containers[0], fmt="€%.0f", padding=5, color="#f0ecff", fontsize=9)
            fig_top.tight_layout()
            st.pyplot(fig_top)
            plt.close(fig_top)

        with col_bot:
            st.markdown("####  Most Affordable Cities")
            fig_bot, ax_bot = plt.subplots(figsize=(6, 4))
            palette_bot = sns.color_palette("YlGn", len(bottom5))[::-1]
            sns.barplot(x=bottom5["Total_Monthly_Spending"], y=bottom5.index,
                        palette=palette_bot, hue=bottom5.index, legend=False, ax=ax_bot)
            ax_bot.set_xlabel("Monthly Spending (€)")
            ax_bot.set_ylabel("")
            ax_bot.set_title("Lowest Typical Monthly Spend", color="#90be6d")
            ax_bot.bar_label(ax_bot.containers[0], fmt="€%.0f", padding=5, color="#f0ecff", fontsize=9)
            fig_bot.tight_layout()
            st.pyplot(fig_bot)
            plt.close(fig_bot)

    except (FileNotFoundError, KeyError) as e:
        st.error(f"Data error: {e}")

    st.markdown("""
    <div style="margin-top:1.5rem; display:grid; grid-template-columns:1fr 1fr; gap:1rem;">

      <div class="metric-card" style="border-left:3px solid #f94144">
        <div class="metric-label"> High-End Spending Cities</div>
        <p style="color:#d0c8f0; font-size:0.9rem; margin:0.5rem 0 0; line-height:1.65">
          <b style="color:#f94144">Zurich, Switzerland</b> tops the chart with monthly costs exceeding <b>€2,250</b>.
          <b style="color:#f94144">London (UK)</b> and <b style="color:#f94144">Dublin (Ireland)</b> follow closely
          at €2,100–2,200 as major global financial hubs. <b style="color:#f94144">Reykjavik (Iceland)</b> and
          <b style="color:#f94144">Amsterdam (Netherlands)</b> round out the top five at €1,900–2,050.
        </p>
      </div>

      <div class="metric-card" style="border-left:3px solid #90be6d">
        <div class="metric-label"> Budget-Friendly Cities</div>
        <p style="color:#d0c8f0; font-size:0.9rem; margin:0.5rem 0 0; line-height:1.65">
          <b style="color:#90be6d">Izmir, Turkey</b> is the most affordable at around <b>€365/month</b>.
          Turkish cities occupy three of the five lowest spots, reflecting local economic conditions and
          exchange rates. <b style="color:#90be6d">Baku (Azerbaijan)</b> and <b style="color:#90be6d">Tbilisi (Georgia)</b>
          also rank among the cheapest at under €425/month.
        </p>
      </div>

    </div>
    <div class="metric-card" style="margin-top:1rem; border-left:3px solid #f9c74f; text-align:center">
      <p style="color:#d0c8f0; font-size:0.95rem; margin:0">
         Living in <b style="color:#f94144">Zurich</b> is approximately
        <b style="color:#f9c74f; font-size:1.2rem">6×</b> more expensive than living in
        <b style="color:#90be6d">Izmir</b> — a striking divide between Western Europe's financial centres
        and the emerging markets of the East and Southeast.
      </p>
    </div>
    """, unsafe_allow_html=True)


st.markdown("""
<hr style="border:none; border-top:1px solid #3d3460; margin-top:2.5rem;">
<p style="text-align:center; color:#5a5080; font-size:0.78rem; font-family:'DM Sans',sans-serif;">
  Data sources: Eurostat Structure of Earnings Survey · Eurostat Purchasing Power Parities · Numbeo Cost of Living
</p>
""", unsafe_allow_html=True)