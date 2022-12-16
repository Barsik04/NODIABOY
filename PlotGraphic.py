import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt



class PlotGraphic():

    def plot_price(excel_data_df, reccomended_price, header):
        plt.rcParams['figure.dpi'] = 250
        plt.rcParams['savefig.dpi'] = 250
        sns.histplot(excel_data_df['Цена'].dropna(), bins=1000, color='purple')
        plt.suptitle(header, fontsize=12, color='black')
        min = excel_data_df["Цена"].min() * 0.9
        max = excel_data_df["Цена"].mean() * 2
        plt.axvline(reccomended_price, 0, excel_data_df['Цена'].dropna().max(), color = 'red', linewidth=2, label= 'РРЦ на момент продажи')
        plt.minorticks_on()
        plt.legend(loc=0)
        plt.ylabel('Количество')
        plt.xlim(min, max)
        plt.grid(True)
        plt.savefig('./output/by_price/' + header)

        # sns.histplot(excel_data_df['Цена'].dropna(), bins=50, color='purple')
        # plt.suptitle(header, fontsize=12, color='black')
        # min = excel_data_df["Цена"].min() * 0.9
        # max = excel_data_df["Цена"].mean() * 2
        # plt.axvline(reccomended_price, 0, excel_data_df['Цена'].dropna().max(), color='red', linewidth=2,
        #             label='РРЦ на момент продажи')
        # plt.minorticks_on()
        # plt.legend(loc=0)
        # plt.ylabel('Количество')
        # plt.xlim(max, )
        # plt.ticklabel_format(style='plain')
        # plt.ylim(0, 10)
        # plt.grid(True)
        # plt.savefig('./output/by_price' + header + ' second_part')
        # plt.show()


    def plot_pie(excel_data_df, header):
        city_data = excel_data_df['Город'].value_counts()
        k = 0;
        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
        counts = city_data.tolist()
        cities = city_data.index.tolist()
        sum_counter=len(counts)//40;
        sum = 0
        all = 0
        for i in counts:
            all = all + i
            k = k + 1
            if (i>=50):
                sum = sum + i
        del counts[sum_counter:]
        del cities[sum_counter:]

        counts.append(sum)
        cities.append('other cities')

        wedges, texts, autotexts = ax.pie(counts, wedgeprops=dict(width=0.5), startangle=-40, autopct=lambda pct: func(pct, counts))

        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        kw = dict(arrowprops=dict(arrowstyle="-"),
                  bbox=bbox_props, zorder=0, va="center")

        for i, p in enumerate(wedges):
            ang = (p.theta2 - p.theta1) / 2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = "angle,angleA=0,angleB={}".format(ang)
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            ax.annotate(cities[i], xy=(x, y), xytext=(1.35 * np.sign(x), 1.4 * y),
                        horizontalalignment=horizontalalignment, **kw)

        ax.set_title("Распределение по городам для " + header + " всего "+ str(all))
        plt.savefig('./output/by_city/' + header)
        #plt.show()




def func(pct, allvals):


    absolute = int(np.round(pct / 100. * np.sum(allvals)))
    return "{:.1f}%".format(pct, absolute)





