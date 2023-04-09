from testing_keywords_mai import apply_methods
import sys
stats = {"ready_keywords": {"description": "Пользовательские ключевые слова"},
         "manual": {"description": "Прямой поиск"},
         "rake": {"description": "RAKE"},
         "yake": {"description": "YAKE"},
         "text_rank_keywords2": {"description": "TextRank"},
         }
for method in stats.values():
    method["keywords"] = []
    method["sum"] = 0
    method["all"] = 0
print("Введите текст (ctrl + d для завершения или ctrl+z и затем Enter на Windows)")
text = sys.stdin.readlines()
text = "".join(text)
print("Выполняются вычисления...")
apply_methods(text, stats, [])
