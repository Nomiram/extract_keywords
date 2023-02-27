'''extract keywords from AiK thesis'''
import json
import sys

import nltk
import pytextrank
import spacy

from manual_m import manual_m

nltk.download("stopwords", quiet=True)
nltk.download('punkt', quiet=True)

def TextRank_m(text):
    nltk.download("stopwords", quiet=True)
    nltk.download('punkt', quiet=True)

    nlp = spacy.load("ru_core_news_sm")

    # add PyTextRank to the spaCy pipeline
    nlp.add_pipe("textrank")

    # TEXT RANK
    doc = nlp(text)

    # examine the top-ranked phrases in the document
    return [phrase.text for phrase in doc._.phrases]

def extract_keywords(text):
    '''extract keywords by `TextRank`'''
    result = manual_m(text)
    text_rank_result = TextRank_m(text)
    return {"manual": result, "TextRank": text_rank_result}

if __name__ == "__main__":
    nltk.download("stopwords", quiet=True)
    input_text = sys.stdin.readlines()
    print(json.dumps(extract_keywords("\n".join(input_text))))
