import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import map
import pie
import trend_line
import top_and_bottom_5
import absolute_savings

europe_map = map.europe_map()
format_europe = europe_map.format_data()
plot_europe = europe_map.plot_map()

trend = trend_line.cost_trend()
trend_format = trend.format()
trend_plot = trend.plot_trend()

pie_chart = pie.rent_vs_rest()
format_pie = pie_chart.format_data()
pie_factors = pie_chart.factors()
pie_plot = pie_chart.plot_pie()

bar = top_and_bottom_5.best_and_worst()
format_bar = bar.format()
plot_bar = bar.plot_bar()

savings = absolute_savings.savings()
savings_format = savings.format()
savings_plot_bar = savings.plot_bar()

