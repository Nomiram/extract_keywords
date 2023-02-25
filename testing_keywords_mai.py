'''extract keywords from AiK thesis'''
import json

import nltk
import pytextrank
import spacy
import yake
from nlp_rake import Rake
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from summa import keywords

from yake_keywords_mai import extract_keywords

nltk.download("stopwords")

nlp = spacy.load("ru_core_news_sm")

# add PyTextRank to the spaCy pipeline
nlp.add_pipe("textrank")

def stat(list1: list[str], list2: list[str]) -> tuple[int, int]:
    sum_ = sum(el in list1 for el in list2)
    neg = len(list2) - sum_
    if neg:
        return sum_, neg, sum_/len(list2)
    else:
        return sum_, neg, 0



# with open("theses_full.json","r",encoding="utf8") as f:
with open("ГЧ21_keywords_theses.json","r",encoding="utf8") as f:
    all_texts = json.load(f)[2]["data"]
cnt = 0
# for i in list(all_texts):
stats = {}
stats["rake"] = {}
stats["yake"] = {}
stats["text_rank_keywords2"] = {}
stats["rake"]["sum"]=0
stats["rake"]["all"]=0
stats["yake"]["sum"]=0
stats["yake"]["all"]=0
stats["text_rank_keywords2"]["sum"]=0
stats["text_rank_keywords2"]["all"]=0
for i, raw_data in enumerate(all_texts):
    cnt+=1
    if cnt >= 200:
        break
    print(f"{cnt}/{len(all_texts)}")
    ready_keywords = raw_data["keywords"]
    text = raw_data["thesis"]
    if raw_data["keywords"] is None:
        continue
    # print()
    # print(subject)
    # print()
    # print(text)
    # print("\n\nManual")
    # print(extract_keywords(text)["manual"])
    # print("Ready", ready_keywords)
    # print("\n\nRAKE")
    stops = list(set(stopwords.words("russian")))

    rake = Rake (stopwords = stops, max_words = 3)
    # print(rake.apply(text)[:10]) # raw output
    rake_keywords = [i[0] for i in rake.apply(text)[:10]]
    # print(rake_keywords)
    # print("\n\nYAKE!")
    extractor = yake.KeywordExtractor (
        lan = "ru",     # язык
        n = 3,          # максимальное количество слов в фразе
        dedupLim = 0.3, # порог похожести слов
        top = 10        # количество ключевых слов
    )
    # print(extractor.extract_keywords(text)) # raw output
    yake_keywords = [i[0] for i in extractor.extract_keywords(text)]
    # print(yake_keywords)

    # print("\n\nTextRank")
    text_clean = ""
    # уберем стоп-слова
    for i in text.split():
        if i not in stops:
            text_clean += i + " "
    text_rank_keywords = keywords.keywords(text_clean, language = "russian").split("\n")
    # print(text_rank_keywords)
    from textblob import TextBlob
    blob = TextBlob(text_clean)
    noun = blob.noun_phrases

    # print("\n\nTextRank v2")
    doc = nlp(text)

    # examine the top-ranked phrases in the document
    text_rank_keywords2 = [phrase.text for phrase in doc._.phrases]
    # print(text_rank_keywords2)

    # print("\n\nTfidfVectorizer")
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(noun)
    from pymorphy3 import MorphAnalyzer
    morph = MorphAnalyzer()
    words = nltk.word_tokenize(text_clean)

    items = [(str(morph.parse(w)[0].tag.POS), w) for w in words]
    # print(items)
    # print(vectorizer.get_feature_names_out())
    print("SUM:")
    print(ready_keywords)
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

print(stats)
