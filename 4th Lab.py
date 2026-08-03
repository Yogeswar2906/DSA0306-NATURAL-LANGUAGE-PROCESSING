def generate_plural(noun):

    if noun.endswith(("s", "x", "z", "ch", "sh")):
        plural = noun + "es"

    elif noun.endswith("y") and noun[-2].lower() not in "aeiou":
        plural = noun[:-1] + "ies"

    else:
        plural = noun + "s"

    return plural


words = ["cat", "dog", "bus", "box", "church",
         "dish", "baby", "city", "toy", "book"]

print("Singular\tPlural")
print("----------------------")

for word in words:
    print(word, "\t\t", generate_plural(word))