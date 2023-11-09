import requests

def search_restaurant_location_ID(location):

    url =  "https://tripadvisor16.p.rapidapi.com/api/v1/restaurant/searchLocation"

    querystring = {"query":location}

    headers = {
        "X-RapidAPI-Key": "ec4caddecdmsh87e7c19c561feccp16ba86jsn2c30183bfe50",
        "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    json = response.json()
    # print(json) # debugging
    id = str(json['data'][0]['locationId']) 

    return id

def search_restaurant(location_id): 

    url = "https://tripadvisor16.p.rapidapi.com/api/v1/restaurant/searchRestaurants"
    querystring = {"locationId":location_id}

    headers = {
        "X-RapidAPI-Key": "ec4caddecdmsh87e7c19c561feccp16ba86jsn2c30183bfe50",
        "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    restaurants = response.json()
    
    restaurant_list = {}
    for i in restaurants['data']['data']:  
        restaurant_list[i['name']] = [i['establishmentTypeAndCuisineTags'], i['priceTag'], i['averageRating']]

    return restaurant_list

# Function that takes in city and returns the list of restaurants
def restaurants(city):
    location_id = search_restaurant_location_ID(city)
    restaurant_list = search_restaurant(location_id)
    return restaurant_list


# print(restaurants('Cape Town, South Africa'))


def search_country_activity(country): 
    url = "https://travel-info-api.p.rapidapi.com/country-activities"

    querystring = {"country":country}

    headers = {
        "X-RapidAPI-Key": "53bd119ccfmsh364f7fc48f6cb7bp182915jsnd2899197f369",
        "X-RapidAPI-Host": "travel-info-api.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    activities = response.json()
    print(activities)
    print(activities['activities'])
    return activities['data']['activities']