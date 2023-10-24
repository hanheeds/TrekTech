import requests
from pathlib import Path

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

    restaurants = response.json()
    
    restaurant_list = {}
    for i in restaurants['data']['data']:  
        restaurant_list[i['name']] = [i['establishmentTypeAndCuisineTags'], i['priceTag'], i['averageRating']]

    return restaurant_list


def generate_prompt_restaurants(restaurant_list): 
    prompt = """
    this is a restaurant dictionary that has the following information: the keys are the restaurant name, 
    then the first element in the value is the cuisine type, the second value is the price range, and the third value is the user rating. 
    Given this list, choose an assortment of the best  restaurants for a 5 day vacation itinerary in boston. 
    Please do not categorize the days by cuisine, such that there is variety in each day. Choose 3 restaurants for each day(breakfast, lunch, and dinner): \n
    """ + restaurant_list


#location_id = search_restaurant_location_ID('boston')
#restaurant_list = search_restaurant(60745)