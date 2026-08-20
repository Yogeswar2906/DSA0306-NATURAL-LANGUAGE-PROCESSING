import nltk
from nltk import CFG
from nltk.parse import ChartParser

grammar = CFG.fromstring("""
S -> NP VP
NP -> DET NS | DET NP
NP -> DET NSG
VP -> V NS | V NP
DET -> 'the'
NS -> 'cats' | 'dogs'
NSG -> 'cat' | 'dog'
V -> 'run' | 'runs'
""")

parser = ChartParser(grammar)

sentences = [
    "the cat runs",
    "the cats run",
    "the cat run",
    "the cats runs"
]

for sentence in sentences:
    words = sentence.split()
    trees = list(parser.parse(words))

    print("Sentence:", sentence)

    if trees:
        print("Agreement: Correct")
    else:
        print("Agreement: Incorrect")

    print()