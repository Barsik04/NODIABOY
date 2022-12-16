import matplotlib
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
        plt.savefig('./output/by_price' + header)


        sns.histplot(excel_data_df['Цена'].dropna(), bins=50, color='purple')
        plt.suptitle(header, fontsize=12, color='black')
        min = excel_data_df["Цена"].min() * 0.9
        max = excel_data_df["Цена"].mean() * 2
        plt.axvline(reccomended_price, 0, excel_data_df['Цена'].dropna().max(), color='red', linewidth=2,
                    label='РРЦ на момент продажи')
        plt.minorticks_on()
        plt.legend(loc=0)
        plt.ylabel('Количество')
        plt.xlim(max, )
        plt.ticklabel_format(style='plain')
        plt.ylim(0, 10)
        plt.grid(True)
        plt.savefig('./output/by_price' + header + ' second_part')
        plt.show()

    def plot_pie(excel_data_df, header):
        city_data = excel_data_df['Город'].value_counts()
        #data = city_data.transpose()


        #data = pd.DataFrame(data = city_data.tolist(), columns = city_data.index.tolist())
        data  = pd.DataFrame([city_data.tolist()], columns = city_data.index.tolist())



        print(data)
        print (city_data.tolist())
        plt.pie(city_data.tolist(), labels=city_data.index.tolist())
        plt.show()


