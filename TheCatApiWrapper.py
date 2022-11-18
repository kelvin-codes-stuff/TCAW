# Getting the required modules
import requests
from dotenv import load_dotenv
import os
from datetime import datetime


#TODO: Make own caching code
#TODO: Use Exception instead of "return "Error"
#TODO: More information inside comments
#TODO: Make code more flexible
#TODO: Make handling_url more efficient

# Loads env values
load_dotenv()

# Base URL and API key stuff, adding header to request.
BASE_API_URL = "https://api.thecatapi.com/v1/"
API_KEY = os.getenv("API_KEY")
HEADERS = {f"x-api-key": "{API_KEY}"}


# Cache module
cache_files = {}

def write_cache(breed, breedkey, img_url):
    now = datetime.now()
    cache_files[breed] = {
        "breed_id": breedkey,
        "expire": int(now.strftime("%H%M%S")) + 10,
        "image_url": img_url
    }
    return cache_files[breed]["image_url"]

def read_cache(breed):
    if not (cache_files.get(breed) is None):
        return cache_files[breed]["image_url"]
    return None

def check_cache(breed):
    now = datetime.now()

    cache_file_expire = cache_files[breed]["expire"]
    if int(now.strftime("%H%M%S")) > cache_file_expire:
        return None
    else:
        return "IDK"


# Main class to access all different functions
class Tcaw:

    # Gets a random image
    def get_random_image():
        # Making the request with joined URL and header for the API KEY
        get_request = requests.get(BASE_API_URL + "images/search?", headers=HEADERS)
        # Execute handling_url while passing getRequest trough the function, and returning the value from handling_url to getRandomImage
        return handling_url(get_request)

    # Gets a image from the requested cat breed
    def get_breed_image(breed_input):
        # Request all breeds, if breed is in the request, get the id from that breed
        for key in requests.get("https://api.thecatapi.com/v1/breeds").json():
            # if key is breed input, add id from that breed to cat_id
            if key["name"].lower() == breed_input.lower():
                
                # Making the request with joined URL, cat breed and header for the API KEY
                get_request = requests.get(BASE_API_URL + "images/search?" + key["id"], headers=HEADERS)

                if get_request.status_code != 200:
                    return "Error, got a invalid respone!"

                if read_cache(breed_input) == None:   
                    print("DEBUG, writing to cache")
                    return write_cache(breed=breed_input, breedkey=key["id"], img_url=get_request.json()[0]["url"])

                if check_cache(breed=breed_input) == None:
                    print("DEBUG, expired, writing new to cache")
                    return write_cache(breed=breed_input, breedkey=key["id"], img_url=get_request.json()[0]["url"])
                
                if check_cache != None:
                    print("DEBUG, reading from cache")
                    return read_cache(breed=breed_input)


        
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



# UI
while True:
    # Getting image of a cat breed
    input_breed_user = input(">").lower()

    if input_breed_user == "exit":
        break

    if input_breed_user == "random":
        print(Tcaw.get_random_image())        
    else:
        print(Tcaw.get_breed_image(input_breed_user))


