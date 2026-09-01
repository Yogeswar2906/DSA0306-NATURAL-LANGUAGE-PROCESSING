from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "Helsinki-NLP/opus-mt-en-fr"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

text = "The cat is sitting on the mat."

inputs = tokenizer(text, return_tensors="pt")

output = model.generate(**inputs)

translation = tokenizer.decode(output[0], skip_special_tokens=True)

print("English:", text)
print("French:", translation)