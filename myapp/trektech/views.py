from django.shortcuts import render
from datetime import datetime

from .gpt import parse_trip
from .models import Trip


def get_chatbot_response(user_text):
	return f"i'm a bot, you said {user_text}"

# Create your views here.
def index(request):
	# chat_history = request.session.get('chat_history', [])
	context = {}
	chat_history = request.session.get('chat_history', []) 
	bot_response = ""
	if request.method == 'POST':
		user_text = request.POST['user_text']
		chat_history.append({'user': True, 'text': user_text})
		# get trip details from user
		if request.session.get('initial', False) is False:
			generated_text = parse_trip(user_text, call_api=False) 
			trip = create_trip_from_values(generated_text)
			bot_response = f"Your party of {trip.num_travelers} wants to go to {trip.city}, {trip.country} from {trip.start_date} to {trip.end_date}."
			request.session['initial'] = True
		else:
			bot_response = get_chatbot_response(user_text)
	elif request.method == 'GET':
		# for the first message in chat, ask user for trip details
		if len(chat_history) == 0:
			bot_response = "What type of trip would you like to go one? Please tell me where, when, and how many people"
	else:
		# only handling get and post requests so far
		print("unsupported request")
	if bot_response:
		chat_history.append({'user': False, 'text': bot_response})
	request.session['chat_history'] = chat_history
	context['chat_history'] = chat_history
	return render(request, template_name="index.html", context=context)


def create_trip_from_values(generated_text):
	values = generated_text.split(",")
	# create a new Trip object
	new_trip = Trip()
	# set fields if they exist
	if values[0]:
		try:
			new_trip.start_date = datetime.strptime(values[0], "%Y%m%d").date()
		except:
			pass
	if values[1]:
		try:
			new_trip.end_date = datetime.strptime(values[1], "%Y%m%d").date()
		except:
			pass
	if values[2]:
		try:
			new_trip.city = values[2]
		except:
			pass
	if values[3]:
		try:
			new_trip.country = values[3]
		except:
			pass
	if values[4]:
		try:
			new_trip.num_travelers = int(values[4])
		except:
			pass
	# Save the object to the database
	new_trip.save()
	return new_trip
