from bs4 import BeautifulSoup
import numpy as np
import re
import json


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
    items = list()

    with open(file_name, encoding="utf-8") as file:
        text = ""
        for row in file.readlines():
            text += row

        root = BeautifulSoup(text, 'xml')

        for clothing in root.find_all("clothing"):
            item = dict()
            for gg in clothing.contents:
                if gg.name is None:
                    continue
                elif gg.name == "price" or gg.name == "reviews":
                    item[gg.name] = int(gg.get_text().strip())
                elif gg.name == "rating":
                    item[gg.name] = float(gg.get_text().strip())
                elif gg.name == "new":
                    item[gg.name] = gg.get_text().strip() == "+"
                elif gg.name == "exclusive" or gg.name == "sporty":
                    item[gg.name] = gg.get_text().strip() == "yes"
                else:
                    item[gg.name] = gg.get_text().strip()

            items.append(item)

        return items


items = []
for i in range(1, 101):
    file_name = f"zip_var_78/{i}.xml"
    items += handle_file(file_name)

with open("result_4.json", 'w', encoding="utf-8") as result:
    result.write(json.dumps(items))
items = sorted(items, key=lambda x: x['price'], reverse=True)

with open("result_price.json", 'w', encoding="utf-8") as result:
    result.write(json.dumps(items))

filtered = []
for item in items:
    if item['rating'] <= 3.8:
        filtered.append(item)

with open("result_rating.json", 'w', encoding="utf-8") as result:
    result.write(json.dumps(filtered))

num_stat = get_num('price', items)

print(num_stat)

title_freq = get_freq("color", items)

print(title_freq)