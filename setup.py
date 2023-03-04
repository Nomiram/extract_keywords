import nltk

download_dir = "/usr/share/nltk_data"
nltk.download("stopwords", download_dir=download_dir)
nltk.download('punkt', download_dir=download_dir)
nltk.download('brown', download_dir=download_dir)
