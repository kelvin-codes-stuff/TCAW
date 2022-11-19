# Getting the required modules
import requests
from dotenv import load_dotenv
import os
from datetime import datetime

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
class Cache:
    def __init__(self, breed, breedkey, img_url):

        print(breed, breedkey, img_url)

        self.breed = breed
        self.breedkey = breedkey
        self.img_url = img_url

        print(self.breed, self.breed)

    def write(self):
        now = datetime.now()
        cache_files[self.breed] = {
            "breed_id": self.breedkey,
            "expire": int(now.strftime("%H%M%S")) + 10,
            "image_url": self.img_url
        }

    def read(self):
        if not (cache_files.get(self.breed) is None):
            return cache_files[self.breed]["image_url"]
        return None

    def check(self):
        now = datetime.now()

        if int(now.strftime("%H%M%S")) > cache_files[self.breed]["expire"]:
            return True



# Main class to access all different functions
class Tcaw:

    # Gets a random image
    def get_random_image():
        # Making the request with joined URL and header for the API KEY
        get_request = requests.get(BASE_API_URL + "images/search?", headers=HEADERS)
        # Execute handling_url while passing getRequest trough the function, and returning the value from handling_url to getRandomImage
        return handling_url(get_request)


    # Gets a image from the requested cat breed
    def get_breed_image(self, breed):
        cache = Cache()
        # Request all breeds, if breed is in the request, get the id from that breed
        for key in requests.get("https://api.thecatapi.com/v1/breeds").json():
            # if key is breed input, add id from that breed to cat_id
            if key["name"].lower() == breed.lower():
                
                # Making the request with joined URL, cat breed and header for the API KEY
                get_request = requests.get(BASE_API_URL + "images/search?" + key["id"], headers=HEADERS)

                if get_request.status_code != 200:
                    return "Error, got a invalid respone!"

                if self.cache.read(breed) == None:   
                    print("DEBUG, writing to cache")
                    self.cache.write(breed, breedkey=key["id"], img_url=get_request.json()[0]["url"])
                    return breed, key["id"], get_request.json()[0]["url"]

                if Cache.check(breed):
                    print("DEBUG, expired, writing new to cache")
                    Cache.check(breed, breedkey=key["id"], img_url=get_request.json()[0]["url"])
                    return breed, key["id"], get_request.json()[0]["url"]

                if Cache.check(breed) != None:
                    print("DEBUG, reading from cache")
                    return Cache.read(breed)


        
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