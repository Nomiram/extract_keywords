'''extract keywords from AiK thesis'''
import json
import string
import sys

import nltk
import yake
from nltk.stem import SnowballStemmer


def stem(text):
    '''Tokenize and stemming text'''
    words = nltk.word_tokenize(text)
    words = [word for word in words if word.isalpha()]
    snowball_ru = SnowballStemmer(language="russian")
    snowball_en = SnowballStemmer(language="english")
    text_strip = []
    for word in words:
        if word[0].lower() in string.ascii_lowercase:
            text_strip.append(snowball_en.stem(word))
        else:
            text_strip.append(snowball_ru.stem(word))
    text_strip = " ".join(text_strip)
    return text_strip

def extract_keywords(text):
    '''extract keywords by manual method using file `keywords.json` and `YAKE!`'''
    # Manual method
    text_stem = stem(text)
    stem_keywords = {}
    with open("keywords.json","r",encoding="utf8") as f:
        keywords = json.load(f)
        for kw in keywords:
            stem_keywords[stem(kw)] = kw
    result = []
    # print("+",stem_keywords)
    for kw in list(stem_keywords):
        if text_stem.find(kw) != -1:
            result.append(stem_keywords[kw])
    # print("!",result,"!")
    # YAKE
    extractor = yake.KeywordExtractor (
        lan = "ru",     # язык
        n = 3,          # максимальное количество слов в фразе
        dedupLim = 0.3, # порог похожести слов
        top = 10        # количество ключевых слов
    )
    yake_result = ([i[0] for i in extractor.extract_keywords(text)])
    return json.dumps({"manual": result, "yake": yake_result})

if __name__ == "__main__":
    nltk.download("stopwords", quiet=True)
    input_text = sys.stdin.readlines()
    print(extract_keywords("\n".join(input_text)))
