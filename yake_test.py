'''test file for Pytest'''
import json

from . import manual_m, text_rank_simple, yake_keywords_mai


def test_stem():
    '''test stem'''
    assert manual_m.stem("Два слова") == "Два слов"
    assert manual_m.stem("Это три слова") == "Это три слов"


def test_yake():
    '''test yake'''
    with open("theses.json", "r", encoding="utf8") as f:
        all_texts = json.load(f)
        for i in list(all_texts)[:10]:
            subject = all_texts[i]["subject"]
            text = all_texts[i]["text"]
            print(f"Text {i}:")
            print(subject)
            print(text)
            result = yake_keywords_mai.extract_keywords(text=text)
            print(result)


def test_text_rank():
    '''test yake'''
    with open("theses.json", "r", encoding="utf8") as f:
        all_texts = json.load(f)
        for i in list(all_texts)[:10]:
            subject = all_texts[i]["subject"]
            text = all_texts[i]["text"]
            print(f"Text {i}:")
            print(subject)
            print(text)
            result = text_rank_simple.extract_keywords(text=text)
            print(result)
