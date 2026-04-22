import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import unittest

country_input = input("Enter a European Country: ").title()

class cost_trend:
    def __init__(self):
        self.__df = pd.read_csv("Purchasing Power Parities.csv") 
    def format(self):
        self.country_name = country_input
        self.__df['OBS_VALUE'] = pd.to_numeric(self.__df['OBS_VALUE'], errors='coerce')

        indicator_filter = self.__df['Purchasing power parities indicator'] == 'Nominal expenditure per inhabitant (in euro)'
        category_filter = self.__df['Analytical categories for purchasing power parities (PPPs) calculation (based on COICOP18)'] == 'Actual individual consumption'

        country_filter = self.__df['Geopolitical entity (reporting)'].str.lower() == self.country_name.lower()
    
        self.filtered_df = self.__df[indicator_filter & category_filter & country_filter].copy()
        if self.filtered_df.empty:
            print(f"No data found for country: {self.country_name}")
        return
    
    def plot_trend(self):

        self.filtered_df = self.filtered_df.dropna(subset=['OBS_VALUE', 'TIME_PERIOD'])
        self.filtered_df['TIME_PERIOD'] = self.filtered_df['TIME_PERIOD'].astype(int)

        plt.figure(figsize=(10, 6))
        sns.lineplot(
            data=self.filtered_df,
            x='TIME_PERIOD',
            y='OBS_VALUE',
            marker='o',       
            linewidth=2,
            color='blue'      
        )

        plt.title(f'Nominal Expenditure per Inhabitant (€) - Actual Individual Consumption ({self.country_name.title()})')
        plt.xlabel('Year')
        plt.ylabel('Nominal expenditure per inhabitant (€)')
        plt.grid(True, linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        plt.show()
