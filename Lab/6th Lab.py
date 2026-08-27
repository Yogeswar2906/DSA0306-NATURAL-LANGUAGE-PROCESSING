text = "the cat chases the mouse"

words = text.split()

print("Bigrams:")

for i in range(len(words) - 1):
    print("(", words[i], ",", words[i + 1], ")")