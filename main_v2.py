'''extract keywords from AiK thesis'''
import json
import sys

from manual_m import manual_m
from text_rank_v2_normal_form import TextRank_m


def extract_keywords(text):
    '''extract keywords by manual method using file `keywords.json` and `YAKE!`'''
    # Manual
    result = manual_m(text)
    # TEXT RANK
    text_rank_result = TextRank_m(text)
    return {"manual": result, "TextRank": text_rank_result}


if __name__ == "__main__":
    input_text = sys.stdin.readlines()
    print(json.dumps(extract_keywords("\n".join(input_text))))
