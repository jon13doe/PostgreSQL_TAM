pip install lxml beautifulsoup4 requests

import requests
from bs4 import BeautifulSoup as BS
import lxml
import json
import csv

def requ(url, headers):
    req = requests.get(url, headers=headers)
    src = req.text
    return BS(src, 'lxml')



headers = {'Accept': 'text/html,application/xhtml+xml,\
           application/xml;q=0.9,image/avif,image/webp,\
           image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', \
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
           AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}

url = 'https://meteopost.com/ukraine/ua/'

soup = requ(url, headers)

all_regions = soup.find_all(class_='head3')

all_dict = {}

for region in all_regions:
    region_name = region.text
    region_url = url[:-12] + region.get('href')

    soup = requ(region_url, headers)

    all_districts = soup.find_all(class_='head3')
    
    all_districts_dict = {}

    for district in all_districts:
        district_name = district.text
        district_url = url[:-12] + district.get('href')

        soup = requ(district_url, headers)

        all_cities = soup.find_all(class_='head4')
    
        all_cities_dict = {}
        
        for citie in all_cities:
            citie_name = citie.text
            citie_url = url[:-12] + citie.get('href')
            
            all_cities_dict[citie_name] = citie_url

        with open(f"/data/notebook_files/weather/districts/{district_name}.json", "w", encoding="utf-8") as file:
            json.dump(all_cities_dict, file, indent=4, ensure_ascii=False)

        all_districts_dict[district_name] = district_url
    
    with open(f"/data/notebook_files/weather/regions/{region_name}.json", "w", encoding="utf-8") as file:
        json.dump(all_districts_dict, file, indent=4, ensure_ascii=False)

    all_dict[region_name] = region_url

with open(f"/data/notebook_files/weather/regions.json", "w", encoding="utf-8") as file:
        json.dump(all_dict, file, indent=4, ensure_ascii=False)
        
head = ['Населенний пункт', 'Дата', 'Час', 'Температура', 'Хмарність',
        'Опади', 'Вологість', 'Видимість', 'Тиск', 'Вітер', 'Магнітні бурі',
        'Забруд. повітря', 'Ризик алергії']

citie, date, time, temp, cloud, rain, hum, see, pres, wind, magn, dirt, aler = head


with open(f"/data/notebook_files/weather/base.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                citie, date, time, temp, cloud, rain, hum, see, pres, wind, magn, dirt, aler 
            )
        )
        
with open(f"/data/notebook_files/weather/curent/weather.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                citie, temp, wind, cloud
            )
        )
        
with open('/data/notebook_files/weather/regions.json') as file:
    regions = json.load(file)

for r in regions:
    with open(f"/data/notebook_files/weather/all.csv", "a", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (r, )
        )
        print(r)
    with open(f'/data/notebook_files/weather/regions/{r}.json') as file:
        districts = json.load(file)
    
    for d in districts:
        with open(f"/data/notebook_files/weather/all.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                ('', d, )
            )
        print(d)
        
        with open(f'/data/notebook_files/weather/districts/{d}.json') as file:
            cities = json.load(file)
    
        for c in cities:
            with open(f"/data/notebook_files/weather/all.csv", "a", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(
                    ('', '', c, )
                     )
                     
with open('/data/notebook_files/weather/regions.json') as file:
    regions = json.load(file)

for r in regions:
    with open(f"/data/notebook_files/weather/curent/weather.csv", "a", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (r + 'Область', )
        )
        print(r)
    with open(f'/data/notebook_files/weather/regions/{r}.json') as file:
        districts = json.load(file)
    
    for d in districts:
        with open(f"/data/notebook_files/weather/curent/weather.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (d, )
            )
        print(d)
        
        with open(f'/data/notebook_files/weather/districts/{d}.json') as file:
            cities = json.load(file)
    
        for c in cities:
            citie_url = cities[c]

            soup = requ(citie_url, headers)

            curent_weather = soup.find(class_='divhelp').find(class_='dat')
            

            if curent_weather:
                try:
                    data = curent_weather.text.split(', ')
                    data.pop(1)
                    temp = data[0].rsplit()[-1]
                    wind = data[1].rsplit()[1]
                    cloud = data[2].rsplit()[-1]
                except:
                    temp = wind = cloud = '-'

            else:
                temp = wind = cloud = '-'

            with open(f"/data/notebook_files/weather/curent/weather.csv", "a", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(
                        (
                            c, temp, wind, cloud
                        )
                    )