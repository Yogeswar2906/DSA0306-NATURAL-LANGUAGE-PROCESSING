import math

documents = [
    "the cat sits on the mat",
    "the dog plays in the park",
    "the cat plays with the dog"
]

query = "cat plays"

query_words = query.lower().split()
doc_words = [doc.lower().split() for doc in documents]

vocabulary = set(query_words)

for words in doc_words:
    vocabulary.update(words)

vocabulary = list(vocabulary)


def tf(word, words):
    return words.count(word) / len(words)


def idf(word):
    count = sum(word in words for words in doc_words)
    return math.log(len(documents) / count)


def tfidf_vector(words):
    return [tf(word, words) * idf(word) for word in vocabulary]


def cosine_similarity(v1, v2):
    dot = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a * a for a in v1))
    mag2 = math.sqrt(sum(b * b for b in v2))

    if mag1 == 0 or mag2 == 0:
        return 0

    return dot / (mag1 * mag2)


query_vector = tfidf_vector(query_words)

scores = []

for i, words in enumerate(doc_words):
    vector = tfidf_vector(words)
    score = cosine_similarity(query_vector, vector)
    scores.append((i, score))

scores.sort(key=lambda x: x[1], reverse=True)

print("Query:", query)
print("\nDocument Ranking:")
print("-------------------------")

for rank, (index, score) in enumerate(scores, 1):
    print(rank, documents[index], "->", round(score, 3))