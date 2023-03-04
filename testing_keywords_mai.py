'''extract keywords from AiK thesis'''
import json
from typing import List, Tuple

import nltk
import spacy
import yake
from nlp_rake import Rake
from nltk.corpus import stopwords
from summa import keywords

from yake_keywords_mai import extract_keywords

# Количество текстов для теста
COUNT_OF_TEXTS = 200

nltk.download("stopwords")
nltk.download('brown')


def stat(list1: List[str], list2: List[str]) -> Tuple[int, int]:
    '''providing comparison statistics of 2 lists'''
    copy_list1 = [el.lower() for el in list1]
    copy_list2 = [el.lower() for el in list2]
    sum_ = sum(el in copy_list1 for el in copy_list2)
    neg = len(list2) - sum_
    if neg:
        return sum_, neg, sum_ / len(list2)
    # else:
    return sum_, neg, 0


# with open("theses_full.json","r",encoding="utf8") as f:
with open("ГЧ21_keywords_theses.json", "r", encoding="utf8") as f:
    all_texts = json.load(f)[2]["data"]
stats = {"ready_keywords": {"description": "Пользовательские ключевые слова"},
         "manual": {"description": "Прямой поиск"},
         "rake": {"description": "RAKE"},
         "yake": {"description": "YAKE"},
         "text_rank_keywords2": {"description": "TextRank"},
         }
for _, method in stats.items():
    method["keywords"] = []
    method["sum"] = 0
    method["all"] = 0

for i, raw_data in enumerate(all_texts):
    if i >= COUNT_OF_TEXTS:
        break
    print(f"{i}/{len(all_texts)}")
    if raw_data["keywords"] is None:
        continue
    ready_keywords = raw_data["keywords"].split(", ")
    text = raw_data["thesis"]
    stats["manual"]["keywords"].append(extract_keywords(text)["manual"])
    # print("\n\nRAKE")
    stops = list(set(stopwords.words("russian")))

    rake = Rake(stopwords=stops, max_words=3)
    rake_keywords = [i[0] for i in rake.apply(text)[:10]]
    # print("\n\nYAKE!")
    extractor = yake.KeywordExtractor(
        lan="ru",     # язык
        n=3,          # максимальное количество слов в фразе
        dedupLim=0.3,  # порог похожести слов
        top=10        # количество ключевых слов
    )
    yake_keywords = [i[0] for i in extractor.extract_keywords(text)]

    # print("\n\nTextRank")
    text_clean = ""
    # уберем стоп-слова
    for i in text.split():
        if i not in stops:
            text_clean += i + " "
    text_rank_keywords = keywords.keywords(
        text_clean, language="russian").split("\n")
    from textblob import TextBlob
    blob = TextBlob(text_clean)
    noun = blob.noun_phrases

    # print("\n\nTextRank v2")
    from text_rank_normal_form import TextRank_m

    text_rank_keywords2 = TextRank_m(text)

    print("SUM:")
    print("Ready   ", ready_keywords)
    print("manual  ", stats["manual"]["keywords"][-1])
    print("RAKE    ", rake_keywords)
    print("YAKE    ", yake_keywords)
    print("TextRank", text_rank_keywords2)
    stats["ready_keywords"]["all"] += len(ready_keywords)
    stats["ready_keywords"]["sum"] += len(ready_keywords)
    s, _, _ = stat(ready_keywords, stats["manual"]["keywords"][-1])
    stats["manual"]["sum"] += s
    stats["manual"]["all"] += len(stats["manual"]["keywords"][-1])
    print("manual", stat(ready_keywords, stats["manual"]["keywords"][-1]))

    s, _, _ = stat(ready_keywords, rake_keywords)
    stats["rake"]["sum"] += s
    stats["rake"]["all"] += len(rake_keywords)
    print("RAKE", stat(ready_keywords, rake_keywords))
    s, _, _ = stat(ready_keywords, rake_keywords)
    stats["yake"]["sum"] += s
    stats["yake"]["all"] += len(yake_keywords)
    print("YAKE!", stat(ready_keywords, yake_keywords))
    s, _, _ = stat(ready_keywords, text_rank_keywords2)
    stats["text_rank_keywords2"]["sum"] += s
    stats["text_rank_keywords2"]["all"] += len(text_rank_keywords2)
    # print("text_rank_keywords", stat(ready_keywords, text_rank_keywords))
    print("text_rank_keywords2", stat(ready_keywords, text_rank_keywords2))

print()
print("Всего текстов:", COUNT_OF_TEXTS)
for key, method in stats.items():
    print("\t" + method["description"])
    print(f"Всего предложено:   {method['all']}")
    print(f"Совпадений:         {method['sum']}")
    print(f"Процент совпадений: {method['sum']/method['all']*100}%")
