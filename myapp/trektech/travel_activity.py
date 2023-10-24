import requests
from pathlib import Path





def search_country_activity(country): 
    url = "https://travel-info-api.p.rapidapi.com/country-activities"

    querystring = {"country": country}

    headers = {
        "X-RapidAPI-Key": "53bd119ccfmsh364f7fc48f6cb7bp182915jsnd2899197f369",
        "X-RapidAPI-Host": "travel-info-api.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    activities = response.json()
   # print(activities['activities'])


    return activities['data']['activities']


def generate_prompt_activities(activity_list, cities): 
    activity_prompt = f"""
    this is an activities dictionary that has the following information: the 'title', which is the name of the activity,
      and the 'activity', which is a description of the activity. Give an itinerary for a 5 day trip to {cities} with 
      1-2 activities every day that are plausible for location and proximity: \n\n
    """ + activity_list

    return activity_prompt



# search_country_activity("Spain")


