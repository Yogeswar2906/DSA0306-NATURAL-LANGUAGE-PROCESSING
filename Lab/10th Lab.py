words = ["The", "cat", "is", "running", "quickly", "played"]

tags = []

for word in words:
    tag = "NN"

    if word.lower() == "the":
        tag = "DT"

    elif word.lower() == "is":
        tag = "VBZ"

    elif word.endswith("ing"):
        tag = "VBG"

    elif word.endswith("ed"):
        tag = "VBD"

    elif word.endswith("ly"):
        tag = "RB"

    tags.append((word, tag))

print("Word\t\tPOS Tag")
print("--------------------------")

for word, tag in tags:
    print(word, "\t\t", tag)