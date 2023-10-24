from photo_api import download_photo

def test_download_photo():
    query = 'Stormtrooper'
    save_directory = './images'
    message = download_photo(query, save_directory)
    print(message)

if __name__ == "__main__":
    test_download_photo()
