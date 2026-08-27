import nltk
from nltk import CFG
from nltk.parse import EarleyChartParser

grammar = CFG.fromstring("""
S -> NP VP
NP -> Det N
VP -> V NP
Det -> 'the'
N -> 'cat' | 'mouse'
V -> 'chases'
""")

parser = EarleyChartParser(grammar)

sentence = "the cat chases the mouse".split()

trees = parser.parse(sentence)

if trees:
    print("Sentence accepted")
else:
    print("Sentence rejected")