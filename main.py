import openai
from myapp.trektech.agent import validate
from myapp.trektech.agent import suggest
from myapp.trektech.load_api import load_secrets
import dataclasses
import http.client
import requests
import os
from dotenv import load_dotenv
from pathlib import Path
# Set your api key
# (I put google palm as an example if we wanna switch it out for openai)
api_key = load_secrets()["OPENAI_API_KEY"]
google_palm_api_key = load_secrets()["PALM_API_KEY"]

# Initialize the OpenAI API client
openai.api_key = api_key

# Example of a good query
def validate(): 
    good_query = """""
            I want to do a 5 day roadtrip from Cape Town to Pretoria in South Africa.
            I want to visit remote locations with mountain views
            """
    # Example of a bad query
    bad_query = """
            I want to walk from Cape Town to Pretoria in South Africa.
            I want to visit remote locations with mountain views
            """

    query = good_query

    # Get the response for the validation
    val_response = validate(api_key,query)

    # If the plan is not valid,
    if val_response['plan_is_valid'] =='no':
        print(val_response['updated_request'])
        print('Try another request')
    # If the plan is valid
    else:
        # print either the itinerary or list of places
        itinerary,list_of_places,validation = suggest(api_key, query)
        # print(list_of_places)
        print(list_of_places)



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
def connect_gpt_api(): 
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






