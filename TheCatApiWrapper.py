# Getting the required modules
import requests
import requests_cache
from dotenv import load_dotenv
import os

# Loads env values
load_dotenv()

# Base URL and API key stuff, adding header to request.
BASE_API_URL = "https://api.thecatapi.com/v1/"
API_KEY = os.getenv("API_KEY")
HEADERS = {f"x-api-key": "{API_KEY}"}

# URL collection, callable with Url_join
class Url_join():
    imagesQuestionmark = "images/search?"
    images_get_breed = "images/search?breed_ids="
    images_search = "images/search"
    show_vote_limit10 = "votes?limit=10&order=DESC"
    show_favourites = "favourites"

# Gets executes with each API request.
def handling_url(getRequest):
        # If status code isn't 200, return "Error" to caller
        if getRequest.status_code != 200:
            return "Error"
        # If status code = 200, but result = empty return "No result" to caller
        if getRequest == []:
            return "No result"
        # If everything is fine, make JSON from request, extract URL and return URL to caller
        response = getRequest.json()
        url_extract =  response[0]["url"]
        return url_extract        


# Main class to access all different functions
class Tcaw:
    
    # Gets a random image
    def getRandomImage():
        # Making the request with joined URL
        getRequest = requests.get(BASE_API_URL + Url_join.imagesQuestionmark, headers=HEADERS)
        # Execute handling_url while passing getRequest trough the function, and returning the value from handling_url to getRandomImage
        return handling_url(getRequest)

    # Gets a image from the requested cat breed
    def GetBreedImage(breed):
        getRequest = requests.get(BASE_API_URL + Url_join.images_get_breed + breed, headers=HEADERS)
        # Execute handling_url while passing getRequest trough the function, and returning the value from handling_url to getRandomImage
        return handling_url(getRequest)
    

