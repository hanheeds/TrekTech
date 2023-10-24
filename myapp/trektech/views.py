import openai
from django.shortcuts import render
from datetime import datetime
from .store_trip import store_trip_from_values
from .agent import validate, suggest
from dotenv import load_dotenv
from .load_api import load_secrets

from .gpt import parse_trip

# Set your api key
api_key = load_secrets()["OPENAI_API_KEY"]

# Initialize the OpenAI API client
openai.api_key = api_key


def index(request):
	# initialize values
	session = request.session
	chat_history = session.get('chat_history', []) 
	context = {"itinerary": "", "chat_history":chat_history}
	bot_response = ""

	# user enters text
	if request.method == 'POST':
		# add users message to chat history
		user_text = request.POST['user_text']
		chat_history.append({'user': True, 'text': user_text})

		# get and validate initial trip details from user
		if session.get('valid_trip', False) is False:
			val_response = validate(api_key, user_text)
			if val_response['plan_is_valid'] == 'no':
				bot_response = val_response['updated_request']
			else:
				session['valid_trip'] = True
				generated_text = parse_trip(user_text, call_api=False) 
				store_trip_from_values(request=request, generated_text=generated_text)
				trip = session.get('trip')
				# we could probably do an LLM generated response here too
				bot_response = f'Your party of {trip["num_travelers"]} wants to go to {trip["city"]}, {trip["country"]} from {trip["start_date"]} to {trip["end_date"]}.'
		# if a valid trip has already been created, enter itinerary refinement phase
		else:
			itinerary, list_of_places, validation = suggest(api_key, user_text)
			context["itinerary"] = itinerary
			bot_response = itinerary # I'm not sure if we want to have a different response

	# page is initially loaded
	elif request.method == 'GET':
		# for the first message in chat, ask user for trip details
		if len(chat_history) == 0:
			bot_response = "What type of trip would you like to go one? Please tell me where, when, and how many people"

	# only handling get and post requests so far
	else:
		print("unsupported request")

	# update state
	if bot_response:
		chat_history.append({'user': False, 'text': bot_response})
	session['chat_history'] = chat_history
	context['chat_history'] = chat_history

	return render(request, template_name="index.html", context=context)
