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
                keywords[i.lower()]+=1
            else:
                keywords[i.lower()]=1

sum_one = 0
all = len(keywords)
for key, value in keywords.items():
    if value == 1:
        sum_one+=1
print(f"Всего ключевых слов: {all}")
print(f"Встречаются 1 раз:   {sum_one}")
print(f"Частота:             {sum_one/all*100}%")
# print(sorted(keywords, key=keywords.get, reverse=True))
# print({i:keywords[i] for i in list(keywords)[0:7]})
