from TheCatApiWrapper import *

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
