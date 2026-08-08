grammar = {
    "S": [["NP", "VP"]],
    "NP": [["Det", "N"]],
    "VP": [["V", "NP"]],
    "Det": [["the"]],
    "N": [["cat"], ["mouse"]],
    "V": [["chases"]]
}

sentence = "the cat chases the mouse"
words = sentence.split()
position = 0


def parse(symbol):
    global position

    if symbol not in grammar:
        if position < len(words) and words[position] == symbol:
            position += 1
            return True
        return False

    for rule in grammar[symbol]:
        saved_position = position
        success = True

        for item in rule:
            if not parse(item):
                success = False
                break

        if success:
            return True

        position = saved_position

    return False


if parse("S") and position == len(words):
    print("Sentence accepted")
else:
    print("Sentence rejected")