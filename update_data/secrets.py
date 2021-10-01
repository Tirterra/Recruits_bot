from requests.exceptions import HTTPError
import requests
import json
import os

# Returns the secrets a player has.
def get_secrets(url, player):

    DIR_PATH = os.path.dirname(__file__).replace(r"\data_processing", "")

    try:
        res = requests.get(url)
        res.raise_for_status()   # Raises an HTTPError if there was a connection issue. 
        res = res.json()
        secrets = res["player"]["achievements"]["skyblock_treasure_hunter"]
    except HTTPError:   # If there was an error, get the most recent data.
        with open(DIR_PATH+r"\ressources\guild_data.json", "r") as file:
            secrets = json.load(file)
            try:
                secrets = secrets[player]["secrets"]
            except KeyError:
                secrets = 0
    except KeyError:   # If the API are off, set the secrets to 0.
        secrets = 0
    else:
        secrets = 0
        
    return secrets