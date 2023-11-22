from bs4 import BeautifulSoup
import re
import json
import numpy as np

def get_num(selector: str, items: list):
    nums = list(map(lambda x: x[selector], items))

    stat = {}

    stat['Сумма'] = sum(nums)
    stat['Минимум'] = min(nums)
    stat['Максимум'] = max(nums)
    stat['Среднее'] = np.average(nums)
    stat['Среднеквадратичное_отклонение'] = np.std(nums)

    return stat


def get_freq(selector: str, items: list):
    freq = {}

    for item in items:
        freq[item[selector]] = freq.get(item[selector], 0) + 1

    return freq

def handle_file(file_name):
    with open(file_name, encoding='utf-8') as file:

        text = ''
        for row in file.readlines():
            text += row

        site = BeautifulSoup(text, 'html.parser')
        item = dict()
        item['type'] = site.find_all("span", string=re.compile('Тип:'))[0].get_text().split(":")[1].strip()
        item['tournament'] = site.find_all('h1')[0].get_text().split(":")[1].strip()
        city_start = site.find_all('p', attrs={'class': 'address-p'})[0].get_text()
        city_start = ''.join(re.split('Город:', city_start))
        city_start = re.split('Начало:', city_start)
        item['city'] = city_start[0].strip()
        item['start'] = city_start[1].strip()
        item['tours_amount'] = int(site.find_all('span', attrs={'class': 'count'})[0].get_text().split(':')[1].strip())
        item['time_control'] = int(site.find_all('span', attrs={'class': 'year'})[0].get_text().split(':')[1].replace('мин', '').strip())
        item['min_rank'] = int(site.find_all("span", string=re.compile('Минимальный рейтинг для участия:'))[0].get_text().split(":")[1].strip())
        item['img_url'] = site.find_all('img')[0]['src']
        item['rating'] = float(site.find_all("span", string=re.compile('Рейтинг:'))[0].get_text().split(":")[1].strip())
        item['views'] = int(site.find_all("span", string=re.compile('Просмотры:'))[0].get_text().split(":")[1].strip())


    return item


items = []
for i in range(1,1000):
    file_name = f"zip_var_78/{i}.html"
    items.append(handle_file(file_name))
json_items = json.dumps(items)
with open("result.json", "w", encoding="utf-8") as result:
    result.write(json_items)

views = []
for i in range(1, 1000):
    file_name = f"zip_var_78/{i}.html"
    views.append(handle_file(file_name))
views = sorted(views, key=lambda x: x['views'], reverse=True)
json_views = json.dumps(views)
with open("result_views.json", "w", encoding="utf-8") as result:
    result.write(json_views)

print(len(items))
num_stat = get_num("time_control", items)
print(num_stat)
city_freq = get_freq("city", items)
print(city_freq)