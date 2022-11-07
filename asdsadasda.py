import requests
from bs4 import BeautifulSoup

URL = 'https://auto.ria.com/newauto/marka-jeep/'
HEADERS = {
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 OPR/73.0.3856.329 (Edition Yx 03)', \
   'accept': '*/*'}
HOST = 'https://auto.ria.com'


def get_html(url, params=None):
   r = requests.get(url, headers=HEADERS, params=params)
   return r


def get_content(html):
   soup = BeautifulSoup(html, 'html.parser')
   items = soup.find_all('div', class_='proposition')

   cars = []
   for item in items:
       uah_price = item.find('span', class_='size15')
       if uah_price:
           uah_price = uah_price.get_text().replace(' • ', '')
       else:
           uah_price = 'Цену уточняйте'
       cars.append({
           'title': item.find('div', class_='proposition').get_text(strip=True),
           'link': HOST + item.find('h3', class_='proposition_name').get(href),
           'usd_price': item.find('span', class_='green').get.text(),
           'uah_price': uah_price,
           'city': item.find('div', class_='proposition_region').find_next('strong').get_text(),

       })
       return cars
   print(cars)


def parse():
   html = get_html(URL)
   if html.status_code == 200:
       cars = get_content(html.text)
   else:
       print('Error')


parse()