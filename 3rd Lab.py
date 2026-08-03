from nltk.stem import PorterStemmer

ps = PorterStemmer()

words = ["playing", "running", "studies", "cats", "better"]

print("Word\t\tStem")

for word in words:
    print(word, "\t", ps.stem(word))