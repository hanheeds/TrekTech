import openai
import os
from .load_api import load_secrets
from pathlib import Path
from datetime import datetime


def parse_trip(user_text, call_api=True):
	if call_api:
		# Set your OpenAI API key
		api_key = load_secrets()["OPENAI_API_KEY"]

		# Initialize the OpenAI API client
		openai.api_key = api_key

		# Specify the prompt for text generation
		prompt = f"For a given piece of text describing a trip a user would like to go on, parse the following values: starting date of trip, end date, city, country, and number of travelers. For the dates, use the format YYYYMMDD. If the value of a field cannot be determined from the following text, use the value None. Return the values in a comma separated list without spaces between values, without the label for the value, and do not write anything else. Here is the text: {user_text}"

		# Make a request to the API to generate text
		response = openai.Completion.create(
			engine="text-davinci-002",  # You can choose a different engine if needed
			prompt=prompt,
			max_tokens=50,  # Adjust the number of tokens you want in the response
			temperature=0.7,  # Adjust the creativity (higher values make it more creative)
		)

	# Extract the generated text
		generated_text = response.choices[0].text
	else:
		generated_text = "20240901,20240908,Miami,United States,None"
	return generated_text
