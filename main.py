import openai
from myapp.trektech.agent import Agent
from myapp.trektech.load_api import load_secrets
import json

# Load the API keys
api_key = load_secrets()["OPENAI_API_KEY"]
api_key = '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'

# Initialize the OpenAI API client
openai.api_key = api_key


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

# Update the requests. 
def update_itinerary(itinerary, update_query):
    # Setting up the travel agent
    travel_agent = Agent(api_key,debug=False)

    updated_itinerary_str = travel_agent.update_itinerary(itinerary, update_query)
#     updated_itinerary = json.loads(updated_itinerary) # convert string into dictionary
    updated_itinerary_dict = json.loads(updated_itinerary_str)

    return updated_itinerary_str, updated_itinerary_dict


# Update the itinerary
update_query = "Make it 4 days"
new_itinerary_str,new_itinerary_dict = update_itinerary(itinerary_str, update_query)

print(new_itinerary_dict)


