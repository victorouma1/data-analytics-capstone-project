import pandas as pd
import geopandas as gpd
import plotly.express as px

class europe_map:
    def __init__(self):
        self.salary_data_2022 = pd.read_csv("Structure of Earnings Survey 2022.csv")
        self.ppp_data_2022 = pd.read_csv("Purchasing Power Parities.csv")
    def format_data(self):
        dfs = {
            2022: self.salary_data_2022,
        }           
        for year,df in dfs.items():
            df['TIME_PERIOD'] = pd.to_datetime(df['TIME_PERIOD'], format = '%Y')
        self.salary_2022_grouped = self.salary_data_2022.groupby(['Geopolitical entity (reporting)'])[['OBS_VALUE']].median()
        self.ppp_data_2022['TIME_PERIOD'] = pd.to_datetime(self.ppp_data_2022['TIME_PERIOD'], format = '%Y')
        df_ppp_2022 = self.ppp_data_2022[self.ppp_data_2022['TIME_PERIOD'] == '2022-01-01']
        indicator = 'Nominal expenditure per inhabitant (in euro)'
        category = 'Actual individual consumption'
        ppp_filtered_2022 = df_ppp_2022[
            (df_ppp_2022['Purchasing power parities indicator'] == indicator) & 
            (df_ppp_2022['Analytical categories for purchasing power parities (PPPs) calculation (based on COICOP18)'] == category)
        ]
        self.ppp_2022_grouped = ppp_filtered_2022.groupby('Geopolitical entity (reporting)')[['OBS_VALUE']].median()
    def plot_map(self):
        countries = gpd.read_file("europe.geojson")
        fig = px.choropleth(self.ppp_2022_grouped, geojson=countries, locations=self.ppp_2022_grouped.index, color='OBS_VALUE',
                                color_continuous_scale="Viridis",
                                range_color=(5000,50000),
                                scope="europe",
                                featureidkey="properties.NAME",
                                labels={'OBS_VALUE':'cost_of_living'})
        fig.show()