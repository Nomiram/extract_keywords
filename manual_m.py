'''manual extract keywords from AiK thesis'''

import json
import os
import string
from inspect import getsourcefile
from os.path import abspath

import nltk
from nltk.stem import SnowballStemmer


def stem(text):
    '''Tokenize and stemming text'''
    words = nltk.word_tokenize(text)
    words = [word for word in words if word.isalpha()]
    snowball_ru = SnowballStemmer(language="russian")
    snowball_en = SnowballStemmer(language="english")
    text_strip = []
    for word in words:
        # Чтобы не съедались аббревиатуры
        if len(word) > 4:
            if word[0].lower() in string.ascii_lowercase:
                text_strip.append(snowball_en.stem(word))
            else:
                text_strip.append(snowball_ru.stem(word))
        else:
            text_strip.append(word)
        # Удаление ошибок
        if text_strip[-1] == "":
            del text_strip[-1]
    text_strip = " ".join(text_strip)
    return text_strip


def manual_m(text):
    '''extract keywords by manual method using file `keywords.json`'''
    # Manual method
    text_stem = stem(text)
    text_stem_list = text_stem.split()
    stem_keywords = {}
    with open(os.path.join(os.path.dirname(abspath(getsourcefile(lambda: 0))),
                            "keywords.json"), "r", encoding="utf8") as f:
        keywords = json.load(f)
        for kw in keywords:
            stem_keywords[stem(kw)] = kw
    result = []
    for kw in list(stem_keywords):
        # Если ключевое слово есть в списке слов или списке словосочетаний
        if kw in text_stem_list or \
                kw in [text_stem_list[i] + " " + text_stem_list[i + 1]\
                       for i in range(len(text_stem_list) - 1)]:
            result.append(stem_keywords[kw].lower())
    return result
