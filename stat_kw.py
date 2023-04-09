'''Keywords statistics'''

import json

raw_data = []
with open("ГЧ21_keywords_theses.json", encoding="utf8") as f:
    raw_data = json.load(f)
raw_keywords = [kw["keywords"] for kw in raw_data[2]["data"]]
keywords = {}
for kw in raw_keywords:
    if kw:
        for i in kw.split(", "):
            if i.lower() in keywords:
                keywords[i.lower()] += 1
            else:
                keywords[i.lower()] = 1

all_kw = len(keywords)
sum_one = sum(value == 1 for value in keywords.values())
print(f"Всего ключевых слов: {all_kw}")
print(f"Встречаются 1 раз:   {sum_one}")
print(f"Частота:             {sum_one/all_kw*100}%")
# print(sorted(keywords, key=keywords.get, reverse=True))
# print({i:keywords[i] for i in list(keywords)[0:7]})
