'''extract keywords from AiK thesis'''
import json
import sys

import nltk
import yake

from manual_m import manual_m


def yake_m(text, num=10):
    '''extract keywords by `YAKE!`'''
    extractor = yake.KeywordExtractor(
        lan="ru",     # язык
        n=3,          # максимальное количество слов в фразе
        dedupLim=0.3,  # порог похожести слов
        top=num       # количество ключевых слов
    )
    return ([i[0] for i in extractor.extract_keywords(text)])


def extract_keywords(text, num=10):
    '''extract keywords by manual method using file `keywords.json` and `YAKE!`'''
    # Manual method
    result = manual_m(text)
    # YAKE
    yake_result = yake_m(text, num)
    return {"manual": result, "yake": yake_result}


if __name__ == "__main__":
    nltk.download("stopwords", quiet=True)
    input_text = sys.stdin.readlines()
    print(json.dumps(extract_keywords("\n".join(input_text))))
