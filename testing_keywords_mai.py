'''extract keywords from AiK thesis'''
import json
from typing import List, Tuple

import nltk
import yake
from nlp_rake import Rake
from nltk.corpus import stopwords

from text_rank_normal_form import extract_keywords as TextRank_v1
from text_rank_v2_normal_form import extract_keywords as TextRank_v2
from yake_keywords_mai import extract_keywords as YAKE

# from manual_m import stem


# Количество текстов для теста
COUNT_OF_TEXTS = 200


class keywords_testing:

    def init_stats(self):
        """
        The function initializes a dictionary of methods and their keyword lists,
        sums, and counts.
        """
        self.stats = {"ready_keywords": {"description": "Пользовательские ключевые слова"},
                      "manual": {"description": "Прямой поиск"},
                      "rake_keywords": {"description": "RAKE"},
                      "yake_keywords": {"description": "YAKE"},
                      "text_rank_keywords": {"description": "TextRank"},
                      "text_rank_keywords2": {"description": "TextRank2"},
                      "text_rank+manual": {"description": "TextRank2 + Прямой"},
                      }
        for method in self.stats.values():
            method["keywords"] = []
            method["sum"] = 0
            method["all"] = 0

    def stat(self, list1: List[str], list2: List[str]) -> Tuple[int, int]:
        '''providing comparison statistics of 2 lists'''
        copy_list1 = [el.lower() for el in list1]
        copy_list2 = [el.lower() for el in list2]
        sum_ = sum(el in copy_list1 for el in copy_list2)
        if neg := len(list2) - sum_:
            return sum_, neg, sum_ / len(list2)
        else:
            return sum_, neg, 0

    def __init__(self):
        self.init_stats()

    def apply_methods(self, text, ready_keywords):
        """apply extracting methods

        Args:
            text (str): text to analyze
            ready_keywords (List): User provided keywords
        """
        self.stats["ready_keywords"]["keywords"].append(ready_keywords)
        self.stats["manual"]["keywords"].append(
            YAKE(text)["manual"])
        # print("\n\nRAKE")
        stops = list(set(stopwords.words("russian")))

        rake = Rake(stopwords=stops, max_words=3)
        self.stats["rake_keywords"]["keywords"].append(
            [i[0] for i in rake.apply(text)[:10]])
        # print("\n\nYAKE!")
        extractor = yake.KeywordExtractor(
            lan="ru",      # язык
            n=3,           # максимальное количество слов в фразе
            dedupLim=0.3,  # порог похожести слов
            top=10         # количество ключевых слов
        )
        self.stats["yake_keywords"]["keywords"].append(
            [i[0] for i in extractor.extract_keywords(text)])

        # TextRank v1
        self.stats["text_rank_keywords"]["keywords"].append(TextRank_v1(text))
        # TextRank v2
        self.stats["text_rank_keywords2"]["keywords"].append(TextRank_v2(text))
        # TextRank v2 + Manual
        self.stats["text_rank+manual"]["keywords"].append(list(set(
            self.stats["text_rank_keywords2"]["keywords"][-1]+self.stats["manual"]["keywords"][-1])))
        # self.stats["text_rank_keywords2"]["keywords"].append(
        # keywords.keywords(text, language="russian", words=10).split())

        print("SUM:")
        for method in self.stats.values():
            print(method["description"], method["keywords"][-1])
            s, _, _ = self.stat(ready_keywords, method["keywords"][-1])
            method["sum"] += s
            method["all"] += len(method["keywords"][-1])
            print(method["description"], self.stat(
                ready_keywords, method["keywords"][-1]))
        # self.stats["ready_keywords"]["all"] += len(ready_keywords)
        # self.stats["ready_keywords"]["sum"] += len(ready_keywords)


if __name__ == "__main__":
    nltk.download("stopwords")
    nltk.download('brown')
    # with open("theses_full.json","r",encoding="utf8") as f:
    # with open("text1.txt", "r", encoding="utf8") as f:
    with open("ГЧ21_keywords_theses.json", "r", encoding="utf8") as f:
        # all_texts = [{"thesis": f.read(), "keywords": "ДТА"}]
        all_texts = json.load(f)[2]["data"]
    testing_class = keywords_testing()
    for current_text_num, raw_data in enumerate(all_texts):
        if current_text_num >= COUNT_OF_TEXTS:
            break
        print(f"{current_text_num}/{len(all_texts)}")
        if raw_data["keywords"] is None:
            continue
        ready_keywords = raw_data["keywords"].split(", ")
        text = raw_data["thesis"]
        testing_class.apply_methods(text, ready_keywords)
    print()
    print("Всего текстов:", COUNT_OF_TEXTS)
    for method in testing_class.stats.values():
        print("\t" + method["description"])
        print(f"Всего предложено:   {method['all']}")
        print(f"Совпадений:         {method['sum']}")
        if method['all'] > 0:
            print(
                f"Процент совпадений: {method['sum']/method['all']*100}%")
        else:
            print("Процент совпадений: 0%")
