
import requests
import constants

def get_current_position_focus():
    request = requests.get(constants.stelarium_uri + "main/status?actionId=-1&propId=-2")
    location = request.json()["selectioninfo"]
    
    try:            
        for data in location.split("<br/>"):
            if constants.az_alt_key in data:
                return data.replace("°","º").replace("\"","''").split(" ")[1].split("/")
    except:
        return print("Error when retrieving data from Stelarium.")