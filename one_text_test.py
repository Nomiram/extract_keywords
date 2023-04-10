import sys

from testing_keywords_mai import keywords_testing

testing_class = keywords_testing()
print("Введите текст (ctrl + d для завершения или ctrl+z и затем Enter на Windows)")
text = sys.stdin.readlines()
text = "".join(text)
print("Выполняются вычисления...")
testing_class.apply_methods(text, [])
