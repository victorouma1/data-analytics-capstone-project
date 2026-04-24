import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

class savings:
    def __init__(self):
        self.__df_2022 = pd.read_csv(f"Structure of Earnings Survey 2022.csv")
        self.__df_ppp = pd.read_csv("Purchasing Power Parities.csv")
    def format(self):
        european_countries = [
            'Albania', 'Andorra', 'Austria', 'Belarus', 'Belgium', 'Bosnia And Herzegovina',
            'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Finland',
            'France', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Latvia',
            'Lithuania', 'Luxembourg', 'Malta', 'Moldova', 'Monaco', 'Montenegro', 'Netherlands',
            'North Macedonia', 'Norway', 'Poland', 'Portugal', 'Romania', 'Russia', 'San Marino',
            'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Ukraine', 'United Kingdom'
        ]
        df_2022_rows = self.__df_2022[self.__df_2022['Geopolitical entity (reporting)'].isin(european_countries)]
        df_2022_rows = df_2022_rows[df_2022_rows['OBS_VALUE'] > 1000]
        df_2022_grouped = df_2022_rows.groupby(['Geopolitical entity (reporting)'])[['OBS_VALUE']].median()

        self.__df_ppp['TIME_PERIOD'] = pd.to_datetime(self.__df_ppp['TIME_PERIOD'], format = '%Y') 

        df_ppp_2022 = self.__df_ppp[self.__df_ppp['TIME_PERIOD'] == '2022-01-01']
        indicator = 'Nominal expenditure per inhabitant (in euro)'
        category = 'Actual individual consumption'

        ppp_filtered_2022 = df_ppp_2022[
            (df_ppp_2022['Purchasing power parities indicator'] == indicator) & 
            (df_ppp_2022['Analytical categories for purchasing power parities (PPPs) calculation (based on COICOP18)'] == category)
        ]

        ppp_2022_grouped = ppp_filtered_2022.groupby('Geopolitical entity (reporting)')[['OBS_VALUE']].median()
        ppp_2022_grouped.drop('United States',inplace = True)

        savings = df_2022_grouped.loc[:,'OBS_VALUE'] - ppp_2022_grouped.loc[:,'OBS_VALUE']
        top_5_savings = savings.nlargest(5)

        self.top_5_df = top_5_savings.reset_index()
        self.top_5_df.columns = ['Country', 'Savings']
    def plot_bar(self):
        sns.barplot(data=self.top_5_df, x='Country', y='Savings', palette='viridis', hue = 'Country', legend = False)
        plt.title('Top 5 Largest Savings')
        plt.show()

