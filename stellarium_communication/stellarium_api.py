import requests

STELLARIUM_API_URL = "http://localhost:8090/api/"

def get_current_position_focus():
    request = requests.get(STELLARIUM_API_URL + "main/status?actionId=-1&propId=-2")
    location = request.json()["selectioninfo"]
    az_alt_key = "AZ/ALT:"
    
    try:            
        for data in location.split("<br/>"):
            if az_alt_key in data:
                return data.replace("°","º").replace("\"","''").split(" ")[1].split("/")
    except:
        return print("Error when retrieving data from Stelarium.")