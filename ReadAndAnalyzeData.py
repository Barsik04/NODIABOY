import pandas
from PlotGraphic import PlotGraphic


class ReadAndAnalyzeData():
    def analyze_data(file_name, reccomended_price):
        excel_data_df = pandas.read_excel(file_name + '.xlsx')

        print("До удаления дублирующихся объявлений: " + str(len(excel_data_df.index)))
        excel_data_df = excel_data_df.drop_duplicates(subset='Ссылка')


        PlotGraphic.plot_price(excel_data_df, reccomended_price,
                               'График распределения цен  до чистки данных для ' + file_name)
        PlotGraphic.plot_pie(excel_data_df, file_name)

        excel_data_df = excel_data_df[excel_data_df["Наименование"].str.contains("pro") == False]

        excel_data_df = excel_data_df[excel_data_df["Наименование"].str.contains("Сбер") == False]
        excel_data_df = excel_data_df[excel_data_df["Наименование"].str.contains("альфа") == False]

        print("После удаления дублирующихся объявлений: " + str(len(excel_data_df.index)))

        PlotGraphic.plot_price(excel_data_df, reccomended_price,
                               'График распределения цен до чистки данных для ' + file_name + ' без сервисов')
