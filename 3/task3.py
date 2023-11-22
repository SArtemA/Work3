from bs4 import BeautifulSoup
import numpy as np
import re
import json
import lxml


def get_num(selector: str, items: list):
    nums = list(map(lambda x: int(x[selector]), items))
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
        if selector in item:
            freq[item[selector]] = freq.get(item[selector], 0) + 1

    return freq


def handle_file(file_name):
    with open(file_name, encoding="utf-8") as file:
        text = ""
        for row in file.readlines():
            text += row

        star = BeautifulSoup(text, 'xml').star

        item = dict()
        for el in star.contents:
            if el.name is not None:
                item[el.name] = el.get_text().strip()

        return item


items = []
for i in range(1, 501):
    file_name = f"zip_var_78/{i}.xml"
    items.append(handle_file(file_name))
with open("result.json", 'w', encoding="utf-8") as result:
    result.write(json.dumps(items))
items = sorted(items, key=lambda x: int(x['radius']), reverse=True)

with open("result_radius.json", 'w', encoding="utf-8") as result:
    result.write(json.dumps(items))

filtered = []
for item in items:
    if float(item['distance'].replace(' million km', '').strip()) >= 6000000:
        filtered.append(item)

with open("result_distance.json", 'w', encoding="utf-8") as result:
    result.write(json.dumps(filtered))

num_stat = get_num("radius", items)

print(num_stat)

title_freq = get_freq("name", items)

print(title_freq)