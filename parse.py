import random
import ssl
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import re
import pandas
import requests
from bs4 import BeautifulSoup
from pandas import ExcelWriter

from ReadAndAnalyzeData import ReadAndAnalyzeData
from TlsAdapter import TlsAdapter

CIPHERS = """ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:AES256-SHA"""


def get_content(html):#Подключение драйвера и сбор данных со страницы
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driverServise = Service(executable_path='./driver/chromedriver.exe')
    browser = webdriver.Chrome(service=driverServise, options=options, executable_path='C:/cd/chromedriver.exe')
    browser.get(html)
    htmlp = browser.page_source
    soup = BeautifulSoup(htmlp, 'lxml')
    blocks = soup.find_all('div', class_=re.compile('iva-item-content'))
    data = []
    for block in blocks: # сбор данных с страницы
        data.append({
            "Наименование": block.find('h3', class_=re.compile('title-root')).get_text(strip=True),
            'Цена': block.find('span', class_=re.compile('price-text')).get_text(strip=True).replace('₽', '').replace(
                '\xa0', '').replace('Цена не указана','0'),
            'Город': block.find('a', class_=re.compile('link-link')).get('href').split('/')[1],
            'Район': block.find('div', class_=re.compile('geo-root')).get_text(strip=True),
            "Дата публикации": block.find('div', class_=re.compile('item-date')).get_text(strip=True),
            'Ссылка': url + block.find('a', class_=re.compile('link-link')).get('href'),
        })
    browser.quit()
    return data


def get_pages(html):#Получение количества страниц
    soup = BeautifulSoup(html.text, 'html.parser')
    try:
        pages = soup.find('span', {'data-marker': 'pagination-button/next'}).previous_element
    except:
        pages = 1
    print('Количество найденных страниц: ', pages)
    return pages


def save_excel(data, file_name): #Сохранение полученных данных в Excel
    df_data = pandas.DataFrame(data)
    writer = ExcelWriter(f'{file_name}.xlsx')
    df_data.to_excel(writer, f'{file_name}')
    writer.save()
    print(f'Данные сохранены в файл "{file_name}.xlsx"')


def parse(url, search):
    min_price = 1  #Параметр минимальной цены
    max_price = 10000000  #Параметр максимальной  цены
    html = get_html(url,
                    params={'bt': 1, 'pmax': max_price, 'pmin': min_price, 'q': search, 's': '2', 'view': 'gallery'})
    soup = BeautifulSoup(html.text, 'lxml')
    print(soup.h1.get_text())
    print('Ссылка со всеми параметрами:\n', html.url)
    print('Статус код сайта: ', html.status_code)
    data = []
    # проверка сайта на доступ
    if html.status_code == 200:
        # вызов функции для вывода количества найденных страниц
        get_pages(html)
        pagination = int(input('Сколько страниц спарсить? '))
        for page in range(1, pagination + 1):
            html = get_html(url,
                            params={'bt': 1, 'p': page, 'pmax': max_price, 'pmin': min_price, 'q': search, 's': '2',
                                    'view': 'gallery'})
            print(f'Парсинг страницы {page} из {pagination}...')
            data.extend(get_content(html.url))
            time.sleep(random.randint(1, 3)) #Случайное время для задержки
        print(f'Получили {len(data)} позиций') # сохраняем в эксель, передав наши собранные данные и запрос
        save_excel(data, search)
    else:
        print('Ошибка доступа к сайту')


def get_html(url, params=None): #Получение html страницы
    session.mount("https://", adapter)
    html = session.request('GET', url, params=params)
    print("SITE STATUS CODE ", html.status_code)
    return html

print("Введите значение для поиска: ")
search = input()
start_time = time.time()
session = requests.session()
adapter = TlsAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
session.mount("https://", adapter)
url = "http://avito.ru/all?"
parse(url, search)
print("--- %s время парсинга ---" % (time.time() - start_time))
print("Провести анализ введенных данных?(y/n)")
anwser = input()
if (anwser=='y'):
    print("Введите ррц")
    rrc = input()
    ReadAndAnalyzeData.analyze_data(search, rrc)
else:
    print("Работа программы завершена.")


