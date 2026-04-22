import pandas as pd
import matplotlib.pyplot as plt

class rent_vs_rest:
    def __init__(self):
        self.__df = pd.read_csv('cost-of-living in euros.csv', index_col=0)
    def format_data(self):
        european_countries = [
            'Albania', 'Andorra', 'Austria', 'Belarus', 'Belgium', 'Bosnia And Herzegovina',
            'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Finland',
            'France', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Latvia',
            'Lithuania', 'Luxembourg', 'Malta', 'Moldova', 'Monaco', 'Montenegro', 'Netherlands',
            'North Macedonia', 'Norway', 'Poland', 'Portugal', 'Romania', 'Russia', 'San Marino',
            'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Ukraine', 'United Kingdom'
        ]

        self.euro_cities = [col for col in self.__df.columns if any(col.strip().endswith(country) for country in european_countries)]
        self.df_euro = self.__df[self.euro_cities]
    def factors(self):
        rent_city = 'Apartment (1 bedroom) in City Centre'
        rent_out = 'Apartment (1 bedroom) Outside of Centre'
        salary_metric = 'Average Monthly Net Salary (After Tax)'

        avg_rent_city = self.df_euro.loc[rent_city].dropna().mean()
        avg_rent_out = self.df_euro.loc[rent_out].dropna().mean()
        self.avg_rent = (avg_rent_city + avg_rent_out) / 2

        self.avg_salary = self.df_euro.loc[salary_metric].dropna().mean()

        self.other_factors = self.avg_salary - self.avg_rent
    def plot_pie(self):
        labels = ['Rent (1-Bedroom Apartment)', 'All Other Factors (Food, Utilities, Savings, etc.)']
        sizes = [self.avg_rent, self.other_factors]
        colors = ['#ff7f0e', '#1f77b4']

        plt.figure(figsize=(10, 7))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, explode=(0.05, 0))
        plt.title('Average Distribution of Monthly Net Income in European Cities')
        plt.axis('equal') 

        print(f"Cities analyzed: {len(self.euro_cities)}")
        print(f"Average Monthly Salary: {self.avg_salary:.2f} EUR")
        print(f"Average Rent: {self.avg_rent:.2f} EUR")
        plt.show()
