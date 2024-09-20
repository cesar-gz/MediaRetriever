import os
import random
import requests
import sharedVariables
from dotenv import load_dotenv

def get_album_cover():
    load_dotenv()
    api_key = os.getenv("LAST_FM_API_KEY")

    tempString = sharedVariables.get_video_title()
    tempArray = tempString.split("- ")
    artist = tempArray[0]
    album = tempArray[1]

    url = f'http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={api_key}&artist={artist}&album={album}&format=json'

    response = requests.get(url)
    data = response.json()

    try:
        cover_url = data['album']['image'][3]['#text']  # The large cover image
        return cover_url
    except KeyError:
        return None


def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename}\n")
    else:
        print("Failed to download image. Requesting a random Pokemon for the cover.")
        pokemonURL = get_random_pokemon()
        pokemonImage = requests.get(pokemonURL)
        with open(filename, 'wb') as f:
            f.write(pokemonImage.content)
            print(f"Downloaded Pokemon {filename}\n")



def get_random_pokemon():
    # Get a random Pokémon ID
    pokemon_id = random.randint(1, 898)
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}/'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        image_url = data['sprites']['front_default']
        return image_url
    else:
        return None





cover_url = get_album_cover()
if cover_url:
    download_image(cover_url, 'albumCover.jpg')
else:
    print("Album cover not found.")
