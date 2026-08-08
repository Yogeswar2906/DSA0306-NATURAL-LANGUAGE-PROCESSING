import nltk
from nltk import CFG
from nltk.parse import ChartParser

grammar = CFG.fromstring("""
S -> NP VP
NP -> Det N
VP -> V NP
Det -> 'the'
N -> 'cat' | 'mouse'
V -> 'chases'
""")

parser = ChartParser(grammar)

sentence = "the cat chases the mouse".split()

trees = parser.parse(sentence)

for tree in trees:
    print(tree)
    tree.pretty_print()