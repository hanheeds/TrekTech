import openai
from django.shortcuts import render
from datetime import datetime
from .agent import validate, suggest
from dotenv import load_dotenv
from .load_api import load_secrets
from .photo_api import download_photo
from django.conf import settings


# Set your api key
api_key = load_secrets()["OPENAI_API_KEY"]

# Initialize the OpenAI API client
openai.api_key = api_key


def index(request):
	# initialize values
	session = request.session
	chat_history = session.get('chat_history', []) 
	context = {"itinerary": [], "chat_history": chat_history, "image_name": "default"}
	bot_response = ""

	# user enters text
	if request.method == 'POST':
		# add users message to chat history
		user_text = request.POST['user_text']
		chat_history.append({'user': True, 'text': user_text})

		# get and validate initial trip details from user
		if not session.get('valid_trip', False):
			val_response = validate(api_key, user_text)
			if val_response['plan_is_valid'] == 'no':
				bot_response = val_response['updated_request']
			else:
				session['valid_trip'] = True
				bot_response = "Sounds like fun! I have created a custom itinerary for you" # I'm not sure if we want to have a different response

		# if a valid trip has already been created, enter itinerary refinement phase
		else:
			bot_response = "I have updated your itinerary" # I'm not sure if we want to have a different response

		# create/update itinerary and generate specific images
		if session.get('valid_trip', False):
			itinerary, list_of_places, validation = suggest(api_key, user_text)
			# print(list_of_places)
			itinerary = itinerary.split("- ")
			# print(itinerary)
			context["itinerary"] = itinerary
			download_photo(user_text, settings.MEDIA_ROOT, "itinerary") # we'll probably want a different query
			context["image_name"] = "itinerary"

	# page is initially loaded
	elif request.method == 'GET':
		# for the first message in chat, ask user for trip details and generate a generic image
		if len(chat_history) == 0:
			bot_response = "What type of trip would you like to go one? Please tell me where, when, and how many people"
			download_photo("planning a vacation", settings.MEDIA_ROOT, "travel")
			context["image_name"] = "travel"

	# only handling GET and POST requests so far
	else:
		print("unsupported http request")

	# update state
	if bot_response:
		chat_history.append({'user': False, 'text': bot_response})
	session['chat_history'] = chat_history
	context['chat_history'] = chat_history
	return render(request, template_name="index.html", context=context)
