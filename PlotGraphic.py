import matplotlib
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt



class PlotGraphic():

    def plot_price(excel_data_df, reccomended_price, header):

        fig, axs = plt.subplots(2, 1, constrained_layout=True)

        sns.histplot(excel_data_df['Цена'].dropna(), bins=1000, color='purple')
        #axs[0][0].set_suptitle(header, fontsize=12, color='black')
        min = excel_data_df["Цена"].min() * 0.9
        max = excel_data_df["Цена"].mean() * 2
        #axs[0][0].set_axvline(reccomended_price, 0, excel_data_df['Цена'].dropna().max(), color = 'red', linewidth=2, label= 'РРЦ на момент продажи')
        #axs[0][0].set_minorticks_on()
        #axs[0][0].set_legend(loc=0)
        axs[0][0].set_ylabel('Количество')
        #axs[0][0].set_xlim(min, max)
        axs[0][0].set_grid()







        sns.histplot(excel_data_df['Цена'].dropna(), bins=1000, color='purple')
        #axs[1][0].suptitle(header, fontsize=12, color='black')
        min = excel_data_df["Цена"].mean() * 2
        max = excel_data_df["Цена"].max()
       # axs[1][0].set_axvline(reccomended_price, 0, excel_data_df['Цена'].dropna().max(), color='red', linewidth=2,                  #  label='РРЦ на момент продажи')
        #axs[1][0].set_minorticks_on()
        #axs[1][0].set_legend(loc=0)
        axs[1][0].set_ylabel('Количество')
        #axs[1][0].set_xlim(min, max)
        #axs[1][0].grid()

        plt.minorticks_on()
        plt.show()


