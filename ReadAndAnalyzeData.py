import pandas
from PlotGraphic import PlotGraphic

file_name = 'iphone 14 128'
reccomended_price = 60000

excel_data_df = pandas.read_excel(file_name + '.xlsx')

print(len(excel_data_df.index))
excel_data_df = excel_data_df.drop_duplicates(subset='Ссылка')

PlotGraphic.plot_price(excel_data_df, reccomended_price, 'График распределения до чистки данных для ' + file_name)

excel_data_df = excel_data_df[excel_data_df["Наименование"].str.contains("pro") == False]
excel_data_df = excel_data_df[excel_data_df["Наименование"].str.contains("Сбер") == False]
excel_data_df = excel_data_df[excel_data_df["Наименование"].str.contains("альфа") == False]
print(len(excel_data_df.index))

PlotGraphic.plot_price(excel_data_df, reccomended_price, 'График распределения до чистки данных для ' + file_name + ' без сервисов' )
