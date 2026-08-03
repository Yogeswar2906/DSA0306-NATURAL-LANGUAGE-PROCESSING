from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

words = [
    "running", "playing", "studies", "studying",
    "connected", "connection", "happiness",
    "flying", "wolves", "cars"
]

print("Original Word\tStemmed Word")
print("--------------------------------")

for word in words:
    stem = stemmer.stem(word)
    print(word, "\t", stem)