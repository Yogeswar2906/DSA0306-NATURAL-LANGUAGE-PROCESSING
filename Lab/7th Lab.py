import nltk
from nltk import word_tokenize, pos_tag

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

text = "The cat chased the mouse"

words = word_tokenize(text)

tags = pos_tag(words)

print("Word\tPOS")
print("----------------")

for word, tag in tags:
    print(word, "\t", tag)