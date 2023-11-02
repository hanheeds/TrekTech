import openai
from myapp.trektech.agent import validate
from myapp.trektech.agent import suggest
from myapp.trektech.load_api import load_secrets

# Set your api key
# (I put google palm as an example if we wanna switch it out for openai)
# api_key = load_secrets()["OPENAI_API_KEY"]
api_key = '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'
# google_palm_api_key = load_secrets()["PALM_API_KEY"]

# Initialize the OpenAI API client
openai.api_key = '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'

print("API KEY: ",api_key)
# Example of a good query
good_query = """""
        I want to do a 5 day roadtrip from Cape Town to Pretoria in South Africa.
        I want to visit remote locations with mountain views
        """
# Example of a bad query
bad_query = """
        I want to walk from Cape Town to Pretoria in South Africa.
        I want to visit remote locations with mountain views
        """

query = good_query

# Get the response for the validation
val_response = validate(api_key,query)

# If the plan is not valid,
if val_response['plan_is_valid'] =='no':
    print(val_response['updated_request'])
    print('Try another request')
# If the plan is valid
else:
    # print either the itinerary or list of places
    itinerary,list_of_places,_ = suggest(api_key, query)
    # print(list_of_places)
    print(itinerary)

def main(): 

    return 