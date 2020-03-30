import requests
from bs4 import BeautifulSoup
import csv
import os

URL = 'https://h24.ua/doctors/0-ukraine'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
HOST = 'https://h24.ua'
FILE = 'doctors.csv'

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find('ul', class_='pagination').find_all('li')
    #total_pages = int(soup.find('div', {'class': 'page_listing'}).findAll('a')[-1].text)
    print(pagination)
    if pagination:
        return int(pagination[-2].get_text())
    else:
        return 1

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all(class_="doctors")
    doctors = []
    for item in items:
        doctors.append({
            'full name': item.find('a','div', class_='doctors-about__name').get_text(strip=True),
            #.replace('комментарий',''),
            'link': HOST + item.find('a','div', class_='doctors-about__name').get('href'),
            'speciality': item.find('div', class_='doctorsListPage--body__speciality').find_next('p', class_='doctor-speciality').get_text(strip=True),
            'clinik': item.find('a', 'div', class_='division-title-d').get_text(strip=True),
         })
    
    print(doctors)
    save_file(doctors, FILE)
    os.startfile(FILE)

def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['ФИО', 'Ссылка', 'Специальность', 'Клиника'])
        for item in items:
            writer.writerow([item['full name'], item['link'], item['speciality'], item['clinik']])

def parse():
    URL = input('Введите URL: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        doctors = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            doctors.extend(get_content(html.text))
        save_file(doctors, FILE)
        print(f'Всего {len(doctors)} докторов')
        os.startfile(FILE)
    else:
        print('Error')


parse()
