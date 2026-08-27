pos_prob = {
    "the": "DT",
    "cat": "NN",
    "dog": "NN",
    "runs": "VBZ",
    "eats": "VBZ",
    "mouse": "NN"
}

sentence = "the cat eats the mouse"

words = sentence.split()

print("Word\tPOS Tag")
print("----------------")

for word in words:
    tag = pos_prob.get(word, "Unknown")
    print(word, "\t", tag)