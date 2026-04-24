import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

country_input = input("Enter a European Country: ").title()

SURVEY_FILES = {
    2002: {
        "path": "Structure of Earnings Survey 2002.csv",
        "country_col": "geo",
        "indicator_col": "indic_se",
        "sex_col": "sex",
        "unit_col": "unit",
        "euro_value": "Euro",
    },
    2006: {
        "path": "Structure of Earnings Survey 2006.csv",
        "country_col": "Geopolitical entity (reporting)",
        "indicator_col": "Structure of earnings indicator",
        "sex_col": "Sex.1",
        "unit_col": "Unit of measure",
        "euro_value": "Euro",
    },
    2010: {
        "path": "Structure of Earnings Survey 2010.csv",
        "country_col": "Geopolitical entity (reporting)",
        "indicator_col": "Structure of earnings indicator",
        "sex_col": "Sex.1",
        "unit_col": "Currency.1",
        "euro_value": "Euro",
    },
    2014: {
        "path": "Structure of Earnings Survey 2014.csv",
        "country_col": "Geopolitical entity (reporting)",
        "indicator_col": "Structure of earnings indicator",
        "sex_col": "Sex.1",
        "unit_col": "Currency.1",
        "euro_value": "Euro",
    },
    2018: {
        "path": "Structure of Earnings Survey 2018.csv",
        "country_col": "Geopolitical entity (reporting)",
        "indicator_col": "Structure of earnings indicator",
        "sex_col": "Sex.1",
        "unit_col": "Unit of measure",
        "euro_value": "Euro",
    },
    2022: {
        "path": "Structure of Earnings Survey 2022.csv",
        "country_col": "Geopolitical entity (reporting)",
        "indicator_col": "Structure of earnings indicator",
        "sex_col": "Sex.1",
        "unit_col": "Unit of measure",
        "euro_value": "Euro",
    },
}


class cost_trend:
    def __init__(self):
        self.__df = pd.read_csv("Purchasing Power Parities.csv")

    def format(self):
        self.country_name = country_input
        self.__df["OBS_VALUE"] = pd.to_numeric(self.__df["OBS_VALUE"], errors="coerce")

        indicator_filter = (
            self.__df["Purchasing power parities indicator"]
            == "Nominal expenditure per inhabitant (in euro)"
        )
        category_filter = (
            self.__df[
                "Analytical categories for purchasing power parities (PPPs) calculation (based on COICOP18)"
            ]
            == "Actual individual consumption"
        )
        country_filter = (
            self.__df["Geopolitical entity (reporting)"].str.lower()
            == self.country_name.lower()
        )

        self.filtered_df = self.__df[
            indicator_filter & category_filter & country_filter
        ].copy()

        if self.filtered_df.empty:
            print(f"No cost-of-living data found for country: {self.country_name}")

    def _load_salary_data(self):
        records = []

        for year, schema in SURVEY_FILES.items():
            df = pd.read_csv(schema["path"])
            df["OBS_VALUE"] = pd.to_numeric(df["OBS_VALUE"], errors="coerce")

            country_filter = (
                df[schema["country_col"]].str.lower() == self.country_name.lower()
            )
            indicator_filter = df[schema["indicator_col"]] == "Gross earnings"
            sex_filter = df[schema["sex_col"]] == "Total"
            unit_filter = df[schema["unit_col"]] == schema["euro_value"]
            value_filter = df["OBS_VALUE"] > 1000

            filtered = df[
                country_filter
                & indicator_filter
                & sex_filter
                & unit_filter
                & value_filter
            ]

            if filtered.empty:
                print(
                    f"  [Warning] No salary data found for {self.country_name} in {year}"
                )
                continue

            median_val = filtered["OBS_VALUE"].median()
            records.append({"TIME_PERIOD": year, "median_salary": median_val})

        if not records:
            print(f"No salary data found for country: {self.country_name}")
            return pd.DataFrame(columns=["TIME_PERIOD", "median_salary"])

        return pd.DataFrame(records).sort_values("TIME_PERIOD")

    def plot_trend(self):
        cost_df = self.filtered_df.dropna(subset=["OBS_VALUE", "TIME_PERIOD"]).copy()
        cost_df["TIME_PERIOD"] = cost_df["TIME_PERIOD"].astype(int)

        salary_df = self._load_salary_data()

        fig, ax = plt.subplots(figsize=(12, 6))

        sns.lineplot(
            data=cost_df,
            x="TIME_PERIOD",
            y="OBS_VALUE",
            marker="o",
            linewidth=2,
            color="blue",
            label="Cost of Living (Nominal expenditure per inhabitant, €)",
            ax=ax,
        )

        if not salary_df.empty:
            sns.lineplot(
                data=salary_df,
                x="TIME_PERIOD",
                y="median_salary",
                marker="s",
                linewidth=2,
                color="green",
                linestyle="--",
                label="Median Gross Salary (€, OBS_VALUE > 1000)",
                ax=ax,
            )

        ax.set_xlabel("Year")
        ax.set_ylabel("Value (€)")
        ax.legend(loc="upper left")

        plt.title(
            f"Cost of Living vs. Median Gross Salary over Time ({self.country_name})"
        )
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.tight_layout()
        plt.show()