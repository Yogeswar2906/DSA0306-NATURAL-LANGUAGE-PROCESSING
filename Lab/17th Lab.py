import nltk
from nltk.corpus import wordnet

nltk.download('wordnet')

word = "car"

synsets = wordnet.synsets(word)

print("Word:", word)
print("Synsets and Meanings:")
print("----------------------")

for synset in synsets:
    print("Synset:", synset.name())
    print("Meaning:", synset.definition())
    print()