# adapted from code by @stephenhouser on github
# https://gist.github.com/stephenhouser/c5e2b921c3770ed47eb3b75efbc94799
from bs4 import BeautifulSoup
import requests
import re
import sys
import os
import http.cookiejar
import json
import urllib.request, urllib.error, urllib.parse


def get_soup(url,header):
    return BeautifulSoup(urllib.request.urlopen(
        urllib.request.Request(url,headers=header)),
        'html.parser')

def bing_image_search(query):
    query= query.split()
    query='+'.join(query)
    url="http://www.bing.com/images/search?q=" + query + "&FORM=HDRSC2"

    #add the directory for your image here
    DIR="Pictures"
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    soup = get_soup(url,header)
    image_result_raw = soup.find("a",{"class":"iusc"})

    m = json.loads(image_result_raw["m"])
    murl, turl = m["murl"],m["turl"]# mobile image, desktop image

    image_name = urllib.parse.urlsplit(murl).path.split("/")[-1]
    return (image_name,murl, turl)


def download_image(image_url, local_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(local_path + ".jpg", 'wb') as f:
            f.write(response.content)
        print(f"Image downloaded successfully to {local_path}")
    else:
        print(f"Failed to download image. HTTP Status Code: {response.status_code}")

def download_photo(query, local_folder, filename):
    print("calling new photo api")
    results = bing_image_search(query)
    image_url = results[1]
    image_name = results[0]
    local_path =f'{local_folder}./{filename}'   
    download_image(image_url, local_path)
    print(results)
    
if __name__ == "__main__":
    query = sys.argv[1]
    results = bing_image_search(query)
    # Example usage
    image_url = results[1]
    image_name = results[0]
    local_path =f'media/{image_name}'
    download_image(image_url, local_path)
    print(results)