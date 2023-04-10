'''extract keywords from AiK thesis'''
import nltk
import pytextrank
import spacy

nltk.download("stopwords", quiet=True)
nltk.download('punkt', quiet=True)


def extract_keywords(text: str):
    """
    The function takes in a string of text, uses spaCy and PyTextRank to extract key phrases.

    Args:
      text (str): The input text that needs to be analyzed and extracted for keywords using 
    the TextRank algorithm.

    Returns:
      List of top-ranked phrases in the input text after applying the TextRank algorithm.
    """
    nltk.download("stopwords", quiet=True)
    nltk.download('punkt', quiet=True)

    nlp = spacy.load("ru_core_news_sm")

    # add PyTextRank to the spaCy pipeline
    nlp.add_pipe("textrank")

    # TEXT RANK
    doc = nlp(text)

    # examine the top-ranked phrases in the document
    return [phrase.text for phrase in doc._.phrases]
