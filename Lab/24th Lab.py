dialog = [
    "Hello, how are you?",
    "Can you help me with my homework?",
    "Yes, I can help you.",
    "Thank you very much.",
    "Goodbye."
]

print("Dialog Act Recognition")
print("----------------------")

for sentence in dialog:

    if sentence.lower() in ["hello", "hi", "good morning"] or "how are you" in sentence.lower():
        act = "Greeting"

    elif sentence.lower().startswith(("can you", "could you", "will you")):
        act = "Request"

    elif sentence.lower() in ["yes", "yes, i can help you."]:
        act = "Answer"

    elif "thank" in sentence.lower():
        act = "Thanking"

    elif sentence.lower() in ["goodbye", "bye"]:
        act = "Goodbye"

    else:
        act = "Statement"

    print(sentence, "->", act)