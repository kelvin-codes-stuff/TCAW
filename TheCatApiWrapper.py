# Getting the required modules
import requests
import requests_cache
from dotenv import load_dotenv
import os

#TODO: 1) Add cat information function by breed.
#TODO: 2) Add cache for needed functions. 3) Make code more flexible.
# Loads env values
load_dotenv()

# Caching
if os.getenv("CACHE") == "True":
    requests_cache.install_cache(cache_name='URL_caching', backend='sqlite', expire_after=180)



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


# Main class to access all different functions
class Tcaw:
    # Gets a random image
    def getRandomImage():
        # Making the request with joined URL and header for the API KEY
        getRequest = requests.get(BASE_API_URL + Url_join.imagesQuestionmark, headers=HEADERS)
        # Execute handling_url while passing getRequest trough the function, and returning the value from handling_url to getRandomImage
        return handling_url(getRequest)

    # Gets a image from the requested cat breed
    def GetBreedImage(breed):
        # Request all breeds, if breed is in the request, get the id from that breed
        get_breeds_request = requests.get("https://api.thecatapi.com/v1/breeds").json()
        for key in get_breeds_request:
            # if key == breed input, add id from that breed to cat_id
            if key["name"].lower() == breed.lower():
                cat_id = key["id"]
                # Making the request with joined URL, cat breed and header for the API KEY
                getRequest = requests.get(BASE_API_URL + Url_join.images_get_breed + cat_id, headers=HEADERS)
                # Execute handling_url while passing getRequest trough the function, and returning the value from handling_url to getRandomImage
                return handling_url(getRequest)

        return "Error, unknown cat breed!"


# Gets executes with each API request
def handling_url(getRequest):
        # If status code isn't 200, return "Error" to caller
        if getRequest.status_code != 200:
            return "Error, got a invalid respone!"
        # If everything is fine, make JSON from request, extract URL and return URL to caller
        response = getRequest.json()
        
        # If result isn't nothing
        if response != []:
            url_extract =  response[0]["url"]
            return url_extract, f"Used cache: {getRequest.from_cache}"
        # If result is nothing return "No result"
        return "Error, no results!"        
