def store_trip_from_values(request, generated_text):
	"""Sets details of trip in session storage

	Args:
		request (HTTP Request): request from django form
		generated_text (str): comma seperated list of values
	"""

	values = generated_text.split(",")
	new_trip = request.session.get('trip', {}) 
	# set fields if they exist
	if values[0]:
		try:
			new_trip["start_date"] = values[0]
		except:
			new_trip["start_date"] = "unknown"
	if values[1]:
		try:
			new_trip["end_date"] = values[1]
		except:
			new_trip["end_date"] = "unknown"
	if values[2]:
		try:
			new_trip["city"] = values[2]
		except:
			new_trip["city"] = "unknown"
	if values[3]:
		try:
			new_trip["country"] = values[3]
		except:
			new_trip["country"] = "unknown"
	if values[4]:
		try:
			new_trip["num_travelers"] = int(values[4])
		except:
			new_trip["num_travelers"] = "unknown"
	# Save the object to session
	request.session['trip'] = new_trip
