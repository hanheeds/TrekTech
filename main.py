import dataclasses
import openai
import http.client
import requests
# Set your OpenAI API key
def connect_gpt_api(): 
    api_key = "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"

    # Initialize the OpenAI API client
    openai.api_key = api_key

    # Specify the prompt for text generation
    prompt = "Translate the following English text to French: 'Hello, how are you?'"

    # Make a request to the API to generate text
    response = openai.Completion.create(
        engine="text-davinci-002",  # You can choose a different engine if needed
        prompt=prompt,
        max_tokens=50,  # Adjust the number of tokens you want in the response
        temperature=0.7,  # Adjust the creativity (higher values make it more creative)
    )

    # Extract and print the generated text
    generated_text = response.choices[0].text
    print(generated_text)


def search_restaurant_location_ID(location):

    url =  "https://tripadvisor16.p.rapidapi.com/api/v1/restaurant/searchLocation"

    querystring = {"query":location}

    headers = {
        "X-RapidAPI-Key": "53bd119ccfmsh364f7fc48f6cb7bp182915jsnd2899197f369",
        "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    json = response.json()
    id = str(json['data'][0]['locationId']) 

    return id

def search_restaurant(location_id): 
    import requests

    url = "https://tripadvisor16.p.rapidapi.com/api/v1/restaurant/searchRestaurants"
    querystring = {"locationId":location_id}

    headers = {
        "X-RapidAPI-Key": "53bd119ccfmsh364f7fc48f6cb7bp182915jsnd2899197f369",
        "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    
    restaurant_list = []
    for i in response['data']['data']:  
        restaurant_list.append(i['name'])

    return restaurant_list
    

def search_country_activity(): 
    url = "https://travel-info-api.p.rapidapi.com/country-activities"

    querystring = {"country":"spain"}

    headers = {
        "X-RapidAPI-Key": "53bd119ccfmsh364f7fc48f6cb7bp182915jsnd2899197f369",
        "X-RapidAPI-Host": "travel-info-api.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    activities = response.json()
    print(activities)
   # print(activities['activities'])


    return activities['data']['activities']
    


def main(): 
    #location_id = search_restaurant_location_ID('boston')
    #restaurant_list = search_restaurant(location_id)
    #country_activities = search_country_activity()
    return 

#restaurants = main()
#print(restaurants)
# Extract localized names
#localized_names = [item['localizedName'] for item in restaurants['data']]