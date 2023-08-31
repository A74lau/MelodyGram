from instagrapi import Client
from PIL import Image
from pathlib import Path
from spotify.spotify_api import get_token, get_auth_header, search_for_song
from database import update, close_database
import webbrowser

client = Client()


image = Image.open("background.jpg")
image = image.convert("RGB")
new_image = image.resize((1080,1080))
new_image.save("new_background.jpg")

# fill in the username and password of your account
username = ""
password = ""
client.login(username, password)

photo_path = "new_background.jpg"
photo_path = Path(photo_path)

# post
media = client.photo_upload(photo_path,"Comment below some songs that I should add to my playlist!")

# store songs that you have already searched
searched_queries=[]

while True:
    # retrives the list of comments using media id and number of comments you want (0 - means all comments)
    list_comments = client.media_comments(media.id, 0)

    if not list_comments:
        print("Waiting for comments")
    
    else:
        song_name = list_comments[0].text

        # check if we already searched the exact query so that we don't research the same comment
        if song_name in searched_queries:
            continue

        # retrive the song name and use spotify api to search it up 
            # comment order is top to bottom meaning 0 is the first one 
        searched_queries.append(song_name)

        # get token to access spotify api
        token = get_token()

        # decide whether the song found is the one wanted
        user_decision = False
        # used to access different search results
        index = 0

        while not user_decision:
            search_result = search_for_song(token, song_name, index)
            print(search_result)

            webbrowser.open(search_result['link'])

            # ask user if that's the right song
            user_input = input("Is this the right song? Please input 'yes' or 'no'\n")

            if (user_input == 'yes'):
                update(search_result['id'], search_result['name'], search_result['artists'], search_result['link'])
                user_decision = True
                index = 0
            
            index += 1
        
        # before continuing on, ask if the user wants to end their session
        user_input2 = input("Do you want to end your session? Please input 'yes' or 'no'\n")
        if (user_input2 == 'yes'):
            close_database()

        












