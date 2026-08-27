import nltk
from nltk import word_tokenize, pos_tag
from nltk.chunk import RegexpParser

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

sentence = "The smart student reads a book"

words = word_tokenize(sentence)
tags = pos_tag(words)

grammar = "NP: {<DT>?<JJ>*<NN>}"

parser = RegexpParser(grammar)
tree = parser.parse(tags)

print("Sentence:", sentence)
print("Noun Phrases and Meanings:")
print("--------------------------")

for subtree in tree.subtrees():
    if subtree.label() == "NP":
        noun_phrase = " ".join(word for word, tag in subtree.leaves())
        noun = subtree.leaves()[-1][0]

        print("Noun Phrase:", noun_phrase)
        print("Meaning: Refers to", noun)