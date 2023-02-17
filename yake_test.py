'''test file for Pytest'''
import json

from . import yake_keywords_mai


def test_stem():
    '''test stem'''
    assert yake_keywords_mai.stem("Два слова") == "Два слов"
    assert yake_keywords_mai.stem("Это три слова") == "Это три слов"

def test_yake():
    '''test yake'''
    with open("theses.json","r",encoding="utf8") as f:
        all_texts = json.load(f)
        for i in list(all_texts)[:10]:
            subject = all_texts[i]["subject"]
            text = all_texts[i]["text"]
            print(f"Text {i}:")
            print(subject)
            print(text)
            result = yake_keywords_mai.extract_keywords(text=text)
            print(result)

# test_yake()