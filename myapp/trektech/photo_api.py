import requests
import os
import random

API_KEY = 'rYBWcsj70IHtuiF9UiLCzXwzsPFk9TgXvNwh5alElLEPCGruMcAao5uw'
BASE_URL = 'https://api.pexels.com/v1/search'

def download_photo(query, save_directory='./', save_filename="image"):
    headers = {
        'Authorization': API_KEY
    }
    
    params = {
        'query': query,
        'per_page': 15,  # Adjust as needed. 15 is the default.
        'page': 1
    }
    
    response = requests.get(BASE_URL, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()

        # Randomly select a photo from the returned results
        photo = random.choice(data['photos'])
        photo_url = photo['src']['large']
        
        # Ensure the directory exists. If not, create it.
        os.makedirs(save_directory, exist_ok=True)
        
        photo_response = requests.get(photo_url, stream=True)
        if photo_response.status_code == 200:
            with open(os.path.join(save_directory, f"{save_filename}.jpg"), 'wb') as file:
                for chunk in photo_response.iter_content(chunk_size=8192):
                    file.write(chunk)
            return f"Photo saved as {save_filename}.jpg in {save_directory}"
        else:
            return "Failed to download the photo."
    else:
        return "Failed to fetch photo from Pexels."
