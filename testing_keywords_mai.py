'''extract keywords from AiK thesis'''
import json

import nltk
import yake
from nlp_rake import Rake
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from summa import keywords

nltk.download("stopwords")
with open("theses_grnti.json","r",encoding="utf8") as f:
    all_texts = json.load(f)
cnt = 0
for i in list(all_texts):
    cnt+=1
    if cnt >= 8:
        break
    print(cnt)
    text = ""
    subject = ""
    subject = all_texts[i]["subject"]
    text = all_texts[i]["text"]
    print()
    print(subject)
    print()
    print(text)
    print("\n\nRAKE")
    stops = list(set(stopwords.words("russian")))

    rake = Rake (stopwords = stops, max_words = 3)
    print(rake.apply(text)[:10])
    print("\n\nYAKE!")
    extractor = yake.KeywordExtractor (
        lan = "ru",     # язык
        n = 3,          # максимальное количество слов в фразе
        dedupLim = 0.3, # порог похожести слов
        top = 10        # количество ключевых слов
    )
    print([i[0] for i in extractor.extract_keywords(text)])

    print("\n\nTextRank!")
    text_clean = ""
    # уберем стоп-слова
    for i in text.split():
        if i not in stops:
            text_clean += i + " "
    print(keywords.keywords (text_clean, language = "russian").split("\n"))
    from textblob import TextBlob
    blob = TextBlob(text_clean)
    noun = blob.noun_phrases
    print("\n\nTfidfVectorizer!")
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(noun)
    from pymorphy3 import MorphAnalyzer
    morph = MorphAnalyzer()
    words = nltk.word_tokenize(text_clean)

    items = [(str(morph.parse(w)[0].tag.POS), w) for w in words]
    # print(items)
    print(vectorizer.get_feature_names_out())
