import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class best_and_worst():
    def __init__(self):
        self.__df = pd.read_csv('cost-of-living in euros.csv')
    def format(self):
        european_countries = [
            'Albania', 'Andorra', 'Armenia', 'Austria', 'Azerbaijan', 'Belarus', 'Belgium', 
            'Bosnia And Herzegovina', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 
            'Denmark', 'Estonia', 'Finland', 'France', 'Georgia', 'Germany', 'Greece', 
            'Hungary', 'Iceland', 'Ireland', 'Italy', 'Kazakhstan', 'Kosovo', 'Latvia', 
            'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macedonia', 'Malta', 'Moldova', 
            'Monaco', 'Montenegro', 'Netherlands', 'Norway', 'Poland', 'Portugal', 
            'Romania', 'Russia', 'San Marino', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', 
            'Sweden', 'Switzerland', 'Turkey', 'Ukraine', 'United Kingdom', 'Vatican City'
        ]

        cities = self.__df.columns[1:]
        european_cities = []

        for city_col in cities:
            country = city_col.split(',')[-1].strip()
            if country in european_countries:
                european_cities.append(city_col)

        self.__df.set_index('Unnamed: 0', inplace=True)
        df_europe = self.__df[european_cities]
        df_t = df_europe.transpose()

        basket = {
            'Apartment (1 bedroom) Outside of Centre': 1,
            'Basic (Electricity, Heating, Cooling, Water, Garbage) for 85m2 Apartment': 1,
            'Internet (60 Mbps or More, Unlimited Data, Cable/ADSL)': 1,
            'Monthly Pass (Regular Price)': 1,
            'Fitness Club, Monthly Fee for 1 Adult': 1,
            'Milk (regular), (1 liter)': 10,
            'Loaf of Fresh White Bread (500g)': 15,
            'Eggs (regular) (12)': 2,
            'Local Cheese (1kg)': 1,
            'Chicken Breasts (Boneless, Skinless), (1kg)': 4,
            'Beef Round (1kg) (or Equivalent Back Leg Red Meat)': 2,
            'Apples (1kg)': 3,
            'Oranges (1kg)': 3,
            'Potato (1kg)': 5,
            'Lettuce (1 head)': 4,
            'Rice (white), (1kg)': 3,
            'Tomato (1kg)': 3,
            'Banana (1kg)': 3,
            'Onion (1kg)': 2,
            'Water (1.5 liter bottle)': 15,
            'Meal, Inexpensive Restaurant': 4,
            'Meal for 2 People, Mid-range Restaurant, Three-course': 1,
            'Cappuccino (regular)': 10,
            'Domestic Beer (0.5 liter draught)': 4,
            'Cinema, International Release, 1 Seat': 2
        }
        valid_basket = {k: v for k, v in basket.items() if k in df_t.columns}

        df_t['Total_Monthly_Spending'] = 0
        for item, qty in valid_basket.items():
            df_t['Total_Monthly_Spending'] += pd.to_numeric(df_t[item], errors='coerce').fillna(0) * qty

        self.spending = df_t[['Total_Monthly_Spending']].copy()
        self.spending.dropna(inplace=True)
        self.spending.sort_values(by='Total_Monthly_Spending', inplace=True)
    def plot_bar(self):
        bottom_5 = self.spending.head(5)
        top_5 = self.spending.tail(5)

        plt.figure(figsize=(10, 6))
        sns.barplot(x=top_5['Total_Monthly_Spending'], y=top_5.index, palette='Reds_r', hue = top_5.index, legend = False)
        plt.title('Top 5 European Cities with Highest Typical Monthly Spending (Euros)')
        plt.xlabel('Monthly Spending (Euros)')
        plt.ylabel('City')
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(10, 6))
        sns.barplot(x=bottom_5['Total_Monthly_Spending'], y=bottom_5.index, palette='Greens_r', hue = bottom_5.index, legend = False)
        plt.title('Bottom 5 European Cities with Lowest Typical Monthly Spending (Euros)')
        plt.xlabel('Monthly Spending (Euros)')
        plt.ylabel('City')
        plt.tight_layout()
        plt.show()