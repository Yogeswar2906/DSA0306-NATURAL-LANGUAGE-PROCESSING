import re

words = ["running", "played", "cats", "quickly", "beautiful", "book"]

print("Word\t\tPOS Tag")
print("--------------------------")

for word in words:

    if re.search("ing$", word):
        tag = "VBG"

    elif re.search("ed$", word):
        tag = "VBD"

    elif re.search("ly$", word):
        tag = "RB"

    elif re.search("ful$", word):
        tag = "JJ"

    elif re.search("s$", word):
        tag = "NNS"

    else:
        tag = "NN"

    print(word, "\t\t", tag)