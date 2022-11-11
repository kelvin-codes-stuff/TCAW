# Getting the required modules
import requests
from dotenv import load_dotenv
import os
# Loads env 
load_dotenv()

# Base URL and API key stuff
BASE_API_URL = "https://api.thecatapi.com/v1/"
API_KEY = os.getenv("API_KEY")
HEADERS = {f"x-api-key": "{API_KEY}"}

class Url_join():
    imagesQuestionmark = "images/search?"
    images_get_breed = "images/search?breed_ids="
    images_search = "images/search"
    show_vote_limit10 = "votes?limit=10&order=DESC"
    show_favourites = "favourites"

    
# Main class to access all different functions
class Tcaw:
    
    
    # Getting a random image function
    def getImage():
        # Making the request with joined URL
        get_img = requests.get(BASE_API_URL + Url_join.imagesQuestionmark, headers=HEADERS)
        
        # If shit goes wrong af, return a error
        if get_img.status_code != 200:
            return "Error"    
        
        # If shit goes good, extract URL and return URL
        response = get_img.json()
        url_extract = response[0]["url"]
        return url_extract


    # Get a image from the requested cat breed
    def get_breed_img(breed):
        getRequest = requests.get(BASE_API_URL + Url_join.images_get_breed + breed, headers=HEADERS)
        
        if getRequest.status_code != 200:
            return "Error"

        if getRequest == []:
            return "No result"

        response = getRequest.json()
        url_extract =  response[0]["url"]
        return url_extract        