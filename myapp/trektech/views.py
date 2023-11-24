import openai
from django.shortcuts import render
from datetime import datetime
from .agent import Agent
from dotenv import load_dotenv
from .load_api import load_secrets
from .photo_api2 import download_photo
from .api_functions import *
from .templates import generate_prompt_restaurants
from django.conf import settings
import json
import random


# Set your api key
api_key = load_secrets()["OPENAI_API_KEY"]

# Initialize the OpenAI API client
openai.api_key = api_key


def index(request):
	# initialize values
	session = request.session
	chat_history = session.get('chat_history', []) 
	context = {"itinerary": {}, "chat_history": chat_history}
	bot_response = ""

	# user enters text
	if request.method == 'POST':
		# add users message to chat history
		user_text = request.POST['user_text']
		chat_history.append({'user': True, 'text': user_text})
		# Setting up the travel agent
		travel_agent = Agent(api_key,debug=False)

		# get and validate initial trip details from user
		if not session.get('valid_trip', False):
			val_response = travel_agent.validate_travel(user_text)
			if val_response['plan_is_valid'] == 'no':
				bot_response = val_response['updated_request']
				context["image_name"] = "travel"
			else:
				session['valid_trip'] = True

		# call APIs and generate itinerary and images
		if session.get('valid_trip', False):

			# if it's the initial query, create the initial itinerary
			if session.get('initial_trip', True):
				itinerary_str = travel_agent.suggest_itinerary(user_text)
				bot_response = "Sounds like fun! I have created a custom itinerary for you" # I'm not sure if we want to have a different response
				session['initial_trip'] = False
				print("creating initial itinerary (without API info)")
			# if the initial trip has already been created, update the itinerary 
			else:
				old_itinerary_str = session.get("itinerary_str")
				bot_response = "I have updated your itinerary" # I'm not sure if we want to have a different response
				itinerary_str = travel_agent.update_itinerary(old_itinerary_str, user_text)
				print("creating updated itinerary based on users request (without API info)")

			itinerary_dict = json.loads(itinerary_str)
			# call resteraunt/activity APIs here
			if not session.get('restaurant_list', False):
				print("fetching restaurants")
				city = itinerary_dict['day1']['city']
				location_id = search_restaurant_location_ID(city)
				restaurant_list = search_restaurant(location_id)
				session['restaurant_list'] = restaurant_list
			else:
				print("using saved restaurant list")
				restaurant_list = session.get("restaurant_list")
			activity_list = []
			for day, details in itinerary_dict.items():
				activity_list.append(details['itinerary'])

			update_prompt = generate_prompt_restaurants(restaurant_list, activity_list)
			
			# for BOTH the initial and updates, update
			new_itinerary_str = travel_agent.update_itinerary(itinerary_str, update_prompt)
			print("updating itinerary with real restaurants")
			session['itinerary_str'] = new_itinerary_str
			itinerary_dict = json.loads(new_itinerary_str) # convert string into dictionary
			print(f"\n\nitinerary dict: {itinerary_dict}")

			# generate images
			view_itinerary = {}
			for day, details in itinerary_dict.items():
				day_num = day[3:]
				view_itinerary[day_num] = details['itinerary']
				# pick a random activity to get an image of
				activity = random.choice(details['activity'].split(","))
				print(f"Pictured activity for day {day_num}: {activity}")
				download_photo(activity, settings.MEDIA_ROOT, f"itinerary-{day_num}") # we'll probably want a different query
			context['itinerary'] = view_itinerary

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
