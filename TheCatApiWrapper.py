# Getting the required modules
import requests
from dotenv import load_dotenv
import os
from datetime import datetime

#TODO: Use Exception instead of "return "Error"
#TODO: More information inside comments
#TODO: Make code more flexible
#TODO: Make handling_url more efficient
#TODO:  70-71 make request also in cache

# Loads env values
load_dotenv()

# Base URL and API key stuff, adding header to request.
BASE_API_URL = "https://api.thecatapi.com/v1/"
API_KEY = os.getenv("API_KEY")
HEADERS = {f"x-api-key": "{API_KEY}"}

# Cache module
# cache_files = {}

class Cache:
    
    def __init__(self):
        self.cache_files = {}

    def write(self, breed, breedkey, img_url):

        now = datetime.now()
        self.cache_files[breed] = {
            "breed_id": breedkey,
            "expire": int(now.strftime("%H%M%S")) + 10,
            "image_url": img_url
        }

    def read(self, breed):

        if not (self.cache_files.get(breed) is None):
            return self.cache_files[breed]["image_url"]
        # return None

    def check(self, breed):
        now = datetime.now()
        if int(now.strftime("%H%M%S")) > self.cache_files[breed]["expire"]:
            return None
        
        return "IDK"
                

# Main class to access all different functions
class Tcaw:

    cache = Cache()

    # Gets a random image
    def get_random_image():
        # Making the request with joined URL and header for the API KEY
        get_request = requests.get(BASE_API_URL + "images/search?", headers=HEADERS)
        # Execute handling_url while passing getRequest trough the function, and returning the value from handling_url to getRandomImage
        return handling_url(get_request)


    # Gets a image from the requested cat breed
    def get_breed_image(self, breed):
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
                    self.cache.write(breed, key["id"], get_request.json()[0]["url"])
                    return breed, key["id"], get_request.json()[0]["url"]

                if self.cache.check(breed) == None:
                    print("DEBUG, expired, writing new to cache")
                    self.cache.write(breed, breedkey=key["id"], img_url=get_request.json()[0]["url"])
                    return breed, key["id"], get_request.json()[0]["url"]

                if self.cache.check(breed) != None:
                    print("DEBUG, reading from cache")
                    return self.cache.read(breed)



        
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
    tcaw = Tcaw()

    # Getting image of a cat breed
    input_breed_user = input(">").lower()

    if input_breed_user == "exit":
        break

    if input_breed_user == "random":
        print(tcaw.get_random_image())        
    else:
        print(tcaw.get_breed_image(breed=input_breed_user))