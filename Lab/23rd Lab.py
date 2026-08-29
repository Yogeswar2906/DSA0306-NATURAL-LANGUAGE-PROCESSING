text = "Ravi went to college. He attended his class. He studied for the exam."

sentences = text.split(". ")
words = set(sentences[0].lower().split())

score = 0

for sentence in sentences[1:]:
    current_words = set(sentence.lower().split())

    if words.intersection(current_words):
        score += 1

    words.update(current_words)

print("Text:", text)
print("Coherence Score:", score)

if score > 0:
    print("Text is Coherent")
else:
    print("Text is Not Coherent")