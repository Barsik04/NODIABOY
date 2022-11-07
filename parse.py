import random
import ssl
import time
import random
import ssl
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas
import requests
import re
from bs4 import BeautifulSoup
from pandas import ExcelWriter

from TlsAdapter import TlsAdapter

import pandas
import requests
from bs4 import BeautifulSoup
from pandas import ExcelWriter

from TlsAdapter import TlsAdapter

CIPHERS = """ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:AES256-SHA"""


def get_content(html):
    """ сбор контента со страницы """

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    # executable_path param is not needed if you updated PATH
    driverServise = Service(executable_path='C:/cd/chromedriver.exe')
    browser = webdriver.Chrome(service=driverServise, options=options, executable_path='C:/cd/chromedriver.exe')
    browser.get(html)
    htmlp = browser.page_source
    #print(htmlp)
    soup = BeautifulSoup(htmlp, 'lxml')

    blocks = soup.find_all('div', class_=re.compile('iva-item-content'))
    # сбор данных с страницы
    data = []
    for block in blocks:

        data.append({
            "Наименование": block.find('h3', class_=re.compile('title-root')).get_text(strip=True),
            'Цена': block.find('span', class_=re.compile('price-text')).get_text(strip=True).replace('₽', '').replace('\xa0', ''),
            'Город': block.find('a', class_=re.compile('link-link')).get('href').split('/')[1],
            'Район': block.find('div', class_=re.compile('geo-root')).get_text(strip=True),
            "Дата публикации": block.find('div', class_=re.compile('item-date')).get_text(strip=True),
            'Ссылка': url + block.find('a', class_=re.compile('link-link')).get('href'),
        })
    browser.quit()
    return data

def get_pages(html):
    """ получаем количество страниц """
    soup = BeautifulSoup(html.text, 'html.parser')
    # находим кол-во страниц, иначе количество страниц равно 1
    try:
        pages = soup.find('span', {'data-marker': 'pagination-button/next'}).previous_element
    except:
        pages = 1
    print('Количество найденных страниц: ', pages)
    return pages

def save_excel(data, file_name):
    # сохраняем полученные данные в эксель через pandas
    df_data = pandas.DataFrame(data)
    print(f'До удаления дубликатов: {len(df_data)} записей')
    # чистим дубликаты записей (проплаченные посты дублируются на разных страницах)
    #data_clear = df_data.drop_duplicates('Ссылка')
    #print(f'После удаления дубликатов: {len(data_clear)} записей')
    writer = ExcelWriter(f'{file_name}.xlsx')
    df_data.to_excel(writer, f'{file_name}')
    writer.save()
    print(f'Данные сохранены в файл "{file_name}.xlsx"')

def parse(url, search):
    min_price = 1
    max_price = 10000000
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
        pagination = int(get_pages(html))
        # int(input('Сколько страниц спарсить? '))
        for page in range(1, pagination + 1):
            html = get_html(url,
                            params={'bt': 1, 'p': page, 'pmax': max_price, 'pmin': min_price, 'q': search, 's': '2',
                                    'view': 'gallery'})
            print(f'Парсинг страницы {page} из {pagination}...')
            data.extend(get_content(html.url))
            time.sleep(random.randint(1, 3))
        print(f'Получили {len(data)} позиций')
        # сохраняем в эксель, передав наши собранные данные и запрос
        save_excel(data, search)
    else:
        print('Ошибка доступа к сайту')


def get_html(url, params=None):
    session.mount("https://", adapter)
    """ получение кода страницы """
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0)"
    }
    html = session.request('GET', url, params=params)
    print("SITE ", html.status_code, " CODE ", html)
    return html


session = requests.session()
adapter = TlsAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
session.mount("https://", adapter)
url = "http://avito.ru"
parse(url, "Iphone X 64")
parse(url, "Iphone 11 64")
parse(url, "Iphone 12 64")
parse(url, "Iphone 13 128")
parse(url, "Iphone 14 128")
