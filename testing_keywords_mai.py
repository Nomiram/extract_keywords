'''extract keywords from AiK thesis'''
import json

import nltk
import yake
from nlp_rake import Rake
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from summa import keywords

from yake_keywords_mai import extract_keywords

nltk.download("stopwords")
with open("theses.json","r",encoding="utf8") as f:
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
    print("\n\nManual")
    print(extract_keywords(text)["manual"])
    print("\n\nRAKE")
    stops = list(set(stopwords.words("russian")))

    rake = Rake (stopwords = stops, max_words = 3)
    # print(rake.apply(text)[:10]) # raw output
    print([i[0] for i in rake.apply(text)[:10]])
    print("\n\nYAKE!")
    extractor = yake.KeywordExtractor (
        lan = "ru",     # язык
        n = 3,          # максимальное количество слов в фразе
        dedupLim = 0.3, # порог похожести слов
        top = 10        # количество ключевых слов
    )
    # print(extractor.extract_keywords(text)) # raw output
    print([i[0] for i in extractor.extract_keywords(text)])

    print("\n\nTextRank")
    text_clean = ""
    # уберем стоп-слова
    for i in text.split():
        if i not in stops:
            text_clean += i + " "
    print(keywords.keywords (text_clean, language = "russian").split("\n"))
    from textblob import TextBlob
    blob = TextBlob(text_clean)
    noun = blob.noun_phrases

    print("\n\nTextRank v2")
    import pytextrank
    import spacy

    nlp = spacy.load("ru_core_news_sm")

    # add PyTextRank to the spaCy pipeline
    nlp.add_pipe("textrank")
    doc = nlp(text)

    # examine the top-ranked phrases in the document
    print([phrase.text for phrase in doc._.phrases])

    print("\n\nTfidfVectorizer")
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(noun)
    from pymorphy3 import MorphAnalyzer
    morph = MorphAnalyzer()
    words = nltk.word_tokenize(text_clean)

    items = [(str(morph.parse(w)[0].tag.POS), w) for w in words]
    # print(items)
    print(vectorizer.get_feature_names_out())
