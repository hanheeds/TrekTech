import openai
import os
from dotenv import load_dotenv
from pathlib import Path

def load_secrets():
    """
    Function to get api keys from .env files. More api key scan be added and returned.
    """
    load_dotenv()
    env_path = Path(".") / ".env"
    load_dotenv(dotenv_path=env_path)

    open_ai_key = os.getenv("OPENAI_API_KEY")

    return {
        "OPENAI_API_KEY": open_ai_key
    }

# Set your OpenAI API key
api_key = load_secrets()["OPENAI_API_KEY"]

# Initialize the OpenAI API client
openai.api_key = api_key

# Specify the prompt for text generation
prompt = "Translate the following English text to French: 'Hello, how are you?'"

# Make a request to the API to generate text
response = openai.Completion.create(
    engine="text-davinci-002",  # You can choose a different engine if needed
    prompt=prompt,
    max_tokens=50,  # Adjust the number of tokens you want in the response
    temperature=0.7,  # Adjust the creativity (higher values make it more creative)
)

# Extract and print the generated text
generated_text = response.choices[0].text
print(generated_text)
