import re

text = "Ravi went to the market. He bought a book."

sentences = text.split(". ")

last_person = None

for sentence in sentences:
    words = sentence.split()

    for word in words:
        if re.match(r"^[A-Z][a-z]+$", word) and word not in ["He", "She", "They"]:
            last_person = word

    if "He" in words:
        sentence = sentence.replace("He", last_person)

    print(sentence)
