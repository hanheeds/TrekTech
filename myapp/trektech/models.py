from django.db import models
from datetime import datetime


class TripManager(models.Manager):
	
	def get_last_trip(self):
		"""returns most recently created Trip object"""
		return self.get_queryset().order_by('-id').first()


class Trip(models.Model):

	objects = models.Manager()  # Default manager
	trips = TripManager()  # Custom manager


	# model fields
	start_date = models.DateField("First day of trip", default=datetime.strptime("20240114", "%Y%m%d"))
	end_date = models.DateField("Last day of trip", default=datetime.strptime("20240121", "%Y%m%d"))
	city = models.CharField("City", max_length=200, default="Chicago")
	country = models.CharField("Country", max_length=200, default="USA")
	num_travelers = models.IntegerField("Number of travelers", default=2)


# example object creation
# can run from terminal in `python manage.py shell`
def create_example_trip(city="Chicago"):
	date1 = datetime.strptime("10/16/23", "%m/%d/%y").date()
	date2 = datetime.strptime("10/23/23", "%m/%d/%y").date()

	# Create a new object
	new_object = Trip(
		start_date=date1,
		end_date=date2,
		city=city,
		country="USA",
		num_travelers=2
	)

	# Save the object to the database
	new_object.save()

	# get field from object
	print(f"city: {Trip.trips.get_last_trip().start_date}")
	print(f"city: {Trip.trips.get_last_trip().city}")
	return Trip.trips.get_last_trip()
