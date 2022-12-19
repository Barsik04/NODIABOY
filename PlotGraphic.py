import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plot1
from matplotlib import pyplot as plot2


class PlotGraphic():

    def plot_price(excel_data_df, reccomended_price, header):
        plot1.rcParams['figure.dpi'] = 250
        plot1.rcParams['savefig.dpi'] = 250
        bins = 1000 if len(excel_data_df.index) > 1000 else 100
        sns.histplot(excel_data_df['Цена'].dropna(), bins=bins, color='purple')
        plot1.suptitle(header, fontsize=12, color='black')
        min_price = excel_data_df["Цена"].min() * 0.9
        max_price = excel_data_df["Цена"].mean() * 2 if len(excel_data_df.index) > 1000 \
                                                        else excel_data_df["Цена"].max()
        plot1.axvline(reccomended_price, 0, excel_data_df['Цена'].dropna().max(), color='red', linewidth=1,
                      label='РРЦ на момент продажи')
        plot1.minorticks_on()
        plot1.legend(loc=0)
        plot1.ylabel('Количество')
        plot1.xlim(min_price, max_price)
        plot1.grid(True)
        plot1.savefig('./output/by_price/' + header)
        plot1.show()

    def plot_pie(excel_data_df, header):
        city_data = excel_data_df['Город'].value_counts()
        k = 0

        counts = city_data.tolist()
        cities = city_data.index.tolist()
        sum_counter = len(counts) // 40
        sum_other_cities = 0
        for i in counts:
            k = k + 1
            if i >= 50:
                sum_other_cities = sum_other_cities + i
        del counts[sum_counter:]
        del cities[sum_counter:]

        counts.append(sum_other_cities)
        cities.append('other cities')

        fig1, ax1 = plot2.subplots()
        ax1.pie(counts, labels=cities, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        plot2.title("Распределение по городам для " + header)
        plot2.savefig('./output/by_city/' + header)
        plot2.show()
