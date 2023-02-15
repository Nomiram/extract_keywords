'''testing'''
import json

import yake_keywords_mai

def test_stem():
    '''test stem'''
    assert yake_keywords_mai.stem("Два слова") == "два слов"
    assert yake_keywords_mai.stem("Это три слова") == "эт три слов"

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
            print(json.loads(result))
