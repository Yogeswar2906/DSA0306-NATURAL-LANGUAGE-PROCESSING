import nltk
from nltk import PCFG
from nltk.parse import ViterbiParser

grammar = PCFG.fromstring("""
S -> NP VP [1.0]
NP -> Det N [0.6]
NP -> 'John' [0.4]
VP -> V NP [1.0]
Det -> 'the' [1.0]
N -> 'cat' [0.5]
N -> 'dog' [0.5]
V -> 'sees' [1.0]
""")

parser = ViterbiParser(grammar)

sentence = "John sees the dog".split()

trees = list(parser.parse(sentence))

if trees:
    print("Sentence:", " ".join(sentence))
    print("Probabilistic Parse Tree:")
    print(trees[0])
else:
    print("Sentence cannot be parsed")