import openai
from myapp.trektech.agent import Agent
from myapp.trektech.load_api import load_secrets
import json
from myapp.trektech.api_functions import *

# Load the API keys
api_key = load_secrets()["OPENAI_API_KEY"] ## I don't know why this isn't working right now
api_key = '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'

# Initialize the OpenAI API client
openai.api_key = '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'

# Initial run
def initial_run(query): 

    # Setting up the travel agent
    travel_agent = Agent(api_key,debug=False)

    # Validating if the query is valid
    val_response = travel_agent.validate_travel(query)

    # If the query IS NOT valid, we need to get more input.
    if val_response['plan_is_valid'] =='no':
        print(val_response['updated_request'])
        print('Try another request')

    # If the plan IS valid
    else:
        itinerary_str = travel_agent.suggest_itinerary(query)
        itinerary_dict = json.loads(itinerary_str) # convert string into dictionary

    # returns the string and dictionary version
    return itinerary_str, itinerary_dict

good_query = """""
        I want to do a 5 day roadtrip from Cape Town to Pretoria in South Africa.
        I want to visit remote locations with mountain views
        """
# Example of a bad query
bad_query = """
        I want to walk from Cape Town to Pretoria in South Africa.
        I want to visit remote locations with mountain views
        """

itinerary_str, itinerary_dict = initial_run(good_query)

# Example of looping through each day
for day, value in itinerary_dict.items():
    print(day)


#### Now if you want to update the requests with more prompts ####
def update_itinerary(itinerary, update_query):
    # Setting up the travel agent
    travel_agent = Agent(api_key,debug=False)

    updated_itinerary_str = travel_agent.update_itinerary(itinerary, update_query)
#     updated_itinerary = json.loads(updated_itinerary) # convert string into dictionary
    updated_itinerary_dict = json.loads(updated_itinerary_str)

    return updated_itinerary_str, updated_itinerary_dict


# Update the itinerary
# update_query = "Make it 4 days"
# new_itinerary_str,new_itinerary_dict = update_itinerary(itinerary_str, update_query)

# print(new_itinerary_dict)

city = itinerary_dict['day1']['city']
location_id = search_restaurant_location_ID(city)
restaurant_list = search_restaurant(location_id)

activity_list = itinerary_dict['day1']['country']


def generate_prompt_restaurants(restaurant_list, activity_list): 
    restaurant_prompt = """
    Below you will have the following: a restaurant dictionary and an activities dictionary for the same city/area. 
    the restaurant dictionary thas the following information: the keys are the restaurant name, 
    then the first element in the value is the cuisine type, the second value is the price range, and the third value is the user rating. 
    Please do not categorize the days by cuisine, such that there is variety in each day. \n
    """ + str(restaurant_list)

    activity_prompt = """
    this is the acitvities dictionary. The keys are the name of the activity, and the values are a description of the activity. 
    """ + str(activity_list)

    combo_prompt = """
    Using both of these dictionaries, recreate the original itinerary using activities and restaurants that are listed in the dictionaries. 
    Provide a brief description of each activity as well. 
    """
    
    prompt = restaurant_prompt + activity_prompt + combo_prompt
    return prompt


# Update the itinerary
update_query = generate_prompt_restaurants(restaurant_list, activity_list)
new_itinerary_str,new_itinerary_dict = update_itinerary(itinerary_str, update_query)

print(new_itinerary_dict)


    return 