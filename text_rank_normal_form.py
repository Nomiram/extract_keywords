'''extract keywords from AiK thesis'''
import pymorphy3
import pytextrank
import spacy


def extract_keywords(text: str):
    """
    The function takes in a string of text, uses spaCy and PyTextRank to extract key phrases, 
    and then uses pymorphy3 to normalize the phrases before returning them as a list.

    Args:
      text (str): The input text that needs to be analyzed and extracted for keywords using 
    the TextRank algorithm.

    Returns:
      List of top-ranked phrases in the input text after applying the TextRank algorithm. 
    The returned list contains the normalized form of the phrases.
    """

    nlp = spacy.load("ru_core_news_sm")

    # add PyTextRank to the spaCy pipeline
    nlp.add_pipe("textrank")

    # TEXT RANK
    doc = nlp(text)

    # examine the top-ranked phrases in the document
    raw_text_rank_keywords2 = [phrase.text for phrase in doc._.phrases]

    morph = pymorphy3.MorphAnalyzer()
    text_rank_keywords2 = []
    for phrase in raw_text_rank_keywords2:
        words = phrase.split()
        ready_words = []
        for word in words:
            parsed_word = morph.parse(word)[0]
            ready_words.append(parsed_word.normal_form)

        text_rank_keywords2.append(
            pymorphy3.shapes.restore_capitalization(" ".join(ready_words), phrase))
    return list(set(text_rank_keywords2))
