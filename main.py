'''extract keywords from AiK thesis'''
import json
import sys

from manual_m import manual_m
from text_rank_normal_form import extract_keywords
# from yake_keywords_mai import extract_keywords
# from text_rank_simple import extract_keywords
# from text_rank_v2_normal_form import extract_keywords


def main(text):
    '''extract keywords by manual method using file `keywords.json` and `YAKE!`'''
    # Manual
    result = manual_m(text)
    # TEXT RANK
    text_rank_result = extract_keywords(text)
    return {"manual": result, "TextRank": text_rank_result}


if __name__ == "__main__":
    input_text = sys.stdin.readlines()
    print(json.dumps(main("\n".join(input_text))))
