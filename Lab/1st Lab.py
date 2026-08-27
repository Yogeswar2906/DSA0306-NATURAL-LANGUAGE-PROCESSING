import re

text = "My phone number is 1234567890"

pattern = r"\d{10}"

match = re.search(pattern, text)

if match:
    print("Text :", text)
    print("Pattern Found :", match.group())
else:
    print("Pattern Not Found")