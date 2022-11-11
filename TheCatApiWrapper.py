# Getting the required modules
import requests
import requests_cache
from dotenv import load_dotenv
import os

#TODO: Make own caching code
#TODO: Remove URL joining
#TODO: Use Exceoption instead of "return "Error""
#TODO: More information inside comments
#TODO: Make code more flexible
#TODO: Make handling_url more efficient

# Loads env values
load_dotenv()

# Caching (Only if .env CACHE is true!)
if os.getenv("CACHE") == "True":
    requests_cache.install_cache(cache_name='URL_caching', backend='sqlite', expire_after=180)

# Base URL and API key stuff, adding header to request.
BASE_API_URL = "https://api.thecatapi.com/v1/"
API_KEY = os.getenv("API_KEY")
HEADERS = {f"x-api-key": "{API_KEY}"}

# URL collection, callable with Url_join
class Url_join():
    images_questionmark = "images/search?"
    images_get_breed = "images/search?breed_ids="
    images_search = "images/search"
    show_vote_limit10 = "votes?limit=10&order=DESC"
    show_favourites = "favourites"



# Main class to access all different functions
class Tcaw:
    # Gets a random image
    def get_random_image():
        # Making the request with joined URL and header for the API KEY
        get_request = requests.get(BASE_API_URL + Url_join.images_questionmark, headers=HEADERS)
        # Execute handling_url while passing getRequest trough the function, and returning the value from handling_url to getRandomImage
        return handling_url(get_request)

    # Gets a image from the requested cat breed
    def get_breed_image(breed_input):
        # Request all breeds, if breed is in the request, get the id from that breed
        for key in requests.get("https://api.thecatapi.com/v1/breeds").json():
            # if key == breed input, add id from that breed to cat_id
            if key["name"].lower() == breed_input.lower():
                
                # Making the request with joined URL, cat breed and header for the API KEY
                get_request = requests.get(BASE_API_URL + Url_join.images_get_breed + key["id"], headers=HEADERS)
                # Execute handling_url while passing getRequest trough the function, and returning the value from handling_url to getRandomImage
                return handling_url(get_request)
            
        return "Error, unknown cat breed!"

    # Get information about a breed
    def get_breed_info(breed_input):
        # Request all breeds, and loop for every key in request
        get_breeds_request = requests.get("https://api.thecatapi.com/v1/breeds").json()
        for key in get_breeds_request:
            # if key == breed input, return list with information
            if key["name"].lower() == breed_input.lower():
                    return key
                
        
# Gets executes with each API request
def handling_url(get_request):
        # If status code isn't 200, return "Error" to caller
        if get_request.status_code != 200:
            return "Error, got a invalid respone!"
        # If result isn't nothing
        if get_request.json() != []:
            return get_request.json()[0]["url"]
        # If result is nothing return "No result"
        return "Error, no results!"        
