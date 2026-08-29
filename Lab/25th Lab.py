!pip install -q -U google-genai

from google import genai


client = genai.Client(api_key="AQ.Ab8RN6IXpcZ0nKNupcnBKItg8D8M8QZIs6JUDWJ2wYLDw_ElDw")

prompt = input("Enter your prompt: ")


response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)

print("\nInput:")

print(prompt)

print("\nGenerated Output:")
print(response.text)