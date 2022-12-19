import pandas
from PlotGraphic import PlotGraphic


class ReadAndAnalyzeData():
    def analyze_data(file_name, reccomended_price):
        excel_data_df = pandas.read_excel(file_name + '.xlsx')

        print("До удаления дублирующихся объявлений: " + str(len(excel_data_df.index)) + " строк")

        excel_data_df = excel_data_df.drop_duplicates(subset='Ссылка')

        print("После удаления дублирующихся объявлений: " + str(len(excel_data_df.index)) + " строк")
        PlotGraphic.plot_pie(excel_data_df, file_name)

        if 'iphone' in file_name or 'Iphone' in file_name:
            excel_data_df = excel_data_df[excel_data_df["Наименование"].str.contains("pro") == False]

            data_with_sber = excel_data_df[excel_data_df["Наименование"].str.contains("Сбер|сбер|альфа|Альфа") == True]

            excel_data_df = excel_data_df[excel_data_df["Наименование"].str.contains("Сбер") == False]
            excel_data_df = excel_data_df[excel_data_df["Наименование"].str.contains("альфа") == False]

            print("После удаления несоотвествующих объявлений: " + str(len(excel_data_df.index)) + " строк")



        PlotGraphic.plot_price(excel_data_df, reccomended_price,
                               'График распределения цен для ' + file_name + ' без сервисов')


        if (not data_with_sber.empty):

            PlotGraphic.plot_price(data_with_sber, reccomended_price,
                                   'График распределения цен для устройств с сервисами ' + file_name + ' ')
