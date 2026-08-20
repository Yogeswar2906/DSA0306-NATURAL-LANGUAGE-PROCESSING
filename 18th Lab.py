import re

expression = "Human(Socrates) AND Mortal(Socrates)"

pattern = r"^[A-Za-z]+\([A-Za-z]+\)(\s+(AND|OR)\s+[A-Za-z]+\([A-Za-z]+\))*$"

if re.match(pattern, expression):
    print("Expression:", expression)
    print("FOPC Expression is Valid")
else:
    print("Expression:", expression)
    print("FOPC Expression is Invalid")