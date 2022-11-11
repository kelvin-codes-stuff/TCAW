# Getting the required modules
import requests

# Base URL
BASE_API_URL = "https://api.thecatapi.com/v1/"

class Url_join():
    imagesQuestionmark = "images/search?"
    images_search = "images/search"
    show_vote_limit10 = "votes?limit=10&order=DESC"
    show_favourites = "favourites"

    
# Main class
class Tcaw:
    
    # Getting a random image function
    def getImage():
        # Making the request with joined URL
        get_img = requests.get(BASE_API_URL + Url_join.imagesQuestionmark)
        
        # If shit goes good, extract url
        if get_img.status_code == 200:
            response = get_img.json()
            url_extract = response[0]["url"]
            return url_extract
        
        # If shit goes wrong af, return a error
        return "Error"
